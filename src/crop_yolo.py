import subprocess
import os
import argparse
import sys
import shutil
import time
import cv2
import random

def crop(img_path, teams):
    cur_dir = os.getcwd()
    project_path_src = os.path.abspath(os.path.dirname(sys.argv[0]))
    project_path = os.path.sep.join(project_path_src.split(os.path.sep)[:-1])
    if not os.path.exists(f"{project_path}/yolov7"):
        raise ValueError("No yolov7 model in project")
    os.chdir(f"{project_path}/yolov7")
    if os.listdir(f"{project_path}/yolov7/runs/detect"):
        # there are nonempty results from prev runs
        for run in os.listdir(f"{project_path}/yolov7/runs/detect"):
            shutil.rmtree(f"{project_path}/yolov7/runs/detect/{run}")
    subprocess.run(["python3",  "detect.py", "--weights", "yolov7.pt", "--conf", "0.25", 
                            "--img-size", "640", "--source", img_path, "--save-txt", "--nosave"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # time.sleep(3)
    bdnbxes = []
    filename = os.path.splitext(img_path.split(os.path.sep)[-1])[0]
    
    labels_path = f"{project_path}/yolov7/runs/detect/exp/labels/{filename}.txt"
    if os.path.exists(labels_path):
        with open(labels_path, mode="r") as labels:
            for line in labels:
                box = line.strip().split()
                if box[0] != "0":
                    continue
                bdnbxes.append([float(coord) for coord in box[1:]])


        
        os.chdir(project_path)

        for directory in ["./data", "./data/players", f"./data/players/{teams}"]:
            if not os.path.exists(directory):
                os.mkdir(directory)
        
        img = cv2.imread(img_path)
        imH, imW, _ = img.shape
        
        for idx, bdnbx in enumerate(bdnbxes):
            x_center, y_center, box_w, box_h, = int(bdnbx[0] * imW), int(bdnbx[1] * imH), int(bdnbx[2] * imW), int(bdnbx[3] * imH)
            x1, x2 = max(x_center - box_w // 2, 0), max(x_center + box_w //2, 0)
            y1, y2 = max(y_center + box_h // 2, 0), max(y_center - box_h // 2, 0)
            cropped_img = img[y2:y1, x1:x2]
            cv2.imwrite( f"./data/players/{teams}/{teams}_{filename}_{idx}.png", cropped_img)
        
    os.chdir(cur_dir)

if __name__ == "__main__":
    # import time
    # now = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=str, default='inference/images', help='source')  # file/folder, 0 for webcam
    parser.add_argument('--teams', type=str, default="Team1_Team2", help='naming of the teams of the match')

    opt = parser.parse_args()
    crop(opt.source, opt.teams)
    # print(time.time() - now, "seconds")