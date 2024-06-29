# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 17:29:10 2024

@author: User
"""

import pgeocode
import pandas as pd


food_bank = pd.read_excel('FOODBANK.xlsx')

zip_code = food_bank['Zip Code'].astype(str).to_list()

restaurant = pd.read_excel('restaurant.xlsx')

df = restaurant[restaurant['NAME'] == 'de Paradise']

print(df['ADDRESS'].values[0])

#nomi = pgeocode.Nominatim('in')

#result = nomi.query_postal_code(zip_code)

#result.to_excel('lat_long.xlsx')

#dist = pgeocode.GeoDistance('in')

#print(dist.query_postal_code("110018", "110075"))

