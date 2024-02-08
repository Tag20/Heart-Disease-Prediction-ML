# -*- coding: utf-8 -*-
"""ML_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fZ16c-rSM93VrqDPohrMInHG75mZ4leg

##Importing Libraries
"""

# Importing data processing and Linear Algebra libraries
import pandas as pd
import numpy as np

# Importing data visualization libraries
import seaborn as sns
import matplotlib.pyplot as plt

"""##Loading our Dataset"""

# Readin data from CSV file and loading into df varaible
df = pd.read_csv('/content/heart.csv')
df.head(10)

"""###Preprocessing the dataset"""

df.info()

df.describe(include='all')

# Finding any missing values
missing_data = df.isnull().sum()
missing_data

# Finding the count of unique values in each category
df.nunique()

# categorical data
catg_lst = df.select_dtypes(include='object').columns
# numerical data
num_lst = df.select_dtypes(include=['int64','float64']).columns

#IQR for checking outliers
low_range = df[num_lst].quantile(0.25) #Q1
high_range = df[num_lst].quantile(0.75) #Q3
low_range

high_range

#
iqr = high_range - low_range
iqr

lower_limit = low_range - 1.5*iqr

lower_limit

upper_limit = high_range + 1.5*iqr

upper_limit

"""###Skewness of the Data"""

df_cleaned = df[~((df[num_lst] < lower_limit) | (df[num_lst] > upper_limit)).any(axis=1)]

skewness = df_cleaned.skew()

skewness

"""## Using Boxplot to check outliers"""

num_lst = df_cleaned.select_dtypes(include=['int64', 'float64'])
plt.figure(figsize=(12, 8))

sns.boxplot(data=num_lst)

plt.title("Boxplot of Numerical Attributes")
plt.xticks(rotation=0)
plt.show()

"""##Removing OUtliers"""

#to remove the outliers
(df[['Cholesterol','RestingBP']]==0).sum()

# removing the unnecessary datapoints from dataset
old_data = df.copy()
df = df[ (df['Cholesterol']!=0) & (df['RestingBP']!=0) ]
print('Old Data Shape: ',old_data.shape)
print('New Data Shape: ',df.shape)

"""##Checking the distribution of patients who have heart disease in our dataset

"""

#Proportion of patients who have heart disease in our dataset
plt.figure(figsize=(8, 6))
ax = sns.countplot(data=df, x='HeartDisease')

# Set labels and title
plt.xlabel("Heart Disease (1 = Yes, 0 = No)")
plt.ylabel("Count")
plt.title("Proportion of Heart Disease Cases")

# Show the plot
plt.show()

"""##Converting Categorical to Numerical Values"""

#data preprocessing
# one hot encoding
df_scalled = pd.get_dummies(df,drop_first = True)
df_scalled.head()

x = df_scalled.drop(['HeartDisease'],axis=1)
y = df_scalled['HeartDisease']

"""##Splitting the dataset into 2 partitions - Test & Training Set"""

# splitting the data
# Importing data spliting data library for training and testing from given dataframe
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=.2)

# Scaling the data
# Module for Scaling the data
from sklearn.preprocessing import StandardScaler

# Normalize the data
sc = StandardScaler()
X_train = sc.fit_transform(x_train)
X_test = sc.transform(x_test)

X_train = pd.DataFrame(X_train, columns=x.columns)
X_test = pd.DataFrame(X_test, columns=x.columns)

display(X_train.head())
display(X_test.head())

"""#Logistic Regression"""

# Logistic Regression Model
from sklearn.linear_model import LogisticRegression

# Library module to check performance evaluation measures.
from sklearn.metrics import accuracy_score, roc_curve ,confusion_matrix,classification_report,f1_score
log_reg = LogisticRegression()

# Training the data
log_reg.fit(x_train,y_train)

# Testing the data
y_pred = log_reg.predict(x_test)

# Model Scores
log_train_accuracy = round(log_reg.score(x_train, y_train) * 100, 2)
log_accuracy = round(accuracy_score(y_pred, y_test) * 100, 2)
log_f1_score = round(f1_score(y_pred, y_test) * 100, 2)
print("Training Accuracy    :",log_train_accuracy,"%")
print("Model Accuracy Score :",log_accuracy,"%")
print("Classification_Report: \n",classification_report(y_test,y_pred))

#Plotting of Confusion Matrix
cm=confusion_matrix(y_pred, y_test)
conf_matrix =sns.heatmap(cm,annot=True)
print("Confusion Matrix:\n")
plt.show()

from sklearn.metrics import roc_curve, roc_auc_score

# Calculate the false positive rate, true positive rate, and thresholds
fpr, tpr, thresholds = roc_curve(y_test, y_pred)
# Calculate the AUC score
auc_score = roc_auc_score(y_test, y_pred)

# Plot the ROC curve
plt.plot(fpr, tpr, label='Logistic Regression (AUC = %0.2f)' % auc_score)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc='lower right')
plt.show()

sns.regplot(x=y_test, y=y_pred, logistic=True)
plt.xlabel('Actual Labels')
plt.ylabel('Predicted Probabilities')
plt.title('Logistic Regression Line')
plt.show()

"""##KNN Algorithm"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from sklearn.metrics import accuracy_score
KNN_model = KNeighborsClassifier(n_neighbors=7)
KNN_model.fit(X_train, y_train)

y_pred_k = KNN_model.predict(X_test)

# Model Scores
knn_train_accuracy = round(KNN_model.score(x_train, y_train) * 100, 2)
knn_accuracy = round(accuracy_score(y_pred_k, y_test) * 100, 2)
knn_f1_score = round(f1_score(y_pred_k, y_test) * 100, 2)
print("Training Accuracy    :",knn_train_accuracy,"%")
print("Model Accuracy Score :",knn_accuracy,"%")
print("Classification_Report: \n",classification_report(y_test,y_pred_k))

"""###Confusion Matrix for KNN

"""

cm=confusion_matrix(y_pred_k, y_test)
conf_matrix =sns.heatmap(cm,annot=True)
print("Confusion Matrix:\n")
plt.show()

"""###Selection of K value using Elbow Method"""

#For selecting K value
error_rate = []

# Will take some time
for i in range(1,40):

    knn = KNeighborsClassifier(n_neighbors=i)
    knn.fit(X_train,y_train)
    pred_i = knn.predict(X_test)
    error_rate.append(np.mean(pred_i != y_test))

import matplotlib.pyplot as plt
plt.figure(figsize=(10,6))
plt.plot(range(1,40),error_rate,color='red', linestyle='dashed', marker='o',
         markerfacecolor='green', markersize=10)
plt.title('Error Rate vs. K Value')
plt.xlabel('K')
plt.ylabel('Error Rate')

from sklearn.metrics import roc_curve, roc_auc_score

# Calculate the false positive rate, true positive rate, and thresholds
fpr, tpr, thresholds = roc_curve(y_test, y_pred_k)
# Calculate the AUC score
auc_score = roc_auc_score(y_test, y_pred_k)

# Plot the ROC curve
plt.plot(fpr, tpr, label='KNN Classifier  (AUC = %0.2f)' % auc_score)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc='lower right')
plt.show()

"""#Decision Tree Classification"""

#decision tree classifier
from sklearn.tree import DecisionTreeClassifier
Decision_model = DecisionTreeClassifier()
Decision_model = DecisionTreeClassifier(criterion="entropy",max_depth=7)
Decision_model.fit(X_train, y_train)

y_pred_d = Decision_model.predict(X_test)

#increase accuracy by using k folds cross-validation

from sklearn.model_selection import cross_val_score
scores = cross_val_score(Decision_model, X_train, y_train, cv=5)

from sklearn.tree import plot_tree, export_text

text_rep = export_text(Decision_model)

fig = plt.figure(figsize=(20,20))
graph = plot_tree(Decision_model, feature_names=list(x.columns), filled=True, fontsize=8)

# Model Scores
from sklearn.metrics import accuracy_score, roc_curve ,confusion_matrix,classification_report,f1_score
dec_train_accuracy = round(Decision_model.score(x_train, y_train) * 100, 2)
dec_accuracy = round(accuracy_score(y_pred_d, y_test) * 100, 2)
dec_f1_score = round(f1_score(y_pred_d, y_test) * 100, 2)
print("Training Accuracy    :",dec_train_accuracy,"%")
print("Model Accuracy Score :",dec_accuracy,"%")
print("Classification_Report: \n",classification_report(y_test,y_pred_d))

cm=confusion_matrix(y_pred_d, y_test)
conf_matrix =sns.heatmap(cm,annot=True)
print("Confusion Matrix:\n")
plt.show()

from sklearn.metrics import roc_curve, roc_auc_score

# Calculate the false positive rate, true positive rate, and thresholds
fpr, tpr, thresholds = roc_curve(y_test, y_pred_d)
# Calculate the AUC score
auc_score = roc_auc_score(y_test, y_pred_d)

# Plot the ROC curve
plt.plot(fpr, tpr, label='Decision Tree  (AUC = %0.2f)' % auc_score)
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc='lower right')
plt.show()

"""#Random Forest Classifier"""

# Create a Random Forest model
from sklearn.ensemble import RandomForestClassifier
RandomForest_model = RandomForestClassifier(n_estimators=50, criterion='entropy', random_state=40)

# Train the model
RandomForest_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred_r = RandomForest_model.predict(X_test)

# Visualize individual trees
for i in range(min(4, len(RandomForest_model.estimators_))):
    plt.figure(figsize=(10, 7))
    plot_tree(RandomForest_model.estimators_[i], filled=True, feature_names=[f'feature_{i}' for i in range(x.shape[1])])
    plt.title(f"Decision Tree {i+1}")
    plt.show()

# Model Scores
from sklearn.metrics import accuracy_score, roc_curve ,confusion_matrix,classification_report,f1_score
ran_train_accuracy = round(RandomForest_model.score(x_train, y_train) * 100, 2)
ran_accuracy = round(accuracy_score(y_pred_r, y_test) * 100, 2)
range_f1_score = round(f1_score(y_pred_r, y_test) * 100, 2)
print("Training Accuracy    :",ran_train_accuracy,"%")
print("Model Accuracy Score :",ran_accuracy,"%")
print("Classification_Report: \n",classification_report(y_test,y_pred_r))

cm=confusion_matrix(y_pred_r, y_test)
conf_matrix =sns.heatmap(cm,annot=True)
print("Confusion Matrix:\n")
plt.show()

from sklearn.metrics import roc_curve, roc_auc_score

# Calculate the false positive rate, true positive rate, and thresholds
fpr, tpr, thresholds = roc_curve(y_test, y_pred_r)
# Calculate the AUC score
auc_score = roc_auc_score(y_test, y_pred_r)

# Plot the ROC curve
plt.plot(fpr, tpr, label='Random Forest (AUC = %0.2f)' % auc_score)

plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend(loc='lower right')
plt.show()

"""input code"""

# sc = StandardScaler()
custom_input_data = [[45,140,220, 0, 172, 0.0, 1, 1, 0, 0, 1,0,1,1,0]]

# Make predictions for the specific case
custom_prediction = RandomForest_model.predict(custom_input_data)

print(f"Custom Input Predicted class: {custom_prediction}")

"""https://www.kaggle.com/code/tanmay111999/heart-failure-prediction-cv-score-90-5-models"""