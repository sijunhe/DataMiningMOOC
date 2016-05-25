import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from classifier_stats import *

trainNum = [1, 3, 5, 7, 9, 11, 13, 15, 20]
accuracies = []
accuracies2 = []

for train_num in trainNum:
	accuracies.append(classifier(train_num))

for train_num in trainNum:
	accuracies2.append(classifier(train_num, True))

plt.figure()
plt.title('Stats Learning Winter 2016 profile retension prediction result')
plt.xlabel('Number of previous video data we use')
plt.ylabel('Prediction accuracy')
line_up = plt.plot(trainNum, accuracies, label='User video matrix')
line_down = plt.plot(trainNum, accuracies2, label='Profile')
plt.legend()
plt.show()

