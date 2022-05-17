#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 14 13:06:53 2022

@author: Nish

Wrapping into function, and adding batch processing and utility functions

Read ROI deets.md for details.

"""

def roi_process(fname, frame_show = 0, ROI_show = 0, output = 1):
    
    import cv2
    import time
    xlocs = []
    n = fname[::-1].find("/")

    if output:
        outname = fname[:-n]+"APTlyReady/"+fname[-n:-3]+"avi"

    cap = cv2.VideoCapture(fname)
    framewidth = int(cap.get(3))
    frameheight = int(cap.get(4))
    framefps = int(cap.get(5))
    framenos = int(cap.get(7))

    obj_detector = cv2.createBackgroundSubtractorKNN()

    xmin = 0
    xmax = 200
    ymin = 0
    ymax = frameheight

    count = 1

    if output:
        output = cv2.VideoWriter(outname, cv2.VideoWriter_fourcc(*'MJPG'), framefps, (200,150))

    print("processing "+fname)
    tic = time.perf_counter()
    #while True:
    #while cap.isOpened():
    for i in range(framenos):
        ret, frame = cap.read()
        if frame is not None:
            mask = obj_detector.apply(frame)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 4200:
                    #cv2.drawContours(frame, [cnt], -1, (0,0,255))  
                    x,y,w,h = cv2.boundingRect(cnt)
                    #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                    xloc = x+(w//2)
                    if xloc > 100 and xloc < (framewidth - 100): 
                        xmin = xloc - 100
                        xmax = xloc + 100
                    if xloc < 100:
                        xmin = 0
                        xmax = 200
                    if xloc > framewidth - 100:
                        xmin = framewidth - 200
                        xmax = framewidth
                    
            roi = frame[:,xmin:xmax]
            count += 1
        
            if frame_show:        
                cv2.rectangle(frame,(xmin,ymin),(xmax,ymax),(0,255,0),2)
                cv2.putText(frame, str(count), (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0),2)        
                cv2.imshow("Frame", frame)
                cv2.imshow("Mask", mask)
       
            if ROI_show:
                cv2.imshow("ROI "+fname[-n:-4], roi)
        if output:
            output.write(roi)
        xlocs += [xmin]
    cv2.destroyAllWindows() 
    cap.release()
    if output:
        output.release()
        
    toc = time.perf_counter()
    print(f"Done in {toc - tic:0.4f} seconds")
    
    #function needs to return a list of xlocs
    return xlocs
    
# Calling the function and batch processing starts here:
    
import os
from tkinter import filedialog
from tkinter import Tk
import time
import pandas as pd

print("\nWelcome to APTlyReady by Nish [ in_visilico ] Jana @ the Agrawal Lab\n")

root=Tk()
vids_path = filedialog.askdirectory()
root.destroy()

ready_path = vids_path+"/APTlyReady"
fnames = os.listdir(vids_path)

if not os.path.exists(ready_path):
    os.makedirs(ready_path)

tic = time.perf_counter()
print("\nAPTlyReady has started processing the folder:")

xlocs_dict = {}
count = 1
fcount = len(next(os.walk(vids_path))[2])

for i in fnames:
    # check if the listing is a file by "."
    if "." in i:
        print("\n[File "+str(count)+"/"+str(fcount)+"]")
        count += 1
        j = vids_path+"/"+i
        xlocs_dict[i] = roi_process(j)
        
xlocs_df = pd.DataFrame(xlocs_dict)
xlocs_df.to_csv((ready_path+"/xlocs.csv"))
print("\nLocation of each fly saved in APTlyReady/xlocs.csv")
        
toc = time.perf_counter()
t_min = (toc-tic)/60
print(f"\nFolder processed in {t_min:0.1f} minutes.\n")
