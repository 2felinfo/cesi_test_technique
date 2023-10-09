# Covoiturage 
Ce projet permet de réaliser une récupération des données automatique, ainsi de générer des statistiques de covoiturages sur une Ville, dans notre cas la ville de Rouen.
## Table des matières
[Installation](#installation) \
[Utilisation](#utilisation)
# Installation
1. Cloner le répertoire: `git clone `https://github.com/2felinfo/cesi_test_technique.git`
2. Naviguer vers le dossier du projet: `cd` nom_projet
3. Installer les bibliothèques nécessaires:` pip install` -r requirements.txt"
## Utilisation
1.Ouvrir le terminal dans le dossier du projet. <br>
2.tapez la commande `python` main.py --url "votre chemin de données" --city "nom du ville " --center "coordonnées du centre du ville" <br>
**Exemple:** `python main.py --url "https://static.data.gouv.fr/resources/trajets-realises-en-covoiturage-registre-de-preuve-de-covoiturage/20230921-111347/2023-08.csv" --city "Rouen" --center "49.442120, 1.098870"`<br>
<br>
### Méthodes des classes
  | nom du méthode |utilisation | description |
|--- |--- |--- |
| load_data | varname=load_data() |  Cette méthode permet de charger les données  à partir d'un chemin URL elle retourne une variable de type DataFrame |
| generate_statistics| varname=generate_statistics(data) | Cette méthode sert à générer des statistiques du covoiturages sur une ville, telque le nombre totale de covoiturages, la distance moyenne parcourue par chaque véhicule, etc...Elle prend en argument un dataframe|
| generate_heatmap | generate_heatmap(data,center_location):|  Cette méthode permet de genérer une carte de chaleur à partie des coordonnées (latitude,longitude) <br> Paramètre **data**: les données recuperées de type DataFrame <br> Paramètre **center_location** : coordonées du centre du ville sous la forme d'une liste eg: [49.130,1.0123]|
| generate_figures | generate_figures ()|  Cette méthode permet de générer les diagrammes et histogrammes des colonnes  |
| calculer_Co2 | calculer_Co2( (data)|  Cette méthode calcul le taux de réduction de l'emission du dioxide de carbone en utilisant le covoiturage   |
