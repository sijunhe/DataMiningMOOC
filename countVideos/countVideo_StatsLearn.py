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
fileName = '../../data/HumanitiesSciences_StatLearning_Winter2016_VideoInteraction.csv'
wk1 = ['2wLfFB_6SKI','LvaTokhYnDw'] 
wk2 = ['WjyuiK5taS8','UvxHOkYQl8g','VusKAosxxyk','vVj2itVNku4','jwBgGS_4RQA','jk9S3RTAl38']
wk3 = ['PsE9UqoWtS4','J6AdoiNUyWI','1hbCJyM9ccs','3T6RXmIHbJ4','IFzVxLv0TKQ','5ONFqIk3RFg']
wk4 = ['sqq21-VIa1c','31Q5FGRnxt4','MpX8rVv_u4E','GavRXXEHGqU','RfrGiG1Hm3M',
'QG0pVJXT6EU','X4VDZDp2vqw','6FiNGTYAOAA','TxvEVc8YNlU','2cl7JiPzkBY','9TVVF7CS3F4']
wk5 = ['6l9V1sINzhE','_2ij6eaaSl0','nZAM5OXrktY','S06JpVoNaA0','p4BYWX7PTBM','BzHz0J9a6k0',
'6dSXlqHAoMk','YVSmsWoBKnA']
wk6 = ['MEMGOlJxxz0','91si52nk3LA','nLpJd_iKmrE','NJhMSpI2Uj8','LkifE44myLc','3p9JNaJCOb4',
'cSKzqb0EKS0','A5I1G1MfUmA','xMKVUstjXBE','QlyROnAjnEk','eYxwWGJcOfw','3kwdDGnV8MM','mv-vdysZIb4',
'F8MMHCCoALU','1REe3qSotx8']
wk7 = ['gtXQXA7qF3c','7ZIqzTNB8lk','mxXHJa1DsWQ','N2hBXqPiegQ','uQBnDGu6TYU','DCn83aXXuHc']
wk8 = ['79tR7BvYE6w','6ENTbK3yQUQ','GfPR7Xhdokc','hPEJoITBbQ4','lq_xzBRIWm4','U3MdBNysk9w',
'0wZUXtvAtDc','IY7oWGXb77o']
wk9 = ['QpbynqiTCsY','xKsTsGE7KpI','dm32QvCW7wE','mI18GD4_ysE','qhyyufR0930','L3n2VF7yKkk']
wk10 = ['ipyxSYXgzjQ','dbuSGWCgdzw','aIybuNt9ps4','Tuuc9Y06tAc','yUJcTpWNY_o','lFHISDj_4EQ',
'YDubYJsZ9iM','4u3zvtfqb7w']
videos = wk1 + wk2 + wk3 + wk4 + wk5 + wk6 + wk7 + wk8 + wk9 + wk10
user_watched_video = {} ## a dictionary for the video each user watched
event_type = ['play_video','stop_video','pause_video','seek_video']
with open(fileName,'r') as csvfile :
    lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
    for line in lines :       
        if line[0] in event_type : 
            if line[13] not in user_watched_video:
                user_watched_video[line[13]] = []
            if line[9] not in user_watched_video[line[13]]:
                user_watched_video[line[13]].append(line[9])

## Sorted videos in chronological order 
# sorted_video_name = sorted(video_names, key=lambda video: float(re.search('(?<=Unit)\s\d+\.\d+',video).group(0)))
#sorted_video_name = video_names
## Create a matrix of user - video watched relation 
## 1 = user watched this video
## 0 = user didn't watch this video
outputName = 'HumanitiesSciences_StatLearning_Winter2016_UserVideo_Matrix.csv'
outputFile = open(outputName, 'w')
columnNames = 'UserName,'
for video in videos:
    columnNames += (video + ',')
columnNames = columnNames[:-1] + '\n'
outputFile.write(columnNames)
for user in user_watched_video.keys():
    newLine = user + ','
    for video in videos:
        if video in user_watched_video[user]:
            newLine += '1,'
        else:
            newLine += '0,'
    newLine = newLine[:-1] + '\n'
    outputFile.write(newLine)