import os

weights_folder = 'weights/'  # Replace with the actual path to your weights folder

# Loop through each weight file
for weight_file in os.listdir(weights_folder):
    if weight_file.endswith('.pt'):
        weight_path = os.path.join(weights_folder, weight_file)
        print(weight_path)
        weight_name = os.path.splitext(weight_file)[0]
        # Construct the command with the current weights file
        #***if you use \ for file paths dont forget to escape them so they dont cause an issue with \t becoming a tab
        # --no-trace is faster if the number of images is small like 50 or less otherwise tracing ends up being faster
        command = f"python detect.py --weights {weight_path} --exist-ok --save-txt --save-conf --nosave --img 640 --conf 0.3 --source data/pipe_railing_YOLO/test --name {weight_name}"
        # Run the command
        os.system(command)