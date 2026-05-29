import subprocess
import os
import sys
from ml import eval
from datetime import datetime

def scan():

    outdir = os.path.expanduser("~/Desktop/images")
    os.makedirs(outdir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = f"{outdir}/snapshot_{timestamp}.jpg"

    script_path = os.path.expanduser("~/speckler_maxer/scripts/save_snapshot.sh")
    # script_path = os.path.expanduser("~/speckler_maxer/scripts/pi_one_snapshot.sh")
    result = subprocess.run([script_path, image_path], capture_output=True, text=True)

    # print(f"result: {result}")
    # saved_path = result.stdout.strip()
    # print("Image saved at:", saved_path)

    print(f"Image saved at {image_path}")

    return eval.classify_single_image(image_path), image_path