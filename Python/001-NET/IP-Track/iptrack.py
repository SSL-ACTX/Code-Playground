import os
import json
import requests

API_KEY = "your_api_key"


def get_ip_geolocation(input_ip):
    params = {
        "apiKey": API_KEY,
        "ip": input_ip,
        "lang": "en"
    }

    response = requests.get("https://api.ipgeolocation.io/ipgeo", params=params)
    json_data = response.json()

    result = f"IP Geolocation Result for {input_ip}:\n\n"
    result += f"Country: {json_data['country_name']}\n"
    result += f"Continent: {json_data['continent_name']}\n"
    result += f"Region: {json_data['state_prov']}\n"
    result += f"City: {json_data['city']}\n"
    result += f"District: {json_data['district']}\n"
    result += f"ZIP Code: {json_data['zipcode']}\n"
    result += f"Latitude: {json_data['latitude']}\n"
    result += f"Longitude: {json_data['longitude']}\n"
    result += f"Time Zone: {json_data['time_zone']['name']}\n"
    result += f"Currency: {json_data['currency']['name']} ({json_data['currency']['symbol']})\n"
    result += f"ISP: {json_data['isp']}\n"
    result += f"Organization: {json_data['organization']}\n"
    result += f"Calling Code: {json_data['calling_code']}\n"
    result += f"Geoname ID: {json_data['geoname_id']}\n"
    result += f"Connection Type: {json_data['connection_type']}\n"
    result += f"Languages: {json_data['languages']}\n"
    result += f"Flag: {json_data['country_flag']}\n"

    return result

# Usage example:
input_ip = input("Enter the IP address: ")
result = get_ip_geolocation(input_ip)
print(result)
