from request import request_nlu
from rasa_core import trackers 
from rasa_core.trackers import DialogueStateTracker
import rasa_core.events
from rasa_core.conversation import Dialogue

def get_last_utter_action(tracker):
    ##goes back through the list of events and finds
    ##the last utter_action
    for event in reversed(tracker.events):
        #print(event.get("event"))
        try:
            #print("current action name is", event.get('name'))
            if event.get('name') not in [ 'action_listen', 'ActionSNLU', None , 'action_default_fallback', 'repeat'] :
                last_utter_action = event.get('name')
                #print('found action', last_utter_action)
                return last_utter_action
            else :
                #print(event.get('name'))
                pass
        except:
            pass
            #print(event.get('text'))
    return 'error! no last action found'

def initialize(server_set_file_name, QAMapping_file_name):
    lines = open(server_set_file_name, 'r')
    server_set = {}
    for line in lines:
        data = line.replace('\n',"").split(',')
        #first element is the server name, second is the project directory
        #3rd is the port
        server_set[data[0]] = []
        server_set[data[0]].append({'project_dir': data[1]})
        server_set[data[0]].append({'port': data[2]})
       # print(server_set)
    
    lines = open(QAMapping_file_name, 'r')
    QAMapping = {}
    for line in lines:
        data = line.replace("\n", "").split(',')
        #first line is the question action
        #second line is the server to use
        QAMapping[data[0]] = data[1]
        #print(QAMapping)

    return server_set, QAMapping  

def snlu_api(text, tracker):

    server_set, QAMapping = initialize('snlu_set.txt', 'QAMapping.txt')
    
    #get previous utter_action
    utter_action = get_last_utter_action(tracker)
    #utter_action = 'utter_ask_first_name'
    #if it is in QA Mapping & server in serverset
    """ try: 
        print(QAMapping[utter_action])
        print(server_set[QAMapping[utter_action]][0]['project_dir'])
    except:
        print(utter_action) """
    
    try:
        project_dir = server_set[QAMapping[utter_action]][0]['project_dir']
        server_port = server_set[QAMapping[utter_action]][1]['port']
    except:
        try:
            pass
            # print(server_set[QAMapping[utter_action][0]])
        except:
            pass
        response = 'Error, action or server not found!'
    #  then invoke the request to appropriate port
    response = request_nlu(text, project_dir, server_port)
    return [ response, utter_action ]


if __name__ == '__main__':
    print(snlu_api('Yes'))