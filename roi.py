#!/usr/bin/env python3

import cv2

frame_show = 1 #If you want to see the entire frame
ROI_show = 0 #if you want to see the ROI
output = 0 # if you want output in /processed
sort_show = 1 # if you want to see classification

fname = "/home/cwo/APTlybad/vids/v1f1.mp4"
n = fname[::-1].find("/")

if output:
    outname = fname[:-n]+"processed/"+fname[-n:-3]+"avi"

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

xlocs = []
count = 1

if output:
    output = cv2.VideoWriter(outname, cv2.VideoWriter_fourcc(*'MJPG'), framefps, (200,150))

print("starting to process...")
#while True:
#while cap.isOpened():
for i in range(framenos):
    ret, frame = cap.read()
    if frame is not None:
        xmin_old = xmin
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
        xlocs += xmin
        # sort determination
        """
        Determining sort
        sort is labelled as: Right, Left, Groom, Retreat
        """
        if sort_show:
            if (xmin - xmin_old) > 0: sort = "Right"
            if (xmin - xmin_old) < 0: sort = "Left"
            if xmin == xmin_old: sort = "Groom"
            if xmin < 150 or xmax > (framewidth-150): sort = "Retreat"
        
        roi = frame[:,xmin:xmax]
        count += 1
    
        if frame_show:        
            cv2.rectangle(frame,(xmin,ymin),(xmax,ymax),(0,255,0),2) # Display ROI
            #cv2.putText(frame, str(count), (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0),2) #frame counter

            if sort_show:
                if sort == "Right": cv2.putText(frame, sort, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0),2) # print in green
                if sort == "Left": cv2.putText(frame, sort, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0),2) # print in blue
                if sort == "Groom": cv2.putText(frame, sort, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0),2) # print in black
                if sort == "Retreat": cv2.putText(frame, sort, (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),2) # print in red
            
            cv2.imshow("Frame", frame)
            #cv2.imshow("Mask", mask)
   
        if ROI_show:
            cv2.imshow("ROI", roi)
    if output:
        output.write(roi)
   
    key = cv2.waitKey(1)
    if key == 27:
        break
     
cv2.destroyAllWindows() 
cap.release()
if output:
    output.release()
    


print("Succesfully Processed!")

