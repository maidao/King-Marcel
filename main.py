import matplotlib as plt
from data_clean import *


data_jour = read_data("reporting_jour.csv")
data_produits = read_data("reporting_produits.csv")
data_meteo = read_data("meteo.csv")
data_promotions = read_data("promotions.csv")
data_vacances = read_data("vacances.csv")

data_jour = clean_data_jour(data_jour)
data_jour.to_csv('data_jour_clean.csv')

group_data_jour(data_jour)
group_par_semaine(data_jour)
group_par_midi_soir(data_jour)


