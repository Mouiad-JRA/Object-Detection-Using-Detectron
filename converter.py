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

        {

        },
    ],
    "images": [
        {

        },
    ],
    "annotations": [
        {
        
        },
    ]
}


def process(value):
    if value == '0':
        return '‫ignored‬‬ ‫‪regions‬‬'
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
    path = 'D:/VisDrone2019-MOT/VisDrone2019-MOT-train/VisDrone2019-MOT-train/sequences'
    new_path = 'D:/images'
    content = os.listdir(path)
    for folder in content:
        images = os.listdir(f'{path}/{folder}')
        for image in images:
            new_image = f'{folder}{image}'
            shutil.move(f'{path}/{folder}/{image}', f'{new_path}/{new_image}')


def make_coco(images_path=None, annotations_path=None):
    images_path = 'D:/images'
    annotations_path = 'D:/VisDrone2019-MOT/VisDrone2019-MOT-train/VisDrone2019-MOT-train/annotations'
    annotations_list = os.listdir(annotations_path)
    images_list = os.listdir(images_path)
    for annotation in annotations_list:
        annotation_file = open(f'{annotations_path}/{annotation}', 'r')
        lines_pre = annotation_file.read()
        lines = lines_pre.split('\n')
        for image in images_list:
            if image[:18] == annotation[:18]:
                im = Image.open(f'{images_path}/{image}')
                width, height = im.size
                image_row = image[19:].lstrip('0').replace('.jpg','')
                ss = lines
                for line in ss:
                    line = line.split(',')
                    if line[0] == image_row:
                        if line[6] == 0 :
                            continue
                        else:
                            target_id = line[1]
                            bboxes = [line[2], line[3], line[4], line[5]]
                            category = line[7]
                            data["images"].append({
                                "id": image_row,
                                "license": 1,
                                "file_name": f'{images_path}/{image}',
                                "height": height,
                                "width": width,
                                "date_captured": None
                            })
                            data["annotations"].append({
                                "id": target_id,
                                "image_id": image_row,
                                "category_id": None,
                                "bbox": bboxes,
                                "segmentation": [],
                                "area": None,
                                "iscrowd": None
                            })
                            data["categories"].append({
                                "id": category,
                                "name": process(category),
                                "supercategory": None
                            })
    with open("data_file.json", "w") as write_file:
        json.dump(data, write_file)


if __name__ == '__main__':
    #combine_to_dir()
    make_coco()