import os
import shutil
import random

# Function to copy a set number of classes and images per class from the original database source.
def copy_images_to_selected(source_dir, destination_dir, num_classes=10, num_images_per_class=100):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir) # Create output directory if non-existent

    food_classes = os.listdir(source_dir) # Get a list of all classes
    selected_classes = random.sample(food_classes, min(num_classes, len(food_classes))) # Randomly select classes

    # Iterate through food classes
    for food_class in selected_classes:
        food_class_dir = os.path.join(source_dir, food_class)
        if os.path.isdir(food_class_dir):
            images = [file for file in os.listdir(food_class_dir) if file.lower().endswith(".jpg")] # Store all .jpg files as a list
            selected_images = random.sample(images, min(num_images_per_class, len(images))) # Randomly select image samples

            food_class_destination_dir = os.path.join(destination_dir, food_class)
            if not os.path.exists(food_class_destination_dir):
                os.makedirs(food_class_destination_dir)

            # Copy the selected images to the destination directory with given labeling syntax standard
            for idx, image in enumerate(selected_images):
                src_path = os.path.join(food_class_dir, image)
                dst_filename = f"{food_class}_{idx + 1}.jpg"
                dst_path = os.path.join(food_class_destination_dir, dst_filename)
                shutil.copy(src_path, dst_path)

# Function to split the copied images into Train, Test, and Validation sets based on specified ratios
def split_data_into_train_test_val(source_dir, destination_dir, train_ratio=0.4, test_ratio=0.3):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Iterate through each food class
    for food_class in os.listdir(source_dir):
        food_class_dir = os.path.join(source_dir, food_class)
        if os.path.isdir(food_class_dir):
            images = [file for file in os.listdir(food_class_dir) if file.lower().endswith(".jpg")]
            random.shuffle(images)

            num_images = len(images)
            num_train = int(train_ratio * num_images)
            num_test = int(test_ratio * num_images)
            num_val = num_images - num_train - num_test

            train_images = images[:num_train]
            test_images = images[num_train:num_train + num_test]
            val_images = images[num_train + num_test:]

            train_folder = os.path.join(destination_dir, "Train", food_class)
            test_folder = os.path.join(destination_dir, "Test", food_class)
            val_folder = os.path.join(destination_dir, "Validation", food_class)

            os.makedirs(train_folder, exist_ok=True)
            os.makedirs(test_folder, exist_ok=True)
            os.makedirs(val_folder, exist_ok=True)

            # Copy images to Train, Test, and Validation folders
            for image in train_images:
                src_path = os.path.join(food_class_dir, image)
                dst_path = os.path.join(train_folder, image)
                shutil.copy(src_path, dst_path)

            for image in test_images:
                src_path = os.path.join(food_class_dir, image)
                dst_path = os.path.join(test_folder, image)
                shutil.copy(src_path, dst_path)

            for image in val_images:
                src_path = os.path.join(food_class_dir, image)
                dst_path = os.path.join(val_folder, image)
                shutil.copy(src_path, dst_path)


base_directory = "selectedImages"
food_directory = "Food"
num_classes_to_copy = 10
num_images_per_class_to_copy = 100

copy_images_to_selected(base_directory, food_directory, num_classes_to_copy, num_images_per_class_to_copy)
split_data_into_train_test_val(food_directory, food_directory)
