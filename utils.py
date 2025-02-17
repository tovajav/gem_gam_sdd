import copy
import requests
import base64
import math
import pandas as pd
import pydeck as pdk
from config import AGENT_PROMPT
from typing import Generator
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

INSTRUCT_MODELS = ['qwen-2.5-32b','deepseek-r1-distill-qwen-32b','deepseek-r1-distill-llama-70b','llama-3.3-70b-versatile','llama-3.1-8b-instant','mixtral-8x7b-32768','gemma2-9b-it']

sys_prompt = lambda x: {"role": "system", "content": x}

def custom_ceil(number):
    if number < 1000:
        return math.ceil(number / 50) * 50
    else:
        return math.ceil(number / 100) * 100

def get_points_collecte_from_url():
    url = 'https://data.metropolegrenoble.fr/d4c/api/records/1.0/search/dataset=points_de_collecte_et_de_traitement_des_dechets_et_points_d_ap&rows=2000&facet=secteur'
    response = requests.get(url)
    data = response.json()
    df = pd.json_normalize(data['records'])
    columns = ['fields.id','fields.type_conteneur','fields.geo_point_2d','fields.secteur','fields.commune','fields.adresse','fields.type_dechet']
    df_geo = df[columns]
    df_geo.columns = df_geo.columns.str.replace('fields.', '')
    df_geo.insert(1, 'nom', df_geo['type_dechet'] + ' ' + df_geo['type_conteneur'])
    df_geo = df_geo.drop(columns=['type_conteneur'])
    df_geo['horaires_ouverture'] = '24h'
    df_geo['jours_ouverture'] = 'tous les jours'
    df_geo['types_materiaux'] = df_geo['type_dechet']
    return df_geo

def get_decheteries_from_url():
    url = 'https://data.metropolegrenoble.fr/d4c/api/records/1.0/search/dataset=decheteries_du_territoire_metropolitain&rows=2000&facet=secteur'
    response = requests.get(url)
    data = response.json()
    df = pd.json_normalize(data['records'])
    columns = ['fields.id','fields.nom','fields.geo_point_2d','fields.groupement','fields.commune','fields.adresse','fields.horaires_ouverture','fields.jours_ouverture','fields.types_materiaux']
    df_geo = df[columns].fillna('Inconnu')
    df_geo.columns = df_geo.columns.str.replace('fields.', '')
    df_geo.insert(6, 'type_dechet', 'déchèterie')
    return df_geo

def get_address_geolocation(address):
    """
    Get the geolocation (latitude and longitude) of a given address.

    Args:
        address (str): The address to geocode.

    Returns:
        tuple: A tuple containing the latitude and longitude of the address.
    """
    geolocator = Nominatim(user_agent='gam')
    location = geolocator.geocode(query=address, country_codes='fr')
    return (location.latitude, location.longitude)

def find_nearest_dechet(df, address, type_dechet):
    """
    Find the nearest waste collection point of a specified type.

    Args:
        df (pandas.DataFrame): DataFrame containing waste collection points with columns 'type_dechet', 'x_longitude', and 'y_latitude'.
        address (str): The address to geocode using function get_address_geolocation().
        type_dechet (str): The type of waste to filter the collection points.

    Returns:
        pandas.Series: The record of the nearest waste collection point.
    """
    try:
        df_filtered = df[df['type_dechet'] == type_dechet]                     # Filter the dataframe by type_dechet
        coordinate = get_address_geolocation(address)                          # Get address coordinates
        distances = df_filtered['geo_point_2d'].apply(lambda x: tuple(map(float, x.split(','))))
        distances = distances.apply(lambda x: geodesic(coordinate, x).meters)  # Calculate distances
        nearest_index = distances.idxmin()                                     # Find the index of the smallest distance
        target_location = df.loc[nearest_index].to_dict()                      # Return the record with the smallest distance
        target_location['distance'] = int(distances.min())                     # Add estimate distance
        target_location['user'] = coordinate
        return target_location
    except Exception as e:
        None

def get_bin_location(street, zipcode, type_dechet, df):
    """
    Get the location of the nearest waste bin from user provided address.

    This function finds the nearest waste bin location of the specified type and returns the chat completion response and the nearest location.
    Args:
        street (str): A string containing the number and street name of the address to geocode.
        zipcode (str): A string containing the zip code of the address to geocode.
        type_dechet (str): The type of waste to filter the collection points.
    Returns:
        tuple: A tuple containing the message prompt and the nearest waste bin location.
    """
    address = f'{street} {zipcode}'
    nearest_location = find_nearest_dechet(df, address, type_dechet)
    if nearest_location is not None:
        nearest_bin = copy.deepcopy(nearest_location)
        del nearest_bin['id'], nearest_bin['geo_point_2d'], nearest_bin['secteur'], nearest_bin['commune'], nearest_bin['distance'], nearest_bin['user']
        message = [sys_prompt(AGENT_PROMPT.format(
            address=address, 
            nearest_bin=nearest_bin,
            distance=custom_ceil(nearest_location['distance'])
        ))]
        return (message, nearest_location)
    else:
        error_prompt = 'You are Super Camille working at Grenoble Alpes Metropole. Provide a short and polite response that you were unable to get the bin location with user provided address.'
        return ([sys_prompt(error_prompt)], None)

def gen_gmaps_url(user_location, bin_location):
    if not isinstance(bin_location, tuple):
        bin_location = tuple(map(float, bin_location.split(',')))
    user_lat, user_long = user_location[0], user_location[1]
    bin_lat, bin_long = bin_location[0], bin_location[1]
    return f'https://www.google.com/maps/dir/{user_lat},{user_long}/{bin_lat},{bin_long}'

def encode_image(image_bytes):
    '''
    Function to encode the image
    '''
    return base64.b64encode(image_bytes).decode('utf-8')