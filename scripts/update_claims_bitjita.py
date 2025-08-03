import requests
import json
import math
import time

limit = 100
all_claims = []
all_claims_with_buildings = []
current_page = 1
sleep_time = 0.25
claims_url = 'https://bitjita.com/api/claims/'
user_agent = {'User-agent': 'Manserk For bitcraftmap.com'}
claims_file = 'assets/markers/claims.geojson'

# Requesting the first page of the claim list
full_url = claims_url + '?limit=' + str(limit) + '&page=' + str(current_page)
print('Requesting ' + full_url)
data = requests.get(full_url, user_agent).json()
total_claims = int(data['count'])
total_pages = math.ceil(total_claims / limit)

print('There are ' + data['count'] + ' claims to request in a total of ' + str(total_pages) + ' pages')

# Collecting list of claim entityId from bitjita
for page in range(total_pages) :
    time.sleep(sleep_time)
    full_url = claims_url + '?limit=' + str(limit) + '&page=' + str(page+1)
    print('Requesting ' + full_url)
    data = requests.get(full_url, user_agent).json()
    all_claims.extend(data['claims'])


print(all_claims)
print(str(total_claims))
print(str(len(all_claims)))

# Checking if we got the right number of claims
if total_claims - len(all_claims) > 0:
    print('Total claims from initial count and requested count is not the same, terminating')
    exit(1)

# For each entityId, requesting the list of buildings
counter = total_claims
for claim in all_claims:
    time.sleep(sleep_time)
    counter -= 1
    buildings_endpoint = claims_url + str(claim['entityId']) + '/buildings'
    print('Requesting ' + buildings_endpoint + ' ' + str(counter) + ' left to do')
    claim['buildings'] = requests.get(buildings_endpoint, user_agent).json()
    all_claims_with_buildings.append(claim)
 
print('Counted ' + str(total_claims) + ' claims and there are ' + str(len(all_claims_with_buildings)) + ' total claims in the json file')

with open(claims_file, "w") as file:
    json.dump(all_claims_with_buildings, file)