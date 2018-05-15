import cv2
import pandas as pd
import numpy as np
from os import listdir

data_name = input("Please Input Data Name: \n(Just Enter if you use all data)")

if data_name:
    data_names = [data_name]

else:
    data_names = [x[:-4] for x in listdir('./logs') if x[-4:]=='.csv']

for data_name in data_names:
    data_df = pd.read_csv('./logs/'+data_name+'.csv', names=['name','output'])
    names = data_df['name'].values
    outputs = data_df['output'].values

    for name in names:
        path = "./imgs/"+data_name+'/'+name
        img = cv2.imread(path)
        img = cv2.resize(img, (400,200),interpolation=cv2.INTER_AREA)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #img = cv2.Canny(img, threshold1 = 500, threshold2=100)
        #img_u = img[0:50,100:]
        #img_d = img[130:,100:]
        #img = np.concatenate((img_u, img_d))
        
        
        cv2.imwrite(path, img)

print("Complete!")

