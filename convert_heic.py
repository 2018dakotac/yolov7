from PIL import Image, ImageSequence
import os
import argparse
import pyheif

def convert_heic_to_jpeg(input_directory, output_directory):
    # Get list of HEIF and HEIC files in directory
    files = [f for f in os.listdir(input_directory) if f.endswith('.heic') or f.endswith('.heif')]

    # Convert each file to JPEG and save in the specified output directory
    for filename in files:
        input_path = os.path.join(input_directory, filename)
        output_path = os.path.join(output_directory, os.path.splitext(filename)[0] + '.jpg')

        heif_file = pyheif.read(input_path)

        # Explicitly specify the HEIC plugin for Pillow
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
            heif_file.mode,
            heif_file.stride,
        )

        image.convert('RGB').save(output_path)

def main():
    parser = argparse.ArgumentParser(description='Convert HEIC/HEIF files to JPEG.')
    parser.add_argument('input_directory', help='Input directory containing HEIC/HEIF files')
    parser.add_argument('output_directory', help='Output directory to save converted JPEG files')
    args = parser.parse_args()

    convert_heic_to_jpeg(args.input_directory, args.output_directory)

if __name__ == "__main__":
    main()