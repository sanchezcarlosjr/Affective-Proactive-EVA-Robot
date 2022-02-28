# contains methods for the assistant performance: ibm watson

import json

from ibm_watson import AssistantV2
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


'''
with open('./bbdd.json', 'r') as f:
  data = json.load(f)

USERNAME = data['username']
'''

# Assistant (TODO PROBAR A QUE COJA SOLO LO DE LAS APIKEY)
with open('../credentials/assistant_credentials.json') as json_file:
    auth_data = json.load(json_file)

session_id = ''
final_response = ''
assistant_id = auth_data['assistant_id']

assistant = AssistantV2(
    version='2021-06-14',
)

def createSession(assistant_id):
    try:
        response = assistant.create_session(
            assistant_id=assistant_id
        ).get_result()
        session = response['session_id']
    except Exception as e:
        print(('createSession Error: ' + str(e)))
    return session
    

session_id = createSession(assistant_id)


# Natural Language Understanding: Emotions 
nlu = NaturalLanguageUnderstandingV1(
    version='2021-08-01'
)
nluOptions = {
    'text': '',
    'features': {
        'emotion': {},
    },
    'language': "en"
}




def genResponse(data, context_data={}):
    global session_id

    if not data :
        return None

    try:
        response = assistant.message(
            assistant_id=assistant_id,
            session_id=session_id,
            input={
                'message_type': 'text',
                'text': data,
                'options': {
                    'return_context': True # For returning the context variables
                }
            },
            context={
                "skills": {
                    "main skill": {
                        "user_defined": context_data
                    }
                }
            }
        ).get_result()
        #print(response)

    except Exception as e:
        print('genResponse Error: ', str(e))
        session_id = createSession(assistant_id)
        response = assistant.message(
            assistant_id=assistant_id,
            session_id=session_id,
            input={
                'message_type': 'text',
                'text': data,
                'options': {
                    'return_context': True # For returning the context variables
                }
            },
            context={
                "skills": {
                    "main skill": {
                        "user_defined": context_data
                    }
                }
            }
        ).get_result()
    
    finally:
        final_response = '. '.join([resp['text'] for resp in response['output']['generic']])
        return final_response



def analyzeMood(text):
    nluOptions['text'] = text
    try:
        response = nlu.analyze(**nluOptions).get_result()
    except Exception as e:
        print('analyzeMood error: ', str(e))
    else:
        return response['emotion']['document']['emotion']
