import os
import json
import pandas as pd

def process_text_file(file_path):
    file_name = os.path.basename(file_path)
    image = os.path.splitext(file_name)[0]  # Extract prediction class from file name 
    highest_confidence = 0  # Default value
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

        for line in lines:
            # Split the line into individual digits
            digits = line.split()
            
            # Check if the line has at least six digits, the last/6th one is the confidence of the prediction
            if len(digits) >= 6:
                try:
                    confidence = float(digits[5])
                    highest_confidence = max(highest_confidence, confidence)
                except ValueError:
                    print(f"Skipping line: {line.strip()} - Not a valid number")
    
    return image, highest_confidence

def process_image_folder(image_folder_path, output_folder):
    class_name = os.path.basename(image_folder_path)
    labels_folder_path = os.path.join(image_folder_path, 'labels')
    
    if not os.path.exists(labels_folder_path) or not os.path.isdir(labels_folder_path):
        print(f"Warning: 'labels' folder not found or empty in {image_folder_path}")
        return

    # Check if 'labels' folder is empty
    if not os.listdir(labels_folder_path):
        print(f"Warning: 'labels' folder is empty in {image_folder_path}")
        return

    predictions = []

    # Iterate through each text file in the 'labels' folder
    for file_name in os.listdir(labels_folder_path):
        file_path = os.path.join(labels_folder_path, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.txt'):
            image, confidence = process_text_file(file_path)
            predictions.append({"image": image, "confidence": confidence, "class": class_name})

    # Construct the output JSON file path
    output_json_path = os.path.join(output_folder, f"{class_name}.json")

    # Write the list of predictions to the single JSON file
    with open(output_json_path, 'w') as json_file:
        json.dump(predictions, json_file, indent=2)



def create_excel_sheet(json_folder_path, output_excel_path):
    # Create an empty DataFrame
    df = pd.DataFrame()

    if not os.path.exists(json_folder_path) or not os.path.isdir(json_folder_path):
        print(f"Warning: '{json_folder_path}' folder not found or empty")
        return

    # Iterate through each JSON file in the folder
    for filename in os.listdir(json_folder_path):
        if filename.endswith('.json'):
            json_path = os.path.join(json_folder_path, filename)
            with open(json_path, 'r') as json_file:
                # Load JSON data
                json_data = json.load(json_file)

                # Iterate through each entry in the JSON list
                for entry in json_data:
                    # Append the entry to the main DataFrame
                    df = df.append(entry, ignore_index=True)

    # Save the DataFrame to an Excel file
    df.to_excel(output_excel_path, index=False)
    print(f"Excel file created at: {output_excel_path}")
    
def merge_json_files(input_directory,output_directory):

    # Create the result dictionary to store merged data
    result_dict = {}

    # Loop through each file in the directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".json"):
            file_path = os.path.join(input_directory, filename)

            # Load the JSON file
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Process each entry in the JSON file
            for entry in data:
                image_key = entry['image']
                class_value = entry['class']
                confidence_value = entry['confidence']

                # Create the result_dict if the image_key does not exist
                if image_key not in result_dict:
                    result_dict[image_key] = {}

                # Add or update the class_value and confidence_value
                result_dict[image_key][class_value] = confidence_value

    # Set the output file path
    output_file_path = os.path.join(output_directory, "predictions.json")

    # Write the merged data to the output file
    with open(output_file_path, 'w') as output_file:
        json.dump(result_dict, output_file, indent=2)
        

def main():
    detect_folder_path = 'runs/detect'  # Update this with the actual path

    #Iterate through each subfolder in the 'detect' folder
    for subfolder_name in os.listdir(detect_folder_path):
        subfolder_path = os.path.join(detect_folder_path, subfolder_name)

        #Check if it's a directory
        if os.path.isdir(subfolder_path):
            process_image_folder(subfolder_path, detect_folder_path)

    # Combine top predictions after processing all subfolders
    merge_json_files(detect_folder_path,'.')

if __name__ == "__main__":
    main()