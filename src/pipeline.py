import os
import cv2
import subprocess
import sys

def cut_mp4(filename: str, start: int, end: int, new_name: str):
    os.system(f'ffmpeg -i {filename} -ss {start} -to {end} -y {new_name}')


def process_mp4(txt_path, mp4_path, new_path):
    counter = 1

    with open(txt_path, 'r', encoding='utf-8') as time_file:
        timestamps = time_file.readlines()
    for idx, time_pair in enumerate(timestamps):
        time_pair = time_pair.replace('\n', '')
        time_pair = time_pair.replace(' ', '')
        start, end = time_pair.split(',')
        cut_mp4(mp4_path, start, end, f'{new_path}/{counter}.mp4')
        counter += 1


def mp4_to_png():
    directory = os.fsencode(f'test_data/src')
    fragment_n = 1
    for fragment in os.listdir(directory):
        counter = 1
        print(os.fsdecode(fragment))
        if os.fsdecode(fragment)[-4:] == '.mp4':
            try:
                a = int(os.fsdecode(fragment)[:-4])
            except:
                continue
            os.mkdir(f"test_data/img/{fragment_n}")
            vidcap = cv2.VideoCapture(f'test_data/src/{os.fsdecode(fragment)}')
            success, image = vidcap.read()
            
            while success:
                cv2.imwrite(f"test_data/img/{fragment_n}/{counter}.png", image)    
                success, image = vidcap.read()
                print(counter)
                counter += 1
            fragment_n += 1

def process_frame(path, centroids: list):

    cur_dir = os.getcwd()
    project_path_src = os.path.abspath(os.path.dirname(sys.argv[0]))
    project_path = os.path.sep.join(project_path_src.split(os.path.sep))
    if not os.path.exists(f"{project_path}/yolov7"):
        raise ValueError("No yolov7 model in project")
    os.chdir(f"{project_path}/yolov7")
    subprocess.run(["/usr/local/bin/python3",  "detect.py", "--weights", "yolov7.pt", "--conf", "0.25", 
                            "--img-size", "640", "--source", path, "--save-txt", "--nosave"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.chdir(project_path)
    # if centroids == []:
    #     box_num = 5
    #     # os.system(f"pip install imutils")
    #     os.system(f"/usr/local/bin/python3 ./yolov7/detect.py --weights yolov7.pt --conf 0.25 --no-save --save-txt --img-size 640 --source {path}")
        



def main(fragment_num):
    vid_path = f"/Users/shevdan/Documents/Programming/ML/Player_recognition/test_data/img/{fragment_num}"
    counter = len(os.listdir(vid_path))
    player_data = {
        'to_classify': True,
        'team': '',
        'jersey': '',
        'stats': ''
    }
    for i in range(1, counter+1):
        print(i)
        player_data = process_frame(path=f'{vid_path}/{i}.png', centroids=[])
        # break

if __name__ == "__main__":
    main(fragment_num=3)