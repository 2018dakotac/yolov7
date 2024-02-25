from PIL import Image
import os

# Get list of HEIF and HEIC files in directory
input_directory = '/path/to/directory'
output_directory = '/path/to/output'  # Specify the output directory
files = [f for f in os.listdir(input_directory) if f.endswith('.heic') or f.endswith('.heif')]

# Convert each file to JPEG and save in the specified output directory
for filename in files:
    input_path = os.path.join(input_directory, filename)
    output_path = os.path.join(output_directory, os.path.splitext(filename)[0] + '.jpg')

    image = Image.open(input_path)
    image.convert('RGB').save(output_path)
