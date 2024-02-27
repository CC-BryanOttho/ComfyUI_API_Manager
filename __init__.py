from .api_request import APIRequestNode
from .image_post_node import PostImageToAPI
from .text_prompt_combiner_node import TextPromptCombinerNode

# Define the mappings for your custom nodes
NODE_CLASS_MAPPINGS = {
    "APIRequestNode": APIRequestNode,
    "PostImageToAPI": PostImageToAPI,
    "TextPromptCombinerNode": TextPromptCombinerNode,
}

# Define human-readable names for your nodes (optional)
NODE_DISPLAY_NAME_MAPPINGS = {
    "APIRequestNode": "API Request Node",
    "PostImageToAPI": "Image Post Node",
    "TextPromptCombinerNode": "Text Prompt Combiner Node",
}

# Export the mappings for use by ComfyUI
__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
