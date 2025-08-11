from typing import Dict, Any, Tuple
from web.services.api_client import api_client

def get_analysis_data(content: str | list) -> Dict[str, Any]:
    return api_client.request_data(
        endpoint="analyse/text/advanced", 
        data={'msg': content}
    )
