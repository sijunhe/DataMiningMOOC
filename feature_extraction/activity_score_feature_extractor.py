import csv
from sets import Set

screen_name_activity_score = {}
quiz_id_name = {}
unique_quiz = Set()
count = 0
with open("../../codes/earth_Spring2015/EarthSciences_ResGeo202_Spring2015_ActivityGrade.csv", "r") as csvfile :
	lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
	for line in lines :
		if line[4] != "0" and count < 20 and line[13] not in unique_quiz:
			print line
			count += 1
			unique_quiz.add(line[13])
		if line[14] not in quiz_id_name :
			quiz_id_name[line[14]] = line[13]
		if line[12] == "'anon_screen_name'" :
			continue
		# line[12] -> anon_screen_name, line[14] -> module_id, line[3] -> grade
		if line[12] not in screen_name_activity_score :
			screen_name_activity_score[line[12]] = {}
			screen_name_activity_score[line[12]][line[14]] = line[3]
		else :
			screen_name_activity_score[line[12]][line[14]] = line[3]
		if "Section 3 - Hydraulic Fracturing and Shmax from Wellbore Breakouts" in line :
			if line[4] != "0" :
				print line[4]
# count = 0
# for i in screen_name_activity_score :
# 	count += 1
# 	if count < 20 :
# 		print screen_name_activity_score[i]

# print len(screen_name_activity_score)
# print len(quiz_id_name)
# for i in quiz_id_name: 
# 	print quiz_id_name[i]