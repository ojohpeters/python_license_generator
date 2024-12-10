import requests
import json

def test_license():
    # 1. First Generate a new license
    generate_url = "http://enduranceudoh.pythonanywhere.com/generate"
    generate_data = {
        "username": "0xb17",
        "duration_days": 365  # 1 year license
    }

    headers = {
        'Content-Type': 'application/json'
    }

    print("Generating license...")
    gen_response = requests.post(generate_url, 
                               data=json.dumps(generate_data),
                               headers=headers)
    
    print("Generate Response:", gen_response.json())

    # 2. Then Verify the license
    verify_url = "http://enduranceudoh.pythonanywhere.com/verify"
    verify_data = {
        "username": "0xb17",
        "license_key": "8A75-360F-EFA9-4C33"  # Your existing license key
    }

    print("\nVerifying license...")
    verify_response = requests.post(verify_url, 
                                  data=json.dumps(verify_data),
                                  headers=headers)
    
    print("Verify Response:", verify_response.json())

if __name__ == "__main__":
    test_license()
