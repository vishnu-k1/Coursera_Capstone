import json
import requests
import csv


chennai_area = {
    "Vadapalani" : ['13.049713', '80.212555'],
    "TNagar": ['13.03416','80.23006'],
    "porur": ['13.03478','80.15586'],
    "valasaravakkam" : ['13.04394','80.17251'],
    "Guindy" : ['13.0084125','80.2126875']
}
data_file = open('data_file.csv', 'a')
hline=0
for key in chennai_area.keys():
 for i in range(0,120 , 20):
   print(chennai_area[key][0] + "," + chennai_area[key][1])
   url="https://developers.zomato.com/api/v2.1/search?entity_type=subzone&lat="+chennai_area[key][0]+"&lon="+chennai_area[key][1]+"&radius=50&sort=real_distance&order=desc&start="+str(i)+"&count=20"
   restaurants = requests.get(url, headers={"Accept":"application/json","user-key": "XX"}) # (your url)
   data = restaurants.json()
   with open('data'+str(i)+'.json', 'w') as f:
     json.dump(data, f)
   print(i)
   with open('data'+str(i)+'.json') as json_file:
     csv_data = json.load(json_file)
   data_points = csv_data['restaurants']
   header =['id','name','latitude','longitude','locality_verbose','cuisines','average_cost_for_two','price_range','aggregate_rating','votes','all_reviews_count','photo_count','establishment','establishment_types']
   csv_writer = csv.DictWriter(data_file,header)
   for res in data_points:
     if i==0 and hline == 0:
         csv_writer.writeheader()
         hline = 1
    # Writing data of CSV file

     csv_writer.writerow({'id': str(res['restaurant']['id']),
     'name': str(res['restaurant']['name']),
     'latitude': str(res['restaurant']['location']['latitude']),
     'longitude': str(res['restaurant']['location']['longitude']),
     'locality_verbose': str(res['restaurant']['location']['locality_verbose'].replace(",", "/")),
     'cuisines': str(res['restaurant']['cuisines'].replace(",", "/")),
     'average_cost_for_two': str(res['restaurant']['average_cost_for_two']),
     'price_range': str(res['restaurant']['price_range']),
     'aggregate_rating': str(res['restaurant']['user_rating']['aggregate_rating']),
     'votes': str(res['restaurant']['user_rating']['votes']),
     'all_reviews_count': str(res['restaurant']['all_reviews_count']),
     'photo_count': str(res['restaurant']['photo_count']),
     'establishment': str(res['restaurant']['establishment']).replace(",", "/").replace("[", "").replace("]", "").replace("'", ""),
     'establishment_types': str(res['restaurant']['establishment_types']).replace(",", "/").replace("[", "").replace("]", "").replace("'", "")})
   json_file.close()
data_file.close()

