import cv2
import numpy as np

#Loading Mask RCNN
net = cv2.dnn.readNetFromTensorflow("dnn/frozen_inference_graph_coco.pb" ,
                                    "dnn/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt")

#generate colors for objects
colors = np.random.randint(0, 255, (80, 3))

#Load Image
img = cv2.imread("road.jpg")
#img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
height, width, _ = img.shape
#create new image
black_image = np.zeros((height, width, 3), np.uint8)
black_image[:] = (100, 100, 0)

#Detect Objects
blob = cv2.dnn.blobFromImage(img, swapRB=True)
net.setInput(blob)

boxes, masks = net.forward(["detection_out_final", "detection_masks"])
detection_count = boxes.shape[2]

for i in range(detection_count):
    box = boxes[0, 0, i]
    class_id = box[1]
    score = box[2]
    if score < 0.7:
        continue

    #box coordinates
    x = int(box[3] * width)
    y = int(box[4] * height)
    x2 = int(box[5] * width)
    y2 = int(box[6] * height)

    # Ensure valid bounding box
    if x >= x2 or y >= y2:
        continue

    roi = black_image[y: y2, x: x2]
    roi_height, roi_width, _ = roi.shape
   
    # Check for valid ROI dimensions
    if roi_width <= 0 or roi_height <= 0:
        continue

    # get mask
    mask = masks[i, int(class_id)] 

    # If the mask is too small, resize it to match the ROI dimensions
    if mask.shape != (roi_height, roi_width):
        mask_resized = cv2.resize(mask, (roi_width, roi_height), interpolation=cv2.INTER_LINEAR)
    else:
        mask_resized = mask
    mask = cv2.resize(mask, (roi_width, roi_height))

    _, mask = cv2.threshold(mask, 0.5, 255, cv2.THRESH_BINARY)

    cv2.rectangle(img, (x, y), (x2, y2), (255, 0, 0), 3)

    #get mask coord
    contours, _ = cv2.findContours( np.array(mask,np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    color = colors[int(class_id) % len(colors)]
    for cnt in contours:
        cv2.fillPoly(roi, [cnt], (int(color[0]), int(color[1]), int(color[2])))

    for i in range(int(class_id)):
            # 1. Rectangle
            y1, x1, y2, x2 = r["rois"][i]
            cv2.rectangle(img,(x1, y1), (x2, y2), (25, 15, 220), 3)

            # Width
            width = x2 - x1
            #cv2.putText(img, str(width), (x1 , y1 - 10), cv2.FONT_HERSHEY_PLAIN, 1, (25, 15, 220), 2)

            # height
            height = y2 - y1


            # 1.4 CM = 153
            # 14 MM = 153
            # Ratio Pixels to MM
            ratio_px_mm = 153 / 14
            mm_width = width / ratio_px_mm
            cm_width = mm_width / 10
            mm_height = height / ratio_px_mm
            cm_height = height / ratio_px_mm

cv2.imshow("Image", img)
cv2.imshow("Black image", black_image)


cv2.waitKey(0)