#######################################################################################################################
## count Videos 
## Written by: Sijun He
## Last Modified by: Sijun He
#######################################################################################################################
## The code creates a matrix of whether each user has watched each user or not and print it into a csv file
##   Row: each unique User
##   Columns: each courses (courses have been sorted in chronological order)
#######################################################################################################################
import csv, re
import numpy as np
fileName = 'EarthSciences_ResGeo202_Spring2015_VideoInteraction.csv'
video_names = [] ## a list for all the video names
video_name_id_matching = {} ## one on one matching for video_name to videoID
user_watched_video = {} ## a dictionary for the video each user watched
event_type = ['play_video','stop_video','pause_video','seek_video']
with open('../../data/' + fileName,'r') as csvfile :
    lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
    for line in lines :       
        if line[0] in event_type and re.match('Unit\s\d+\.\d+',line[1]):
            if line[1] not in video_names:
                video_names.append(line[1])
                video_name_id_matching[line[14]] = line[1]
            if line[13] not in user_watched_video:
                user_watched_video[line[13]] = []
            if line[1] not in user_watched_video[line[13]]:
                user_watched_video[line[13]].append(line[1])

## Sorted videos in chronological order 
sorted_video_name = sorted(video_names, key=lambda video: float(re.search('(?<=Unit)\s\d+\.\d+',video).group(0)))

## Create a matrix of user - video watched relation 
## 1 = user watched this video
## 0 = user didn't watch this video
outputName = 'EarthSciences_ResGeo202_Spring2015_UserVideo_Matrix.csv'
outputFile = open(outputName, 'w')
columnNames = 'UserName,'
for video in sorted_video_name:
    columnNames += (video + ',')
columnNames = columnNames[:-1] + '\n'
outputFile.write(columnNames)
for user in user_watched_video.keys():
    newLine = user + ','
    for video in sorted_video_name:
        if video in user_watched_video[user]:
            newLine += '1,'
        else:
            newLine += '0,'
    newLine = newLine[:-1] + '\n'
    outputFile.write(newLine)