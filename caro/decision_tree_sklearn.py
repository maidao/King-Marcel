import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Import dataset
dataset= pd.read_csv('data_cleaned.csv')
print(dataset)
X = dataset[['min', 'max', 'moy', 'ecart_moy_veille']]
Y = dataset[['frequentation']]

#
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3)

# Fit regression model
regr_1 = DecisionTreeRegressor(max_depth=2)
regr_2 = DecisionTreeRegressor(max_depth=5)
regr_1.fit(X_train, Y_train)
regr_2.fit(X_train, Y_train)

# Predict
y_1 = regr_1.predict(X_test)
y_2 = regr_2.predict(X_test)
comparaison = pd.DataFrame(y_1, columns=['y_predit'])
comparaison['y'] = Y_test.values
print(comparaison)
print(regr_1.score(X_test, Y_test))

# Training
clf = DecisionTreeRegressor(min_samples_leaf=10, max_depth=3)
clf = clf.fit(X, Y)
print(clf.score(X, Y))

'''
# Plot the results
plt.figure()
plt.scatter(X, Y, s=20, edgecolor="black",
            c="darkorange", label="data")
plt.plot(X_test, y_1, color="cornflowerblue",
         label="max_depth=2", linewidth=2)
plt.plot(X_test, y_2, color="yellowgreen", label="max_depth=5", linewidth=2)
plt.xlabel("days")
plt.ylabel("frequentation")
plt.title("Decision Tree Regression")
plt.legend()
plt.show()'''
