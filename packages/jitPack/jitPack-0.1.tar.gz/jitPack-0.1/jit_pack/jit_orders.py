import requests
import keyring
from jsonschema import validate, ValidationError


class JitOrders:


    def validate_order_data(self, data):
        """Validate the order data structure against the predefined schema."""

        # Define the schema
        order_schema = {
            'type': 'object',
            'properties': {
                'city': {'type': 'string'},
                'cashToCollect': {'type': 'number'},
                'cashToPay': {'type': 'number'},
                'items': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'item': {'type': 'string'},
                            'quantity': {'type': 'integer'}
                        },
                        'required': ['item', 'quantity']
                    }
                },
                'notes': {'type': 'string'},
                'source': {
                    'type': 'object',
                    'properties': {
                        'location': {
                            'type': 'object',
                            'properties': {
                                'latitude': {'type': 'number'},
                                'longitude': {'type': 'number'}
                            },
                            'required': ['latitude', 'longitude']
                        },
                        'name': {'type': 'string'},
                        'phone': {'type': 'string'},
                        'address': {'type': 'string'}
                    },
                    'required': ['location', 'name', 'phone', 'address']
                },
                'destination': {
                    'type': 'object',
                    'properties': {
                        'location': {
                            'type': 'object',
                            'properties': {
                                'latitude': {'type': 'number'},
                                'longitude': {'type': 'number'}
                            },
                            'required': ['latitude', 'longitude']
                        },
                        'address': {'type': 'string'},
                        'name': {'type': 'string'},
                        'phone': {'type': 'string'}
                    },
                    'required': ['location', 'address', 'name', 'phone']
                },
                'metadata': {'type': 'object',
                             'properties':{'priority': {'type': 'string'}, 'delivery_time': {'type': 'string'}}}
            },
            'required': [
                'city', 'cashToCollect', 'cashToPay', 'items',
                'notes', 'source', 'destination'
            ]
        }

        try:
            validate(instance=data, schema=order_schema)
            print("Validation passed. Data is valid.")
            return True
        except ValidationError as e:
            print(f"Validation error: {e.message}")
            return False


    def new_order(self, data):
        if self.validate_order_data(data=data):
            FUNCTION_URL = "https://europe-west1-test-fcdf2.cloudfunctions.net/new_order"
            ID_TOKEN = keyring.get_password('firebase-auth', 'id_token')
            
            headers = {
                'Authorization': f'Bearer {ID_TOKEN}',  # Add the Firebase ID token for auth
                'Content-Type': 'application/json',
            }
            try:
                response = requests.post(FUNCTION_URL, headers=headers, json={'data': data})

                if response.status_code == 200:
                    print(f"Function call successful. {response.json()}")
                    return response.json()
                else:
                # Raise an exception if the status code indicates an error
                    error_response = response.json()
                    print(error_response)
                    error_message = error_response.get('error', {}).get('message', 'Unknown error')
                    raise Exception(f"Error calling function: {error_response['error']['code']} - {error_message}")

            except requests.exceptions.RequestException as req_err:
                print(f"Request error: {req_err}")
                raise  # Re-raise the exception for the caller to handle

            except Exception as e:
                print(f"An error occurred: {str(e)}")
                raise  # Re-raise the exception for the caller to handle




