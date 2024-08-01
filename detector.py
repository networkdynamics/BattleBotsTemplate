import json


def calculateDetections(sessionData):
    # todo logic
    value = {
        'users': [
            {
                'userId': sessionData['users'][0]['id'],
                'confidence': 50
            }
        ]
    }


    return json.dumps(value)