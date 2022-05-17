# APTLY Ready
___

The APT Preprocessor is meant to be an efficient tool to preprocess tons of video footage of really high resolutions/frame rates using opencv and python3.

Made by Nish [invisilico] @ the Agrawal lab to pre-process footage for post estimation with APT.

It allows you to select a folder containing all the videos and 

Tracking uses the K nearest neighbour algorithm to pick out the largest moving objects (in this case one fly). KNN with default () settings works
really really well for flies in motion. But stagnant flies (grooming, PER, etc.) are not detected - the mask decays. This is not particularly and issue and is readily tackled by using a constantly updating xy location which is maintained even when the fly is not in motion

opencv provides a contour function to outline objects, as well as a rectangle bounding box option, the centre of which is roughly the centre for large blobby objects. We use the centre of this rectangle to determine centre for our ROI, and data from 100px either side (200 wide) and the entire height of the frame is kept.

Python Dependencies:

(Preferably use an anaconda python3 distribution)
 
> Python3.9
> opencv-python 4.5.5.64 (+contrib, numpy)
> tkinter
> os
> pandas
> time


## How to use:

On linux - We use Pop!_OS 22.04LTS

open a bash terminal in the directory of the script:

```
$ conda activate

$ python3 APTlyReady.py
```

Select your folder in the gui, and let the files process.

## Build Log:


 First solve these:
    
 1. ~Does not exit gracefully if allowed to run fully~ - **solved** by adding a for loop instead of while going by number of frames in the video
 2. ~Fails when ROI is not within the frame~ - **solved** kept rect in frame
 3. ~Need to save video properly~ - export as .avi with mjpg compression
 
Then tackle this issue:
 
 1. ~Need to export xloc for each fly to remap data for creative viz~
 
**solved**
import pandas,
list>dict>csv (vert)
save in folder where processed

 2. Need to discard data when grooming/turning/at end
 
Right, Left, Groom, Retreat, 

Need to smooth this information temporally, not supported by current script

Currently left undone because it may not be so important.

 3. Generate stats of bouts at the same time.

Wrap it up into a usable "executable"
 
1. ~should ask which folder to process from, make folders within and dump files into them.~
**solved** currently creates a folder and dumps processed videos into that.
2. ~some kinda progress bar if possible? or just indicator that it is working.~
**solved** currently prints out which file is active and spits out time taken to process given the conditions.