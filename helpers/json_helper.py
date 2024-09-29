import json
import re

from clients.openai_client import call_openai
from utilities.prompts import json_validation_prompt


def convert_to_json(json_string: str) -> dict:
    result_dict = None
    i = 0
    while i < 3:
        try:
            # Remove any non-JSON data outside the first and last curly braces
            first_brace_index = json_string.find('{')
            last_brace_index = json_string.rfind('}')
            cleaned_json_string = json_string[first_brace_index:last_brace_index + 1]

            # Replace single quotes with double quotes to make it JSON-compatible
            cleaned_json_string = cleaned_json_string.replace("'", '"')

            # # Remove any extra commas before closing braces or brackets
            # cleaned_json_string = re.sub(r',(\s*[}\]])', r'\1', cleaned_json_string)
            #
            # # Escape problematic characters that are not JSON-friendly
            # cleaned_json_string = cleaned_json_string.replace('\n', '\\n')

            # Attempt to parse the cleaned JSON string
            result_dict = json.loads(cleaned_json_string)

            i = 5
        except Exception as err:
            print(err)
            json_string = call_openai(json_validation_prompt, {"json_data": json_string, 'error_message': str(err)})
            i += 1
    # if i >= 5:
    #     logger.info("All five iterations ran")
    # if result_dict is None:
    #     # st.error("Couldn't process the llm output, Please select other LLM model and try again")
    #     logger.info(f"process_output: couldn't process the llm output: {json_string}")
    return result_dict
