import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from model import *

def read_data(path):
    data = pd.read_csv(path, low_memory=False, sep=';')
    return data

def read_info(data):
    print(data.columns)
    print('len of data: ',len(data))
    print('shape of data:', data.shape)
    print(data.info())
    print(data.describe())
    print(data.head(5))

def clean_data_jour(data_jour):
    data_jour = data_jour[data_jour['type_vente'] == 'CA']
    data_jour = data_jour.drop(data_jour[(data_jour['frequentation'] == 0.0) & (data_jour['ca_ttc'] == 0.0)].index)
    return data_jour

def group_data_jour(data_jour):
    data_jour = data_jour[['frequentation', 'ca_ttc', 'date_commande','nb_commandes']]
    data_jour['date_commande'] = pd.to_datetime(data_jour['date_commande'])
    data_jour = data_jour.groupby(data_jour['date_commande']).sum()
    data_jour['prix_moyen'] = data_jour['ca_ttc'] / data_jour['frequentation']

    print(read_info(data_jour))
    print(data_jour)
    data_jour.to_csv('group_par_journee.csv')

    num_cols = ["frequentation", "ca_ttc", "nb_commandes"]
    sns.pairplot(data_jour[num_cols], height=2)
    # plt.savefig('beautiful.png', bbox_inches='tight')
    plt.figure("group par journee")
    plt.bar(data_jour.index[:21], data_jour['frequentation'][:21])
    #plt.savefig('semaine.png', bbox_inches='tight')

    plt.show()

def group_par_semaine(data_jour):
    data_jour = data_jour[['frequentation', 'ca_ttc', 'jour_semaine']]
    data_jour = data_jour.groupby(data_jour['jour_semaine']).sum()
    data_jour['prix_moyen'] = data_jour['ca_ttc'] / data_jour['frequentation']
    print(read_info(data_jour))
    print(data_jour)
    data_jour.to_csv('group_par_semaine.csv')

    plt.figure("jour semaine")
    plt.bar(data_jour.index, data_jour['frequentation'])
    #plt.savefig('journee.png', bbox_inches='tight')
    plt.show()


def group_par_midi_soir(data_jour):
    data_jour = data_jour[['frequentation', 'ca_ttc', 'midi_soir']]
    data_jour = data_jour.groupby(data_jour['midi_soir']).sum()
    data_jour['prix_moyen'] = data_jour['ca_ttc'] / data_jour['frequentation']
    print(read_info(data_jour))
    print(data_jour)
    data_jour.to_csv('group_par_midi_soir.csv')

    plt.figure("midi soir")
    plt.bar(data_jour.index, data_jour['frequentation'])
    #plt.savefig('midi_soir.png', bbox_inches='tight')
    plt.show()
