import os
import subprocess
import argparse
import sys




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=str, help='imgs source') 

    opt = parser.parse_args()
    src = opt.directory
    if not os.path.exists(src) or not os.path.isdir(src):
        raise ValueError("Wrong path")
    cur_dir = os.getcwd()
    project_path_src = os.path.abspath(os.path.dirname(sys.argv[0]))
    os.chdir(project_path_src)
    teams = src.split(os.path.sep)[-1]
    print(teams)
    for idx, img in enumerate(os.listdir(f"{src}{os.path.sep}img")):
        print(f"processing {img}") 
        subprocess.run(["/usr/local/bin/python3",  "crop_yolo.py",  "--source", f"{src}{os.path.sep}img{os.path.sep}{img}", "--teams", teams],)
                            # stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
