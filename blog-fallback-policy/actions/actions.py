# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json

class ActionAgriFaq(Action):

    def name(self) -> Text:
        return "action_agri_faq"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # print(tracker.latest_message)
        
        # to get intent of user message
        _intent=tracker.latest_message['intent'].get('name')
        print("Intent of user message predicted by Rasa ",_intent)

        print(tracker.latest_message['text']) # to get user typed message 

        intent_found = json.dumps(tracker.latest_message['response_selector'][_intent]['ranking'][0]['intent_response_key'], indent=4)
        
        # confidence of retrieval intent we found
        retrieval_intent_confidence = tracker.latest_message['response_selector'][_intent]['response']['confidence']*100
        print(f"retrieval_intent_confidence we found was {retrieval_intent_confidence}")

        if retrieval_intent_confidence < 100:
            if "category-1" in _intent:
                print("Custom Fallback for category-1 can be implemented here")
                dispatcher.utter_message(text="Custom Fallback for category-1 can be implemented here")
            elif "category-2" in _intent:
                print("Custom Fallback for category-2 can be implemented here")
                dispatcher.utter_message(text="Custom Fallback for category-2 can be implemented here")
            return []
        #used eval to remove quotes around the string
        intent_found = f'utter_{eval(intent_found)}'
        print('after adding utter we found -- ', intent_found)
        dispatcher.utter_message(response = intent_found) # use response for defining intent name
        
        return [] # setting slot values