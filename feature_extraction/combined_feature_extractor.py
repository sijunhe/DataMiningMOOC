import csv
from collections import defaultdict
import numpy as np
from sklearn.cross_validation import train_test_split
from pre_survey import *
from sets import Set

responseUserID = {}
userScore = {}
userVideoTime = {}
userVideoMatrix = {}
videoNames = []
videoCounts = defaultdict(int)
videoCountsClassification = defaultdict(int)
userAvgExtraTime = defaultdict(int)
userTtlExtraTime = defaultdict(int)
screen_name_to_gender = defaultdict(int)
screen_name_to_year_of_birth = defaultdict(int)
screen_name_to_education = defaultdict(int)
screen_name_to_post_count = defaultdict(int)
screen_name_to_comment_count = defaultdict(int)
screen_name_activity_score = {}
activity_name_set = []
screen_name_to_continent = {}

train_num = 20
countThreshhold = 2

# get activity grade
with open("../../data/EarthSciences_ResGeo202_Spring2015_ActivityGrade.csv", "r") as csvfile :
	lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
	for line in lines :
		if line[12] == "'anon_screen_name'" :
			continue
		# line[12] -> anon_screen_name, line[14] -> module_id, line[3] -> grade
		if line[12] not in screen_name_activity_score :
			screen_name_activity_score[line[12]] = {}
			screen_name_activity_score[line[12]][line[14]] = line[3]
		else :
			screen_name_activity_score[line[12]][line[14]] = line[3]

		if line[14] not in activity_name_set:
			activity_name_set.append(line[14])


# print screen_name_activity_score


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
                userScore[responseUserID[line[1]]] = int(line[4])

# build nationality to continent mapping
Asia = Set()
Europe = Set()
North_America = Set()
South_America = Set()
Africa = Set()
Austrilia = Set()
current_continent = -1
continents = [Asia, North_America, South_America, Africa, Europe, Austrilia]
with open('/Users/guorm/stanford/2016-spring/CS341/codes/countries_of_continent.txt', 'r') as csvfile :
	lines = csv.reader(csvfile)
	for line in lines :
		if len(line) == 0 or line[0].startswith('#') or len(line[0]) == 1 :
			continue
		if line[0].startswith('$') :
			current_continent += 1
		else :
			continents[current_continent].add(line[0])


# extracting demographic feature
first = True
with open('../../data/EarthSciences_ResGeo202_Spring2015_demographics.csv', 'r') as csvfile :
	lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
	for line in lines :
		if first:
			first = False
			continue
		# if line[0] in userScore : 
		if True:

			# gender feature: blank -> 0, m -> -1, f -> +1
			if line[1] == "m" :
				screen_name_to_gender[line[0]] = -1
			if line[1] == "f" :
				screen_name_to_gender[line[0]] = 1
			if line[1] not in screen_name_to_gender and line[0] != "\\N" :
				screen_name_to_gender[line[0]] = 0

			# year_of_birth
			if line[2] != "\\N" :
				screen_name_to_year_of_birth[line[0]] = int(line[2])

			# ?????????????????????????????????????????????????
			## should set it to 0 if birth year not provided???
			if line[2] == "\\N" and line[0] != "\\N":
				screen_name_to_year_of_birth[line[0]] = 0
			
			# level_of_education: 
			# Doctorate -> 7
			# Masters or professional degree -> 6
			# Bachelors -> 5
			# Associates -> 4
			# Secondary/High School -> 3
			# Junior secondary/junior high/middle School -> 2
			# Elementary/Primary School -> 1
			# None, Other, User withheld, Signup before level collected -> 0
			if line[3] == "Doctorate" :
				screen_name_to_education[line[0]] = 7
			if line[3] == "Masters or professional degree" :
				screen_name_to_education[line[0]] = 6
			if line[3] == "Bachelors" :
				screen_name_to_education[line[0]] = 5
			if line[3] == "Associates" :
				screen_name_to_education[line[0]] = 4 
			if line[3] == "Secondary/High School" :
				screen_name_to_education[line[0]] = 3 
			if line[3] == "Junior secondary/junior high/middle School" :
				screen_name_to_education[line[0]] = 2
			if line[3] == "Elementary/Primary School" :
				screen_name_to_education[line[0]] = 1
			if line[0] not in screen_name_to_education and line[0] != "\\N":
				screen_name_to_education[line[0]] = 0
			
			# nationality
			screen_name_to_continent[line[0]] = [0] * 7
			if ";" in line[5] :
				if "Taiwan" in line[5] :
					screen_name_to_continent[line[0]][0] = 1
				else :
					screen_name_to_continent[line[0]][6] = 1
			else :
				for i in range(6) :
					if line[5] in continents[i] :
						screen_name_to_continent[line[0]][i] = 1
						break
				if screen_name_to_continent[line[0]] == [0] * 7 :
					screen_name_to_continent[line[0]][6] = 1

# print len(screen_name_to_gender)
# print len(screen_name_to_year_of_birth)
# print len(screen_name_to_education)

# Extracting forum feature
first = True
with open('../../data/EarthSciences_ResGeo202_Spring2015_Forum.csv', 'r') as csvfile :
	lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
	for line in lines :
		if first:
			first = False
			continue
		# if len(line) > 2 and line[1] in userScore:
		if len(line) > 2:
			# print line[1], line[2]
			if line[2] == "CommentThread":
				screen_name_to_post_count[line[1]] += 1
			if line[2] == "Comment":
				screen_name_to_comment_count[line[1]] += 1


with open('../countVideos/EarthSciences_ResGeo202_Spring2015_VideoNames.csv', 'r') as csvfile :
	lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
	for line in lines :
		video = line[0]
		videoNames.append(video)

# print len(videoNames)

# Extracting video counts
first = True
with open('../countVideos/EarthSciences_ResGeo202_Spring2015_UserVideo_Matrix.csv', 'r') as csvfile :
	lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
	for line in lines :
		if first:
			first = False
			continue
		key = line[0]
		count = 0
		for i in xrange(train_num + 1, len(line)):
			count += int(line[i])
		videoCounts[key] = count
		countClass = 0
		if count >= countThreshhold:
			countClass = 1
		videoCountsClassification[key] = countClass
		# print line
		# print len(line)
		for i in xrange(1, len(line)):
			video = videoNames[i-1]
			if key not in userVideoMatrix:
				userVideoMatrix[key] = {}
			userVideoMatrix[key][video] = int(line[i])


with open('../countVideos/EarthSciences_ResGeo202_Spring2015_UserAvgExtraTime.csv', 'r') as csvfile :
	lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
	for line in lines :
		user = line[0]
		avgTime = int(line[1])
		userAvgExtraTime[user] = avgTime
	# print userAvgExtraTime

with open('../countVideos/EarthSciences_ResGeo202_Spring2015_UserTtlExtraTime.csv', 'r') as csvfile :
	lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
	for line in lines :
		user = line[0]
		avgTime = int(line[1])
		userAvgExtraTime[user] = avgTime

# user video time
with open('../countVideos/EarthSciences_ResGeo202_Spring2015_UserVideoTime.csv', 'r') as csvfile :
	lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
	for line in lines :
		user = line[0]
		video = line[1]
		time = int(line[2])
		if user not in userVideoTime:
			userVideoTime[user] = {}
		userVideoTime[user][video] = time
# print userVideoTime



# print videoNames

activityFeatureLen = len(activity_name_set)
activityFeatureLen = 0
videoFeatureLen = len(videoNames)
videoFeatureTrainLen = train_num
# number of other features
widthOther = 0
width = widthOther + videoFeatureTrainLen + activityFeatureLen
# number of data
height = len(videoCountsClassification)
# height = len(userScore)

X = np.zeros((height, width))
# Y = np.array([0])
Y = np.zeros(height)

i = 0
for id in videoCountsClassification:
# for id in userScore:
	# print id

	# X[i][0] = screen_name_to_gender[id]
	# X[i][1] = screen_name_to_year_of_birth[id]
	# X[i][2] = screen_name_to_education[id]
	# X[i][3] = screen_name_to_post_count[id]
	# X[i][4] = screen_name_to_comment_count[id]
	# X[i][5] = userAvgExtraTime[id]
	# X[i][6] = userTtlExtraTime[id]
	# X[i][7] = screen_name_courses_started[id]
	# X[i][8] = screen_name_courses_finished[id]
	# X[i][9] = screen_name_hours_spent[id]

	for j in range(widthOther, width - activityFeatureLen):
		video = videoNames[j - widthOther]
		X[i][j] = 0
		if id in userVideoTime and video in userVideoTime[id]:
			X[i][j] = userVideoTime[id][video]
			# X[i][j] = userVideoMatrix[id][video]

	# for j in range(activityFeatureLen):
	# 	video = activity_name_set[j]
	# 	if id in screen_name_activity_score and video in screen_name_activity_score[id]:
	# 		X[i][j] = screen_name_activity_score[id][video]

	# X[i][0] = videoCountsClassification[id]
	
	# Y[i] = userScore[id]
	Y[i] = videoCountsClassification[id]
	i += 1

# print X
# print Y

x_train, x_test, y_train, y_test = train_test_split(X, Y,
                                                    test_size=0.2,
                                                    random_state=0)

print len(videoCountsClassification)
print len(userScore)

