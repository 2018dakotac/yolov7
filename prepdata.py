import os
import shutil
import zipfile

def move_txt_files(directory):
    labels_folder = os.path.join(directory, 'labels')

    # Check if the "labels" folder exists
    if os.path.exists(labels_folder):
        # Move all text files out of the "labels" folder
        for txt_file in os.listdir(labels_folder):
            txt_path = os.path.join(labels_folder, txt_file)
            dest_path = os.path.join(directory, txt_file)
            shutil.move(txt_path, dest_path)
            #print(f"Moved: {txt_file}")

        # Remove the "labels" folder
        os.rmdir(labels_folder)
        print("Removed: 'labels' folder")
    else:
        print("Error: No 'labels' folder found. Stopping.")
        exit(1)

def create_empty_txt_files(directory):
    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.lower().endswith((".jpg", ".jpeg", ".webp", ".png")):
            txt_path = os.path.join(directory, os.path.splitext(filename)[0] + ".txt")

            # Check if corresponding TXT file exists
            if not os.path.exists(txt_path):
                # Create an empty TXT file if missing
                open(txt_path, 'w').close()
                print(f"Created empty TXT file: {os.path.basename(txt_path)}")

def copy_photos_from_newdata(directory):
    newdata_folder = os.path.join('..', '..', 'data', 'NEWDATA')
    
    # Check if the "NEWDATA" folder exists
    if os.path.exists(newdata_folder):
        # Copy all photos from "NEWDATA" to the specified directory
        for photo_file in os.listdir(newdata_folder):
            if photo_file.lower().endswith(('.jpg', '.jpeg', '.webp', '.png')):
                src_path = os.path.join(newdata_folder, photo_file)
                dest_path = os.path.join(directory, photo_file)
                shutil.copy(src_path, dest_path)
                #print(f"Copied: {photo_file}")

        # Create empty TXT files for photos without one
        create_empty_txt_files(directory)

    else:
        print("Error: No 'NEWDATA' folder found. Stopping.")
        exit(1)


def create_obj_data_file(directory):
    obj_data_file_path = os.path.join(directory, "obj.data")
    # Create an obj.data file only if it doesn't already exist
    if not os.path.exists(obj_data_file_path):
        with open(obj_data_file_path, 'w') as obj_data_file:
            obj_data_file.write("classes = 1\n")
            obj_data_file.write("Train = data/Train.txt\n")
            obj_data_file.write("names = data/obj.names\n")
            obj_data_file.write("backup = backup/")
        print(f"Created obj.data file: {os.path.basename(obj_data_file_path)}")

def create_obj_names_file(directory,class_name):
    obj_names_file_path = os.path.join(directory, "obj.names")
    # Create an obj.names file only if it doesn't already exist
    if not os.path.exists(obj_names_file_path):
        with open(obj_names_file_path, 'w') as obj_data_file:
            obj_data_file.write(f"{class_name}")
        print(f"Created obj.names file: {os.path.basename(obj_names_file_path)}")

def zip_directory(directory, class_name):
    zip_filename = f"{class_name}.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        base_folder_name = os.path.basename(directory)
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                # Calculate the relative path with respect to the specified directory
                rel_path = os.path.relpath(file_path, directory)
                # Include the base folder name in the arcname
                arcname = os.path.join(base_folder_name, rel_path)
                zip_file.write(file_path, arcname)

        # Add additional files to the zip
        obj_data_file_path = os.path.join("obj.data")
        obj_names_file_path = os.path.join("obj.names")
        train_txt_path = os.path.join("Train.txt")

        zip_file.write(obj_data_file_path, os.path.basename(obj_data_file_path))
        zip_file.write(obj_names_file_path, os.path.basename(obj_names_file_path))
        zip_file.write(train_txt_path, os.path.basename(train_txt_path))

    print(f"Created zip file: {zip_filename}")

if __name__ == "__main__":

    # TODO: make this work from outside run directory and also add the obj_Validation_data folder as well as corresponding Validation.txt file with image paths
    # Hardcoded directory path
    directory_path = 'obj_Train_data'

    # Copy photos from "NEWDATA" to the specified directory
    copy_photos_from_newdata(directory_path)

    # Move text files out of the "labels" folder and remove the "labels" folder
    move_txt_files(directory_path)
    
    #add empty labels for non recognized images
    create_empty_txt_files(directory_path)
    
    # Create "obj.data" file
    create_obj_data_file('.')

    # Prompt user for the class name
    class_name = input("Enter the name of the class: ")

    # Create "obj.names" file
    create_obj_names_file('.',class_name)

    # Zip the directory along with additional files
    zip_directory(directory_path, class_name)
