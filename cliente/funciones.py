import base64

import requests


PAYPAL_CLIENT_ID = 'AY8FyPJKMUNIbciGoGlOvac7sAGn3JPer7M74lFjV57W6iDvjfI5tSoWWOiSvJ1G_rDjMag-V6lbH_Lp'
PAYPAL_CLIENT_SECRET = 'EIhM8RtIS2q5KBvc4ToqoqeG9Mktz6A5UCuJedARtuXNU_vNJtzLwCex94144Y1BUfdZON6Q6elj9JUJ'
BASE_URL = "https://api-m.sandbox.paypal.com"

def generateAccessToken():
    if not PAYPAL_CLIENT_ID or not PAYPAL_CLIENT_SECRET:
        raise ValueError('no se hay credenciales')
    
    auth = f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}"
    auth = base64.b64encode(auth.encode()).decode('utf-8')
    
    respose = requests.post(
        "https://api-m.sandbox.paypal.com/v1/oauth2/token",
        data={"grant_type": "client_credentials"},
        headers={"Authorization": f"Basic {auth}"}
    )
    data = respose.json()
    return data['access_token']


def create_order(productos):
    print(productos)
    
    try:
        accsess_token = generateAccessToken()
        url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
        subtotal = productos[-1]            
        for k, v in subtotal.items():
            print(v)
            payload = {
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": "USD",
                            "value": str(v)
                        }
                    }
                ]
            }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {accsess_token}"
        }
        
        response = requests.post(url, headers=headers, json=payload)
        # Obtener la respuesta JSON
        response_json = response.json()
        
        # Agregar el carrito a la respuesta
        response_json['cart'] = productos
        print('--- response ---', response_json)
        return response_json
    except Exception as error:
        print('*****')
        print(error)


def capture_order(orderID):
    access_token = generateAccessToken()
    url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{orderID}/capture"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    
    response = requests.post(url, headers=headers)
    
    return response.json()