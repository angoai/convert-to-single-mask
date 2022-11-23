# convert-to-single-mask
Generate single masks from Ango export files.

__For the polygon tool:__  [[polygon_to_single_mask](1_polygon_to_single_mask.py)]

```
if __name__ == "__main__":
    api_key = 'YOUR_API_KEY'
    project_id = 'YOUR_PROJECT_ID'
    json_path = 'YOUR_JSON_FILE.json'
    output_folder = 'masks_segmentation'
    class_mapping_type = 'multi_channel_qualitative'
    polygon_to_single_mask(api_key, project_id, json_path, output_folder, class_mapping_type)
```

__For the segmentation tool:__ [[segmentation_to_single_mask](2_segmentation_to_single_mask.py)]

```
if __name__ == "__main__":
    api_key = 'YOUR_API_KEY'
    project_id = 'YOUR_PROJECT_ID'
    json_path = 'YOUR_JSON_FILE.json'
    output_folder = 'masks_segmentation'
    class_mapping_type = 'multi_channel_qualitative'
    segmentation_to_single_mask(api_key, project_id, json_path, output_folder, class_mapping_type)
```


___class_mapping_type___ options:
- __single_channel_sequential:__  ```{'class_1': 1, 'class_2': 2, 'class_3': 3, ...}```
- __single_channel_diverging:__ ```{'class_1': 255, 'class_2': 128, 'class_3': 192, 'class_4': 64 ...}```
- __multi_channel_qualitative:__ ```{'class_1': (R1, G1, B1), 'class_2': (R2, G2, B2), 'class_3': (R3, G3, B3), ...}```
