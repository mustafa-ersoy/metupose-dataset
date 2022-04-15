This codes help users to create background images to be used in pose estimation dataset generation process.
We already provide 57000 background images. If you want to create more background images, you have to work in this directory. Otherwise, you can ignore this directory.
The code takes video and number of seconds between each frame as input an create images with no human in them. Output images will appear on ../create_dataset/background_images  folder.

if you have a video in path 'video_input/abcd.mp4' and you want to get images in every 3 seconds from that video you can use the command below in this directory:


python create_bg.py video_input/abcd.mp4 3

You need to download code files and models from [Google Drive](https://drive.google.com/drive/folders/1FlUvIuvKNHVlWH7m3Dic6cNy__qx8EqC?usp=sharing) and the final version of this directory should look like this:

![image](https://user-images.githubusercontent.com/63475020/163540920-17503e3a-aeb6-4438-af4a-024455d91e8a.png)

The original source of the code in this directory is given below. The code has been modified to suit our purposes.
For more information, please refer to the link below:

https://github.com/Daniil-Osokin/lightweight-human-pose-estimation-3d-demo.pytorch
