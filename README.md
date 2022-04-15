# bld-dataset
This code helps you create your own synthetic pose estimation dataset in MPII format using Python. Firstly, we created human models in Blender 3D software and cropped human models from 3D environment. Later, we pasted cropped images onto varying background to create multi-person pose estimation dataset. Sample images are given below:

![image](https://user-images.githubusercontent.com/63475020/163546505-3d5d2953-4d3f-4ee9-bd9d-0148eb784b1f.png)

![image](https://user-images.githubusercontent.com/63475020/163546553-85961606-4511-44a9-a955-ca70ec2cc431.png)

![image](https://user-images.githubusercontent.com/63475020/163546601-c2e8883b-967e-4690-8a51-e02165b33521.png)



![image](https://user-images.githubusercontent.com/63475020/163467630-7c7d80c6-d8d4-406e-aeb2-47761d387a14.png)

![image](https://user-images.githubusercontent.com/63475020/163467686-a4030064-cbff-4c4f-b196-6f580dbbc292.png)

![image](https://user-images.githubusercontent.com/63475020/163546338-6732b005-c0bd-4c73-8d1b-e93006b8aa8c.png)



There are four different folders and each of the four folders have their own README files and they cover everyting.
Firstly, Github provides only source codes but Google Drive provides source code, images, Blender files and everything.
In short, you can download everything you need from Google Drive. If you want to use Github, you can download repository including Python files and add additional data files (images, Blender files etc.) by downloading them from Google Drive.

Explanation for each folder is given below:

--------------------------------------------------------------------------------------------------------------------------
'blender_models'
-	this directory contains Blender files to create person images and coordinates

-	we already provide 49000 person images, so you don't have to do anything within this folder. Only if you want to create your own images or increase the number of person images, you can use this folder

-	for example if you create extra 11000 images and crop the green screen, you will have total 49000+11000=60000 cropped person library.

-	in that case your final dataset will be created by selecting person images from a pool of 60000 people instead of 49000 people.


--------------------------------------------------------------------------------------------------------------------------
'create_background_images'
-	this directory contains code for creating extra background images

-	we already provide 57000 background images.

-	by using this directory, if you create additonal 13000 background images you will have 57000+13000=70000 total background images

-	in that case, your final dataset will be created by randomly choosing background images from a pool 70000 images instead of 570000


---------------------------------------------------------------------------------------------------------------------------
'create_dataset'
-	if you want to create your dataset you need to use this directory

-	this directory has two features

-	if Blender was used and if there is additional images in 'create_dataset/blender_green_images' folder, these additional images need to be cropped before creating dataset

-	if Blender is not used, dataset can be created by filling config.csv file and running python files.

-	final dataset and annotation files will appear on 'create dataset/final_dataset' folder





----------------------------------------------------------------------------------------------------------------------------
'dataset_provided_by_us'
-	this directory contains ready to use dataset created by us.

-	dataset contains 178000 images with total 402000 people in them

-	dataset format is MPII but not original MPII, it was converted from .json files to .mat file.

-	to get more details about the dataset format, please refer to the link below


https://github.com/microsoft/human-pose-estimation.pytorch
