import numpy as np
import pandas as pd
from sklearn.feature_selection import chi2
from sklearn.feature_extraction.text import CountVectorizer

class Chi2:
    
    def __init__(self):
        pass
        

    def x_to_dataframe(self, x_array):
        vect = CountVectorizer()
        x_dtm = vect.fit_transform(x_array)
        x_dtm = x_dtm.toarray()
        df = pd.DataFrame(x_dtm, columns = vect.get_feature_names())

        return df

    def calculate_chi2(self, df, y_array):
        chi2_score = chi2(df, y_array)

        return chi2_score

    def get_position_to_extract(self, chi2_score):
        position_to_extract = []
     
        for i in range(0, len(chi2_score[0])):
            if(chi2_score[0][i] >= 6.63):
                if(chi2_score[1][i] < 0.01):
                    position_to_extract.append(i)

        return position_to_extract

    def get_features(self, df, position_to_extract):
        extracted_features = []

        for pos in position_to_extract:
            extracted_features.append(df.columns[pos])

        return extracted_features
