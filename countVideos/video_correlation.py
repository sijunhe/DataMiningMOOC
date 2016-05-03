import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sets import Set

video_count_distribution = {}
# ids = []

response_ids = Set()
response_user_mapping = {}
user_response_mapping = {}
# with open('../../codes/earth_Spring2015/survey_post_EarthSciences_ResGeo202_Spring2015_response.csv', 'r') as csvfile :
# # with open('../../codes/networking_winter2014/Engineering_Networking_Winter2014_survey_responses.csv', 'r') as csvfile :
# 	lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
# 	for line in lines :
# 		if (line[2] == "Q1.1" and line[4] != ''):
# 			response_ids.add(line[1])
# # print len(response_ids)

# with open('../../codes/earth_Spring2015/survey_post_EarthSciences_ResGeo202_Spring2015_respondent_metadata.csv', 'r') as csvfile :
# # with open('../../codes/networking_winter2014/Engineering_Networking_Winter2014_survey_response_metadata.csv', 'r') as csvfile :
# 	lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
# 	for line in lines :
# 		# if line[0] not in response_user_mapping and line[0] in response_ids :
# 		if line[1] not in response_user_mapping and line[1] in response_ids :
# 			# response_user_mapping[line[0]] = line[1]
# 			response_user_mapping[line[1]] = line[2]	
# 			# user_response_mapping[line[1]] = line[0]
# 			user_response_mapping[line[2]] = line[1]
# print len(response_user_mapping)

with open('EarthSciences_ResGeo202_Spring2015_UserVideo_Matrix.csv') as csvfile:
# with open('Engineering_Networking_Winter2014_UserVideo_Matrix.csv') as csvfile:
	lines = csv.reader(csvfile, delimiter = ',') 
	for line in lines :
		# if line[0] not in user_response_mapping:
		if line[0] == 'UserName' or line[0] in user_response_mapping:
			continue
		length = len(line)
		count = 0
		for i in range(1, length) :
			if int(line[i]) == 1:
				count += 1
		if count in video_count_distribution:
			video_count_distribution[count] += 1
		else :
			video_count_distribution[count] = 1
		# if count == 1:
		# 	ids.append(line[0])
print video_count_distribution
print len(video_count_distribution)
# print ids
# print len(ids)

total_people = 0
for key in video_count_distribution :
	total_people += video_count_distribution[key]
print "total_people" , total_people
bins = [] 
nums = []
for i in range(1, 94):
# for i in range(1, 122):
	bins.append(i)
	if i in video_count_distribution :
		nums.append(video_count_distribution[i])
	else :
		nums.append(0)

nums_series = pd.Series.from_array(nums)
plt.figure()
ax = nums_series.plot(kind='bar')

# ax.set_title('Distribution of Networking - Winter2014')
ax.set_title('Distribution of EarthSciences - Spring2015')
#ax.set_title('Histogram of Medicine - Summer2015')
#ax.set_title('Histogram of humanitiesSciences_econ1_summer2015')
ax.set_xlabel('Total Videos Watched')
ax.set_ylabel('Distribution')
ax.set_xticklabels(bins)

# rects = ax.patches
# labels = [str(i) for i in nums]

# for rect, label in zip(rects, labels) :
# 	height = rect.get_height()
# 	ax.text(rect.get_x() + rect.get_width() / 2, height + 5, label, ha = 'center', va = 'bottom')
plt.show()

