import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import requests
import os

# Function to get basic phone number information
def get_basic_info(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number)
        if not phonenumbers.is_valid_number(parsed_number):
            return {'error': 'Invalid phone number'}
        
        location = geocoder.description_for_number(parsed_number, 'en')
        phone_carrier = carrier.name_for_number(parsed_number, 'en')
        time_zones = timezone.time_zones_for_number(parsed_number)

        return {
            'Number': phone_number,
            'Location': location,
            'Carrier': phone_carrier,
            'Time Zones': time_zones
        }
    except phonenumbers.phonenumberutil.NumberParseException as e:
        return {'error': str(e)}

# Function to get additional information using external API
def get_additional_info(phone_number):
    api_key = os.getenv('NUMVERIFY_API_KEY')
    url = f'http://apilayer.net/api/validate?access_key={api_key}&number={phone_number}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if not data.get('valid', False):
            return {'error': 'Invalid phone number according to external API'}
        return data
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

if __name__ == "__main__":
    phone_number = input("Enter the phone number (with country code): ")
    
    # Get basic phone number info
    basic_info = get_basic_info(phone_number)
    if 'error' in basic_info:
        print(f"Error: {basic_info['error']}")
    else:
        print("Basic Info:")
        for key, value in basic_info.items():
            print(f"{key}: {value}")
    
    # Get additional phone number info
    additional_info = get_additional_info(phone_number)
    if 'error' in additional_info:
        print(f"Error: {additional_info['error']}")
    else:
        print("Additional Info:")
        for key, value in additional_info.items():
            print(f"{key}: {value}")
