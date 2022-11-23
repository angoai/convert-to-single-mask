import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def variable_check(variable, variable_name, variable_type):
    if not isinstance(variable, variable_type):
        error_message = 'The input parameter "' + variable_name + '" must be a ' + str(variable_type).split("'")[1] + '!'
        raise ValueError(error_message)


def check_input_parameters(api_key: str, project_id: str, json_path: str, output_folder: str, class_mapping_type: str):
    # Check input types
    variable_check(api_key, 'api_key', str)
    variable_check(project_id, 'project_id', str)
    variable_check(json_path, 'json_path', str)
    variable_check(output_folder, 'output_folder', str)
    variable_check(class_mapping_type, 'class_mapping_type', str)
    
    # Check JSON file
    if not os.path.exists(json_path):
        error_message = "JSON file doesn't exist!"
        raise ValueError(error_message)
    
    # Check class_mapping_type
    options = ['single_channel_sequential', 'single_channel_diverging', 'multi_channel_qualitative']
    if class_mapping_type not in options:
        error_message = 'The input parameter "class_mapping_type" must be one of the following: ' + ', '. join(options)
        raise ValueError(error_message)


def check_inputs(num_classes: int, class_mapping_type: str):
    variable_check(num_classes, 'num_classes', int)
    variable_check(class_mapping_type, 'class_mapping_type', str)
    
    if num_classes == 0:
        error_message = 'No classes were found!'
        raise ValueError(error_message)
        
    if class_mapping_type in ['single_channel_sequential', 'single_channel_diverging']:
        if num_classes > 255:
            error_message = 'The number of classes is too high for the input parameter ' + class_mapping_type + '! Use multi channel options.' 
            raise ValueError(error_message)
    elif class_mapping_type in ['multi_channel_qualitative']:
        if num_classes > 949:
            error_message = 'The number of classes is too high for the input parameter ' + class_mapping_type + '! Use multi channel options.' 
            raise ValueError(error_message)
    else:
        error_message = 'The input parameter "class_mapping_type" is wrong!'
        raise ValueError(error_message)


def get_diverge_index_list():
    np.random.seed(0)
    factor_list = []
    for index_1 in range(9):
        division_factor = np.power(2, index_1)
        random_indices = np.random.permutation(division_factor)
        for index_2 in random_indices:
            multiplication_factor = index_2 + 1
            factor = 256 * multiplication_factor / division_factor
            factor = int(factor)
            if factor == 256:
                factor = 255
            if factor not in factor_list:
                factor_list.append(factor)
    return factor_list


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def get_rgb_codes(num_classes):
    color_codes_rgb = []
    if num_classes <= 10:
        color_codes_rgb = np.round(plt.cm.tab10(np.arange(10))[:, 0:3]*255).astype(np.uint32)
    elif (num_classes > 10) & (num_classes <= 60):
        color_code_1 = np.round(plt.cm.tab20(np.arange(20))[:, 0:3]*255).astype(np.uint32)
        color_code_2 = np.round(plt.cm.tab20b(np.arange(20))[:, 0:3]*255).astype(np.uint32)
        color_code_3 = np.round(plt.cm.tab20c(np.arange(20))[:, 0:3]*255).astype(np.uint32)
        color_codes_rgb = np.concatenate((color_code_1, color_code_2, color_code_3))
    elif (num_classes > 60) & (num_classes <= 148):
        color_codes = mcolors.XKCD_COLORS
        color_codes_rgb = []
        for code in color_codes:
            rgb_code = hex_to_rgb(color_codes[code])
            if rgb_code == (0, 0, 0):
                continue
            color_codes_rgb.append(rgb_code)
    elif (num_classes > 148) & (num_classes <= 949):
        color_codes = mcolors.XKCD_COLORS
        color_codes_rgb = []
        for code in color_codes:
            rgb_code = hex_to_rgb(color_codes[code])
            if rgb_code == (0, 0, 0):
                continue
            color_codes_rgb.append(rgb_code)
    
    color_codes_rgb = np.array(color_codes_rgb)[0:num_classes, :]
    color_codes_list = []
    for index in range(num_classes):
        color_codes_list.append(tuple(color_codes_rgb[index, :]))
    
    return color_codes_list
