"""
Definitions of all services in BioModels
"""
import os
from datetime import datetime
from joblib import Memory
import requests

from .constants import API_URL

"""
MODEL RELATED OPERATIONS
"""


# GET /{model_id}?format=json|xml
memory = Memory("~/.biomodels")
@memory.cache
def get_model_info(model_id, out_format="json"):
    response = requests.get(API_URL + "/" + model_id + "?format=" + out_format)
    if out_format == "xml":
        # todo: implement me
        output = None
    else:
        output = response.json()
    return output


# GET /model/files/{model_id}
memory = Memory("~/.biomodels")
@memory.cache
def get_model_files_info(model_id, out_format="json"):
    response = requests.get(API_URL + "/model/files/" + model_id + "?format=" + out_format)
    if out_format == "xml":
        # todo: implement me
        output = None
    else:
        output = response.json()
    return output


# GET /model/identifiers
memory = Memory("~/.biomodels")
@memory.cache
def get_model_identifiers(out_format="json"):
    response = requests.get(API_URL + "/model/identifiers?format=" + out_format)
    return response.json()


# GET /model/download/{model_id}
memory = Memory("~/.biomodels")
@memory.cache
def download(model_id, filename=None, local_file=None):
    download_url = API_URL + "/model/download/" + model_id
    if filename is not None:
        response = requests.get(download_url + "?filename=" + filename)
    else:
        response = requests.get(download_url)

    # Determine local file name, if not given
    if local_file is None:
        if filename is not None:
            local_file = filename
        else:
            # make up a name for the entire archive
            local_file = f"{model_id}.omex"
    else:
        local_file = model_id + ".omex"

    # Save the file data to the local file
    with open(local_file, 'wb') as file:
        file.write(response.content)

    return os.path.abspath(local_file)


"""
MODEL SEARCH OPERATIONS
"""


# GET /search
memory = Memory("~/.biomodels")
@memory.cache
def search(query="*:*", offset=0, num_results=10, sort="publication_year-desc", out_format="json"):
    search_url: str = API_URL + "/search?query=" + query + "&offset=" + str(offset)
    search_url += "&numResults=" + str(num_results) + "&sort=" + sort + "&format=" + out_format
    results = requests.get(search_url)
    return results.json()


# GET /search/download
memory = Memory("~/.biomodels")
@memory.cache
def download_bulk(model_ids, save_as_file=""):
    if model_ids is None:
        return None
    
    if save_as_file is None or save_as_file == "":
        dt = datetime.now().strftime("%Y%m%d-%H%M%S")
        save_as_file = f"biomodels-download-{dt}.zip"

    download_url: str = API_URL + "/search/download?models=" + model_ids
    headers = { 
        "Content-Type": "application/zip",
        "Content-disposition": f'attachment;filename="{save_as_file}"'
    }
    response = requests.get(download_url, headers=headers, stream=True, allow_redirects=True)
    # Save the file data to the local file
    with open(save_as_file, mode="wb") as file:
        for chunk in response.iter_content(chunk_size=10*1024):
            file.write(chunk)

    return os.path.abspath(save_as_file)


"""
PARAMETERS SEARCH
"""


# GET /parameterSearch/search
memory = Memory("~/.biomodels")
@memory.cache
def parameter_search(query="*:*", start=0, size=10, sort="model:ascending", out_format="json"):
    search_url: str = API_URL + "/parameterSearch/search?query=" + query + "&start=" + str(start)
    search_url += "&size=" + str(size) + "&sort=" + sort + "&format=" + out_format
    results = requests.get(search_url)
    return results.json()
