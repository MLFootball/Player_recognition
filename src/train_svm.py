from skimage.feature import hog
import joblib,glob,os,cv2

from sklearn.svm import LinearSVC
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn import svm, metrics
import numpy as np 
from sklearn.preprocessing import LabelEncoder

train_data = []
train_labels = []
pos_im_path = "/Users/shevdan/Documents/Programming/ML/Player_recognition/SoccerNet/jersey-2023/test/images" 
neg_im_path= "/Users/shevdan/Documents/Programming/ML/Player_recognition/natural_images"
model_path = 'models/models.npy'

for subdir, dirs, files in os.walk(neg_im_path):
    print("Negative. Dir:", subdir)
    for file in files:
        fd = cv2.imread(f"{subdir}/{file}",0)
        fd = cv2.resize(fd,(64,128))
        fd = hog(fd,orientations=9,pixels_per_cell=(8,8),visualize=False,cells_per_block=(3,3))
        train_data.append(fd)
        train_labels.append(0)

for subdir, dirs, files in os.walk(pos_im_path):
    print("Positive. Dir: ", subdir)
    for file in files:
        fd = cv2.imread(f"{subdir}/{file}",0)
        fd = cv2.resize(fd,(64,128))
        fd = hog(fd,orientations=9,pixels_per_cell=(8,8),visualize=False,cells_per_block=(3,3))
        train_data.append(fd)
        train_labels.append(1)


train_data = np.float32(train_data)
train_labels = np.array(train_labels)

print("Training SVM")
model = LinearSVC()
model.fit(train_data,train_labels)
joblib.dump(model, 'svm.npy')
