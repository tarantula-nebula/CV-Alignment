This project is for my design course at univeristy.

The aim of the project is to align a custom hose fitting with a corresponding hose connection. 

The connection has markings on it allow for alignment. 

Obtain-Expected-Positions: 
From .jpeg file of ideal marking locations find the pixel location of the markings to use
in other code. 

Markings-Alignment:
Using webcam, converts feed to grayscale and finds the contours. 
The contours are filtered by size, as the markings have an expected size. 
All contours that fit that expected size are show up as green dots. 
Communicates whether system is aligned with markings using alignment status printed to 
webcam feed. 

Markings-Alignment-Suggest:
Similar to Markings-Alignment, but offers alignment suggestions. 
Displays expected markings position to further help with alignment. 
This is the most refined code as the other's were prototypes that built into this. 

I this was my first computer vision project, I don't know any of the maths behind it.. or 
really how it works. 
I think it is super cool though! 
