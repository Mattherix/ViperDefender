from azure.eventgrid import EventGridPublisherClient, EventGridEvent
from azure.core.credentials import AzureKeyCredential

class Event:
    def __init__(self, topic_key, endpoint):
        self.topic_key = topic_key
        self.endpoint = endpoint

        self.credential = AzureKeyCredential(topic_key)
        self.client = EventGridPublisherClient(self.endpoint, self.credential)
    
    def results(self, id: str, suspicious: bool):
        data = {
                "id": id,
                "suspicious": suspicious
        }

        event = EventGridEvent(
            data=data,
            subject="Results",
            event_type="ViperDefense.Analyse.Result",
            data_version="1.0"
        )

        self.client.send(event)
        print("Result sent: ", data)
