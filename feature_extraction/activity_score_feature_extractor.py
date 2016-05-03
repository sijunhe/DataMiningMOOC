import csv

screen_name_activity_score = {}

with open("../../codes/earth_Spring2015/EarthSciences_ResGeo202_Spring2015_ActivityGrade.csv", "r") as csvfile :
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

# count = 0
# for i in screen_name_activity_score :
# 	count += 1
# 	if count < 20 :
# 		print screen_name_activity_score[i]
