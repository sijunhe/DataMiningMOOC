import csv
from collections import defaultdict
import numpy as np

responseUserID = {}
userScore = {}
screen_name_to_post_count = defaultdict(int)
screen_name_to_comment_count = defaultdict(int)


## Get ResponseID - UserID matching
with open('../../data/survey_post_EarthSciences_ResGeo202_Spring2015_respondent_metadata.csv', 'r') as csvfile :	
    lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
    
    for line in lines :
        if line[1] not in responseUserID:
            responseUserID[line[1]] = line[2]

# print responseUserID

# Get Survey Data, only get the ID that has a matching 
with open('../../data/survey_post_EarthSciences_ResGeo202_Spring2015_response.csv', 'r') as csvfile :	
    lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
    for line in lines :
        if (line[2] == "Q1.1" and line[4] != ''):
            if line[1] in responseUserID:
                userScore[responseUserID[line[1]]] = line[4]

# print userScore

with open('../../data/EarthSciences_ResGeo202_Spring2015_Forum.csv', 'r') as csvfile :
	lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
	for line in lines :
		if len(line) > 2 and line[1] in userScore:
			# print line[1], line[2]
			if line[2] == "CommentThread":
				screen_name_to_post_count[line[1]] += 1
			if line[2] == "Comment":
				screen_name_to_comment_count[line[1]] += 1
			

# print screen_name_to_post_count
# print screen_name_to_comment_count
print len(screen_name_to_post_count)
print len(screen_name_to_comment_count)

X = np.array([0, 0])
# Y = np.array([0])
Y = [0]

for id in userScore:
	newrow = [screen_name_to_post_count[id], screen_name_to_comment_count[id] ]
	X = np.vstack([X, newrow])
	# Y = np.vstack([Y, [userScore[id]]])
	Y.append(userScore[id])

# print X
# print Y

