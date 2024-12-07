import os
from PIL import Image
import cv2
import numpy as np
import pandas as pd

def preprocess_image(image, target_size):
    h, w, _ = image.shape
    scale = min(target_size / w, target_size / h)
    new_w, new_h = int(w * scale), int(h * scale)

    resized_image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    pad_w = (target_size - new_w) // 2
    pad_h = (target_size - new_h) // 2

    padded_image = cv2.copyMakeBorder(resized_image, pad_h, target_size - new_h - pad_h,
                                      pad_w, target_size - new_w - pad_w,
                                      cv2.BORDER_CONSTANT, value=(0, 0, 0))
    return padded_image




# Function to convert CSV bounding boxes to YOLO format
def convert_bboxes_to_yolo(csv_file, folder_images, output_directory, target_size=416):
    # Load the CSV file
    df = pd.read_csv(csv_file)

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Loop through each row in the CSV to convert bounding boxes
    for _, row in df.iterrows():
        image_name = row['FileName']
        digit_label = row['DigitLabel']
        left = row['Left']
        top = row['Top']
        width = row['Width']
        height = row['Height']

        # Create the full path for the image
        image_path = os.path.join(folder_images, image_name)

        # Read the image to get the original size
        img = cv2.imread(image_path)

        # Check if the image was read successfully
        if img is None:
            print(f"Error reading image: {image_path}")
            continue

        # Get the original dimensions of the image
        old_width = img.shape[1]
        old_height = img.shape[0]

        # Preprocess the image (resize to target size)
        processed_image = preprocess_image(img, target_size)

        # Resize the bounding box coordinates to match the target image size
        x_center = (left + width / 2) / old_width
        y_center = (top + height / 2) / old_height
        normalized_width = width / old_width
        normalized_height = height / old_height

        # Create the YOLO formatted string: <class_id> <x_center> <y_center> <width> <height>
        yolo_bbox = f"{digit_label} {x_center} {y_center} {normalized_width} {normalized_height}"

        # Get the filename without extension
        filename = os.path.splitext(image_name)[0]

        # Define the path for the label file (same name as image, but with .txt extension)
        label_file_path = os.path.join(output_directory, f"{filename}.txt")

        # Write the YOLO formatted bounding box to the label file
        with open(label_file_path, 'a') as label_file:
            label_file.write(yolo_bbox + '\n')

        # Save the processed image (if required)
        output_image_path = os.path.join(output_directory, f"{filename}.jpg")
        cv2.imwrite(output_image_path, processed_image)

#
# # Example usage:
# csv_file = 'bounding_boxes.csv'  # Path to your CSV file
# folder_images = "SVHNLite/test"  # Path to the images
# output_directory = "output"  # Path to save the output labels and images
# convert_bboxes_to_yolo(csv_file, folder_images, output_directory, target_size=416)

if  __name__ == '__main__':
# Example usage:


    csv_file = 'train_digitStruct.csv'  # Path to your CSV file
    folder_images = "SVHNLite/train"  # Path to the images
    output_directory = "output"  # Path to save the output labels and images
    convert_bboxes_to_yolo(csv_file, folder_images, output_directory, target_size=1280)

#------------------------------------------------------

# For scaling and padding only
# folder_images = "SVHNLite/test"
    # output_directory = "output"
    #
    # # Ensure the output directory exists
    # os.makedirs(output_directory, exist_ok=True)
    #
    # for dirpath, _, filenames in os.walk(folder_images):
    #     for path_image in filenames:
    #         image_path = os.path.abspath(os.path.join(dirpath, path_image))
    #
    #         # Extract the filename without the extension
    #         filename = os.path.splitext(path_image)[0]
    #
    #         # Read the image using cv2.imread
    #         img = cv2.imread(image_path)
    #
    #         # Check if the image was read successfully
    #         if img is None:
    #             print(f"Error reading image: {image_path}")
    #             continue
    #
    #         # Preprocess the image
    #         processed_image = preprocess_image(img, 1280)
    #
    #         # Save the processed image with the extracted filename
    #         output_path = os.path.join(output_directory, f"{filename}.jpg")
    #         cv2.imwrite(output_path, processed_image)

    #image = cv2.imread("example.jpg")
    #processed_image = preprocess_image(image, 416)
    #cv2.imwrite("processed_image.jpg", processed_image)


