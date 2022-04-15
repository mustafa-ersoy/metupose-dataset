import cv2
import numpy as np
import time
import csv
from PIL import Image
import os
import shutil

blender_path='blender_green_images/'
tr_path='cropped_images/'


if not os.path.isdir(tr_path+'older_csv/'):
	os.mkdir(tr_path+'older_csv/')
if not os.path.isdir(blender_path+'older_csv/'):
	os.mkdir(blender_path+'older_csv/')

bbox, blend= [], []
for csvfile in os.listdir(tr_path+'older_csv/'):
	if csvfile.endswith('.csv') and csvfile[0:2]=='bb':
		bbox.append(csvfile)

for csvfile in os.listdir(blender_path+'older_csv/'):
	if csvfile.endswith('.csv') and csvfile[0:2]=='bl':
		blend.append(csvfile)

if os.path.exists(blender_path+'blender.csv'):
	shutil.copy(blender_path+'blender.csv', blender_path+'older_csv/'+'blender_old_'+str(len(blend))+'.csv')

if os.path.exists(tr_path+'bbox.csv'):
	shutil.copy(tr_path+'bbox.csv', tr_path+'older_csv/'+'bbox_old_'+str(len(bbox))+'.csv')


fn=[]

jpgcnt=0
for filename in os.listdir(tr_path):
    if filename.endswith(".png"):
    	jpgcnt+=1
trname=jpgcnt


for filename in os.listdir(blender_path):
    if filename.endswith(".jpg") and filename[0]!= '_':
    	fn.append(filename)
title=0
resume = 0
if os.path.exists('cropped_images/tr1.png'):
	resume=1

alr_crop = len(os.listdir('blender_green_images/already_cropped'))+1

for filenum in range(1, len(fn)+1):
	file=str(filenum)+'.jpg'

	start_time = time.time()

	img=cv2.imread(blender_path+file, cv2.IMREAD_UNCHANGED)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

	height, width = img.shape[:2]
	img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	lower_green = np.array([48,100,50])
	upper_green = np.array([72,255,255])
	mask = cv2.inRange(img_hsv, lower_green, upper_green)


	# set my output img to zero everywhere except my mask
	output_img = img.copy()
	output_img[np.where(mask>0.2)] = 0

	output_img[np.where(np.all(output_img[..., :3] == 0, -1))] = 0

	lx=width
	ux=0
	ly=height
	uy=0
	

	#to get the minimum time to search from derivative, use this equation
	step=int((height*width*2/(2*height+2*width))**(1/3))

	step=min(step, 8)
	step=max(1, step)

	for y in range(0, height, step):
		for x in range(0, width, step):
			if output_img[y][x][-1]!=0:
				lx=min(x, lx)
				ly=min(y, ly)
				ux=max(x, ux)
				uy=max(y, uy)


	for y in range(max(0, ly-step), ly):
		for x in range(0, width):
			if output_img[y][x][-1]!=0:
				ly=min(y, ly)

	for y in range(uy, min(uy+step,height)):
		for x in range(0, width):
			if output_img[y][x][-1]!=0:
				uy=max(y, uy)

	for y in range(0, height):
		for x in range(max(0, lx-step), lx):
			if output_img[y][x][-1]!=0:
				lx=min(x, lx)

	for y in range(max(0, height)):
		for x in range(ux, min(ux+step, width)):
			if output_img[y][x][-1]!=0:
				ux=max(x, ux)


	cropdata=[['tr'+str(filenum+trname)+'.png',lx, ly, ux, uy]]

	with open(r'cropped_images/bbox.csv', 'a', newline='') as f:
	    writer = csv.writer(f)

	    if title == 0 and resume == 0:
		    writer.writerow(['image_name', 'lower_x', 'lower_y', 'upper_x', 'upper_y'])
		    title=1
	    for line in cropdata:
	        writer.writerow(line)
	    f.close()
	print('count: ', filenum+trname, '	duration: ', round((time.time()-start_time),2))


	output_img=output_img[ly:uy, lx:ux]

	cv2.imwrite(tr_path+'tr'+str(filenum+trname)+'.png', output_img)
	

for filenum in range(1, len(fn)+1):

	shutil.move(blender_path+str(filenum)+'.jpg', blender_path+'already_cropped/'+str(alr_crop)+'.jpg')
	alr_crop+=1

for i in os.listdir(blender_path):
	if i.endswith('.jpg') and i[0]=='_':
		os.remove(blender_path + i)

os.remove(blender_path+'imgcnt.csv')