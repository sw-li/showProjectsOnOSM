from geopy.geocoders import Nominatim
import pandas as pd
import folium
import time

def geocode_with_retry(geolocator, address, max_retries=3, delay=1):
    for _ in range(max_retries):
        try:
            location = geolocator.geocode(address)
            if location:
                return location
        except Exception as e:
            print("geopy was unable to convert this address: " + address)
            time.sleep(delay)
    return None


geoLocator = Nominatim(user_agent="sli")
# to use it, geolocator.geocode("adress")
# (location.latitude, location.longitude)
location = geoLocator.geocode("88 Rue Robespierre, Montreuil")
# print(location.latitude, location.longitude)
paris = folium.Map([48.866667,2.333333], zoom_start=10)

projects = pd.read_excel("./sources/projets.xlsx", header=0, sheet_name="Table")
projectsWithAdress = projects[projects["Affaires_Adresse"].apply(lambda add: type(add) is str) ]


for index, project in projectsWithAdress.iterrows():
    location = geocode_with_retry(geoLocator, str(project.Affaires_Adresse) + " " 
                                  + str(project["Adresse-Ville de l'affaire"]))
    
    color = "green" if project["Affaire active"] else "purple"
    if location:
        # print('get location : ' + str(location.latitude) + str(location.longitude))
        folium.Circle(location=[location.latitude, location.longitude], 
                     radius=200, 
                     color=color,
                     fillColor=color,
                     popup=project.Affaires_Code,
                     tooltip=project.Affaires_Nom,
                     fillOpacity=0.6).add_to(paris),
    
paris.save("./outputs/projects.html")