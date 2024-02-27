class JSONArrayIteratorNode:
    """
    A custom node for iterating through a JSON array and outputting specific objects
    based on a selection number provided via the node interface.
    """

    @classmethod
    def INPUT_TYPES(cls):
        """
        Define input parameters for the JSONArrayIteratorNode.
        """
        return {
            "required": {
                "json_array": ("JSON", {"default": "[]"}),
                "selection_number": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 9999,  # Adjust based on expected maximum array length
                    "step": 1,
                    "display": "number"  # Allow users to input or select the index number
                }),
            },
        }

    RETURN_TYPES = ("JSON",)  # Output type: the selected JSON object from the array
    FUNCTION = "iterate"  # The entry-point method for this node
    CATEGORY = "Data Processing"  # Category under which the node will appear in the UI

    def __init__(self):
        pass

    def iterate(self, json_array, selection_number):
        print(f"JSONArrayIteratorNode: Iterating with selection_number={selection_number}")
        print (f"JSONArrayIteratorNode: Iterating with json_array={json_array}")

        # Check if the selection number is within the bounds of the json_array
        if isinstance(json_array, list) and 0 <= selection_number < len(json_array):
            selected_object = json_array[selection_number]
        else:
            print(f"Selection number {selection_number} is out of bounds for the array length {len(json_array)}.")
            selected_object = {}  # Return an empty object or handle as needed

        return selected_object
