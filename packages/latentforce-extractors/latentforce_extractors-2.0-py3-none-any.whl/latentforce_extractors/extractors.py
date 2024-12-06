import requests 
import base64
from .config import EXTRACTORS_ENDPOINT, EXTRACTOR_OPTIONS

class Extractors :

    def __init__(self, api_key) : 
        self.backend_url = EXTRACTORS_ENDPOINT
        self.api_key = api_key

    def load_input_file(self, file_path) :

        with open(file_path, 'rb') as f :
            content = f.read()

        encoded_file = base64.b64encode(content).decode("utf-8")
        return encoded_file
    
    def __process_extractor(self, data) : 
        url = f"{self.backend_url}/api/extractors/dev/convert"
        payload = {
            "model_name": data["model_name"],  # Replace with a valid model name
            "inputs": data["inputs"]
        }
        auth_header = {"Authorization": f"Bearer {data['api_key']}"}

        try:
            response = requests.post(url, json=payload, headers=auth_header, timeout=120.0)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401 :
                raise PermissionError("Unauthorized!. Please verify you have a valid API Key. To generate a new API Key, visit https://extractors.ai")
            elif response.status_code == 422 : 
                raise ValueError("Incorrect API Format has been called.")
            elif response.status_code == 429 : 
                raise PermissionError("Too Many Requests! Please try again later!")
            else :
                raise ValueError("Something went wrong on the server side. Please try contacting the developers.")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Request failed: {str(e)}")

    def process(self, extractor_name, extractor_inputs) :
        if extractor_name is None : 
            raise ValueError("Missing Parameter: extractor_name")

        if extractor_inputs is None : 
            raise ValueError("Missing Parameter: extractor_inputs")
        
        if "input_file" not in extractor_inputs.keys() : 
            raise KeyError("Missing Key in extractor_inputs : input_file")
        
        if type(extractor_inputs["input_file"]) != str : 
            raise ValueError("The input_file format is invalid. Please use the load_input_file() function to process input_file")

        if extractor_name == EXTRACTOR_OPTIONS[0] :

            if "query" in extractor_inputs.keys() : 
                query =  extractor_inputs["query"]
            else : 
                query = {}
            input_dict = {
                "imageb" : extractor_inputs["input_file"], 
                "query" : query
            }

        elif extractor_name == EXTRACTOR_OPTIONS[1] : 
            if "query" in extractor_inputs.keys() : 
                query =  extractor_inputs["query"]
            else : 
                query = {}
            input_dict = {
                "pdf_b" : extractor_inputs["input_file"], 
                "query" : query
            }

        elif extractor_name == EXTRACTOR_OPTIONS[2] : 
            if "query" in extractor_inputs.keys() : 
                query =  extractor_inputs["query"]
            else : 
                query = {}
            input_dict = {
                "pdf_b" : extractor_inputs["input_file"], 
                "query" : query
            }

        elif extractor_name == EXTRACTOR_OPTIONS[3] : 
            if "query" in extractor_inputs.keys() : 
                query =  extractor_inputs["query"]
            else : 
                query = {}
            input_dict = {
                "imageb" : extractor_inputs["input_file"], 
                "query" : query
            }


        elif extractor_name == EXTRACTOR_OPTIONS[4] : 
            if "query" in extractor_inputs.keys() : 
                query =  extractor_inputs["query"]
            else : 
                query = {}
            input_dict = {
                "images" : extractor_inputs["input_file"], 
            }

        else : 
            raise RuntimeError("Unsupported Extractor Specified!")
        
        data = {
            "api_key" : self.api_key,
            "model_name" : extractor_name,
            "inputs" : input_dict
        }

        response = self.__process_extractor(data)
        return response
    
    def save(self, response, extractor_name, output_file_path = "output") : 
        if response is None :
            raise ValueError("Missing Parameter: response")
        
        if extractor_name is None :
            raise ValueError("Missing Parameter: extractor_name")

        if extractor_name == EXTRACTOR_OPTIONS[0] : 
            xl_file = response["xl_file"]
            csv_file = response["csv_file"]

            base64_string = xl_file.split(",")[1]
            decoded_data = base64.b64decode(base64_string)

            output = f"{output_file_path}.xlsx"
            with open(output, "wb") as file:
                file.write(decoded_data)

            base64_string = csv_file.split(",")[1]
            decoded_data = base64.b64decode(base64_string)
            output = f"{output_file_path}.csv"
            with open(output, "wb") as file:
                file.write(decoded_data)

            print(f"Response files saved at {output_file_path}")
            return 

        elif extractor_name == EXTRACTOR_OPTIONS[1] : 
            xl_file = response["xl_file"]
            csv_file = response["csv_file"]

            base64_string = xl_file.split(",")[1]
            decoded_data = base64.b64decode(base64_string)

            output = f"{output_file_path}.xlsx"
            with open(output, "wb") as file:
                file.write(decoded_data)

            base64_string = csv_file.split(",")[1]
            decoded_data = base64.b64decode(base64_string)
            output = f"{output_file_path}.csv"
            with open(output, "wb") as file:
                file.write(decoded_data)

            print(f"Response files saved at {output_file_path}")
            return

        elif extractor_name == EXTRACTOR_OPTIONS[4] : 
            doc_file = response["doc_file"]

            base64_string = doc_file.split(",")[1]
            decoded_data = base64.b64decode(base64_string)

            output = f"{output_file_path}.docx"
            with open(output, "wb") as file:
                file.write(decoded_data)

            print(f"Response files saved at {output_file_path}")
            return
        
        elif extractor_name == EXTRACTOR_OPTIONS[2] or extractor_name == EXTRACTOR_OPTIONS[3]:
            raise RuntimeError("Saving to output file not Possible for the specified Extractor")  

        else :
            raise RuntimeError("Unsupported Extractor Specified!")
