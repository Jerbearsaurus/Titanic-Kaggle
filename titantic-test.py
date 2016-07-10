## Import packages to build a basic model
import pandas as pd
import numpy as np
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
import re

## Create training DataFrame
df = pd.read_csv('/Users/jerrykhong/Desktop/Projects/Kaggle/train.csv')
df['Age'] = df['Age'].fillna(df['Age'].median())

## Convert the categorical 'Sex' column into a numeric column
df.loc[df['Sex'] == 'male','Sex'] = 0
df.loc[df['Sex'] == 'female','Sex'] = 1

## Convert the categorical 'Embarked' column into a numeric column. Also, filling in n/a rows with the most common class 'S'.
df['Embarked'] = df['Embarked'].fillna('S')
df.loc[df['Embarked'] == 'S','Embarked'] = 0
df.loc[df['Embarked'] == 'C','Embarked'] = 1
df.loc[df['Embarked'] == 'Q','Embarked'] = 2

## Create Testing DataFrame and duplicate the changes we made to the Training set.
titanic_test = pd.read_csv('/Users/jerrykhong/Desktop/Projects/Kaggle/test.csv')
titanic_test['Age'] = titanic_test['Age'].fillna(titanic_test['Age'].median())
titanic_test['Fare'] = titanic_test['Fare'].fillna(titanic_test['Fare'].median())
titanic_test.loc[titanic_test['Sex'] == 'male', 'Sex'] = 0
titanic_test.loc[titanic_test['Sex'] == 'female', 'Sex'] = 1
titanic_test['Embarked'] = titanic_test['Embarked'].fillna('S')

titanic_test.loc[titanic_test['Embarked'] == 'S', 'Embarked'] = 0
titanic_test.loc[titanic_test['Embarked'] == 'C', 'Embarked'] = 1
titanic_test.loc[titanic_test['Embarked'] == 'Q', 'Embarked'] = 2

## Drop columns that are not needed
titanic_test = titanic_test.drop('Name',1)

## Select features that the model will predict on
predictors = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']

## Import the Random Forest model, and instantiate it. Fit and predict.
alg = RandomForestClassifier(random_state=1, n_estimators=150, min_samples_split=4, min_samples_leaf=2)
scores = cross_validation.cross_val_score(alg, df[predictors], df['Survived'], cv=3)
alg.fit(df[predictors], df["Survived"])
predictions = alg.predict(titanic_test[predictors])

submission = pd.DataFrame({
        "PassengerId": titanic_test["PassengerId"],
        "Survived": predictions
    })
submission.to_csv("kaggle.csv", index=False)
