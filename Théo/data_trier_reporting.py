import pandas as pd
import matplotlib.pyplot as plt
import statistics

from sklearn.preprocessing import OneHotEncoder

from constantes import valeurs_jours, listes_jour, jours

class DataTrierReporting:

    def __init__(self, path):
        self.df = pd.read_csv(path, sep=';')

    def tri_type_vente(self):
        self.df = self.df[self.df['type_vente'] == 'CA']

    def remove_empty(self):
        self.df = self.df[(self.df['frequentation'] != 0) & (self.df['ca_ttc'] != 0.00)]

    def remove_columns(self):
        self.df = self.df[['frequentation', 'ca_ttc', 'date_commande', 'jour_semaine']]
        self.df = self.df.drop(self.df[(self.df['frequentation'] == 0) & (self.df['ca_ttc'] == 0)].index)
    
    def convert_date(self):
        self.df['date_commande'] = pd.to_datetime(self.df['date_commande'])

    def group_by_date(self):
        self.df = self.df.groupby(['date_commande', 'jour_semaine']).sum()
    
    def prix_moyen(self):
        self.df['prix_moyen'] = self.df['ca_ttc'] / self.df['frequentation']

    def create_day_value(self):
        day = []
        for elt in self.df.index.get_level_values('jour_semaine').values:
            for jour, val in valeurs_jours.items():
                if elt == jour:
                    day.append(val)
        self.df['jour_semaine'] = day

    def create_week_end(self):
        week_end = []
        for elt in self.df['jour_semaine'].values:
            if elt == 6 or elt == 7:
                week_end.append(1)
            else:
                week_end.append(0)
        self.df['week_end'] = week_end

    def create_delta(self):
        delta = []
        for i in range(len(self.df)):
            if i == 0 or i == 1:
                delta.append(0)
            else:
                delta.append(self.df['frequentation'].iloc[i-1] - self.df['frequentation'].iloc[i-2])
        self.df['delta_2_jours'] = delta

    def date(self):
        date = []
        for elt in self.df.index.get_level_values('date_commande').values:
             date.append(elt)
        self.df['date'] = date
    
    def clean_data(self):
        self.tri_type_vente()
        self.remove_columns()
        self.convert_date()
        self.group_by_date()
        self.prix_moyen()
        self.create_day_value()
        self.create_week_end()
        self.create_delta()
        self.date()
        self.add_jour()
        self.df = self.df.drop([self.df.index[904]])
        self.df = self.df.reset_index(drop=True)
        self.encode_jour()

    def join_stats(self):
        mini = []
        maxi = []
        moy = []
        stats = pd.read_csv('Data/stats.csv', header=0, index_col=0)
        for elt in self.df['jour_semaine'].values:
            for num,jour in listes_jour.items():
                if num == elt:
                    mini.append(stats.loc[jour].values[0])
                    maxi.append(stats.loc[jour].values[1])
                    moy.append(stats.loc[jour].values[2])
        self.df['min'] = mini
        self.df['max'] = maxi
        self.df['moy'] = moy

    def ecart_moy_vielle(self):
        ecarts = []
        for i in range(len(self.df['frequentation'])):
            if i == 0:
                ecarts.append(0)
            else:
                ecart = (self.df['frequentation'].iloc[i-1] - self.df['moy'].iloc[i-1]) / self.df['moy'].iloc[i-1]
                ecarts.append(ecart)
        self.df['ecart_moy_veille'] = ecarts

    def add_meteo(self):
        meteo = pd.read_csv('Data/meteo.csv', sep=';')
        meteo = meteo[['date_meteo','icon', 'temperaturehigh', 'temperaturelow', 'precipprobability']]
        meteo['date_meteo'] = pd.to_datetime(meteo['date_meteo'])
        self.df = self.df.merge(meteo, left_on='date', right_on='date_meteo')

    def add_vacances(self):
        vacances = pd.read_csv('Data/vacances.csv', sep=';')
        vacances = vacances[['date_vacances', 'zone_a', 'zone_b', 'zone_c']]
        vacances['date_vacances'] = pd.to_datetime(vacances['date_vacances'])
        self.df = self.df.merge(vacances, left_on='date', right_on='date_vacances')

    def add_freq_n1(self):
        freq_sem_dernier = []
        for i in range(len(self.df['frequentation'])):
            if i == 0 or i == 1 or i == 2 or i == 3 or i == 4 or i == 5 or i == 6:
                freq_sem_dernier.append(0)
            else:
                freq_sem_dernier.append(self.df['frequentation'].iloc[i - 7])
        self.df['freq_n1'] = freq_sem_dernier
        self.df = self.df.drop(self.df.index[:7])

    def add_freq_n2(self):
        freq_sem_dernier = []
        for i in range(len(self.df['frequentation'])):
            if i == 0 or i == 1 or i == 2 or i == 3 or i == 4 or i == 5 or i == 6:
                freq_sem_dernier.append(0)
            else:
                freq_sem_dernier.append(self.df['freq_n1'].iloc[i - 7])
        self.df['freq_n2'] = freq_sem_dernier
        self.df = self.df.drop(self.df.index[:7])

    def add_freq_n3(self):
        freq_sem_dernier = []
        for i in range(len(self.df['frequentation'])):
            if i == 0 or i == 1 or i == 2 or i == 3 or i == 4 or i == 5 or i == 6:
                freq_sem_dernier.append(0)
            else:
                freq_sem_dernier.append(self.df['freq_n2'].iloc[i - 7])
        self.df['freq_n3'] = freq_sem_dernier
        self.df = self.df.drop(self.df.index[:7])

    def add_freq_n4(self):
        freq_sem_dernier = []
        for i in range(len(self.df['frequentation'])):
            if i == 0 or i == 1 or i == 2 or i == 3 or i == 4 or i == 5 or i == 6:
                freq_sem_dernier.append(0)
            else:
                freq_sem_dernier.append(self.df['freq_n3'].iloc[i - 7])
        self.df['freq_n4'] = freq_sem_dernier
        self.df = self.df.drop(self.df.index[:7])

    def add_semaine_passe(self):
        self.add_freq_n1()
        self.add_freq_n2()
        self.add_freq_n3()
        self.add_freq_n4()

    def add_moy_mois(self):
        self.df['moy_mois'] = (self.df['freq_n1'] + self.df['freq_n2'] + self.df['freq_n3'] +
        self.df['freq_n4']) / 4

    def ecart_moy_n2(self):
        ecarts = []
        for i in range(len(self.df['frequentation'])):
            if i == 0 or i == 1:
                ecarts.append(0)
            else:
                ecart = (self.df['frequentation'].iloc[i-2] - self.df['moy'].iloc[i-2]) / self.df['moy'].iloc[i-2]
                ecarts.append(ecart)
        self.df['ecart_moy_n2'] = ecarts

    def ecart_moy_n3(self):
        ecarts = []
        for i in range(len(self.df['frequentation'])):
            if i == 0 or i == 1 or i == 2:
                ecarts.append(0)
            else:
                ecart = (self.df['frequentation'].iloc[i-3] - self.df['moy'].iloc[i-3]) / self.df['moy'].iloc[i-2]
                ecarts.append(ecart)
        self.df['ecart_moy_n3'] = ecarts

    def ecart_moy(self):
        self.ecart_moy_vielle()
        self.ecart_moy_n2()
        self.ecart_moy_n3()
        self.df = self.df.drop(self.df.index[:3])

    def add_jour(self):
        jours = []
        for elt in self.df['jour_semaine'].values:
            for num,jour in listes_jour.items():
                if elt == num:
                    jours.append(jour)

        self.df['jour'] = jours

    def encode_jour(self):
        encode = OneHotEncoder().fit_transform(self.df[['jour']]).todense()
        jour_encoder = pd.DataFrame(encode, columns=jours, dtype=int)
        self.df = self.df.join(jour_encoder)
        self.df = self.df.drop(columns=['jour', 'week_end', 'delta_2_jours', 'ca_ttc',
                    'prix_moyen'])




"""rep_jour = DataTrierReporting('Data/reporting_jour.csv')
rep_jour.clean_data()
rep_jour.join_stats()
rep_jour.ecart_moy()
#rep_jour.add_semaine_passe()
#rep_jour.add_moy_mois()
rep_jour.pred_arima()"""


