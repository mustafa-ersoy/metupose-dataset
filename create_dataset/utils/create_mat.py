import json, csv
from scipy.io import savemat as sa
from scipy.io import loadmat as lo
import numpy as np

with open('final_dataset/annot/valid.json') as f:
    data=json.load(f)

all_joints=[]

for frame in range(len(data)):

	joints=data[frame]['joints']
	all_joints.append(joints)


pos_gt=[]
vis_gt=[]
for i in range(16):
	pos_gt.append([[],[]])
	vis_gt.append([])
head_gt=[[[],[]],[[],[]]]

for joint in range(16):
	for i in range(2):
		for frame in range(len(data)):

			pos_gt[joint][i].append(all_joints[frame][joint][i])
			
			if i==1:
				vis_gt[joint].append(1-data[frame]['joints_vis'][joint])
			if joint==9:
				head_gt[0][i].append(all_joints[frame][joint][i])

			if joint==8:
				head_gt[1][i].append(all_joints[frame][joint][i])

dataset_joints = ['rank', ['rkne'], ['rhip'], ['lhip'], ['lkne'], ['lank'], ['pelv'], ['thor'], ['neck'], ['head'], ['rwri'], ['relb'], ['rsho'], ['lsho'], ['lelb'], ['lwri']]

mat_d = {'dataset_joints':dataset_joints,'headboxes_src': head_gt, 'jnt_missing': vis_gt, 'pos_gt_src': pos_gt}

sa('final_dataset/annot/gt_valid.mat', mat_d)
