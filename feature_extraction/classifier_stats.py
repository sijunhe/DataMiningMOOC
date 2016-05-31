from sklearn import linear_model, datasets, metrics
from sklearn.cross_validation import train_test_split
from sklearn import linear_model, datasets, metrics
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV

#from demographic_feature_extraction import *
from stats_feature_extractor import *

def classifier(train_num, use_profile=False):

	X,Y = feature_extractor(train_num, use_profile)

	logistic_classifier = linear_model.LogisticRegression(C=100.0, penalty='l1')
	X_train, X_test, Y_train, Y_test = train_test_split(X, Y,
	                                                    test_size=0.2,
	                                                    random_state=0)
	logistic_classifier.fit(X_train, Y_train)



	logistic = linear_model.LogisticRegression()
	rbm = BernoulliRBM(random_state=0, verbose=True)

	classifier = Pipeline(steps=[('rbm', rbm), ('logistic', logistic)])

	rbm.learning_rate = 0.06
	rbm.n_iter = 20
	# More components tend to give better prediction performance, but larger
	# fitting time
	rbm.n_components = 100
	logistic.C = 6000.0

	# Training RBM-Logistic Pipeline
	# classifier.fit(X_train, Y_train)

	# print("Logistic regression using RBM features:\n%s\n" % (
	#     metrics.classification_report(
	#         Y_test,
	#         classifier.predict(X_test))))

	# param_grid = {'penalty':['l1','l2'], 'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000] }
	# GridSearch = GridSearchCV(logistic_classifier, param_grid, cv = 10)
	# GridSearch.fit(X_train, Y_train)
	# bestLRclf = GridSearch.best_estimator_

	bestLRclf = logistic_classifier

	print("Logistic regression using raw features:\n%s\n" % (
	    metrics.classification_report(
	        Y_test,
	        bestLRclf.predict(X_test))))

	print bestLRclf.coef_


	# print "logistic_classifier RBM accuracy", metrics.accuracy_score(Y_test, classifier.predict(X_test))
	print "logistic_classifier accuracy", metrics.accuracy_score(Y_test, bestLRclf.predict(X_test))
	print "logistic_regression mean_squared_error", metrics.mean_squared_error(Y_test, bestLRclf.predict(X_test))

	logProb = bestLRclf.predict_log_proba(X_test)
	second_col = logProb[:,1]
	sorted_index = np.argsort(second_col)

	correct_count = 0
	for i in range(1, 427):
		index = sorted_index[-i]
		if Y_test[index] == 1:
			correct_count += 1
	correct_percentage = correct_count / 426.0
	print "correct_percentage", correct_percentage

	return metrics.accuracy_score(Y_test, bestLRclf.predict(X_test))
	# return correct_percentage

if __name__ == "__main__":
	train_num = 10
	classifier(train_num, False)

