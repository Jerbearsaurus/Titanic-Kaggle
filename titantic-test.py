import pandas as pd
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
import re

## Create Training DataFrame 
df = pd.read_csv('/Users/jerrykhong/Desktop/Projects/Kaggle/train.csv')
df['Age'] = df['Age'].fillna(df['Age'].median())

## Convert 'Sex' column into numeric
df.loc[df['Sex'] == 'male','Sex'] = 0
df.loc[df['Sex'] == 'female','Sex'] = 1

## Convert 'Embarked' column into numeric. Fill in n/a rows.
df['Embarked'] = df['Embarked'].fillna('S')
df.loc[df['Embarked'] == 'S','Embarked'] = 0
df.loc[df['Embarked'] == 'C','Embarked'] = 1
df.loc[df['Embarked'] == 'Q','Embarked'] = 2

## Create Testing DataFrame
titanic_test = pd.read_csv('/Users/jerrykhong/Desktop/Projects/Kaggle/test.csv')
titanic_test['Age'] = titanic_test['Age'].fillna(titanic_test['Age'].median())
titanic_test['Fare'] = titanic_test['Fare'].fillna(titanic_test['Fare'].median())
titanic_test.loc[titanic_test['Sex'] == 'male', 'Sex'] = 0
titanic_test.loc[titanic_test['Sex'] == 'female', 'Sex'] = 1
titanic_test['Embarked'] = titanic_test['Embarked'].fillna('S')

titanic_test.loc[titanic_test['Embarked'] == 'S', 'Embarked'] = 0
titanic_test.loc[titanic_test['Embarked'] == 'C', 'Embarked'] = 1
titanic_test.loc[titanic_test['Embarked'] == 'Q', 'Embarked'] = 2

def get_title(name):
	title_search = re.search(' ([A-Za-z]+)\.',name)
	if title_search:
		return title_search.group(1)
	return ''
titles = df['Name'].apply(get_title)

title_mapping = {'Mr': 1, 'Miss': 2, 'Mrs': 3, 'Master': 4, 'Dr': 5, 'Rev': 6, 'Major': 7, 'Col': 7, 'Mlle': 8, 'Mme': 8, 'Don': 9, 'Lady': 10, 'Countess': 10, 'Jonkheer': 10, 'Sir': 9, 'Capt': 7, 'Ms': 2}
for k,v in title_mapping.items():
    titles[titles == k] = v
titanic['Title'] = titles

## Classify predictors for Random Forest
predictors = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']

alg = RandomForestClassifier(random_state=1, n_estimators=150, min_samples_split=4, min_samples_leaf=2)
scores = cross_validation.cross_val_score(alg, df[predictors], df['Survived'], cv=3)

df['FamilySize'] = df['SibSp'] + df['Parch']
df['NameLength'] = df['Name'].apply(lambda x: len(x))
