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
