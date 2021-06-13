from PIL import Image
import json
import os
import cv2


def check():
    with open('data_file.json') as f:
        data = json.load(f)
    path = 'result/'
    content = os.listdir(path)
    for image in content:
        for anno in data['images']:
            if image == anno["file_name"][8:]:
                id = anno['id']
                print(id)
                for i in data['annotations']:
                    if i['image_id'] == id:
                        print(i['image_id'])
                        bbox = i['bbox']
                        x_left, y_left, x_right, y_right = bbox[0], bbox[1], bbox[2], bbox[3]
                        start = (int(x_left), int(y_left))
                        end = (int(x_right), int(y_right))
                        color = (255, 0, 0)
                        thickness = 1
                        image_res = cv2.rectangle(cv2.imread('result//'+image), start, end, color, thickness)
                        cv2.imshow(f'{image}', image_res)
                        cv2.waitKey()
