import requests
import shutil

def upscale_image(image_path):
    try:
        r = requests.post(
            "https://api.deepai.org/api/torch-srgan",
            files={
                'image': open(image_path, 'rb'),
            },
            headers={'api-key': 'YOUR-API-KEY'}
        )
        response_data = r.json()
        output_url = response_data['output_url']

        # Download the upscaled image
        response = requests.get(output_url, stream=True)
        with open('upscaled_image.jpg', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)

        del response

        print("Image upscaled and saved as 'upscaled_image.jpg'.")
    except:
        print("An error occurred during the upscaling process.")

def main():
    image_path = 'image.jpg'  # Replace with your image path
    upscale_image(image_path)

if __name__ == '__main__':
    main()
