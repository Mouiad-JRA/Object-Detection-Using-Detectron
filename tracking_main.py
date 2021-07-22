import cv2
import glob
import numpy as np
from kalman import KalmanFilter
from detector import detect
# Create KalmanFilter object KF
# KalmanFilter(dt, u_x, u_y, std_acc, x_std_meas, y_std_meas)
#todo: adjust the paramaters to get optimal result and make training on good iterations
KF = KalmanFilter(0.1, 1.5, 1, 0.5, 0.0, 0.0)
# Create opencv video capture object
frames = glob.glob('MM/*.jpg')
base = 'MM/0000001.jpg'
frames.remove(base)
frames.sort()
base_frame = cv2.imread(base)
centers = detect(base_frame, predictor=predictor)# get the predictor from colab
print(centers)
print(frames)

predicted = []
updated = []
counter = 0
for center in centers:
    cv2.circle(base_frame, (int(center[0]), int(center[1])), 10, (0, 191, 255), 2)
# cv2_imshow(base_frame)
for frame in frames:
    frame = cv2.imread(frame)
    if counter == 0:
        # Draw the detected circle
        # cv2.circle(frame, (int(centers[0][0]), int(centers[0][1])), 10, (0, 191, 255), 2)
        # Predict
        for center in centers:
            (x, y) = KF.predict()
            (x1, y1) = KF.update(center)
            x, y = (x, y)
            x1, y1 = (x1, y1)
            updated.append(np.array([[float(x1)], [float(y1)]]))
            predicted.append(np.array([[float(x)], [float(y)]]))
        # print("predicted", predicted)
        # print("updated", updated)

    else:
        for point in range(len(predicted)):
            (x, y) = KF.predict()
            # print(updated[point])
            (x1, y1) = KF.update(updated[point])
            predicted[point] = np.array([[float(x)], [float(y)]])
            updated[point] = np.array([[float(x1)], [float(y1)]])
            # print ("predicted" , predicted)
            # print("updated",updated)

    for point in range(len(predicted)):
        x, y = predicted[point]
        x1, y1 = updated[point]
        # Draw a rectangle as the predicted object position
        cv2.rectangle(frame, (x - 15, y - 15), (x + 15, y + 15), (255, 0, 0), 2)
        # Draw a rectangle as the estimated object position
        cv2.rectangle(frame, (x1 - 15, y1 - 15), (x1 + 15, y1 + 15), (0, 0, 255), 2)
        cv2.putText(frame, "Estimated Position", (x1 + 15, y1 + 10), 0, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, "Predicted Position", (x + 15, y), 0, 0.5, (255, 0, 0), 2)
        # cv2.putText(frame, "Measured Position", (centers[0][0] + 15, centers[0][1] - 15), 0, 0.5, (0,191,255), 2)

    cv2_imshow(frame)
    counter += 1
    if cv2.waitKey(2) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break