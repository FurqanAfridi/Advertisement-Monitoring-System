###################################################################################################################
'''
                                                PURPOSE
 This  Program is for the features extraction from video ads and to and save it to an existing model. The model
 will further help the user to monitor his ads on live broadcasts. The results will be shown to in terms of time and
 duration of his ads played in live broadcast.
'''
###################################################################################################################
import datetime
import time

'''
                                                PROGRAMMERS
 MUHAMMAD FURQAN JAVED AFRIDI (01-134191-082)
 HASSAN RAZA KHAN TAREEN (01-134191-081)
 CLASS: BS CS 8B
            
                                                CONTACTS
                                     furqanjavedafridi@gmail.com,  
                                         hrkhan390@gmail.com
                                         
                                          DATE : 01 OCT 2022
            
'''
###################################################################################################################
'''
PRE CONDITIONS: 
MUST HAVE AMS INSTALLED IN YOUR MACHINE.
MUST HAVE INTERNET TO CHECK ON LIVE BROADCASTS.

POST CONDITIONS:


'''
###################################################################################################################
'''                                                CODE                                                         '''

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# 'Defining required libraries' #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras.applications.vgg16 import VGG16
import os, shutil
from keras.preprocessing.image import ImageDataGenerator
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Convolution2D, MaxPooling2D, Flatten, Dense, Dropout, GlobalAveragePooling2D
from keras.applications import VGG16
from keras.models import Model
from keras.layers import Conv2D, MaxPool2D
import cv2
import pandas as pd
from skimage.io import imread, imshow
import vlc
import pafy
import cv2
import youtube_dl
import os

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# 'Functions Prototypes' #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def lw(bottom_model):pass
'''This is the function to attach the basemodel with the aditional required layers of CNN'''
def extract_features(directory, sample_count):pass
'''This function is extracting the features using the model base. It takes arguments directory of advertisement frames
and the number of frames exist in directory. Then by processing the frames this returns features array of 4096 for each

 frame.'''
def feed_ad(vid_loc, ad_name):pass
'''This function is '''
def files_count(to_find_dir):pass

def del_dir(loc):pass

def load_ad_features(ad_loc):pass

def match_feature(trained_features,test_features):pass

def advertisement_frames_extraction(Ad_location,Ad_name):pass

def live_broadcast_frames_extraction(ad_features):pass
'This function is to extract frames per second and to save them to the designated directory, after saving it calls the function of ' \
'features extraction to extract features from the frame, after saving the extracted features it calls the function to delete the frame' \
'which has been analyzed. After deletion of that frame it calls the function to match extracted features with the features of advertisement'

def monitor_frames(): pass

def archeive_video_frames_extraction(Archeive_location): pass
'This function is used to extract frames and pass them to features extraction function and gets back features of the frame, after getting ' \
'back the features it passes those features to the match feature function and gets back result in boolian form, and desplay the results in' \
'report section.'


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~# 'Functions Definitions' #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

monitoring_start = True
history_text = ""

#|||||||||||||||||||||||||||||||||||||||||||||||||| LIVE BROADCAST FRAMES EXTRACTION ||||||||||||||||||||||||||||||||||||||||||||||||||


def live_broadcast_frames_extraction(ad_features,url):
    video = pafy.new(url, ydl_opts={'nocheckcertificate': True})
    best = video.streams[2]
    assert best is not None
    print(best.url)
    cam = cv2.VideoCapture(best.url)

    # video frames per sec(fps)
    fps = cam.get(cv2.CAP_PROP_FPS)

    ## Parent Directory
    parent = "Datasets\\Live Frames\\"

    # frame
    currentframe = 0
    FrameNo = 0
    Ad_time = []
    sec = 0
    not30 = 0
    Text = ""
    global history_text
    while monitoring_start:
        # reading from frame
        ret, frame = cam.read()
        if FrameNo % fps == 0:
            if not os.path.exists(parent+'ClassFolder'):
                os.mkdir(parent+'ClassFolder')
            final_directory = os.path.join(parent, 'ClassFolder')
            cv2.imwrite(f"{final_directory}\\{currentframe}.jpg", frame)
            return_features = extract_features(parent, 1)
            del_dir(final_directory)
            res = match_feature(ad_features, return_features[0])
            nnn = 0
            nnn+=1
            print(nnn)
            currentframe += 1
            if res == True:
                Ad_time[sec] = datetime.datetime.now()
                Text = (f"Ad is detected from {Ad_time[0].strftime('%H:%M:%S')} to {Ad_time[sec].strftime('%H:%M:%S')} for {sec+1} seconds.<br>")
                sec+=1
                not30 = 0
            if res == False:
                not30 +=1
                if not30 == 30:
                    t = datetime.datetime.now()
                    aa = datetime.timedelta(seconds=30)
                    history_text += (f"Ad is not detected from {(t-aa).strftime('%H:%M:%S')} to {t.strftime('%H:%M:%S')} for 30 seconds.<br>")
                history_text += Text
                sec = 0
                Ad_time = []

            #if cv2.waitKey(15) & 0xFF == ord('q'): break
        # show time in seconds and frames created in this second
        FrameNo += 1
        if ret == False: break

    # Release all space and windows once done
    cam.release()
    # cv2.destroyAllWindows()

#|||||||||||||||||||||||||||||||||||||||||||||||||| ARCHEIVE VIDEO MONITORING ||||||||||||||||||||||||||||||||||||||||||||||||||


def monitor_archeive(ad_features,ar_location, ar_name):
    global history_text
    ar_frame_location = advertisement_frames_extraction(ar_location,ar_name,True)
    ar_no_of_frames = files_count(ar_frame_location)
    ar_video_features = extract_features(ar_frame_location,ar_no_of_frames)
    print(len(ar_video_features))
    del_dir(ar_frame_location)
    frames_matced = []
    matched_time = str()
    loop = 0
    for loop in range (ar_no_of_frames):
        detection = match_feature(ad_features,ar_video_features[loop])
        loop += 1
        if not monitoring_start:
            break
        if detection == True:
            frames_matced.append(loop)
    if monitoring_start:
        for m in range (len(frames_matced)):
            matched_time += f"<br> {str(datetime.timedelta(seconds=frames_matced[m]))}"
        totaltime = datetime.timedelta(seconds=len(frames_matced))
        T_text = (f"Ad matched at following time of video : <br>  {matched_time} <br> Total Time matched = {totaltime}, (Hr:Min:Sec)")
        history_text += T_text

################################# Setting Directories ############################################

base_dir = 'C:\\Users\\DELL\Jupyter Projects'
train_dir = os.path.join(base_dir, 'Ad Classification Model\\Check1Frames')
validation_dir = os.path.join(base_dir, 'Validation')
test_dir = '\\Test'
# test_dir = os.path.join(base_dir,'Test')

################################# Adding VGG16 Base and Extra Conv Layers #########################

img_width, img_height = 150, 150

batch_size = 1
datagen = ImageDataGenerator(rescale=1. / 255)
conv_base = VGG16(weights='imagenet',
                  include_top=False,
                  input_shape=(img_width, img_height, 3))


def lw(bottom_model):
    """creates the top or head of the model that will be placed ontop of the bottom layers"""

    top_model = bottom_model.output
    top_model = Dense(units=4096, activation="relu")(top_model)
    top_model = GlobalAveragePooling2D()(top_model)
    return top_model


FC_Head = lw(conv_base)
model_base = Model(inputs=conv_base.input, outputs=FC_Head)
model_base.save("MODELX")


########################################## Features Extraction ################################################

def extract_features(directory, sample_count):
    from tensorflow import keras
    feature_model = keras.models.load_model(os.path.abspath('MODELX'))
    features = np.zeros(shape=(sample_count, 4096))
    labels = np.zeros(shape=(sample_count))
    generator = datagen.flow_from_directory(
        directory,
        target_size=(150, 150),
        batch_size=batch_size,
        class_mode='binary')
    i = 0

    for inputs_batch, labels_batch in generator:
        features_batch = feature_model.predict(inputs_batch)
        features[i * batch_size: (i + 1) * batch_size] = features_batch
        labels[i * batch_size: (i + 1) * batch_size] = labels_batch
        i += 1
        if i * batch_size >= sample_count: break

    return features


############################### Feeding and loading the extracted features in local Drive ############################

def feed_ad(vid_loc, ad_name):
    frames_loc = advertisement_frames_extraction(vid_loc, ad_name)
    frames_count = files_count(frames_loc)
    print(frames_count)
    frames_features = extract_features(frames_loc, frames_count)
    # save to numpy file
    np.save(f'{ad_name}.npy', frames_features)
    del_dir(frames_loc)


########################################## Counting Frames in Directory ###############################################

def files_count(to_find_dir):
    count = 0
    for root_dir, cur_dir, files in os.walk(to_find_dir):
        count += len(files)
    return count


################################################# Delete Directory ###################################################

def del_dir(loc):
    shutil.rmtree(loc)


############################################### Load user_ad_features #############################################

def load_ad_features(ad_loc):
    # load numpy array from npy file
    from numpy import load
    # load array
    data = load(ad_loc)
    # print the array
    return data


############################################### Features Matching ####################################################
import math
def euclidean_distance(p1,p2):
    d = 0
    for i in range(len(p1)):
        d +=abs(p1[i]-p2[i])
    return d

def match_feature(ad_features, monitor_features):
    # Ad_features = the features which we have extracted from ad
    # & monitor_features = the features of archeive/live broadcast video
    from math import dist
    i = 0
    return_val = False
    ad_count = len(ad_features)
    #monitor_count = len(monitor_features)
    for i in range(ad_count):
        #a = euclidean_distance(monitor_features,ad_features[i])
        a = dist(monitor_features, ad_features[i])
        print(a)
        if (a < 1.5):
            return_val = True
            return return_val
    return return_val


###################################### ADVERTISEMENT FRAMES EXTRACTION ###############################################

def advertisement_frames_extraction(Ad_location,Ad_name, is_parent=False):
    # Read the video from specified path
    cam = cv2.VideoCapture(Ad_location)
    # video frames per sec(fps)
    fps = cam.get(cv2.CAP_PROP_FPS)

    # frame
    currentframe = 0
    FrameNo = 0
    if is_parent == False:
        parent_dir = (f"Datasets\\Ad frames\\")
    if is_parent == True:
        parent_dir = (f"Datasets\\Archeive Frames\\")
    os.makedirs(f'{parent_dir}\\{Ad_name}\\ClassX')
    Parent = os.path.join(parent_dir, f'{Ad_name}')
    final_dir = os.path.join(Parent, r'ClassX')
    while (True):

        # reading from frame
        ret, frame = cam.read()

        if FrameNo % fps == 0:
            cv2.imwrite(f"{final_dir}\\{currentframe}.jpg", frame)
            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1

        # show time in seconds and frames created in this second
        FrameNo += 1
        if ret == False:
            break

    # Release all space and windows once done
    cam.release()
    # cv2.destroyAllWindows()
    return Parent


##################################################################################################################

#______________________________________________________________________________________________________