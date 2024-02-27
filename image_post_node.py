import json
import requests
from io import BytesIO
import numpy as np
from PIL import Image

class PostImageToAPI:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE", ),
                "api_url": ("STRING", {"default": ""}),
                "api_object_id": ("STRING", {"forceInput": True}),
                "api_key": ("STRING", {"forceInput": True})
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "post_images"
    CATEGORY = "API Manager"
    OUTPUT_NODE = True

    def post_images(self, images, api_url, api_object_id, api_key=""):
        api_url = api_url.replace("$id", api_object_id)
        headers = {'Authorization': api_key} if api_key else {}
        results = []

        for (batch_number, image_tensor) in enumerate(images):
            image_np = 255. * image_tensor.cpu().numpy()
            image = Image.fromarray(np.clip(image_np, 0, 255).astype(np.uint8))
            buffer = BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)

            # Specify file name and MIME type
            files = {'file': ('image.png', buffer, 'image/png')}

            response = requests.post(api_url, headers=headers, files=files)

            if response.status_code == 200:
                results.append(response.json())
            else:
                print(f"Error posting image {batch_number}: {response.text}")

            print(f"PostImageToAPI: Posted image to {api_url}\nResponse: {results}")
            return {"api_responses": results}
