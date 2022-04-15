import json, csv



#input_path='C:/Users/MUSTAFA/Desktop/ptry2/MPII_Label/inputs'
#output_path='C:/Users/MUSTAFA/Desktop/ptry2/MPII_Label/outputs'


with open('final_dataset/annot/valid.json') as f:
    data=json.load(f)

print('total frames: ', len(data))



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
			if joint==8:
				head_gt[0][i].append(all_joints[frame][joint][i])

			if joint==9:
				head_gt[1][i].append(all_joints[frame][joint][i])



with open('final_dataset/annot/pos_gt.csv', 'w', newline='') as pgt:
    csv_writer=csv.writer(pgt)

    for joint in range(len(pos_gt)):
    	for i in range(2):
    		csv_writer.writerow(pos_gt[joint][i])
    		#print(len(pos_gt[joint][i]))
    	csv_writer.writerow('\n')


with open('final_dataset/annot/head_gt.csv', 'w', newline='') as hgt:
    csv_writer=csv.writer(hgt)

    for joint in range(len(head_gt)):
    	for i in range(2):
    		csv_writer.writerow(head_gt[joint][i])
    	csv_writer.writerow('\n')


with open('final_dataset/annot/jnt_missing.csv', 'w', newline='') as mis:
    csv_writer=csv.writer(mis)

    for joint in range(len(vis_gt)):
    	csv_writer.writerow(vis_gt[joint])
    	csv_writer.writerow('\n')
