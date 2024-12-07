import cv2

# Function to read bounding boxes from a YOLO .txt file
def read_bboxes_from_txt(txt_file):
    bboxes = []
    with open(txt_file, 'r') as f:
        for line in f:
            # Split the line by spaces and convert to float
            parts = line.strip().split()
            class_id = int(parts[0])
            x_center = float(parts[1])
            y_center = float(parts[2])
            width = float(parts[3])
            height = float(parts[4])
            bboxes.append([class_id, x_center, y_center, width, height])
    return bboxes

# Function to visualize bounding boxes on an image
def visualize_bboxes(image_path, txt_file):
    # Read the image
    img = cv2.imread(image_path)

    # Check if the image was read successfully
    if img is None:
        print(f"Error reading image: {image_path}")
        return

    # Read the bounding boxes from the .txt file
    bboxes = read_bboxes_from_txt(txt_file)

    # Loop through each bounding box and draw it on the image
    for bbox in bboxes:
        # Bounding box format: [class_id, x_center, y_center, width, height]
        class_id, x_center, y_center, width, height = bbox

        # Convert from normalized coordinates to pixel values
        img_height, img_width = img.shape[:2]
        left = int((x_center - width / 2) * img_width)
        top = int((y_center - height / 2) * img_height)
        right = int((x_center + width / 2) * img_width)
        bottom = int((y_center + height / 2) * img_height)

        # Draw a rectangle on the image
        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)  # Green color for rectangle

        # Optionally, put a label with the class ID
        cv2.putText(img, f"Class {class_id}", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the image with bounding boxes
    cv2.imshow("Image with Bounding Boxes", img)
    cv2.waitKey(0)  # Wait until any key is pressed
    cv2.destroyAllWindows()  # Close the window

# Example usage:
image_path = "output/20.jpg"  # Path to an example image
txt_file = "output/20.txt"  # Path to the corresponding YOLO label file (txt file with bounding boxes)
visualize_bboxes(image_path, txt_file)
