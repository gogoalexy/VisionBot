# The format specification of the optic flow file (.flow)

The `.flow` file is actually a pure `.txt` file. You can open the file with any general text editor. And the datum format is described below:

1. Each line in the file describes all optic flow vectors in a single frame and the lines are wrapped with a pair of `[]`. Next, each row in a frame is separated by a semicolon.
2. Each vector is presented in the order of `x direction, y direction`, and the two elements are divided by a comma without any space.
3. The order presenting all the pixels in a frame is from upper-left to lower-right, and pixels are divided by semicolons.
4. The element type is floating point number rounded to the second place after decimal point.

__[Pixel order]__
```
      1---->
	  ---------------------------
	2  |				|
	|  |				|
	\/ |				|
	   |				|
	  ---------------------------
```
__[Example]__

```
0.00,0.00,0.00,0.00;......;0.00,0.00,0.00,0.00;
0.00,0.00,1.20,0.30;......;2.20,1.90,3.40,0.00;
.
.
.
```
