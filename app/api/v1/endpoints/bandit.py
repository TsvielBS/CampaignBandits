from typing import Dict
from fastapi import APIRouter, Depends, HTTPException
from app.models.bandit import Bandit, BanditReward
from app.schemas.bandit_schema import (
    GetArmsResponse,
    AddArmsRequest,
    AddArmsResponse,
    NewCampaignRequest,
    NewCampaignResponse
)
from app.dependencies import get_bandit, bandit_db
from app.core import storage

router = APIRouter()


@router.get("/get-arms", response_model=GetArmsResponse)
def get_arms(campaign_id: int, p: int, bandit: Bandit = Depends(get_bandit)):
    selected_arms = bandit.choose_arms_ucb(p)
    return GetArmsResponse(campaign_id=campaign_id, selected_arms=selected_arms)


@router.post("/add-arms", response_model=AddArmsResponse)
def add_arms(campaign_id: int, request: AddArmsRequest, bandit: Bandit = Depends(get_bandit)):
    bandit.update_unexplored(set(request.new_arms))
    storage.save_bandit(campaign_id, bandit)  # Save only the modified bandit
    return AddArmsResponse(campaign_id=campaign_id, new_arms_added=request.new_arms)


@router.post("/new-campaign", response_model=NewCampaignResponse)
def new_campaign(request: NewCampaignRequest):
    if request.campaign_id in bandit_db:
        raise HTTPException(status_code=400, detail="Campaign already exists")
    explored_arms = {arm: BanditReward(0) for arm in request.explored_arms}
    new_bandit = Bandit(explored_arms, set(request.unexplored_arms))
    bandit_db[request.campaign_id] = new_bandit
    storage.save_bandit(request.campaign_id, new_bandit)  # Save only the newly created bandit
    return NewCampaignResponse(campaign_id=request.campaign_id)
