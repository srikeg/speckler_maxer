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

    script_path = os.path.expanduser("~/speckler_maxer/scripts/pi_one_snapshot.sh")
    result = subprocess.run([script_path, image_path], capture_output=True, text=True)

    saved_path = result.stdout.strip()
    print("Image saved at:", saved_path)

    return eval.classify_single_image(saved_path)