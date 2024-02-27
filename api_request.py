import datetime
import requests
import json

class APIRequestNode:
    """
    A custom node for making API requests and processing responses.

    Attributes and class methods are defined to match the framework's expectations,
    similar to the provided Example node structure.
    """
    @classmethod
    def INPUT_TYPES(cls):
        """
        Define input parameters for the APIRequestNode.
        """
        return {
            "required": {
                "api_url": ("STRING", {"default": ""}),
                "auth_url": ("STRING", {"default": ""}),
                "token_attribute_name": ("STRING", {"default": ""}),
                "auth_body_text": ("STRING", {"multiline": True}),
                "array_path": ("STRING", {"default": ""}),
                "iteration_index": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 9999,  # Adjust based on expected maximum array length
                    "step": 1,
                    "display": "number"  # Allow users to input or select the index number
                })
            }
        }

    RETURN_TYPES = ("JSON", "INT", "STRING")  # Output types: JSON response
    RETURN_NAMES = ("API_RESPONSE", "LENGTH", "API_KEY")
    FUNCTION = "execute"  # The entry-point method for this node
    CATEGORY = "API Manager"  # Category under which the node will appear in the UI

    def __init__(self):
        pass

    def authenticate(self, auth_url, auth_body, token_attribute_name):
        """
        Authenticate and retrieve a bearer token using the provided authentication URL and body.
        """
        try:
            response = requests.post(auth_url, json=auth_body)
            response.raise_for_status()
            token = response.json().get(token_attribute_name)
            print(f"APIRequestNode: Obtained token")
            return token
        except requests.exceptions.RequestException as e:
            print(f"APIRequestNode: Error obtaining bearer token - {e}")
            return None

    def execute(self, api_url, auth_url, token_attribute_name, auth_body_text, array_path, iteration_index):
        """
        The main logic for making an API request, processing the response,
        and potentially queuing image generation requests or other post-processing steps.
        """
        auth_body = None
        if auth_body_text:
            try:
                auth_body = json.loads("{" + auth_body_text + "}")
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON input: {e}")
                return None, None, None

        token = self.authenticate(auth_url, auth_body, token_attribute_name) if auth_url else None
        headers = {'Authorization': f'Bearer {token}'} if token else {}
        response_data, error = self.make_api_request(api_url, headers)

        if error:
            return {}, None, ""

        array_data = self.extract_array_data(response_data, array_path) if array_path else response_data
        selected_item = array_data[iteration_index] if isinstance(array_data, list) else array_data
        return selected_item, len(array_data), f'Bearer {token}'

    def make_api_request(self, api_url, headers, params={}):
        """
        Make the actual API request and return the response.
        """
        try:
            response = requests.get(api_url, headers=headers, params=params)
            response.raise_for_status()
            return response.json(), None
        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return None, e

    def extract_array_data(self, response_data, array_path):
        # Navigate through the JSON structure to extract the specified array
        target_data = response_data
        for key in array_path.split('.'):
            target_data = target_data.get(key, [])
        return target_data if isinstance(target_data, list) else []

NODE_CLASS_MAPPINGS = {
    "APIRequestNode": APIRequestNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "APIRequestNode": "API Request Node"
}
