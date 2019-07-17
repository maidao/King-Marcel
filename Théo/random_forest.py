import pandas as pd
import matplotlib.pyplot as plt

from data_trier_reporting import DataTrierReporting

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

rep_jour = DataTrierReporting('Data/reporting_jour.csv')
rep_jour.clean_data()
rep_jour.join_stats()
rep_jour.ecart_moy()
rep_jour.add_semaine_passe()
rep_jour.add_moy_mois()
print(rep_jour.df.columns)
rep_jour.df.to_csv('dvore2.csv', index=False, header=True)

Xtrain = rep_jour.df[['Lundi', 'Mardi', 'Mercredi',
       'Jeudi', 'Vendredi', 'Samedi', 'Dimanche', 'min', 'max', 'moy',
       'ecart_moy_veille', 'ecart_moy_n2', 'ecart_moy_n3', 'freq_n1',
       'freq_n2', 'freq_n3', 'freq_n4', 'moy_mois']]
Ytrain = rep_jour.df['frequentation'].values

train_x, test_x, train_y, test_y = train_test_split(Xtrain, Ytrain, random_state=1, test_size=0.2)

regr = RandomForestRegressor(n_estimators=200, min_samples_split=17, min_samples_leaf=5,
max_features='sqrt', max_depth=10, bootstrap=True)

regr.fit(train_x, train_y)
y_rf = regr.predict(test_x)
comparaison = pd.DataFrame(y_rf, columns=['y_predit'])
comparaison['y'] = test_y
comparaison = comparaison.rename(index=str, columns={'y': 'reel', 'y_predit': 'prediction'})
print(comparaison)
print(regr.score(test_x, test_y))

comparaison.plot()
plt.savefig('random_forest_pred.png')
plt.show()

