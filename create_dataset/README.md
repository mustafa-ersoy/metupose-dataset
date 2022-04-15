In this directory, you can create your own dataset by using cropped person images, background images and occlusion object images. We already provided 178000 image pose estimation dataset and if you want to create your own additional dataset, then you need to work in this directory. Otherwise, you can ignore this directory.

Firstly, make sure you downloaded necessary folders that contain images from [Google Drive](https://drive.google.com/drive/folders/1-6mHbNkTYFlfO-tPvLpbzHeBBge0YMfK?usp=sharing) (32 GB) Final version of this directory should look like this:

![image](https://user-images.githubusercontent.com/63475020/163531742-c88f7f4e-ad1d-437b-b0f7-39e930c63dfc.png)

in this directory, there are two things you can do

1. CROPPING PERSON IMAGES IN THE 'blender_green_images' DIRECTORY
2. CREATING A POSE ESTIMATION DATASET BY USING ALREADY CROPPED IMAGES

-------------------------------------------------------------------------
1. CROPPING PERSON IMAGES IN THE 'blender_green_images' DIRECTORY:
-	our source code already provides 49000 cropped images in 'cropped_images' directory. Only if you want more cropped person then you will use this method.
-	you don't have to but if you ran Blender files inside 'blender_models' directory and created extra green background images, they will appear on 'blender_green_images' directory.
-	to be able to use those images, green background needs to be removed and we call this 'person cropping' from background.
-	you only need to run the code below, to crop all the person images.

python crop_person.py

-----------------------------------------------------------------------
2. CREATING A POSE ESTIMATION DATASET BY USING ALREADY CROPPED IMAGES
-	you can create multiperson dataset by using our background images, cropped person images and occlusion object images
-	a random background image is selected and person images and random object images are pasted on background image to create pose estimation dataset
-	all you need to do is to fill config.csv file based on your requirements and run the code below from terminal.

python create_dataset.py 1 &python create_dataset.py 2&python create_dataset.py 3&python create_dataset.py 4

-----------------------------------------------------------------------
