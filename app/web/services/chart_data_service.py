from typing import Dict, Any, Tuple
from web.services.api_client import api_client

def get_entities_categories_data(period: dict) -> Dict[str, Any]:
    return api_client.request_data(
        endpoint="graph/categories_organizations", 
        data={
            'start': period['start'].isoformat(), 
            'end': period['end'].isoformat()
        }
    )

def get_categories_time_data(period: dict, interval: str) -> Dict[str, Any]:
    return api_client.request_data(
        endpoint="graph/stack_bar_time_categories", 
        data={
            'start': period['start'].isoformat(), 
            'end': period['end'].isoformat(),
            'interval': interval
        }
    )

def get_categories_data(period: dict) -> Dict[str, Any]:
    return api_client.request_data(
        endpoint="graph/msg_categories", 
        data={
            'start': period['start'].isoformat(), 
            'end': period['end'].isoformat()
        }
    )

def get_smishing_text_data(period: dict) -> Dict[str, Any]:
    return api_client.request_data(
        endpoint="graph/smishing_messages", 
        data={
            'start': period['start'].isoformat(), 
            'end': period['end'].isoformat()
        }
    )
