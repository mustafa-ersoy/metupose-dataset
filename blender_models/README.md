This folder is used for pose estimation dataset generation from scratch in Blender software.

If you want to build everything from scratch and don't want to use any dataset or person image provided by us, then you have to work in this directory. Otherwise, you can ignore this directory.

Firstly, you need to download all necessary files from [Google Drive](https://drive.google.com/drive/folders/1FnpukmwsdHjtwxJF23tBHmguwwvTj61x?usp=sharing) and place those files in this directory.

Final version of this directory should look like this:

![image](https://user-images.githubusercontent.com/63475020/163544505-4027373f-f5c3-4eb5-9670-3b3db8ef3017.png)

you can see the instructions in image below:

![demo](https://user-images.githubusercontent.com/63475020/163538141-be564416-879b-482d-bf90-35e42774bad6.png)


firstly, please open any of the .blend file 

1.	click on 'Layout' button at the top

2.	in the window appearing on right side, please choose one of the cameras (Camera0, Camera1..) by clicking green camera icon

3.	later, please click the 'Scripting' button above

4.	if you want, you can change first and last frame from line 22 and 23. difference is number of images to be created. please do not exceed 1000

5.	click run button at the top



and thats all. images will appear on '../create_dataset/blender_green_images'    directory

After that, you need to crop person images from green background. To do that, please go to '../create_dataset/' folder and run 'crop_person.py' file.
