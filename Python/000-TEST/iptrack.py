import json
import requests
import telebot

API_KEY = "IPGEOLOCATION_API"

bot = telebot.TeleBot("TG_API")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to IP Geolocation Bot! Please enter the IP address or use the '/getmine' command.")

@bot.message_handler(commands=['getmine'])
def get_mine_handler(message):
    params = {
        "apiKey": API_KEY,
        "lang": "en"
    }

    response = requests.get("https://api.ipgeolocation.io/ipgeo", params=params)
    json_data = response.json()

    result = f"IP Geolocation Result for the User:\n\n"
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

    bot.reply_to(message, result)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    input_ip = message.text
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

    bot.reply_to(message, result)

bot.polling()

