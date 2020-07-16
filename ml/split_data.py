#!/usr/bin/python

import os
import numpy as np
import pandas as pd
import seaborn as sns
from pathlib import Path
import shutil
import sys

if len(sys.argv) < 2:
    print("Provide data path as argument: python script.py path")
    sys.exit(2)

PATH = sys.argv[1]
training_data = Path(PATH + '/training/') 
validation_data = Path(PATH + '/validation/') 
labels_path = Path(PATH + '/monkey_labels.txt')

labels_dict= {'n0':0, 'n1':1, 'n2':2, 'n3':3, 'n4':4, 'n5':5, 'n6':6, 'n7':7, 'n8':8, 'n9':9}

train_df = []
for folder in os.listdir(training_data):
    # Define the path to the images
    imgs_path = training_data / folder
    
    # Get the list of all the images stored in that directory
    imgs = sorted(imgs_path.glob('*.jpg'))
    
    # Store each image path and corresponding label 
    for img_name in imgs:
        train_df.append((str(img_name), labels_dict[folder]))


train_df = pd.DataFrame(train_df, columns=['image', 'label'], index=None)
# shuffle the dataset 
train_df = train_df.sample(frac=1.).reset_index(drop=True)

valid_df = []
for folder in os.listdir(validation_data):
    imgs_path = validation_data / folder
    imgs = sorted(imgs_path.glob('*.jpg'))
    for img_name in imgs:
        valid_df.append((str(img_name), labels_dict[folder]))

        
valid_df = pd.DataFrame(valid_df, columns=['image', 'label'], index=None)
# shuffle the dataset 
valid_df = valid_df.sample(frac=1.).reset_index(drop=True)

print("Number of traininng samples: ", len(train_df))
print("Number of validation samples: ", len(valid_df)) 
df = pd.concat([train_df, valid_df], axis=0) 

def train_validate_test_split(df, train_percent=.70, validate_percent=.15, seed=None): 
    np.random.seed(seed) 
    perm = np.random.permutation(df.index)
    m = len(df.index)
    train_end = int(train_percent * m)
    validate_end = int(validate_percent * m) + train_end
    train = df.iloc[perm[:train_end]]
    validate = df.iloc[perm[train_end:validate_end]]
    test = df.iloc[perm[validate_end:]]
    return train, validate, test


# split dataset
split_data = train_validate_test_split(df)
train = split_data[0]
valid = split_data[1]
test = split_data[2]
 
shutil.rmtree(PATH + '/exports')

os.mkdir(PATH + '/exports')
os.mkdir(PATH + '/exports/train')
os.mkdir(PATH + '/exports/test')
os.mkdir(PATH + '/exports/valid')

# set working directory

def export_data(data, name):
    for i in range(0, 10):
        os.mkdir(PATH + '/exports/' + name + '/n' + str(i))
    for index, item in data.iterrows():
        dest = "%s/exports/%s/n%d" % (PATH, name, item['label'])
        shutil.copy(item['image'], dest)        

export_data(train, 'train')  
export_data(valid, 'valid')  
export_data(test, 'test')  
