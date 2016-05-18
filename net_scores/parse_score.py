###################################################################################################
# parse csv file and read Net Promoter Score
###################################################################################################

scores = {}
count = 0
#totallines = 0
import csv
#with open('survey_post_EarthSciences_ResGeo202_Spring2015_response.csv', 'r') as csvfile :
with open('../../data/survey_post_Medicine_MedStats_Summer2015_response.csv', 'r') as csvfile :	
#with open('test.csv', 'r') as csvfile :
	lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
	for line in lines :
		#totallines += 1
		if line[2] == "Q1.1":
			count += 1
			if line[4] == '':
				continue
			score = int(line[4])
			if score in scores :
				scores[score] += 1
			else :
				scores[score] = 1
validCount = 0
for record in scores:
	validCount += scores[record]

print "########## validCount"
print validCount
print "########## scores"
print scores
print "########## count" 
print count

#print totallines

###################################################################################################
# plot histogram
###################################################################################################
#bins = [0]
bins = [] 
nums = []
for record in scores:
	bins.append(record)
	#nums += scores[record] * [record]
	nums.append(scores[record])

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# inspired by http://stackoverflow.com/questions/28931224/adding-value-labels-on-a-matplotlib-bar-chart

nums_series = pd.Series.from_array(nums)
#plt.yscale('log')
plt.figure()
ax = nums_series.plot(kind='bar')
#ax.set_title('Histogram of EarthSciences - Spring2015')
ax.set_title('Histogram of Medicine - Summer2015')
ax.set_xlabel('Net Promoter Score')
ax.set_ylabel('Distribution')
ax.set_xticklabels(bins)

rects = ax.patches
labels = [str(i) for i in nums]
print labels

for rect, label in zip(rects, labels) :
	height = rect.get_height()
	ax.text(rect.get_x() + rect.get_width() / 2, height + 5, label, ha = 'center', va = 'bottom')
plt.show()
