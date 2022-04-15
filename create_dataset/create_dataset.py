import cv2
import numpy as np
import time
import csv
from PIL import Image
import os, random, time
from random import randint as ran
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import shutil
import subprocess
import json
import argparse



c1=time.time()

blender_path='blender_green_images/'
tr_path='cropped_images/'
bg_path='background_images/'
final_path='final_dataset/images/'
obj_path='occlusion_objects/'

#pnum=int(os.path.basename(__file__).split('_')[-1].split('.')[0])
parser = argparse.ArgumentParser(description = 'Parameters')
parser.add_argument('pnum', type=int)
args = parser.parse_args()
pnum = args.pnum

height=540
width=960
jntcnt=18

con=[]
with open('config.csv', 'r') as config:
	csv_reader = csv.reader(config)

	for line in csv_reader:
		con.append(line)

imnum = int(con[pnum][1])
startpoint = 0
for i in range(pnum-1):
	startpoint+=int(con[i+1][1])
total_image = 0
for i in range(4):
	total_image += int(con[i+1][1])
print('TOTAL_IMAGE__ :', total_image)
minjoints = int(con[5][1])
occ_level = int(con[6][1])
single_pos_compl = [int(con[7][1].split(' ')[0]), int(con[7][1].split(' ')[1])]
multi_pos_compl = [int(con[8][1].split(' ')[0]), int(con[8][1].split(' ')[1])]
plot = int(con[9][1])
nobadview = int(con[10][1])
val_percent = int(con[11][1])
combine = int(con[12][1])
vis_joint = list(con[13][1].split(' '))
visible_joint=[]
for i in vis_joint:
	visible_joint.append(int(i))
objnum = int(con[14][1])
fresh_start = int(con[15][1])

deleted=0
if fresh_start == 1 and not os.path.exists('final_dataset/deleted.csv'):
	a= input('are you sure you want to delete your old created dataset? (y/n)')
	if a == 'y':
		for i in os.listdir('final_dataset/annot'):
			os.remove('final_dataset/annot/'+i)
		for i in os.listdir('final_dataset/images'):
			os.remove('final_dataset/images/'+i)
		with open('final_dataset/deleted.csv', 'w') as f:
			csv_writer = csv.writer(f)

			csv_writer.writerow([1])
			deleted = 1
	else:
		pass

a1=time.time()


if os.path.exists('utils/combined.csv') and not os.path.exists('final_dataset/annot/train.json'):
	os.remove('utils/combined.csv')


back_list=[]
for ba in os.listdir(bg_path):
	if ba.endswith('.jpg'):
		back_list.append(ba)

trcnt=0
for filename in os.listdir(tr_path):
    if filename.endswith(".png"):
    	trcnt+=1

fnlcnt=0
if not os.path.exists(final_path+'fnlcnt.csv'):
	for filename in os.listdir(final_path):
	    if filename.endswith(".jpg") and filename[0]!='_':
	    	fnlcnt+=1
	with open(final_path+'fnlcnt.csv', 'w') as f:
		csv_writer=csv.writer(f)

		csv_writer.writerow([fnlcnt])
		print('FNLCNT___ = ', fnlcnt)
else:
	fnlcnt2=[]
	with open(final_path+'fnlcnt.csv') as f:
		csv_reader=csv.reader(f)

		for line in csv_reader:
			fnlcnt2.append(line[0])
			break
	fnlcnt=int(fnlcnt2[0])
	print('FNLCNT___ = ', fnlcnt)

objcnt=0
obj_cat=[]
for folder in os.listdir(obj_path):
	if os.path.isdir(obj_path + folder):
		objcnt+=1
		obj_cat.append(folder)
obj_list=[]
for i in range(objcnt):
	for j in obj_cat:
		if int(j.split('_')[0])==i:
			obj_list.append(j)

i=0
bl_list,bl_list1=[],[]
with open(blender_path+'blender.csv') as csv_file:
	csv_reader=csv.reader(csv_file)

	for line in csv_reader:
		if line[0] != '\n':
			bl_list.append(line)
		else:
			bl_list1.append(bl_list)
			bl_list=[]
			continue
		i+=1
		if i==trcnt*(jntcnt+1):
			break

bbox=[]
with open(tr_path+'bbox.csv') as bb:
	csv_readerbb=csv.reader(bb)

	for line in csv_readerbb:
		bbox.append(line)
del(bbox[0])

subprocess.run('python utils/pose_comp_single.py '+str(pnum)+' '+ str(single_pos_compl[0])+' '+str(single_pos_compl[1]), shell=True)
rejected_single=[]
with open('utils/rejected_single_'+str(pnum)+'.csv', 'r') as rej_single:
		csv_reader = csv.reader(rej_single)

		for line in csv_reader:
			rejected_single.append(int(line[0]))

os.remove('utils/rejected_single_'+str(pnum)+'.csv')

if nobadview == 1:
	subprocess.run('python utils/nobadview.py '+str(pnum), shell=True)

badview=[]
if os.path.exists('utils/badview_'+str(pnum)+'.csv'):
	with open('utils/badview_'+str(pnum)+'.csv') as csv_file:
		csv_reader=csv.reader(csv_file)

		for line in csv_reader:
			badview.append(int(line[0]))
	os.remove('utils/badview_'+str(pnum)+'.csv')


tr_list=list(range(1, trcnt))
tr_list= [f for f in tr_list if f not in rejected_single and f not in badview]
a2=time.time()


def is_occluded(fincoords, person_scales, person_rcoords, obj_scales, obj_rcoords, chosenobjs, category):

	person_cnt=len(fincoords)
	obj_cnt=len(obj_rcoords)
	vis1, truncation1=[],[]
	
	pimgs, oimgs=[], []

	for pindex in range(person_cnt):
		pimgs.append(Image.open(tr_path+'tr'+str(person_list[pindex])+'.png'))

	for oindex in range(obj_cnt):
		objimg=Image.open(obj_path+obj_list[category[oindex]]+'/'+str(chosenobjs[oindex]))
		objimg.convert('RGBA')
		oimgs.append(objimg)


	for person in range(person_cnt):
		vis, truncation=[],[]
		for fill in range(18):
			vis.append(1)
			truncation.append(1)
		
		for joint in range(18):
			b1=time.time()
			if person!=person_cnt:
				for otherperson in range(person+1, person_cnt):
					check_y=int((fincoords[person][joint][1]-person_rcoords[otherperson][1])/person_scales[otherperson])
					check_x=int((fincoords[person][joint][0]-person_rcoords[otherperson][0])/person_scales[otherperson])

					#img=cv2.imread(tr_path+'tr'+str(person_list[otherperson])+'.png', cv2.COLOR_RGB2RGBA)
					img=pimgs[otherperson]
					imgwid, imghei=img.size
					alpha=img.split()[-1]
					
					if 0 < check_x < imgwid and 0 < check_y < imghei:
						if alpha.getpixel((check_x, check_y))>180:
							vis[joint]=0

			b2=time.time()


			for obj in range(obj_cnt):
				check_y=int((fincoords[person][joint][1]-obj_rcoords[obj][1])/obj_scales[obj])
				check_x=int((fincoords[person][joint][0]-obj_rcoords[obj][0])/obj_scales[obj])

				o_img=oimgs[obj]

				alpha=o_img.split()[-1]

				imgwid, imghei=o_img.size
				if 0 < check_x < imgwid and 0 < check_y < imghei:
					if alpha.getpixel((check_x, check_y))>220:
						vis[joint]=0
			finx, finy = fincoords[person][joint][0],fincoords[person][joint][1]
			if not (0 < finx < 960 and 0 < finy < 540):
				truncation[joint]=0
				vis[joint]=0

		vis1.append(vis)
		truncation1.append(truncation)
		if vis.count(1)<minjoints:
			vis1=[[0]*18]*person_cnt
			break

	return vis1, truncation1

sc_list=[0.3, 1.2, 0.24, 0.85, 0.75, 0.5, 1, 0.5, 0.5, 0.5, 0.9, 0.7, 1.5, 1, 0.35, 0.25, 0.25, 1.5, 1.6, 0.8, 0.3, 0.35, 1.2, 0.2, 0.8, 0.4]

def scale(person_list, rand_scale, cat):

	person_scales=[]
	person_rcoords=[]
	person_sizes=[]

	person_index=0
	for p in person_list:
		person_scales.append(random.randint(16, 24)/20*rand_scale)

		p_img=Image.open(tr_path+'tr'+str(p)+'.png')
		hei_pimg=person_scales[-1]*540
		wid_pimg=hei_pimg*p_img.size[0]/p_img.size[1]
		#print('hei, wid: ', hei_pimg, wid_pimg)
		person_sizes.append((wid_pimg**2+hei_pimg**2)**0.5)

		ycor=[]
		if hei_pimg>0 and hei_pimg <= 540:
			for ii in range(0, 540):
				if ii%2==0 and ii<540-hei_pimg:
					ycor.append(ii)
				elif ii%8==0 and 540-hei_pimg < ii < 540*0.6:
					ycor.append(ii)
		else:
			ycor.append(ran(0, 540/6))
		x_range=int((960*0.7+100))

		ind_rat=float(person_index)/len(person_list)

		separation = 100 - occ_level*20
		x1, x2 = int(-100+x_range*(ind_rat)+separation), int(-100 + x_range*(ind_rat+1/len(person_list))-separation)
		person_rcoords.append([ran(x1,x2), random.choice(ycor)])
		
		person_index+=1

	avg_size=sum(person_sizes)/len(person_sizes)
	
	chosenobjs, objsizes, obj_scales, obj_rcoords=[],[],[],[]
	for obj in cat:
		while True:
			chosenobjs.append(random.choice(os.listdir(obj_path+obj_list[obj])))
			if chosenobjs[-1][-1]!='i':
				break
			else:
				del chosenobjs[-1]
		o_img=Image.open(obj_path+obj_list[obj]+'/'+chosenobjs[-1])
		wid_oimg, hei_oimg=o_img.size
		objsz=(wid_oimg**2+hei_oimg**2)**0.5
		objsizes.append(objsz)

		obj_scales.append(avg_size/objsizes[-1]*sc_list[obj])

		if objsz*obj_scales[-1] > 400:
			obj_scales[-1]=(400/objsz)

		obj_rcoords.append([ran(0, 960*0.8), ran(0, 540*0.8)])

	return person_scales, person_rcoords, obj_scales, obj_rcoords, chosenobjs

saved_img=fnlcnt+startpoint

unsaved=0
finpos2=[]
is_visible=[]
timetable=[]
success=0
plotcnt=0

in_cat=list(range(0, 26))
in_cat = [e for e in in_cat if e not in (6, 9, 10, 12,13)]
#print(in_cat)
gara_cat=[0, 5,6,7,8,9,10,13, 23]
out_cat=[0, 5,6,7,8,9,10,12,13, 23]

mpii_to_bl = [14, 13, 12, 15, 16, 17, 11, 10, 1, 0, 5, 4, 3, 7, 8, 9]

while saved_img<imnum+fnlcnt+startpoint:
	success+=1
	sav=1

	a3=time.time()

	backname=random.choice(back_list)
	back=Image.open(bg_path+backname)

	back_num=int(backname.split('_')[0])

	if back_num in range(0,34000):
		cat_list=in_cat
	elif back_num in range(34000, 40000):
		cat_list=gara_cat
	else:
		cat_list=out_cat

	person_list=random.sample(tr_list, pnum)

	person_scale=[ii for ii in range(10, 28 , 1)]
	for jj in range(len(person_scale)):
		person_scale[jj]=person_scale[jj]/40
	rand_scale=random.choice(person_scale)
	cat=random.sample(cat_list, objnum)
	a4=time.time()

	person_scales, person_rcoords, obj_scales, obj_rcoords, chosenobjs = scale(person_list, rand_scale, cat)

	finpos, finpos1=[],[]
	for person in range(pnum):
		for joint in range(18):
			x=(float(bl_list1[person_list[person]-1][joint][0])-float(bbox[person_list[person]-1][1]))*person_scales[person]+ person_rcoords[person][0]
			y=(float(bl_list1[person_list[person]-1][joint][1])-float(bbox[person_list[person]-1][2]))*person_scales[person]+ person_rcoords[person][1]

			finpos.append([x,y])
		finpos1.append(finpos)
		finpos=[]
	a5=time.time()
	visible, inside=is_occluded(finpos1, person_scales, person_rcoords, obj_scales, obj_rcoords, chosenobjs, cat)
	a6=time.time()
	vis_cnt=[]
	for vision in visible:
		for jnt in visible_joint:
			if vision[mpii_to_bl[jnt]] == 0:
				sav=0
				unsaved+=1
				break
		if sav!= 0 and vision.count(1)<minjoints+2 or vision[0]==0 or vision[1]==0:
			sav=0
			unsaved+=1
			break
	if sav==1:
		is_visible.append(visible)
		finpos2.append(finpos1)
		print('saved images: ', saved_img)

		for p in range(len(person_list)):
			img=Image.open(tr_path+'tr'+str(person_list[p])+'.png')
			wid, hei = img.size
			img=img.resize((int(wid*person_scales[p]), int(hei*person_scales[p])))
			back.paste(img, (person_rcoords[p][0], person_rcoords[p][1]), img)
			
		for o in range(len(cat)):
			img=Image.open(obj_path+obj_list[cat[o]]+'/'+str(chosenobjs[o])).convert("RGBA")
			wid, hei = img.size

			img=img.resize((int(wid*obj_scales[o]), int(hei*obj_scales[o])), Image.ANTIALIAS)
			back.paste(img, (obj_rcoords[o][0], obj_rcoords[o][1]), img)

		back.save(final_path+str(saved_img)+'.jpg')
		timetable.append(time.time()-a3)


		if plotcnt<plot:

			img_path = final_path+str(saved_img)+'.jpg'
			img = cv2.imread(img_path)
			height, width, channels = img.shape
			img=mpimg.imread(img_path)
			implot = plt.imshow(img)

			for person_cnt in range(len(person_list)):
				for joint_cnt in range(18):
					scatter_x, scatter_y = finpos1[person_cnt][joint_cnt][0], finpos1[person_cnt][joint_cnt][1]
					if scatter_x>=0 and scatter_x<= width:
						if scatter_y >= 0 and scatter_y <= height:

							if visible[person_cnt][joint_cnt]==1:
								col='g'
							else:
								col='r'
							plt.scatter(scatter_x,scatter_y, s=0.2, color=col)
			save_path = final_path+'_'+str(saved_img)+'__.jpg'
			plt.savefig(save_path, dpi=300)
			plt.close()
			plotcnt+=1



		saved_img+=1


print('average time: ', sum(timetable)/len(timetable))
print('success at first try: ', success)

finpos3, finpos4, finpos5=[], [], []
for frame in range(len(finpos2)):
	for joint in range(len(finpos2[0][0])):
		for person in range(len(finpos2[0])):
			finpos3.append(finpos2[frame][person][joint][0])
			finpos3.append(finpos2[frame][person][joint][1])
		for person in range(len(finpos2[0])):
			finpos3.append(is_visible[frame][person][joint])
		finpos4.append(finpos3)
		finpos3=[]
	finpos5.append(finpos4)
	finpos4=[]


with open('final_coords_'+str(pnum)+'.csv', 'w', newline='') as csv_file:
    csv_writer=csv.writer(csv_file)
    
    for i in range(imnum):
        for j in range(18):
            csv_writer.writerow(finpos5[i][j])
        csv_writer.writerow('\n')

subprocess.run('python utils/pose_comp_multi.py '+str(pnum)+' '+str(fnlcnt+startpoint)+' '+str(multi_pos_compl[0])+' '+str(multi_pos_compl[1]), shell=True)

edit = {'edit' : ['edit']}
while os.path.exists('final_dataset/annot/edit.json'):
	time.sleep(15)

with open('final_dataset/annot/edit.json', 'w') as ed:
	json.dump(edit, ed)


subprocess.run('python utils/csvtojson_multiperson.py '+str(pnum)+' '+str(fnlcnt+startpoint) + ' '+str(imnum) + ' '+ str(val_percent)+ ' '+ str(combine), shell=True)
os.remove('final_dataset/annot/edit.json')

print(time.time()-c1)

os.remove('utils/rejected_multi_'+str(pnum)+'.csv')
os.remove('final_coords_'+str(pnum)+'.csv')

if deleted==1:
	os.remove('final_dataset/deleted.csv')

new_fnlcnt=0
for filename in os.listdir(final_path):
    if filename.endswith(".jpg") and filename[0]!='_':
    	new_fnlcnt+=1
if (new_fnlcnt > total_image + fnlcnt-2) and os.path.exists(final_path+'fnlcnt.csv'):
	os.remove(final_path+'fnlcnt.csv')
	print('DELETED')
