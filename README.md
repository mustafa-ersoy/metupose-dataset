# bld-dataset
This code helps you create your own synthetic pose estimation dataset in MPII format using Python. Firstly, we created human models in Blender 3D software and cropped human models from 3D environment. Later, we pasted cropped images onto varying background images and added some objects to create occlusion effect. Sample images are given below:

![image](https://user-images.githubusercontent.com/63475020/163546505-3d5d2953-4d3f-4ee9-bd9d-0148eb784b1f.png)

![image](https://user-images.githubusercontent.com/63475020/163547065-69843e83-80fa-4c27-babc-2091fa9af42c.png)

![image](https://user-images.githubusercontent.com/63475020/163546601-c2e8883b-967e-4690-8a51-e02165b33521.png)



There are four different folders and each of the four folders have their own README files and they cover everyting.
Firstly, Github provides only source codes but Google Drive provides source code, images, Blender files and everything.
In short, you can download everything you need from Google Drive. If you want to use Github, you can download repository including Python files and add additional data files (images, Blender files etc.) by downloading them separately from [Google Drive](https://drive.google.com/drive/folders/1-3NnpnKSBVgotMPqNe6fdZfMEEE7fPeE?usp=sharing)

We already provide 178000 final ready-to-use dataset images. We also provided additonal 49000 cropped person images and 57000 to create new dataset.
- If you want to use our 178000 images pose estimation dataset, please go to 'dataset_provided_by_us' folder and download it. That's all
- If you don't want to use our 178000 image dataset and want to create your own dataset by cropped person images and background images provided by us, then please go to 'create_dataset' folder.
- If you don't want to use 178000 image dataset images, cropped person images etc. and create everything from scratch on your own, please go to 'blender_models' folder.
- Also, if you want to enrich the content of background images (57000 images), please go to 'background_images' folder.

Explanation for each folder is given below:

--------------------------------------------------------------------------------------------------------------------------
'blender_models'
-	this directory contains Blender files to create person images and coordinates

-	we already provided 178000 dataset images and 49000 cropped person images, so you don't have to do anything within this folder. Only if you want to create your own images or increase the number of person images, you can use this folder

-	for example if you create extra person 11000 images and crop the green screen, you will have total 49000+11000=60000 cropped person library.

-	in that case your final dataset will be created by selecting person images from a pool of 60000 people instead of 49000 people.


--------------------------------------------------------------------------------------------------------------------------
'create_background_images'
-	this directory contains code for creating extra background images

-	we already provide 57000 background images.

-	by using this directory, if you create additonal 13000 background images, you will have 57000+13000=70000 total background images

-	in that case, your final dataset will be created by randomly choosing background images from a pool of 70000 images instead of 570000


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
