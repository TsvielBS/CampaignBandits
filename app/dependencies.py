from typing import Dict
from fastapi import Depends, HTTPException
from app.models.bandit import Bandit

bandit_db: Dict[int, Bandit] = {}


def get_bandit(campaign_id: int, db: Dict[int, Bandit] = Depends(lambda: bandit_db)) -> Bandit:
    bandit = db.get(campaign_id)
    if not bandit:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return bandit
