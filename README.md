# Harry-Potters-Invisible-cloak
Image masking basic techniques

Tired of scratching your head through hectic reasearch papers? Common lets make something interesting with the help of basic computer vision knowledge using opencv library.

![](display.gif)

## Lets run the code first:
- Install all dependencies:
```
pip install -r requirements.txt
```
- Run code:
```
python src.py
```
Stay away from frame untill video window pops up for the background image to be created

## What's in the code:
The code has been written to recognize RED color as cloak for now.
```
lower_range = np.array([0,120,50])
higher_range = np.array([10,255,255])
```
You can change the color bound according to yourself.The color range for HSV value are available [here](http://colorizer.org/). For HSV, Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255]. Different softwares use different scales. So if you are comparing OpenCV values with them, you need to normalize these ranges.


- Masking is one of the key features for this project:
```
mask1 = cv2.inRange(hsv, lower_range, higher_range)
```
The above forms a mask of the area we want to make invisible to frame-feed.


- The next task is to extract the above mask from the frame,background and foreground.
```
#segmenting out cloth color
mask2 = cv2.bitwise_not(mask1)

#Segment the red color part out of the frame using bitwise and with the inverted mask
layer1 = cv2.bitwise_and(img, img, mask = mask2)

#Create image showing static background frame pixels only for the masked region
layer2 = cv2.bitwise_and(background, background, mask = mask1)

```
- This is now where the magic happens:
```
#output
output = cv2.addWeighted(layer1,1,layer2,1,0)
```
Both the mask were added with equal weights using opencv's [addWeight](https://docs.opencv.org/master/d2/de8/group__core__array.html#gafafb2513349db3bcff51f54ee5592a19)

## References:
www.machinelearningman.com

https://docs.opencv.org/master/d0/d86/tutorial_py_image_arithmetics.html
