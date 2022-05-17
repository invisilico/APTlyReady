# APTLY Ready

The APT Preprocessor is meant to be an efficient tool to preprocess tons of video footage of high resolutions and frame rates using opencv and python3. The tool tracks a single fly walking in a channel and produces a video with the fly centered in frame. It was made to reduce processing overhead with APT and also because both flytracker and ctrax are not just incredibly resource intensive but also very inefficient/inaccurate. This method (in our hands) takes less than 15 seconds per video and produces virtually no errors.

A future version will be more extensible with flexibility in parameters. It will also classify motion into Rest, Left, Right and Retreat with temporal smoothing while also providing an option to discard frames/bouts of rest to save only important bouts of motion for analysis.

It allows you to select a folder containing all the videos and process them sequentially. 

Tracking uses the K nearest neighbour algorithm to pick out the largest moving objects (in this case one fly). KNN with default () settings works
really really well for flies in motion. But stagnant flies (grooming, PER, etc.) are not detected - the mask decays. This is not particularly and issue and is readily tackled by using a constantly updating xy location which is maintained even when the fly is not in motion

opencv provides a contour function to outline objects, as well as a rectangle bounding box option, the centre of which is roughly the centre for large blobby objects. We use the centre of this rectangle to determine centre for our ROI, and data from 100px either side (200 wide) and the entire height of the frame is kept.

Python Dependencies:

(Preferably use an anaconda python3 distribution)
 
```
> Python3.9
> opencv-python 4.5.5.64 (+contrib, numpy)
> tkinter
> os
> pandas
> time
```

## How to use:

On linux - We use Pop!_OS 22.04LTS

open a bash terminal in the directory of the script:

```
$ conda activate
```
```
$ python3 APTlyReady.py
```

Select your folder in the gui, and let the files process.

---

Made by Nish [invisilico] @ the Agrawal lab to pre-process footage for post estimation with APT.
