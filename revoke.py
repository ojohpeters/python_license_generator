import requests
import json

# Verify License
revoke_url = "http://enduranceudoh.pythonanywhere.com/revoke"
uname = input("Enter User to revoke")
revoke_data = {
    "username": uname,
}

headers = {
    'Content-Type': 'application/json'
}

response = requests.post(revoke_url, 
                        data=json.dumps(revoke_data),
                        headers=headers)

print("revoke Response:", response.json())
