import numpy as np
import cv2


def detect(frame, predictor):
    centers = []
    contours = predictor(frame)["instances"].get_fields()["pred_boxes"].tensor.cpu().numpy()
    for box in contours:
        xleft = box[0]
        yleft = box[1]
        xright = box[2]
        yright = box[3]
        width = np.abs(xleft - xright)
        height = np.abs(yleft - yright)
        centerx = width / 2 + xleft
        centery = height / 2 + yleft
        centers.append(np.array([[centerx], [centery]]))
    return centers                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           