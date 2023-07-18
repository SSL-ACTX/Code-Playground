import requests
import replicate

client = replicate.Client(api_token='replicate_api_token')

options = {}

output = client.run(
    "xinntao/realesrgan:1b976a4d456ed9e4d1a846597b7614e79eadad3032e9124fa63859db0fd59b56",
    input={"img": open("input_file_location", "rb"), "scale": 4, "version": "Anime - anime6B", "tile": 0},
    options=options
)

url = output
response = requests.get(url)

with open("output.png", "wb") as f:
    f.write(response.content)
