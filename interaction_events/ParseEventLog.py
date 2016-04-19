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
event_type = ['play_video','stop_video','pause_video','seek_video']
video_names = {}
## need to change the file name to STDIN afterwards
with open('EarthSciences_ResGeo202_Spring2015_EventXtract.csv','r') as csvfile :
    lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
    for line in lines :
        if line[1] in event_type and re.search(r'Unit ', line[6]):
            if line[6] not in video_names:
                video_names[line[6]] = {}
                
            video = video_names[line[6]]
            
            # use user names as keys to store events of each users
            if line[0] not in video:
                video[line[0]] = {}
            user = video[line[0]]
            
            # separates events since different events has differnet data
            
            
            ## 1. seek_video contains  "'video_old_time'", "'video_new_time'
            ##    store each seek events as a tuple of (old_time, new_time)
            if line[1] == 'seek_video':
                if 'seek_video' not in user:
                    user['seek_video'] = [(line[11], line[12])]
                else:
                    user['seek_video'].append((line[11], line[12]))
            
            ## 2. play_video & pause_video & stop_video contains video_current_time
            else:
                if line[1] not in user:
                    user[line[1]] = [line[9]]
                else:
                    user[line[1]].append(line[9])   


## EXAMPLE 

## video_names dictionary
print video_names.keys()[0:5]

## video dictionary
print video_names['Unit 1.3 -  Overview of Units 4-8'].keys()[0:5]

## user
print video_names['Unit 1.3 -  Overview of Units 4-8']['70e57033c52922dc01e9363090d3a0704ec6643f'].keys()
print video_names['Unit 1.3 -  Overview of Units 4-8']['70e57033c52922dc01e9363090d3a0704ec6643f']['play_video']
