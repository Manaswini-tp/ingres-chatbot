from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import httpx

BACKEND_URL = "http://localhost:8000"

class ActionGetGroundwaterData(Action):
    def name(self) -> Text:
        return "action_get_groundwater_data"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        state = tracker.get_slot("state")
        district = tracker.get_slot("district")
        
        if state:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{BACKEND_URL}/stats/{state}")
                    stats = response.json()
                
                message = f"Groundwater data for {state}:\n"
                message += f"• Average Rainfall: {stats['avg_rainfall']:.2f} mm\n"
                message += f"• Average Extraction Stage: {stats['avg_extraction_stage']:.2f}%\n"
                message += f"• Total Districts: {stats['total_records']}"
                
                dispatcher.utter_message(text=message)
            except Exception as e:
                dispatcher.utter_message(text=f"Sorry, I couldn't fetch data for {state}. Please try another state.")
        else:
            dispatcher.utter_message(text="Please specify a state name.")
        
        return []

class ActionGetStateList(Action):
    def name(self) -> Text:
        return "action_get_state_list"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{BACKEND_URL}/states")
                states = response.json()
            
            message = f"I have groundwater data for {len(states)} states:\n"
            message += ", ".join(states[:10])
            if len(states) > 10:
                message += f" and {len(states) - 10} more..."
            
            dispatcher.utter_message(text=message)
        except Exception as e:
            dispatcher.utter_message(text="Sorry, I couldn't fetch the state list.")
        
        return []
