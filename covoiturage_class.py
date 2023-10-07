import pandas as pd 
import numpy as np 
import os
import seaborn as sns 
import matplotlib.pyplot as plt 
import warnings
import folium
import folium.plugins as plugins
from folium.plugins import HeatMap
warnings.filterwarnings('ignore')
class Covoiturage(object):
    """
    Class pour automatiser la récuperation des données et faire des stastiques sur une ville."
    """
    def __init__(self,data_url,city):
        """
        paramètre data_url: le chemin pour le jeu de données
        paramètre city: eg: Rouen
        """
        self.data_url=data_url
        self.city=city
    def load_data(self):
        """
         cette methode permet de charger les données  à partir d'un chemin URL
         elle retourne une variable de type DataFrame
         """
        try:
            df = pd.read_csv(self.data_url,sep=';')
            df = df[(df["journey_start_town"] == self.city) & (df["journey_end_town"] == self.city)]
            return df
        except FileNotFoundError:
            print("Error: URL not found .")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
    def numToMonth(self,num):
        return {
            1:'Janvier',
            2:'Fevrier', 
            3:'Mars', 
            4:'Avril', 
            5:'Mai', 
            6:'Juin', 
            7:'Juillet', 
            8:'Aout', 
            9:'Septembre', 
            10:'Octobre', 
            11:'Novembre', 
            12:'Décembre', 
        }[num]
    def generate_statistics(self,data):
        print("Statistiques de covoiturage pour la ville de "+self.city+" :")
        print("Nombre total de covoiturage pour le mois de "+self.numToMonth(int(self.data_url[-5])) +" sur "+self.city +" :", data.shape[0])
        print('La distance moyenne parcourue pour chaque trajet est :',data['journey_distance'].mean()," mètres")
        print('La durée moyenne pour chaque trajet est :',data['journey_duration'].mean())
        print('La distance maximale parcourue par une véhicle :',data['journey_distance'].max()," mètres"," avec une durée de ",data['journey_duration'].max()," minutes")
    
    def generate_heatmap(self,newdata,center_location):
        """
        cette méthode permet de genérer une carte de chaleur à partie des coordonnées (latitude,longitude)
        paramètre newdata: les données recuperées de type DataFrame
        paramètre center_location : coordonées du centre du ville sous la forme d'une liste 
        eg: [49.130,1.0123]
        """

        newdata['Departure'] = newdata.apply(lambda x: (x.journey_start_lat, x.journey_start_lon), axis=1)
        newdata['Destination'] = newdata.apply(lambda x: (x.journey_end_lat, x.journey_end_lon), axis=1)
        positions=newdata[['Departure','Destination']].to_dict(orient='records')
        city_map = folium.Map(location=center_location, zoom_start=12)
        coordinates = [(offer['Departure'][0], offer['Departure'][1]) for offer in positions]
        coordinates += [(offer['Destination'][0], offer['Destination'][1]) for offer in positions]
        HeatMap(coordinates).add_to(city_map)
        city_map.save('covoiturage_heatmap.html')

        print("La carte de chaleur  sera ouverte dans votre navigateur par défaut.")
        
    def generate_animated_heatmap(self,data,center_location):
        data2=data
        data2['journey_start_date'] = data2['journey_start_date'].sort_values(ascending=True)

        data1 = []

        for _, d in data2.groupby('journey_start_date'):
            data1.append([[row['journey_start_lat'], row['journey_start_lon']] for _, row in d.iterrows()])
        city_animated_map = folium.Map(location=[49.442120, 1.098870], zoom_start=13, tiles='CartoDB positron')
        heatmap = plugins.HeatMapWithTime(data1, auto_play=True,
                             display_index=True,
                             gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 1: 'red'},
                             index = data2['journey_start_date'].drop_duplicates().tolist(),
                            )
        heatmap.add_to(city_animated_map)

        city_animated_map.save("animated_heatmap.html")
        city_animated_map
    def generate_figures(self,data):
        output_folder = 'output'
        os.makedirs(output_folder, exist_ok=True)
        plt.figure(figsize=(40,20))
        sns.countplot(data['journey_start_date'])
        plt.savefig(os.path.join(output_folder, 'Diagramme des dates de départ'))

        plt.figure(figsize=(50,20))
        sns.countplot(data['journey_start_time'])
        plt.savefig(os.path.join(output_folder, 'Diagramme des heures de départ'))
        plt.figure(figsize=(20,10))
        data['journey_start_lon'].hist(legend=True);
        plt.savefig(os.path.join(output_folder, 'histogramme des coordonnées longitude de départ'))
        plt.figure(figsize=(20,10))
        data['journey_start_lat'].hist(legend=True);
        plt.savefig(os.path.join(output_folder, 'histogramme des coordonnées latitude de départ'))
        plt.figure(figsize=(20,10))
        data['journey_end_lon'].hist(legend=True);
        plt.savefig(os.path.join(output_folder, 'histogramme des coordonnées longitude d\'arrivée '))
        plt.figure(figsize=(20,10))
        data['journey_end_lat'].hist(legend=True);
        plt.savefig(os.path.join(output_folder, 'histogramme des coordonnées latitude d\'arrivée'))
        plt.figure(figsize=(20,10))
        data['journey_distance'].hist(legend=True);
        plt.savefig(os.path.join(output_folder, 'histogramme des distances parcourues'))
        plt.figure(figsize=(20,10))
        data['journey_duration'].hist(legend=True);
        plt.savefig(os.path.join(output_folder, 'histogramme des durées du trajets'))




    





            

            