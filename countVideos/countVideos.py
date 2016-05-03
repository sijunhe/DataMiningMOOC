#######################################################################################################################
## count Videos 
## Written by: Sijun He
## Last Modified by: Sijun He
#######################################################################################################################
## The code creates a matrix of whether each user has watched each user or not and print it into a csv file
##   Row: each unique User
##   Columns: each courses (courses have been sorted in chronological order)
#######################################################################################################################
#######################################################################################################################
## Parse Event Log 
## Written by: Sijun He
## Last Modified by: Sijun He
#######################################################################################################################
## The code extracts interaction events out of the log and store it in a dict for further development
## 1. Dictionary video_names:  
##      keys: the names of each video in the course
##      values: dictionarys (video) of data for each video
## 2. Dictionary video:  
##      keys: the names of users that watched the video
##      values: dictionarys (user) of data for each user
## 3. Dictionary user:  
##      keys: the four types of different events: 'play_video','stop_video','pause_video','seek_video'
##      values: a list of datas, for 'seek_video', the data is a tuple of ((old_time, new_time)
##                               for others, the data is just video_current_time
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
        if line[0] in event_type:
            if re.match('Unit\s+\d+\.\d+',line[1]):
                if line[1] not in video_names:
                    video_names.append(line[1])
                    video_name_id_matching[line[14]] = line[1]
                if line[13] not in user_watched_video:
                    user_watched_video[line[13]] = []
                if line[1] not in user_watched_video[line[13]]:
                    user_watched_video[line[13]].append(line[1])
            if line[1] == 'Welcome' or line[1] == 'Welcome Video':
                if line[13] not in user_watched_video:
                    user_watched_video[line[13]] = []
                if line[1] not in user_watched_video[line[13]]:
                    user_watched_video[line[13]].append(line[1])
                
        

## Sorted videos in chronological order 
sorted_video_name = sorted(video_names, key=lambda video: float(re.search('(?<=Unit)\s+\d+\.\d+',video).group(0)))
## Create a matrix of user - video watched relation 
## 1 = user watched this video
## 0 = user didn't watch this video
outputName = 'EarthSciences_ResGeo202_Spring2015_UserVideo_Matrix.csv'
outputFile = open(outputName, 'w')
columnNames = 'UserName,Welcome,'
for video in sorted_video_name:
    columnNames += (video + ',')
columnNames = columnNames[:-1] + '\n'
outputFile.write(columnNames)
for user in user_watched_video.keys():
    newLine = user + ','
    if 'Welcome' in user_watched_video[user] or 'Welcome Video' in user_watched_video[user]:
        newLine += '1,'
    else:
        newLine += '0,'
    for video in sorted_video_name:
        if video in user_watched_video[user]:
            newLine += '1,'
        else:
            newLine += '0,'
    newLine = newLine[:-1] + '\n'
    outputFile.write(newLine)