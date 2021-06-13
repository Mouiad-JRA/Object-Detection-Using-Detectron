import os
import shutil
from PIL import Image
import json

data = {
    "info": {
        "year": "2021",
        "version": "1.0",
        "description": "Exported from Visdrones",
        "contributor": "Casper",
        "url": "https://VisDrones.net",
        "date_created": "2021-01-19T09:48:27"
    },
    "licenses": [
        {
            "url": "http://MIT.net",
            "id": 1,
            "name": "MIT License"
        },
    ],
    "categories": [
        {"supercategory": "regions", "id": 0, "name": "ignored_regions"},
        {"supercategory": "human", "id": 1, "name": "‫‪pedestrian‬‬"},
        {"supercategory": "human", "id": 2, "name": "‫‪people‬‬"},
        {"supercategory": "vehicle", "id": 3, "name": "bicycle"},
        {"supercategory": "vehicle", "id": 4, "name": "car"},
        {"supercategory": "vehicle", "id": 5, "name": "van"},
        {"supercategory": "vehicle", "id": 6, "name": "truck"},
        {"supercategory": "vehicle", "id": 7, "name": "‫‪tricycle‬‬"},
        {"supercategory": "vehicle", "id": 8, "name": "‫‪awning-tricycle‬‬"},
        {"supercategory": "vehicle", "id": 9, "name": "bus"},
        {"supercategory": "vehicle", "id": 10, "name": "motor"},
        {"supercategory": "vehicle", "id": 11, "name": "other"},

    ],
    "images": [
    ],
    "annotations": [
    ]
}

next_image_id = 1


def process(value):
    if value == '0':
        return '‫ignored‬‬_‫‪regions‬‬'
    elif value == '1':
        return '‫‪pedestrian‬‬'
    elif value == '2':
        return '‫‪people‬‬'
    elif value == '3':
        return '‫‪bicycle‬‬'
    elif value == '4':
        return '‫‪car‬‬'
    elif value == '5':
        return '‫‪van‬‬'
    elif value == '6':
        return '‫‪truck‬‬'
    elif value == '7':
        return '‫‪tricycle‬‬'
    elif value == '8':
        return '‫‪awning-tricycle‬‬'
    elif value == '9':
        return '‫‪bus‬‬'
    elif value == '10':
        return '‫‪motor‬‬'
    elif value == '11':
        return 'others'


def combine_to_dir(path=None, new_path=None):
    path = 'train/'
    new_path = 'result/'
    content = os.listdir(path)
    for folder in content:
        images = os.listdir(f'{path}/{folder}')
        for image in images:
            new_image = f'{folder}{image}'
            shutil.copy(f'{path}/{folder}/{image}', f'{new_path}/{new_image}')


# Convert to coco
# Get all annotation files names
# For each annotation file name
#   Get a list of all images which start with the file name
#   Read the annotation file
#   for each line in annotation file
#     get or create image in coco dict and return it's id
#     insert annotation and increment id


def get_or_create_image(image_path):
    image_data_list = list(filter(lambda image_data: image_data.get("file_name", "") == image_path, data["images"]))
    if image_data_list:
        return image_data_list[0]["id"]
    image = Image.open(image_path)
    width, height = image.size
    global next_image_id
    data["images"].append({
        "id": next_image_id,
        "license": 1,
        "file_name": image_path,
        "height": height,
        "width": width,
        "date_captured": None
    })
    image_id = next_image_id
    next_image_id += 1
    return image_id


def make_coco(images_path=None, annotations_path=None):
    images_path = 'result/'
    annotations_path = r'annotations/'
    annotations_list = os.listdir(annotations_path)
    images_list = os.listdir(images_path)
    for annotation in annotations_list:
        annotation_file = open(f'{annotations_path}/{annotation}', 'r')
        lines_pre = annotation_file.read()
        lines = lines_pre.split('\n')
        annotation_images = list(filter(lambda name: name.startswith(annotation[:-4]), images_list))
        for line in lines:
            line = line.split(',')
            if len(line) < 6:
                break
            if line[6] == 0 or line[6] == '0':
                continue
            image_name = list(filter(lambda name: name.endswith(line[0] + ".jpg"), annotation_images))[0]
            image_path = f'{images_path}/{image_name}'
            image_id = get_or_create_image(image_path)
            target_id = int(line[1])
            bboxes = [float(line[2]), float(line[3]), float(line[4]), float(line[5])]
            category = int(line[7])
            data["annotations"].append({
                "id": target_id,
                "image_id": image_id,
                "category_id": category,
                "bbox": bboxes,
                "segmentation": [],
                "area": None,
                "iscrowd": None
            })

    with open("data_file.json", "w") as write_file:
        json.dump(data, write_file)


if __name__ == '__main__':
    # combine_to_dir()
    make_coco()
