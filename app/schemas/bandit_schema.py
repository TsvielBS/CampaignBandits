from typing import Dict, Union, List
from pydantic import BaseModel


class GetArmsResponse(BaseModel):
    campaign_id: int
    selected_arms: Dict[str, Dict[str, Union[float, str]]]


class AddArmsRequest(BaseModel):
    new_arms: List[str]


class AddArmsResponse(BaseModel):
    campaign_id: int
    new_arms_added: List[str]


class NewCampaignRequest(BaseModel):
    campaign_id: int
    explored_arms: List[str] = []
    unexplored_arms: List[str] = []


class NewCampaignResponse(BaseModel):
    campaign_id: int
