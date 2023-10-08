import joblib as jb
from tqdm.auto import trange
from datetime import datetime
import pandas as pd
class Calcul(object):

    def __init__(self,data,T):
        self.data=data
        self.T=T
    @staticmethod
    def align_time(t,T):
        # ce code permet de faire l'alignement des heures de départ
        if round(t.minute % T / T) == 1: t += pd.Timedelta(minutes = T)
        t += pd.Timedelta(minutes = -t.minute % T, seconds = -t.second)
        return t
    def string_to_date(self,stringdate):
        date_string_t=stringdate[:10]+" "+stringdate[11:19]
        date_format = "%Y-%m-%d %H:%M:%S"
        datetime_obj = datetime.strptime(date_string_t, date_format)
        return datetime_obj
    
    def covoiturage(self,df, T=10):
    
        # création d'une copie du dataset
        df=df.copy()
    
        #faire le regroupement des date et heures de départ
        df.insert(loc=0, column="pool_pickup_datetime", value=jb.Parallel(n_jobs=-1)(jb.delayed(self.align_time)(df.journey_start_datetime.iloc[i], T=T) for i in trange(df.shape[0], desc="Align timestamps")))


        df_group = df.groupby(["pool_pickup_datetime", "Departure", "Destination"])
        df = df_group.agg(journey_duration=pd.NamedAgg(column="journey_duration", aggfunc=lambda t: t.values.mean()), journey_distance = pd.NamedAgg(column="journey_distance", aggfunc="mean"), passenger_count = pd.NamedAgg(column="passenger_seats", aggfunc="sum"), CO2_grams = pd.NamedAgg(column="CO2_grams", aggfunc="max")).reset_index()
        df.insert(loc=0, column="pool", value=[list(x) for x in df_group.groups.values()])

        return df
    
    def calculer_Co2(self,df):
        temp_data=df # on crée un copie du données originales
        temp_data["CO2_grams"] = temp_data.journey_distance * (251.186 /1000) # car la distance dans notre base est en mètre
        temp_data['Departure'] = temp_data.apply(lambda x: (x.journey_start_lat, x.journey_start_lon), axis=1)
        temp_data['Destination'] = temp_data.apply(lambda x: (x.journey_end_lat, x.journey_end_lon), axis=1)
        temp_data['journey_start_datetime']=temp_data['journey_start_datetime'].apply(self.string_to_date)
        df_pool = self.covoiturage(temp_data,self.T)
        CO2 = temp_data.CO2_grams.sum()/1e+3
        CO2_pool = df_pool.CO2_grams.sum()/1e+3

        print("CO2 produit avant: \t{:.0f} KG".format(CO2))
        print("CO2 produit aprés le partage des véhicules : \t{:.0f} KG ({:.0%})".format(CO2_pool, (CO2_pool - CO2)/CO2))
      