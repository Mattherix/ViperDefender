import http.client
import json

def is_id_valid(id):
    # Id must exist, else an error is raised
    conn = http.client.HTTPSConnection("viperdefense.azurewebsites.net")
    conn.request("GET", f"/api/Session?id={id}")

    res = conn.getresponse()
    data = res.read()

    result = json.loads(data.decode("utf-8"))
    
    return not result['session_ended']
