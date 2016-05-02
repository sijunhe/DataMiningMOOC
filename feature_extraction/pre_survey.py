import csv
from collections import defaultdict

survey_id_courses_started = {}
survey_id_courses_finished = {}
courses_started_dict = {0:0}
courses_finished_dict = {0:0}
screen_name_courses_started = defaultdict(int)
screen_name_courses_finished = defaultdict(int)
with open ('../../data/EarthSciences_ResGeo202_Spring2015_survey_responses.csv', 'r') as csvfile :
	lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
	for line in lines :
		
		# How many open online courses have you started before this one? 
		if line[0] == "SV_dhGmpvbbuyNZEA5" and line[2] == "Q2.3" :
			if line[4] == "" or line[4] == ".5" :
				survey_id_courses_started[line[1]] = 0
				courses_started_dict[0] += 1
			# elif line[4] == ".5" :
			# 	print line
			# elif line[4] == "202" :
			# 	print line
			else :
				num_course = int(line[4])
				survey_id_courses_started[line[1]] = num_course
				if num_course in courses_started_dict :
					courses_started_dict[num_course] += 1
				else :
					courses_started_dict[num_course] = 1
		
		# How many open online courses have you finished before this one?
		if line[0] == "SV_dhGmpvbbuyNZEA5" and line[2] == "Q2.4" :
			if line[4] == "" or line[4] == "0.0":
				survey_id_courses_finished[line[1]] = 0
				courses_finished_dict[0] += 1
			# elif line[4] == ".5" :
			# 	print line
			# elif line[4] == "202" :
			# 	print line
			else :
				num_course = int(line[4])
				survey_id_courses_finished[line[1]] = num_course
				if num_course in courses_finished_dict :
					courses_finished_dict[num_course] += 1
				else :
					courses_finished_dict[num_course] = 1			
# print courses_started_dict
# print len(survey_id_courses_started)
# print courses_finished_dict	
# print len(survey_id_courses_finished)

with open('../../data/EarthSciences_ResGeo202_Spring2015_survey_response_metadata.csv', 'r') as csvfile :
	lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
	for line in lines :
		if line[0] == "SV_dhGmpvbbuyNZEA5" and line[1] in survey_id_courses_started :
			screen_name_courses_started[line[2]] = survey_id_courses_started[line[1]]
		if line[0] == "SV_dhGmpvbbuyNZEA5" and line[1] in survey_id_courses_finished :
			screen_name_courses_finished[line[2]] = survey_id_courses_finished[line[1]]

# print len(screen_name_courses_started)
# print len(screen_name_courses_finished)
count = 0
for i in screen_name_courses_finished :
	# print i, screen_name_courses_finished[i]
	count += 1
	if count > 20:
		break

# print screen_name_courses_started
# print screen_name_courses_finished