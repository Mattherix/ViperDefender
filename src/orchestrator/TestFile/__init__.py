import logging
import json
import requests
import azure.functions as func
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    # get file from request
    # file = req.files['file']
    file = req.files.get('file')
    # if file is not found, return error
    if not file:
        return func.HttpResponse(
             "Please pass a file in the request",
             status_code=400
        )
    # get file name
    filename = file.filename
    # get file content
    filecontent = file.stream.read()
    # fetch the virustotal API to test the file
    
    url = "https://www.virustotal.com/api/v3/files"

    api_key = os.environ["VIRUSTOTAL_API_KEY"]
    headers = {
        "accept": "application/json",
        "x-apikey": api_key
    }

    files = {
        "file": (filename, filecontent)
    }

    response = requests.post(url, headers=headers, files=files)
    response_json = response.json()

    # check the analysis status
    analysis_url = f"https://www.virustotal.com/api/v3/analyses/{response_json['data']['id']}"

    
    analysis_response = requests.get(
        analysis_url,
        headers=headers
    )
    analysis_response_json = analysis_response.json()

    # return the filename and the verification status in a dictionary
    analysis_response_stats = analysis_response_json["data"]["attributes"]["stats"]
    suspicious = analysis_response_stats["suspicious"] + analysis_response_stats["malicious"]
    

    body = {
        "filename": filename,
        "status": "malicious" if suspicious > 0 else "clean"
    }

    return func.HttpResponse(
        json.dumps(body),
        mimetype="application/json",
        status_code=200
    )



