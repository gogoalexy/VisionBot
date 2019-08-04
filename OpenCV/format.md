# The format specification of the optic flow file (.flow)

The `.flow` file is actually a pure `.txt` file. You can open the file with any general text editor. And the datum format is described below:

1. Each line in the file describes all optic flow vectors in a single frame. And there is no extra notation to the frames.
2. Each vector is presented in the order of `x direction, y direction`, and the two elements are divided by a comma without any space.
3. The order presenting all the pixels in a frame is from upper-left to lower-right, and pixels are divided by semicolons.
4. The element type is floating point number rounded to the first place after decimal point.

___[Pixel order]___

     1---->
     -----------------
  2  |               |
  |  |               |
  \/ |               |
     |               |
     -----------------

___[Example]___

```
0.0,0.0;0.0,0.0;......;0.0,0.0;
0.0,0.0;1.2,0.3;......;3.4,0.0;
.
.
.
```
