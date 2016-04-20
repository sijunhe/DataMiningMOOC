import csv
from collections import defaultdict
import numpy as np

responseUserID = {}
userScore = {}
screen_name_to_gender = defaultdict(int)
screen_name_to_year_of_birth = defaultdict(int)
screen_name_to_education = defaultdict(int)

## Get ResponseID - UserID matching
with open('survey_post_EarthSciences_ResGeo202_Spring2015_respondent_metadata.csv', 'r') as csvfile :	
    lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
    
    for line in lines :
        if line[1] not in responseUserID:
            responseUserID[line[1]] = line[2]

# print responseUserID

# Get Survey Data, only get the ID that has a matching 
with open('survey_post_EarthSciences_ResGeo202_Spring2015_response.csv', 'r') as csvfile :	
    lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
    for line in lines :
        if (line[2] == "Q1.1" and line[4] != ''):
            if line[1] in responseUserID:
                userScore[responseUserID[line[1]]] = line[4]

# print userScore
year_count = 0
gender_count = 0
education_count = 0
birth_years = []

with open('EarthSciences_ResGeo202_Spring2015_demographics.csv', 'r') as csvfile :
	lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
	for line in lines :
		if line[0] in userScore : 
			if line[2] != "\\N" :
				birth_years.append(int(line[2]))
birth_years = sorted(birth_years)
median_birht_year = birth_years[len(birth_years) / 2]
#print median_birht_year

with open('EarthSciences_ResGeo202_Spring2015_demographics.csv', 'r') as csvfile :
	lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')				
	for line in lines :
		if line[0] in userScore : 

			# gender feature: blank -> 0, m -> -1, f -> +1
			if line[1] == "m" :
				screen_name_to_gender[line[0]] = -1
			if line[1] == "f" :
				screen_name_to_gender[line[0]] = 1
			if line[1] not in screen_name_to_gender and line[0] != "\\N" :
				#gender_count += 1
				screen_name_to_gender[line[0]] = 0

			# year_of_birth
			if line[2] != "\\N" :
				screen_name_to_year_of_birth[line[0]] = int(line[2])

			# median interpolation
			if line[2] == "\\N" and line[0] != "\\N":
				screen_name_to_year_of_birth[line[0]] = median_birht_year
				#year_count += 1
			
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
				#education_count += 1
#print birth_years			
#print year_count
#print gender_count
#print education_count
print len(screen_name_to_gender)
print len(screen_name_to_year_of_birth)
print len(screen_name_to_education)

X = np.array([0, 0, 0])
# Y = np.array([0])
Y = [0]

for id in userScore:
	newrow = [screen_name_to_gender[id], screen_name_to_year_of_birth[id], screen_name_to_education[id]]
	X = np.vstack([X, newrow])
	# Y = np.vstack([Y, [userScore[id]]])
	Y.append(userScore[id])

X = np.delete(X, 0, 0)
print X
print Y

print len(X)
print len(Y)

