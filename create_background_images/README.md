This codes help users to create background images to be used in pose estimation dataset generation process.

it takes video and number of seconds between each frame as input an create images with no human in them. output images will appear on ../create_dataset/background_images  folder.

if you have a video in path 'video_input/abcd.mp4' and you want to get images in every 3 seconds from that video you can use the command below in this directory:


python create_bg.py video_input/abcd.mp4 3

You need to download code files and models from [a link](https://drive.google.com/drive/folders/1-3NnpnKSBVgotMPqNe6fdZfMEEE7fPeE?usp=sharing) Google Drive and the final version of this directory should look like this:
![image](https://user-images.githubusercontent.com/63475020/163540920-17503e3a-aeb6-4438-af4a-024455d91e8a.png)

The original source of the code in this directory is given below. The code has been modified to suit our purposes.
For more information, please refer to the link below:

https://github.com/Daniil-Osokin/lightweight-human-pose-estimation-3d-demo.pytorch
