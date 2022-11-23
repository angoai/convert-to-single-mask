import cv2
import json
import pydicom
import requests
from PIL import Image
from io import BytesIO
from skimage import io
from ango.sdk import SDK
from utils import *


def segmentation_to_single_mask(api_key: str, project_id: str, json_path: str, output_folder: str = 'masks', class_mapping_type: str = 'multi_channel_qualitative'):
    check_input_parameters(api_key, project_id, json_path, output_folder, class_mapping_type)

    # Get label set
    ango_sdk = SDK(api_key=api_key)
    project_info = ango_sdk.get_project(project_id)

    if project_info['status'] == 'fail':
        error_message = project_info['message']
        raise ValueError(error_message)

    tool_list = project_info['data']['project']['categorySchema']['tools']

    class_name_list = []
    for tool in tool_list:
        if tool['tool'] == 'segmentation':
            class_name = tool['title']
            class_name_list.append(class_name)

    num_classes = len(class_name_list)
    check_inputs(num_classes, class_mapping_type)

    # Map classes to colors
    class_mapping = {}
    if class_mapping_type == 'single_channel_sequential':
        for class_index, class_name in enumerate(class_name_list):
            class_mapping[class_name] = class_index+1
    elif class_mapping_type == 'single_channel_diverging':
        diverge_index_list = get_diverge_index_list()
        for class_index, class_name in enumerate(class_name_list):
            class_mapping[class_name] = diverge_index_list[class_index]
    elif class_mapping_type == 'multi_channel_qualitative':
        color_codes_rgb = get_rgb_codes(num_classes)
        for class_index, class_name in enumerate(class_name_list):
            class_mapping[class_name] = color_codes_rgb[class_index]

    # Read JSON File
    f = open(json_path, encoding="utf8")
    data = json.load(f)
    f.close()

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    # Convert Segmentation to Single Mask
    for current_data in data:
        img_url = current_data['asset']
        file_type = img_url.split('.')[-1]

        response = requests.get(img_url)
        if file_type == 'dcm':
            dicom_data = pydicom.dcmread(BytesIO(response.content))
            img = dicom_data.pixel_array
        else:
            img = Image.open(BytesIO(response.content))
            img = np.array(img)
        
        task_id = current_data['tasks'][0]['taskId']
        objects = current_data['tasks'][0]['objects']

        # Semantic Segmentation
        if class_mapping_type in ['single_channel_sequential', 'single_channel_diverging']:
            mask_array = np.zeros(img.shape[0:2], dtype=np.uint8)
            for obj_ind, obj in enumerate(objects):
                instance_mask_array = np.zeros(img.shape[0:2], dtype=np.uint8)
                class_name = obj['title']
                if class_name not in class_name_list:
                    continue
                
                segmentation = obj['segmentation']
                zones = segmentation['zones']
                for zone in zones:
                    region = np.array(zone['region'])
                    region = np.round(region).astype(int)
                    holes = zone['holes']
                    instance_mask_array = cv2.fillPoly(instance_mask_array, pts=[region], color=(class_mapping[class_name]))
                    for hole in holes:
                        hole = np.array(hole)
                        hole = np.round(hole).astype(int)
                        instance_mask_array = cv2.fillPoly(instance_mask_array, pts=[hole], color=(0))

                    # Merge masks
                    x_indices, y_indices = np.where(instance_mask_array != 0)
                    mask_array[x_indices, y_indices] = instance_mask_array[x_indices, y_indices]
        elif class_mapping_type in ['multi_channel_qualitative']:
            mask_array = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
            for obj_ind, obj in enumerate(objects):
                instance_mask_array = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
                class_name = obj['title']
                if class_name not in class_name_list:
                    continue
                
                segmentation = obj['segmentation']
                zones = segmentation['zones']
                for zone in zones:
                    region = np.array(zone['region'])
                    region = np.round(region).astype(int)
                    holes = zone['holes']

                    color = class_mapping[class_name]
                    color_int = tuple([int(color[0]), int(color[1]), int(color[2])])
                    instance_mask_array = cv2.fillPoly(instance_mask_array, pts=[region], color=color_int)
                    for hole in holes:
                        hole = np.array(hole)
                        hole = np.round(hole).astype(int)
                        instance_mask_array = cv2.fillPoly(instance_mask_array, pts=[hole], color=(0, 0, 0))

                    # Merge masks
                    x_indices, y_indices, z_indices = np.where(instance_mask_array != [0, 0, 0])
                    mask_array[x_indices, y_indices, z_indices] = instance_mask_array[x_indices, y_indices, z_indices]

        filepath = os.path.join(output_folder, task_id + '.png')
        io.imsave(filepath, mask_array)

    mapping_path = os.path.join(output_folder, 'class_mapping.txt')
    with open(mapping_path, 'w') as data:
        data.write(str(class_mapping))


if __name__ == "__main__":
    api_key = 'YOUR_API_KEY'
    project_id = 'YOUR_PROJECT_ID'
    json_path = 'YOUR_JSON_FILE.json'
    output_folder = 'masks_segmentation'
    class_mapping_type = 'multi_channel_qualitative'
    segmentation_to_single_mask(api_key, project_id, json_path, output_folder, class_mapping_type)
