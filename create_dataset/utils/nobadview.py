import csv
import os
import argparse



blender_path='blender_green_images/'
parser = argparse.ArgumentParser(description = 'Parameters')
parser.add_argument('person_number', type=int)
args = parser.parse_args()

person_number = args.person_number

frame_bl, list_bl=[], []
with open(blender_path+'blender.csv') as csv_file:
    csv_reader=csv.reader(csv_file)

    for line in csv_reader:
        if len(frame_bl)==18:
            list_bl.append(frame_bl)
            frame_bl=[]
            continue
        frame_bl.append(line)
    if frame_bl != []:
        list_bl.append(frame_bl)

frame_cnt=len(list_bl)
joint_cnt=18

joints, joints1, joints2 = [],[],[]
for i in range(frame_cnt):
    json_person=[]
    for person in range(1):
        for joint in range(joint_cnt):
            joints.append([float(list_bl[i][joint][person*2]), float(list_bl[i][joint][person*2+1])])
        joints1.append(joints)
        joints=[]
    joints2.append(joints1)
    joints1=[]

jo=joints2

badview=[]

def dist(l1, l2):
	return ((l1[0]-l2[0])**2 + (l1[1]-l2[1])**2)**0.5

for i in range(frame_cnt):
	if dist(jo[i][0][0], jo[i][0][1])<100 or (dist(jo[i][0][13], jo[i][0][16])<100 and dist(jo[i][0][12], jo[i][0][15])<100) or (dist(jo[i][0][3], jo[i][0][7])<100 and dist(jo[i][0][4], jo[i][0][8])<100):
		badview.append(i+1)
	# if (dist(jo[i][0][13], jo[i][0][16])<80 and dist(jo[i][0][12], jo[i][0][15])<80) or (dist(jo[i][0][3], jo[i][0][7])<80 and dist(jo[i][0][4], jo[i][0][8])<80):
	# 	print(i+1)

print('badview: ', len(badview))

with open('utils/badview_'+str(person_number)+'.csv', 'w', newline='') as bad:
    csv_writer=csv.writer(bad)

    for i in badview:
        csv_writer.writerow([i])
