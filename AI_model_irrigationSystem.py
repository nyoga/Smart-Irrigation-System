# -*- coding: utf-8 -*-
"""FINAL YR PROJECT

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QPqYcDYrWQIyEd1K3PIwHiMAMFKWqXkw
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from sklearn import model_selection
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.ensemble import BaggingClassifier

import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file into a DataFrame
df = pd.read_csv('3_plant.csv')

# Extract N, P, and K values
N_values = df['N']
P_values = df['P']
K_values = df['K']

# Plotting
plt.scatter(df.index, N_values, label='N')
plt.scatter(df.index, P_values, label='P')
plt.scatter(df.index, K_values, label='K')

# Adding labels and title
plt.xlabel('Data Points')
plt.ylabel('Values')
plt.title('N, P, and K values')
plt.legend()
plt.show()

df.head()

print("Shape of the dataframe: ",df.shape)
df.isna().sum()

df.info()

df.describe()

df.dtypes

sns.displot(x=df['N'], bins=20,kde=True,edgecolor="black",color='black',facecolor='#ffb03b')

plt.title("Nitrogen",size=20)
plt.show()

sns.displot(x=df['P'],bins=20,color='black',edgecolor='black',kde=True,facecolor='#ffb03b')
plt.title("Phosphorus", size=20)

plt.show()

sns.displot(x=df['K'],kde=True, bins=20, facecolor='#ffb03b',edgecolor='black', color='black')
plt.title("Potassium",size=20)
plt.show()

sns.displot(x=df['temperature'], bins=20,kde=True,edgecolor="black",color='black',facecolor='#ffb03b')
plt.title("Temperature",size=20)
plt.show()

sns.displot(x=df['humidity'], color='black',facecolor='#ffb03b',kde=True,edgecolor='black')
plt.title("Humidity",size=20)
plt.show()

sns.relplot(x='humidity',y='temperature',data=df,kind='scatter',hue='label',height=5)
plt.show()

sns.pairplot(data=df,hue='label')
plt.show()

crops = df['label'].unique()
print(len(crops))
print(crops)
print(pd.value_counts(df['label']))

df2=[]
for i in crops:
    df2.append(df[df['label'] == i])
df2[1].head()

import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

# Load dataset from CSV file
# Assuming the CSV file has columns: N, P, K, humidity, temperature, label
# Replace 'your_dataset.csv' with the actual file name
dataset = pd.read_csv('rice_dataset.csv')

# Manually provide optimum values for pump on and pump off
optimum_values_pump_off = [60, 35, 35, 84.97 , 20.5]
optimum_values_pump_on =  [99, 60, 45, 80.12, 26.93]

# Add a new column 'label' based on the distance to optimum values
dataset['label'] = np.where(np.linalg.norm(dataset[['N', 'P', 'K', 'humidity', 'temperature']].values - optimum_values_pump_off, axis=1) <
                            np.linalg.norm(dataset[['N', 'P', 'K', 'humidity', 'temperature']].values - optimum_values_pump_on, axis=1), 0, 1)

# Separate features and labels
X = dataset[['N', 'P', 'K', 'humidity', 'temperature']]
y = dataset['label']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

# Normalize the data (optional but recommended)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define weights for each attribute (adjust these according to your requirements)
weights = [2,1,1,3,2]  # Adjust these weights based on the importance of each attribute

# Apply weights to the training and testing data
X_train_weighted = X_train * weights
X_test_weighted = X_test * weights

# Initialize the KNN classifier
knn_classifier = KNeighborsClassifier(n_neighbors=3)  # You can adjust the number of neighbors

# Train the classifier
knn_classifier.fit(X_train_weighted, y_train)

# Make predictions on the test set
predictions = knn_classifier.predict(X_test_weighted)


# Evaluate the accuracy
#accuracy = np.mean(predictions == y_test)
accuracy = np.mean(predictions == y_test)
print("Accuracy:", accuracy)

# Print pump status for each entry in the dataset
dataset['predicted_label'] = knn_classifier.predict(scaler.transform(dataset[['N', 'P', 'K', 'humidity', 'temperature']] * weights))
dataset['pump_status'] = np.where(dataset['predicted_label'] == 0, 'Pump Off', 'Pump On')

# Print pump status and accuracy for each entry
# Print the pump status for each entry in the dataset
for index, row in dataset.iterrows():
    print(f"Entry {index + 1}: Pump {'On' if row['label'] == 1 else 'Off'}")

# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load your CSV file
file_path = 'rice_dataset_1.csv'
df = pd.read_csv(file_path)

# Specify input features (X) and target variable (y)
X = df[['N', 'P', 'K', 'humidity', 'temperature']]
y = df['Pump_status']  # Assuming 'PumpStatus' is the column indicating pump on/off

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1875, random_state=40)

# Define the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)
class_report = classification_report(y_test, y_pred)

print(f'Accuracy: {accuracy}')
print(f'Confusion Matrix:\n{conf_matrix}')
print(f'Classification Report:\n{class_report}')

# Import necessary libraries
import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Read data from CSV file
# Replace 'rice_dataset_1.csv' with the actual path to your CSV file
data = pd.read_csv('rice_dataset_1.csv')

# Assuming the CSV file has columns 'N', 'P', 'K', 'humidity', 'temperature', and 'Pump_status'
# 'Pump_status' is the target variable indicating pump ON (1) or pump OFF (0)
X = data[['N', 'P', 'K', 'humidity', 'temperature']]
y = data['Pump_status']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.45, random_state=42)

# Define SVM model
model = svm.SVC(kernel='linear', C=1)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
predictions = model.predict(X_test)

# Evaluate the accuracy of the model
accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy}")

# Iterate through each row in the CSV file
for index, row in data.iterrows():
    new_entry = pd.DataFrame([row[['N', 'P', 'K', 'humidity', 'temperature']]])
    prediction_new_entry = model.predict(new_entry)
    # Output the result
    print(f"For entry {index + 1}:")
    if prediction_new_entry == 1:
        print("  Pump ON")
    else:
        print("  Pump OFF")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load dataset from CSV file
# Assuming the CSV file has columns: N, P, K, humidity, temperature, label
# Replace 'your_dataset.csv' with the actual file name
dataset = pd.read_csv('rice_dataset.csv')

# Manually provide optimum values for pump on and pump off
optimum_values_pump_off = [60, 35, 35, 84.97, 20.5]
optimum_values_pump_on = [99, 60, 45, 80.12, 26.93]

# Add a new column 'label' based on the distance to optimum values
dataset['label'] = np.where(np.linalg.norm(dataset[['N', 'P', 'K', 'humidity', 'temperature']].values - optimum_values_pump_off, axis=1) <
                            np.linalg.norm(dataset[['N', 'P', 'K', 'humidity', 'temperature']].values - optimum_values_pump_on, axis=1), 0, 1)

# Separate features and labels
X = dataset[['N', 'P', 'K', 'humidity', 'temperature']]
y = dataset['label']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

# Normalize the data (optional but recommended)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define weights for each attribute (adjust these according to your requirements)
weights = [2, 1, 1, 3, 2]  # Adjust these weights based on the importance of each attribute

# Apply weights to the training and testing data
X_train_weighted = X_train * weights
X_test_weighted = X_test * weights

# Initialize the KNN classifier
knn_classifier = KNeighborsClassifier(n_neighbors=3)  # You can adjust the number of neighbors

# Train the classifier
knn_classifier.fit(X_train_weighted, y_train)

# Make predictions on the test set
predictions = knn_classifier.predict(X_test_weighted)

# Evaluate the accuracy
correct_predictions = np.sum(predictions == y_test)
total_samples = len(y_test)
accuracy = correct_predictions / total_samples
print("Accuracy:", accuracy)

# Compute confusion matrix manually
conf_matrix = np.zeros((2, 2))
for true_label, pred_label in zip(y_test, predictions):
    conf_matrix[true_label][pred_label] += 1

# Print confusion matrix
print("Confusion Matrix:")
print(conf_matrix)

# Visualize confusion matrix (optional)
plt.imshow(conf_matrix, cmap=plt.cm.Blues, interpolation='nearest')
plt.title('Confusion Matrix')
plt.colorbar()
plt.xticks([0, 1], ['Predicted Off', 'Predicted On'])
plt.yticks([0, 1], ['Actual Off', 'Actual On'])
plt.show()

# Print pump status for each entry in the dataset
dataset['predicted_label'] = knn_classifier.predict(scaler.transform(dataset[['N', 'P', 'K', 'humidity', 'temperature']] * weights))
dataset['pump_status'] = np.where(dataset['predicted_label'] == 0, 'Pump Off', 'Pump On')

# Print pump status and accuracy for each entry
for index, row in dataset.iterrows():
    print(f"Entry {index + 1}: Pump {'On' if row['label'] == 1 else 'Off'}")

import pandas as pd
from sklearn import svm
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt

# Read data from CSV file
# Replace 'rice_dataset_1.csv' with the actual path to your CSV file
data = pd.read_csv('rice_dataset.csv')

# Assuming the CSV file has columns 'N', 'P', 'K', 'humidity', 'temperature', and 'Pump_status'
# 'Pump_status' is the target variable indicating pump ON (1) or pump OFF (0)
X = data[['N', 'P', 'K', 'humidity', 'temperature']]
y = data['Pump_status']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.45, random_state=42)

# Define SVM model
model = svm.SVC(kernel='poly', C=1)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
predictions = model.predict(X_test)

# Calculate accuracy
correct_predictions = np.sum(predictions == y_test)
total_samples = len(y_test)
accuracy = correct_predictions / total_samples
print(f"Accuracy: {accuracy}")

# Confusion matrix calculation
conf_matrix = np.zeros((2, 2))
for true_label, pred_label in zip(y_test, predictions):
    conf_matrix[true_label][pred_label] += 1

# Print confusion matrix
print("Confusion Matrix:")
print(conf_matrix)

# Visualize confusion matrix
plt.imshow(conf_matrix, cmap=plt.cm.Blues, interpolation='nearest')
plt.title('Confusion Matrix')
plt.colorbar()
plt.xticks([0, 1], ['Predicted OFF', 'Predicted ON'])
plt.yticks([0, 1], ['Actual OFF', 'Actual ON'])
plt.show()

# Iterate through each row in the CSV file
for index, row in data.iterrows():
    new_entry = pd.DataFrame([row[['N', 'P', 'K', 'humidity', 'temperature']]])
    prediction_new_entry = model.predict(new_entry)

    # Output the result
    print(f"For entry {index + 1}:")
    if prediction_new_entry == 1:
        print("  Pump ON")
    else:
        print("  Pump OFF")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load your CSV file
file_path = 'rice_dataset_1.csv'
df = pd.read_csv(file_path)

# Specify input features (X) and target variable (y)
X = df[['N', 'P', 'K', 'humidity', 'temperature']]
y = df['Pump_status']  # Assuming 'PumpStatus' is the column indicating pump on/off

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1875, random_state=40)

# Define the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Calculate accuracy
correct_predictions = np.sum(y_pred == y_test)
total_samples = len(y_test)
accuracy = correct_predictions / total_samples
print(f"Accuracy: {accuracy}")

# Confusion matrix calculation
conf_matrix = np.zeros((2, 2))
for true_label, pred_label in zip(y_test, y_pred):
    conf_matrix[true_label][pred_label] += 1

# Print confusion matrix
print("Confusion Matrix:")
print(conf_matrix)

# Visualize confusion matrix
plt.imshow(conf_matrix, cmap=plt.cm.Blues, interpolation='nearest')
plt.title('Confusion Matrix')
plt.colorbar()
plt.xticks([0, 1], ['Predicted OFF', 'Predicted ON'])
plt.yticks([0, 1], ['Actual OFF', 'Actual ON'])
plt.show()

# Classification Report
unique_labels = np.unique(np.concatenate((y_test, y_pred)))
class_report = ''
for label in unique_labels:
    class_report += f'Class {label}:\n'
    class_report += f'   Precision: {conf_matrix[label, label] / np.sum(conf_matrix[:, label]):.2f}\n'
    class_report += f'   Recall: {conf_matrix[label, label] / np.sum(conf_matrix[label, :]):.2f}\n'
    class_report += f'   F1 Score: {2 * (conf_matrix[label, label] / np.sum(conf_matrix[:, label]) * conf_matrix[label, label] / np.sum(conf_matrix[label, :])) / (conf_matrix[label, label] / np.sum(conf_matrix[:, label]) + conf_matrix[label, label] / np.sum(conf_matrix[label, :])):.2f}\n\n'

print(f'Classification Report:\n{class_report}')

# Import necessary libraries
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

# Load dataset from CSV file
dataset = pd.read_csv('rice_dataset.csv')

# Manually provide optimum values for pump on and pump off
optimum_values_pump_off = [60, 35, 35, 84.97 , 20.5]
optimum_values_pump_on =  [99, 60, 45, 80.12, 26.93]

# Add a new column 'label' based on the distance to optimum values
dataset['label'] = calculate_labels(dataset, optimum_values_pump_off, optimum_values_pump_on)

# Separate features and labels
X, y = prepare_features_and_labels(dataset)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = split_data(X, y)

# Normalize the data (optional but recommended)
X_train, X_test = normalize_data(X_train, X_test)

# Define weights for each attribute (adjust these according to your requirements)
weights = [2, 1, 1, 3, 2]  # Adjust these weights based on the importance of each attribute

# Apply weights to the training and testing data
X_train_weighted, X_test_weighted = apply_weights(X_train, X_test, weights)

# Initialize the KNN classifier
knn_classifier = initialize_knn_classifier()

# Train the classifier
train_classifier(knn_classifier, X_train_weighted, y_train)

# Make predictions on the test set
predictions = make_predictions(knn_classifier, X_test_weighted)

# Evaluate the accuracy
accuracy = calculate_accuracy(predictions, y_test)
print("Accuracy:", accuracy)

# Print pump status for each entry in the dataset
dataset['predicted_label'] = knn_classifier.predict(scaler.transform(dataset[['N', 'P', 'K', 'humidity', 'temperature']] * weights))
dataset['pump_status'] = np.where(dataset['predicted_label'] == 0, 'Pump Off', 'Pump On')

# Print pump status and accuracy for each entry
print_pump_status_and_accuracy(dataset)