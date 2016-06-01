import pandas as pd
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('/Users/jerrykhong/Desktop/Projects/Kaggle/train.csv')

df['Age'] = df['Age'].fillna(df['Age'].median())

df.loc[df['Sex'] == 'male','Sex'] = 0
df.loc[df['Sex'] == 'female','Sex'] = 1

df['Embarked'] = df['Embarked'].fillna('S')
df.loc[df['Embarked'] == 'S','Embarked'] = 0
df.loc[df['Embarked'] == 'C','Embarked'] = 1
df.loc[df['Embarked'] == 'Q','Embarked'] = 2

titanic_test = pd.read_csv("/Users/jerrykhong/Desktop/Projects/Kaggle/test.csv")
titanic_test["Age"] = titanic_test["Age"].fillna(titanic_test["Age"].median())
titanic_test["Fare"] = titanic_test["Fare"].fillna(titanic_test["Fare"].median())
titanic_test.loc[titanic_test["Sex"] == "male", "Sex"] = 0
titanic_test.loc[titanic_test["Sex"] == "female", "Sex"] = 1
titanic_test["Embarked"] = titanic_test["Embarked"].fillna("S")

titanic_test.loc[titanic_test["Embarked"] == "S", "Embarked"] = 0
titanic_test.loc[titanic_test["Embarked"] == "C", "Embarked"] = 1
titanic_test.loc[titanic_test["Embarked"] == "Q", "Embarked"] = 2

predictors = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "Embarked"]

alg = RandomForestClassifier(random_state=1, n_estimators=150, min_samples_split=4, min_samples_leaf=2)
scores = cross_validation.cross_val_score(alg, df[predictors], df["Survived"], cv=3)
print(scores.mean())