import os
import argparse


# If you use \ for file paths, don't forget to escape them to avoid issues.
# *** weight names using ANY UPPERCASE LETTERS may fail due issue with YOLO software itself 



def run_detection(weights_folder, target_folder):
    # Loop through each weight file
    for weight_file in os.listdir(weights_folder):
        if weight_file.endswith('.pt'):
            weight_path = os.path.join(weights_folder, weight_file)
            print(weight_path)
            weight_name = os.path.splitext(weight_file)[0]
            
            # Argument tweaking:
            # --conf is the confidence cutoff so anything with lower confidence is ignored  
            # --no-trace is faster if the number of images is small like 50 or less, otherwise traced model ends is overall faster
            # if you wish to see the prediction on the actual images remove --nosave
            
            command = f"python detect.py --weights {weight_path} --exist-ok --save-txt --save-conf --nosave --img 640 --conf 0.3 --source {target_folder} --name {weight_name}"
            # Run the detection command
            os.system(command)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run detection using weights on images in the target folder.")
    parser.add_argument("--weights_folder", required=True, help="Path to the folder containing weights files.")
    parser.add_argument("--target_folder", required=True, help="Path to the target folder containing images.")

    args = parser.parse_args()

    run_detection(args.weights_folder, args.target_folder)
