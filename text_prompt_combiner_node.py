class TextPromptCombinerNode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text_prompt_template": ("STRING", {"multiline": True}),
                "api_response": ("JSON", {"default": {}}),
                "id_field_name": ("STRING", {"default": ""}),
                "clip": ("CLIP", )
            },
        }

    RETURN_TYPES = ("CONDITIONING", "STRING")  # Combined Text Prompt, UUID, Auth Token
    RETURN_NAMES = ("CONDITIONING", "ID")
    FUNCTION = "execute"
    CATEGORY = "API Manager"

    def execute(self, text_prompt_template, api_response, id_field_name, clip):
        print("TextPromptCombinerNode: Starting to combine text prompt...")

        # Initialize the combined text prompt with the template
        combined_text_prompt = text_prompt_template

        if isinstance(api_response, dict):
            # Iterate through each key in the api_response
            for key, value in api_response.items():
                # Define the placeholder pattern with the $ prefix
                placeholder = f"${key}"
                # Replace each occurrence of the placeholder in the template with its corresponding value
                combined_text_prompt = combined_text_prompt.replace(placeholder, str(value))

        # Extract the ID using the id_field_name, if provided and api_response is a dict
        extracted_id = api_response.get(id_field_name, "") if isinstance(api_response, dict) else ""

        print(f"Combined Text Prompt: {combined_text_prompt}")
        print(f"Extracted ID: {extracted_id}")

        # Now encode the combined text using CLIP, similar to CLIPTextEncode class
        tokens = clip.tokenize(combined_text_prompt)
        cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)

        # Return the conditioning and the extracted ID
        return ([[cond, {"pooled_output": pooled}]], extracted_id)
