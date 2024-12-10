import requests
import json

# Generate License
generate_url = "http://enduranceudoh.pythonanywhere.com/generate"
username = input("Username: ")
generate_data = {
    "username": username,
    "duration_days": 10  # optional, defaults to 30 if not specified
}

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(generate_url, 
                        data=json.dumps(generate_data),
                        headers=headers)

print("Generate Response:", response.json())
