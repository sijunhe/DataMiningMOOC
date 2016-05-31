import csv
from collections import defaultdict
import numpy as np
from sklearn.cross_validation import train_test_split
from pre_survey import *

def feature_extractor(train_num = 1, use_profile=False):

	responseUserID = {}
	userScore = {}
	userVideoTime = {}
	userVideoPeakPercentage = {}
	userVideoMatrix = {}
	userVideoGrade = {}
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
	userGrade = {}

	# train_num = 1

	# 3 categories
	countThreshholds = [1, 10]

	predict_activity_grade = False

	# get activity grade
	# with open("../../stats_data/HumanitiesSciences_StatLearning_Winter2016_ActivityGrade.csv", "r") as csvfile :
	# 	lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
	# 	for line in lines :
	# 		if line[12] == "'anon_screen_name'" :
	# 			continue
	# 		# line[12] -> anon_screen_name, line[14] -> module_id, line[3] -> grade
	# 		if line[12] not in screen_name_activity_score :
	# 			screen_name_activity_score[line[12]] = {}
	# 			screen_name_activity_score[line[12]][line[14]] = line[3]
	# 		else :
	# 			screen_name_activity_score[line[12]][line[14]] = line[3]

	# 		if line[14] not in activity_name_set:
	# 			activity_name_set.append(line[14])


	# print screen_name_activity_score


	## Get ResponseID - UserID matching
	with open('../../stats_data/HumanitiesSciences_StatLearning_Winter2016_survey_response_metadata.csv', 'r') as csvfile :	
	    lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
	    
	    for line in lines :
	        if line[1] not in responseUserID:
	            responseUserID[line[1]] = line[2]

	# print responseUserID

	# Get Survey Data, only get the ID that has a matching 
	with open('../../stats_data/survey_post_humanitiesSciences_statLearning_winter2016_response.csv', 'r') as csvfile :	
	    lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
	    for line in lines :
	        if (line[2] == "experience" and line[4] != ''):
	            if line[1] in responseUserID:
	                userScore[responseUserID[line[1]]] = int(line[4])

	for id in userScore:
		if userScore[id] <= 5:
			userScore[id] = 5;

	# extracting demographic feature
	first = True
	with open('../../stats_data/HumanitiesSciences_StatLearning_Winter2016_demographics.csv', 'r') as csvfile :
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
				


	# print len(screen_name_to_gender)
	# print len(screen_name_to_year_of_birth)
	# print len(screen_name_to_education)

	# Extracting forum feature
	first = True
	with open('../../stats_data/HumanitiesSciences_StatLearning_Winter2016_Forum.csv', 'r') as csvfile :
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


	with open('../countVideos/HumanitiesSciences_StatLearning_Winter2016_video_id_names.csv', 'r') as csvfile :
		lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
		for line in lines :
			video = line[0]
			videoNames.append(video)

	# print len(videoNames)

	# Extracting video counts
	first = True
	with open('../countVideos/HumanitiesSciences_StatLearning_Winter2016_UserVideo_Matrix.csv', 'r') as csvfile :
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
			for i in range(len(countThreshholds)):
				threshhold = countThreshholds[i]
				if count >= threshhold:
					countClass = i+1

			videoCountsClassification[key] = countClass
			# print line
			# print len(line)
			for i in xrange(1, len(line)):
				video = videoNames[i-1]
				if key not in userVideoMatrix:
					userVideoMatrix[key] = {}
				userVideoMatrix[key][video] = int(line[i])


	# with open('../countVideos/EarthSciences_ResGeo202_Spring2015_UserAvgExtraTime.csv', 'r') as csvfile :
	# 	lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
	# 	for line in lines :
	# 		user = line[0]
	# 		avgTime = int(line[1])
	# 		userAvgExtraTime[user] = avgTime
	# 	# print userAvgExtraTime

	# with open('../countVideos/EarthSciences_ResGeo202_Spring2015_UserTtlExtraTime.csv', 'r') as csvfile :
	# 	lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
	# 	for line in lines :
	# 		user = line[0]
	# 		avgTime = int(line[1])
	# 		userAvgExtraTime[user] = avgTime

	# user video time
	with open('../countVideos/HumanitiesSciences_StatLearning_Winter2016_UserVideoTime.csv', 'r') as csvfile :
		lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
		for line in lines :
			user = line[0]
			video = line[1]
			time = int(line[2])
			if user not in userVideoTime:
				userVideoTime[user] = {}
			userVideoTime[user][video] = time
	# print userVideoTime


	with open('../countVideos/HumanitiesSciences_StatLearning_Winter2016_UserVideoPeakPercentage.csv', 'r') as csvfile :
		lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
		for line in lines :
			user = line[0]
			video = line[1]
			time = float(line[2])
			if user not in userVideoPeakPercentage:
				userVideoPeakPercentage[user] = {}
			userVideoPeakPercentage[user][video] = time


	# load quiz grades
	with open('../../stats_data/StatLearningFirst6.csv', 'r') as csvfile :
		lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
		videoId = ""
		for line in lines:
			if len(line) == 1:
				# print line
				videoId = line[0]
			else:
				user = line[0]
				quiz1 = line[1]
				quiz2 = "-"
				if len(line) > 2:
					quiz2 = line[2]
				if user not in userVideoGrade:
					userVideoGrade[user] = {}
				if videoId not in userVideoGrade[user]:
					userVideoGrade[user][videoId] = {}
				userVideoGrade[user][videoId] = (quiz1, quiz2)


	# statLearnWinter16Grades (grade, distinction, was_certified)
	first = True
	with open('../../stats_data/statLearnWinter16Grades.csv', 'r') as csvfile :
		lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
		for line in lines:
			if first:
				first = False
				continue
			user = line[0]
			grade = float(line[1])
			distinction = int(line[2])
			was_certified = int(line[3])
			good_grade = 0
			if grade > 0.05:
				good_grade = 1
			if grade > 0.5:
				good_grade = 2
			userGrade[user] = (grade, distinction, was_certified, good_grade)

	# print userGrade

	# print userVideoGrade

	# print len(userScore)

	# print videoNames
	if not predict_activity_grade:

		activityFeatureLen = len(activity_name_set)
		activityFeatureLen = 0
		videoFeatureTrainLen = train_num
		# number of other features
		widthOther = 0
		width = widthOther + videoFeatureTrainLen * 2 + activityFeatureLen
		# number of data
		height = len(videoCountsClassification)
		# height = len(userScore)

		X = np.zeros((height, width))
		Y = np.zeros(height)

		i = 0
		# for id in userGrade:
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

			for j in range(widthOther, widthOther + videoFeatureTrainLen):
				video = videoNames[j - widthOther]
				X[i][j] = 0

				if use_profile:
					if id in userVideoTime and video in userVideoTime[id]:
						X[i][j] = userVideoTime[id][video]
				else:
					if id in userVideoMatrix and video in userVideoMatrix[id]:
						X[i][j] = userVideoMatrix[id][video]
				
			if use_profile:
				k = 0
				for j in range(widthOther + videoFeatureTrainLen, widthOther + videoFeatureTrainLen * 2):
					video = videoNames[k]
					k += 1
					X[i][j] = 0
					if id in userVideoPeakPercentage and video in userVideoPeakPercentage[id]:
						X[i][j] = userVideoPeakPercentage[id][video]

			# k = 0
			# for j in range(widthOther + videoFeatureTrainLen * 2, widthOther + videoFeatureTrainLen * 3):
			# 	video = videoNames[k]
			# 	k += 1
			# 	X[i][j] = 0
			# 	if id in userVideoGrade and video in userVideoGrade[id]:
			# 		quizGradeStr = userVideoGrade[id][video][0]
			# 		quizGrade = 0
			# 		if quizGradeStr == "+":
			# 			quizGrade = 1
			# 		X[i][j] = quizGrade

			# 		quizGradeStr = userVideoGrade[id][video][1]
			# 		quizGrade = 0
			# 		if quizGradeStr == "+":
			# 			quizGrade = 1
			# 		X[i][j+videoFeatureTrainLen] = quizGrade

			# for j in range(activityFeatureLen):
			# 	video = activity_name_set[j]
			# 	if id in screen_name_activity_score and video in screen_name_activity_score[id]:
			# 		X[i][j] = screen_name_activity_score[id][video]

			# X[i][0] = videoCountsClassification[id]
			
			# Y[i] = userScore[id]
			Y[i] = videoCountsClassification[id]
			# Y[i] = userGrade[id][2] 
			i += 1

	if predict_activity_grade:

		# number of other features
		widthOther = 0
		videoFeatureTrainLen = 40
		width = widthOther + 2 * videoFeatureTrainLen
		# number of data
		height = 0

		for user in userVideoGrade:
			for videoId in userVideoGrade[user]:
				height += 1 

		quiz_num = 0

		X = np.zeros((height, width))
		Y = np.zeros(height)

		print width
		print height

		i = 0
		for user in userVideoGrade:
			for videoId in userVideoGrade[user]:

				# X[i][0] = 0
				# if videoId in userVideoTime[user]:
				# 	X[i][0] = userVideoTime[user][videoId]

				# X[i][1] = 0
				# if videoId in userVideoPeakPercentage[user]:
				# 	X[i][1] = userVideoPeakPercentage[user][videoId]

				for j in range(widthOther, widthOther + videoFeatureTrainLen):
					video = videoNames[j - widthOther]
					X[i][j] = 0
					if user in userVideoTime and video in userVideoTime[user]:
						X[i][j] = userVideoTime[user][video]
						# X[i][j] = userVideoMatrix[id][video]

				k = 0
				for j in range(widthOther + videoFeatureTrainLen, widthOther + videoFeatureTrainLen * 2):
					video = videoNames[k]
					k += 1
					X[i][j] = 0
					if user in userVideoPeakPercentage and video in userVideoPeakPercentage[user]:
						X[i][j] = userVideoPeakPercentage[user][video]

				quizGradeStr = userVideoGrade[user][videoId][quiz_num]
				# print quizGradeStr
				quizGrade = 0
				if quizGradeStr == "+":
					quizGrade = 1

				Y[i] = quizGrade
				i += 1


	print X
	# print Y

	x_train, x_test, y_train, y_test = train_test_split(X, Y,
	                                                    test_size=0.2,
	                                                    random_state=0)

	# np.savetxt('../../export/x_train.csv', x_train, delimiter=',')
	# np.savetxt('../../export/x_test.csv', x_test, delimiter=',')
	# np.savetxt('../../export/y_train.csv', y_train, delimiter=',')
	# np.savetxt('../../export/y_test.csv', y_test, delimiter=',')

	# for i in range(7):
	# 	video = videoNames[i]
	# 	for user in userVideoPeakPercentage:
	# 		if video in userVideoPeakPercentage[user]:
	# 			print i
	# 			break

	# print len(videoCountsClassification)
	# print len(userScore)
	# print videoCounts
	# print videoCountsClassification

	print len(X)
	print len(Y)

	print len(userScore)

	return X,Y

