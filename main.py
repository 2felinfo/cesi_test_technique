from covoiturage_class import Covoiturage
import argparse
import webbrowser
import sys
from calcul_Co2 import Calcul
parser = argparse.ArgumentParser()
parser.add_argument('--url', type=str, default="https://static.data.gouv.fr/resources/trajets-realises-en-covoiturage-registre-de-preuve-de-covoiturage/20230921-111347/2023-08.csv", help="URL du jeu de doonées")
parser.add_argument('--city', type=str, default="Rouen", help="Nom du Ville")
parser.add_argument('--center', type=list, default=[49.442120, 1.098870], help="coordonnées du centre du ville sous forme d'une liste")
args = parser.parse_args()
arg1 = args.url
arg2 = args.city
arg3 = args.center
cov=Covoiturage(data_url="C:\\Users\\Administrateur\\Downloads\\2023-01.csv",
                 city="Rouen")
data=cov.load_data()
cov.generate_statistics(data)
center_location=[49.442120, 1.098870]
cov.generate_heatmap(data,center_location)
cov.generate_animated_heatmap(data,center_location)
cov.generate_figures(data)
print("Les figures sont sauvgardées dans un dossier output ")
file_path = 'covoiturage_heatmap.html'

webbrowser.open_new_tab(file_path)
calcul=Calcul(data,10)
calcul.calculer_Co2(data)
