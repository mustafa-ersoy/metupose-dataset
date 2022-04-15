in this directory, there are two things you can do

1. CROPPING PERSON IMAGES IN THE 'blender_green_images' DIRECTORY

2. CREATING A POSE ESTIMATION DATASET BY USING ALREADY CROPPED IMAGES

-------------------------------------------------------------------------

Let's start with first one.
1. CROPPING PERSON IMAGES IN THE 'blender_green_images' DIRECTORY:
-	our source code already provides 49000 cropped images in 'cropped_images' directory. Only if you want more cropped person then you will use this method.
-	you don't have to but if you ran Blender models and created extra green background images, they will appear on 'blender_green_images' directory.
-	to be able to use those images, green background needs to be removed and we call this 'person cropping' from background.
-	you only need to run the code below, to crop all the person images.


python crop_person.py



-----------------------------------------------------------------------


2. CREATING A POSE ESTIMATION DATASET BY USING ALREADY CROPPED IMAGES
-	you can create multiperson dataset by using our background images, cropped person images and object images
-	a random background image is selected and person images and random object images are pasted on background image to create pose estimation dataset
-	all you need to do is to fill config.csv file based on your requirements and run the code below from terminal below, each in a different terminal.
-	with 4 terminals, dataset will be created in parallel which takes less time


python create_dataset.py 1 &python create_dataset.py 2&python create_dataset.py 3&python create_dataset.py 4


-----------------------------------------------------------------------