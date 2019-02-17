from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.events import UserUtteranceReverted
from snlu_api import snlu_api
from request import request_nlu
import json
from rasa_core.trackers import DialogueStateTracker
import rasa_core.events
from rasa_core.conversation import Dialogue

def get_entity_value():
    lines = open('entity_mapping.txt', 'r')
    entities = {}
    for line in lines:
        data = line.replace('\n',"").split(',')
        entities[data[0]] = data[1]
    return entities

def parse_nlu_output(data):
    spacy = False
    if data['intent']['name'] == 'inform'  and len(data['entities']) > 0  :
        for entity in data['entities'] :
            if entity['extractor'] == 'ner_spacy' :
                spacy = True
                spacy_value = entity['value']
            elif entity['extractor'] == 'ner_crf' :
                crf_value = entity['value']
                crf_confidence = entity['confidence']

        if spacy :
            return [ spacy_value, 0.0 ]
        else: 
            return [ crf_value, crf_confidence ]
            
    else:
	    return ["error.  data not recognized", 0.0]


class ActionSNLU(Action):
    def name(self):
        return "ActionSNLU"
    
    def run(self, dispatcher, tracker, domain):
        #get the latest user utterance and pass it
        #with the tracker for the Special NLU processing
        #print('invoked ActionSNLU')
        user_message = tracker.latest_message.get('text')
        #print('user message is ', user_message)
        """  for event in tracker.events:
            print(event.keys())
            print(event.get('event'))
            try:
                print(event.get('name'))
            except:
                print(event.get('text')) """
        nlu_output, utter_action = snlu_api(user_message, tracker)
        print(nlu_output)
        #get a dictionary of questions (utter_action) and answers (entity in the output)
        entities = get_entity_value()
        slot = entities[utter_action]
        ##now parse nlu_output to find out the entity
        entity_value, entity_confidence = parse_nlu_output(nlu_output)
        return [SlotSet(slot, entity_value)]

