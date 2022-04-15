#blender.csv dosyasini alir ve tum dataseti tarayarak jointlerin poselarinin
#distributionini cikarir. sonra da en common 10% icinde olan imagelarin listesini verir.


import csv
import numpy as np
import matplotlib.pyplot as plt
import argparse


parser = argparse.ArgumentParser(description = 'Parameters')
parser.add_argument('person_number', type=int)
parser.add_argument('start', type=int)
parser.add_argument('top', type=int)
parser.add_argument('bottom', type=int)
args = parser.parse_args()

person_number = args.person_number

#matplotlib inline
plt.rcParams.update({'figure.figsize':(7,5), 'figure.dpi':100})


bl_list, bl_list1=[],[]
wid, hei = 960, 540
top_cut, bottom_cut = args.top, args.bottom
startpoint = args.start

frame_bl, list_bl=[], []
with open('final_coords_'+str(person_number)+'.csv') as csv_file:
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
    pers_cnt=0
    for pp in list_bl[i][0]:
        if pp not in ['', '0', '1']:
            pers_cnt+=1
    json_person=[]
    for person in range(int(pers_cnt/2)):
        for joint in range(joint_cnt):
            joints.append([float(list_bl[i][joint][person*2]), float(list_bl[i][joint][person*2+1]), int(list_bl[i][joint][pers_cnt+person])])
        joints1.append(joints)
        joints=[]
    joints2.append(joints1)
    joints1=[]


#con1 includes the movable joints in body such as elbow-wrist but not stationary such as throax-shoulder
#last item is relative position of left and right hip which gives information about orientation of body
#con1=[[0,1], [3,4], [4,5], [7,8], [8,9], [1,11], [12,13], [13,14], [15,16], [16,17], [12,15]]
con1=[[3,4], [4,5], [7,8], [8,9], [1,11], [12,13], [13,14], [15,16], [16,17]]
segment_cnt=len(con1)

#con2 includes all connected joints whether they are redundant or not
con2=[]

con=con1
pos, pos1, pos2, bounds = [], [], [], []


#bounds variable will be used for bounding of each joint in the entire dataset
for i in range(len(con)):
    bounds.append([10000,10000,-10000,-10000])

#to find the bounding box covering all joints in dataset:
#print(joints2)
frameindex=0
for frame in joints2:
    frameindex+=1
    for person in range(len(frame)):
        for seg in range(segment_cnt):
            #print('frame: ', frameindex, 'person: ', person, 'segment: ', seg)
            #calculating x and y difference of each connection in the entire dataset
            if not (0 < frame[person][con[seg][1]][0] < wid or 0 < frame[person][con[seg][0]][0] < wid or 0 < frame[person][con[seg][1]][1] < hei or 0 < frame[person][con[seg][0]][1] < hei):
                pos.append([-2.2*wid, -2.2*hei])
                continue
            else:
                xdiff=float(frame[person][con[seg][1]][0])-float(frame[person][con[seg][0]][0])
                ydiff=float(frame[person][con[seg][1]][1])-float(frame[person][con[seg][0]][1])
                pos.append([xdiff, ydiff])

            #updating bounding list of all connections
            bounds[seg][0]=min(bounds[seg][0], xdiff)
            bounds[seg][1]=min(bounds[seg][1], ydiff)
            bounds[seg][2]=max(bounds[seg][2], xdiff)
            bounds[seg][3]=max(bounds[seg][3], ydiff)

        pos1.append(pos)
        pos=[]
    pos2.append(pos1)
    pos1=[]

#creating grid dimensions for bounds variable. simulating 2D finite integral

x_grid=50
y_grid=50

#distribution matrices to be used
dist, dist1=[], []

#a=[[0]]*8 creates problems. when an element was changed, every element changes
#thats why I used loop
for i in range(segment_cnt):
    for j in range(x_grid*y_grid):
        dist.append(0)

    dist1.append(dist)
    dist=[]


#calculating scores. if grid sizes are 20x20, I group all data as 1x400 as below
scores=[]
for frame in range(frame_cnt):
    for person in range(len(pos2[frame])):
        for seg in range(segment_cnt):
            xran=bounds[seg][2]-bounds[seg][0]
            yran=bounds[seg][3]-bounds[seg][1]
            xloc= int(((pos2[frame][person][seg][0]-bounds[seg][0])/xran)*x_grid)
            yloc= int(((pos2[frame][person][seg][1]-bounds[seg][1])/yran)*y_grid)

            loc=x_grid*yloc+xloc

            if loc<0:
                loc=0
            if loc>=x_grid*y_grid:
                loc=x_grid*y_grid-1
            dist1[seg][loc]+=1

#finding the maximum distribution number of each joint. i.e. 3452 out of 52704 belongs to group 45/400 grid
maxd=[]
for seg in range(segment_cnt):
    maxd.append(max(dist1[seg]))

def is_occluded(frame_o, person_o):
    is_occ=[]
    for o_joint in range(joint_cnt):
        #print(frame_o, person_om o_joint )
        is_occ.append(joints2[frame_o][person_o-1][o_joint][2])

    return 1+(is_occ.count(0))/9




#scor function that takes person connection coordinates and calculate score using distribution matrix
def scor(frame1, framenum):
    score, score1 = 1.0, 0
    person_index=0
    pcount=len(frame1)
    for person in frame1:
        person_index+=1
        for seg in range(segment_cnt):
            xran=bounds[seg][2]-bounds[seg][0]
            yran=bounds[seg][3]-bounds[seg][1]

            if person[seg][0] < -2*wid or person[seg][1] < -2*hei:
                continue
            else:
                xloc= int(((person[seg][0]-bounds[seg][0])/xran)*x_grid)
                yloc= int(((person[seg][1]-bounds[seg][1])/yran)*y_grid)

                loc=x_grid*yloc+xloc
                if loc<0:
                    loc=0
                if loc>=x_grid*y_grid:
                    loc=x_grid*y_grid-1

                score*=(float((float(maxd[seg])*2-dist1[seg][loc]))/float(maxd[seg]))**1.2
        #print(score)
        occ=is_occluded(framenum, person_index)
        #4**4 is the coefficient for occlusion. I gave the maximum possible point coming from 4 joints as the maximum point that can be obtained from occlusion
        #occ=1
        score *= occ**3
        score1+=score
        score=1.0
    #print(score1)
    return score1

#getting scores in a list
scores=[]
for frame in range(frame_cnt):
    scores.append(scor(pos2[frame], frame))


#getting min/max, above threshold scores
max_score=max(scores)
max_index=scores.index(max_score)
min_score=min(scores)
min_index=scores.index(min_score)

thr=600000
cnt=0
for i in scores:
    if i>thr:
        cnt+=1

mscore=scores.copy()
#print(mscore)

sort=int(frame_cnt*0.1)
mscore.sort()

print('max_score, index: ', max_score, scores.index(max_score))
print('min_score, index: ', min_score, scores.index(min_score))
print('sort_score: ', mscore[-1*sort], scores.index(mscore[-1*3]))
print('above_threshold: ', cnt)
#print(scores)
print(mscore[0:10])

rejected=[]
cut1=int(frame_cnt*top_cut/100)
cut2=int(frame_cnt*bottom_cut/100)
th1=mscore[cut1*-1-1]
th2=mscore[cut2*-1]



for sco in range(len(scores)):

    if scores[sco]>th1 or scores[sco] < th2:
        rejected.append(sco)

print('rejected: ', len(rejected))


with open('utils/rejected_multi_'+str(person_number)+'.csv', 'w', newline='') as reje:
    csv_writer=csv.writer(reje)

    for i in rejected:
        csv_writer.writerow([i+startpoint])


npscores=np.array(scores)
fig = plt.figure()
plt.hist(npscores, bins=5000)


timer = fig.canvas.new_timer(interval = 2000)
timer.add_callback(plt.close)
timer.start()

plt.show()
