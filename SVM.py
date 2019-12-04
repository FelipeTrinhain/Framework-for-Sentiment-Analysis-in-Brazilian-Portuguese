from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm

class SVM:

    def __init__(self):
        #Create a svm Classifier
        self.clf = svm.SVC(kernel='linear') # Linear Kernel

    def x_to_dataframe(self, x_array):
        vect = CountVectorizer()
        x_dtm = vect.fit_transform(x_array)
        x_dtm = x_dtm.toarray()
        
        return x_dtm
        #Train the model using the training sets
    def train_svm_model(self, x_train, y_train):
        
        return self.clf.fit(x_train, y_train)

        #Uses the test dataset to classify data
    def test_svm_model(self, x_test, trained_model):
        
        y_pred = trained_model.predict(x_test)

        return y_pred