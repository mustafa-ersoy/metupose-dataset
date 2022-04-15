import csv
import json
import copy
import argparse
import subprocess
import os

csv_list=[]
cnt=0
max_cnt=-60
num_joint=16
joint_cnt_bl=18
width=960
height=540
frame_bl=[]
list_bl=[]

first_frame = 0

headcheck_cnt=0


parser = argparse.ArgumentParser(description = 'Parameters')
parser.add_argument('person_number', type=int)
parser.add_argument('start_point', type=int)
parser.add_argument('img_number', type=int)
parser.add_argument('val_percent', type=int)
parser.add_argument('combine', type=int)
args = parser.parse_args()

person_number = args.person_number
start = args.start_point
last_frame = args.img_number
fraction = int(100/args.val_percent)
combine = args.combine


imageformat = '.jpg'


def headbound(top2, nose):
	#if top2[0]>width or top2[0]<0 or nose[0]>width or nose[0]<0 or top2[1]>height or top2[1]<0 or nose[1]>height or nose[1]<0:
	#	return [[-1.0, -1.0], [-1.0, -1.0]]

	x_diff=top2[0]-nose[0]
	y_diff=top2[1]-nose[1]
	mag=(x_diff**2+y_diff**2)**0.5

	#bottom=nose-(top-nose)*0.55

	bottom= [nose[0]*1.55-top2[0]*0.55, nose[1]*1.55-top2[1]*0.55]
	top= [top2[0]*1.2-0.2*nose[0], top2[1]*1.2-0.2*nose[1]]

	dis=18
	#slope=y_diff/x_diff
	newbound=[top[0]+dis*y_diff/mag, top[1]+dis*x_diff/mag, top[0]-dis*y_diff/mag, top[1]-dis*x_diff/mag, \
	bottom[0]+dis*y_diff/mag, bottom[1]+dis*x_diff/mag, bottom[0]-dis*y_diff/mag, bottom[1]-dis*x_diff/mag]

	maxx=0
	maxy=0
	minx=10000
	miny=10000


	for i in range(8):
		if i%2==0:
			minx=max(min(minx, newbound[i]),0)
			maxx=max(max(maxx, newbound[i]),0)

		if i%2==1:
			miny=max(min(miny, newbound[i]),0)
			maxy=max(max(maxy, newbound[i]),0)

	finalbound=[[minx, maxy], [maxx, miny]]
	#return finalbound
	return bottom

def centerandscale(poselist):
	boundbox=[10000, 0, 10000, 0]
	boundboxs=[10000, 0, 10000, 0]
	sumx=0
	sumy=0

	for i in poselist:
		if i[0]==-1.0 or i[1]==-1.0:
			continue
		else:
			boundbox[0]=min(boundbox[0], i[0])
			boundbox[1]=max(boundbox[1], i[0])
			boundbox[2]=min(boundbox[2], i[1])
			boundbox[3]=max(boundbox[3], i[1])
	cnt=0
	for isc in poselist:
		if cnt in [10,11,14,15]:
			continue
		else:
			boundboxs[0]=min(boundboxs[0], isc[0])
			boundboxs[1]=max(boundboxs[1], isc[0])
			boundboxs[2]=min(boundboxs[2], isc[1])
			boundboxs[3]=max(boundboxs[3], isc[1])
		cnt+=1


	center2=[float(int(max((boundbox[0]+boundbox[1])/2,0))), float(int(max((boundbox[2]+boundbox[3])/2,0)))]
	scale2=float((((boundboxs[1]- boundboxs[0])**2 + (boundboxs[3]- boundboxs[2])**2)**0.5)/200)
	#print(boundboxs)
	return scale2, center2

def checkjoints(joint_array):
	vis=[]
	headcheck=0
	for i in range(len(joint_array)):
		#print(json_frame_original[0])
		if (joint_array[i][0]<0 or joint_array[i][0]>width) or (joint_array[i][1]<0 or joint_array[i][1]>height):
			if i==8 or i==9:
				headcheck=1
			#print('yess')
			joint_array[i]=[-1.0, -1.0, 0]
			vis.append(0)
		
		# elif len(joint_array[i])==3 and joint_array[i][2]==0:
		# 	vis.append(0)
		else:
			vis.append(1)
	jnt2, jnt3=[], []
	for ii in range(len(joint_array)):
		for jj in range(2):
			jnt2.append(joint_array[ii][jj])
		jnt3.append(jnt2)
		jnt2=[]
	return jnt3, vis, headcheck


with open('final_coords_' + str(person_number)+ '.csv') as csv_file:
	csv_reader=csv.reader(csv_file)

	for line in csv_reader:
		if len(frame_bl)==joint_cnt_bl:
			list_bl.append(frame_bl)
			frame_bl=[]
			continue
		frame_bl.append(line)
	if frame_bl != []:
		list_bl.append(frame_bl)


rejected=[]
with open('utils/rejected_multi_'+str(person_number)+'.csv') as csv_file:
	csv_reader=csv.reader(csv_file)

	for line in csv_reader:
		rejected.append(int(line[0]))



json_list=[]

#bl_to_mpii=[17, 16, 15, 12, 13, 14, 11, 2, 1, 0, 9, 8, 7, 3, 4, 5]
bl_to_mpii=[14,13,12,15,16,17,11,6,1,0,5,4,3,7,8,9]

json_frame=[]
json_person=[]
json_joint=[]

#print('blender list: ', list_bl[0])

for i in range(first_frame, last_frame):
	pers_cnt=0
	for pp in list_bl[i][0]:
		if pp not in ['', '0', '1']:
			pers_cnt+=1

	#print('person count: ',pers_cnt)
	json_person=[]
	for person in range(int(pers_cnt/2)):
		json_joint=[]
		for joint in bl_to_mpii:
			#print(i, person, joint)
			json_joint.append([list_bl[i][joint][person*2],list_bl[i][joint][person*2+1], list_bl[i][joint][2*int(pers_cnt/2)+person]])


		json_person.append(json_joint)

	json_frame.append(json_person)
	#json_frame[-1].append(i)

#print('frame num: ', json_frame[0])

for i in range(len(json_frame)):
	for j in range(len(json_frame[i])):
		for k in range(len(json_frame[0][0])):
			#print(json_frame[i][j][k][0])
			json_frame[i][j][k][0]=float(json_frame[i][j][k][0])
			json_frame[i][j][k][1]=float(json_frame[i][j][k][1])
			json_frame[i][j][k][2]=float(json_frame[i][j][k][2])

json_final=[]
json_final_val=[]

json_frame_original=copy.deepcopy(json_frame)
#print(json_frame_original[0])
#print(json_frame_original[9][0])


frame_num=len(json_frame)
for i in range(frame_num):
	for p in range(len(json_frame[i])):
		json_frame[i][p] = checkjoints(json_frame[i][p])[0]

for fram in range(len(json_frame)):
	nextimage=0
	for p in range(int(len(json_frame[fram]))):
		if nextimage==1:
			break
		if fram%fraction != 0:
			#print(fram,p)
			temp_dict={"joints_vis": checkjoints(json_frame_original[fram][p])[1], "joints": checkjoints(json_frame[fram][p])[0], "image": str(fram+start)+imageformat, "scale": centerandscale(json_frame_original[fram][p])[0], "center": centerandscale(json_frame[fram][p])[1]}
			if checkjoints(json_frame[fram][p])[1][8]!=0 and checkjoints(json_frame[fram][p])[1][9]!=0 and json_frame_original[fram][p][8][2]!=0 and json_frame_original[fram][p][9][2]!=0 and checkjoints(json_frame_original[fram][p])[1].count(1) > 5 and (fram+start) not in rejected:
			#print(temp_dict)
				json_final.append(temp_dict)
			else:
				for pindex in range(p):
					del json_final[-1]
				nextimage=1

			if checkjoints(json_frame[fram][p])[2]==1:
				headcheck_cnt+=1
		else:
			temp_dict_val={"joints_vis": checkjoints(json_frame_original[fram][p])[1], "joints": checkjoints(json_frame[fram][p])[0], "image": str(fram+start)+imageformat, "scale": centerandscale(json_frame_original[fram][p])[0], "center": centerandscale(json_frame[fram][p])[1]}
			if checkjoints(json_frame[fram][p])[1][8]!=0 and checkjoints(json_frame[fram][p])[1][9]!=0 and json_frame_original[fram][p][8][2]!=0 and json_frame_original[fram][p][9][2]!=0 and checkjoints(json_frame_original[fram][p])[1].count(1) > 5 and (fram+start) not in rejected:
				json_final_val.append(temp_dict_val)

			else:
				for pindex in range(p):
					del json_final_val[-1]
				nextimage=1
					
			if checkjoints(json_frame[fram][p])[2]==1:
				#print(str(json_frame[i][-1]+1))
				headcheck_cnt+=1

print('json_final: ', len(json_final))

full_cnt=[frame_num]*16
joint_cnt=[0]*16
headless=0

for i in range(frame_num):
	for j in range(16):
		if checkjoints(json_frame[i][0])[1][8]!=0 and checkjoints(json_frame[i][0])[1][9]!=0:
			if checkjoints(json_frame[i][0])[1][j]==0:
				joint_cnt[j]=joint_cnt[j]+1
		else:
			headless+=1

net_image=frame_num-headless
#print(frame_num-headcheck_cnt)


for i in range(16):
	joint_cnt[i]=frame_num-headcheck_cnt-joint_cnt[i]
#print(joint_cnt)


#print(json_final[-1]['joints'])



if os.path.exists('final_dataset/annot/train.json'):
	with open('final_dataset/annot/train.json') as f:
		data1=json.load(f)
	data3=data1+json_final
else:
	data3 = json_final

if os.path.exists('final_dataset/annot/valid.json'):
	with open('final_dataset/annot/valid.json') as f2:
		data2=json.load(f2)
	data4=data2+json_final_val
else:
	data4=json_final_val



with open('final_dataset/annot/train.json', 'w') as f:
	json.dump(data3, f, indent=3)

with open('final_dataset/annot/valid.json', 'w') as f2:
	json.dump(data4, f2, indent=3)

if combine == 1 and not os.path.exists('utils/combined.csv'):
	subprocess.run('python utils/combine.py', shell = True)

	with open('utils/combined.csv', 'a', newline='') as cmb:
		csv_writer=csv.writer(cmb)

else:
	subprocess.run('python utils/create_mat.py', shell = True)
