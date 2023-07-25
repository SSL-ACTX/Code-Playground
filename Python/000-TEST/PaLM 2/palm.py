import requests

# API Key
api_key = "PALM_API_KEY"
# PALM2 URL
url = f"https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText?key={api_key}"

def use_palm():
    prompt = input("Prompt: ")

    temperature = 0.70
    max_output_tokens = 950

    # JSON data to send in the request
    data = {
        "prompt": {
            "text": prompt
        },
        "temperature": temperature,
        "maxOutputTokens": max_output_tokens
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Send the POST request to the API
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an exception for unsuccessful requests

        # Parse the response JSON
        response_data = response.json()
        # Get the 'output' field from the response_data
        output_text = response_data['candidates'][0]['output']
        if output_text:
            print(output_text)
        else:
            print("No 'output' field found in the response.")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

if __name__ == '__main__':
    use_palm()
