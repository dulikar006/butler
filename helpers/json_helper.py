import json

from clients.openai_client import call_openai
from utilities.prompts import json_validation_prompt


def convert_to_json(json_string: str) -> dict:
    result_dict = None
    i = 0
    while i < 3:
        try:
            # clean json string
            first_brace_index = json_string.find('{')
            last_brace_index = json_string.rfind('}')
            extracted_json = json_string[first_brace_index:last_brace_index + 1]
            extracted_json = extracted_json.replace("'", '"')
            result_dict = json.loads(extracted_json)
            i = 5
        except:
            json_string = call_openai(json_validation_prompt, {"json_data": json_string})
            i += 1
    # if i >= 5:
    #     logger.info("All five iterations ran")
    # if result_dict is None:
    #     # st.error("Couldn't process the llm output, Please select other LLM model and try again")
    #     logger.info(f"process_output: couldn't process the llm output: {json_string}")
    return result_dict
