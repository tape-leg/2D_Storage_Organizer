import cv2
import numpy as np
import book as bk

# Load Mask RCNN model
net = cv2.dnn.readNetFromTensorflow("dnn/frozen_inference_graph_coco.pb",
                                    "dnn/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt")

# Create list for transfer
def add_book_size_info(books_list, width, height, name):
    # Create a dictionary with the given information
    obj_info = bk.Book(name, height*10, width*10)
    # Add the dictionary to the list
    books_list.append(obj_info)

def process_image_and_get_books_list(image_path):
    # Initialize books list
    books_list = []

    # Generate random colors for objects (80 classes in COCO dataset)
    colors = np.random.randint(0, 255, (80, 3))

    # Load image
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.GaussianBlur(img, (3, 3), 0)
    if img is None:
        print("Error: Image not found.")
        return None  # Return None if the image is not found
    height, width = img.shape

    # Create new black image for mask visualization
    black_image = np.zeros((height, width, 3), np.uint8)
    black_image[:] = (100, 100, 0)

    # Prepare image for Mask R-CNN input
    blob = cv2.dnn.blobFromImage(img, swapRB=True)
    net.setInput(blob)

    # Run Mask R-CNN detection
    boxes, masks = net.forward(["detection_out_final", "detection_masks"])
    detection_count = boxes.shape[2]

    for i in range(detection_count):
        box = boxes[0, 0, i]
        list_num = i
        class_id = int(box[1])
        score = box[2]
        if score < 0.2:
            continue  # Skip detections with low confidence

        # Get bounding box coordinates
        x = int(box[3] * width)
        y = int(box[4] * height)
        x2 = int(box[5] * width)
        y2 = int(box[6] * height)

        # Ensure valid bounding box (x < x2 and y < y2)
        if x >= x2 or y >= y2 or x2 <= x or y2 <= y:
            continue

        # Region of interest (ROI) in black image
        roi = black_image[y:y2, x:x2]
        roi_height, roi_width, _ = roi.shape

        # Skip empty or invalid ROIs
        if roi_width <= 0 or roi_height <= 0:
            continue

        # Get object mask
        mask = masks[i, class_id]
        mask_resized = cv2.resize(mask, (roi_width, roi_height), interpolation=cv2.INTER_LINEAR)
        
        # Threshold the mask to binary (0 or 255)
        _, mask = cv2.threshold(mask_resized, 0.5, 255, cv2.THRESH_BINARY)

        # Draw the bounding box on the original image
        cv2.rectangle(img, (x, y), (x2, y2), (255, 0, 0), 3)

        # Find contours for the mask and fill the polygons in the ROI
        contours, _ = cv2.findContours(np.array(mask, np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        color = colors[class_id % len(colors)]
        for cnt in contours:
            cv2.fillPoly(roi, [cnt], (int(color[0]), int(color[1]), int(color[2])))

        # calculate width and height in CM
        width_pixels = x2 - x
        height_pixels = y2 - y
        ratio_px_mm = 153 / 14  # Example ratio, not accurate
        width_mm = width_pixels / ratio_px_mm
        width_cm = width_mm / 10
        height_mm = height_pixels / ratio_px_mm
        height_cm = height_mm / 10

        # Add the dimensions to the books list
        add_book_size_info(books_list, width_cm, height_cm, list_num)

        # Display dimensions for both width and height in CM
        # Display width
        cv2.rectangle(img, (x, y - 60), (x + 130, y - 5), (25, 15, 220), -1)
        cv2.putText(img, "Width: " "{} CM".format(round(width_cm, 2)), (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)

        # Display height
        cv2.rectangle(img, (x, y - 120), (x + 130, y - 65), (25, 15, 220), -1)
        cv2.putText(img, "Height: " + "{} CM".format(round(height_cm, 2)), (x, y - 70), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 2)

    # Show the original image with bounding boxes and masks
    cv2.imshow("Image", img)
    cv2.imshow("Black image (Masks)", black_image)

    # Print the book information (width, height, list_num)
    for book in books_list:
        print(f"Width: {book.width} cm")
        print(f"Height: {book.height} cm")
        print(f"list num: {book.name}")
        print()  # Print a new line

    # Return the list after processing
    return books_list

#Call function
#books_list = process_image_and_get_books_list("books.jpg")

# Wait until a key is pressed, then close all windows
