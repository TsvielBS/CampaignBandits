import os
import pickle
from typing import Dict, Optional
from app.models.bandit import Bandit

# Directory where bandits will be saved
BANDITS_DIR = "bandits_storage"

if not os.path.exists(BANDITS_DIR):
    os.makedirs(BANDITS_DIR)


def save_bandit(campaign_id: int, bandit: Bandit):
    file_path = os.path.join(BANDITS_DIR, f"{campaign_id}.pkl")
    with open(file_path, "wb") as f:
        pickle.dump(bandit, f)


def load_bandit(campaign_id: int) -> Optional[Bandit]:
    file_path = os.path.join(BANDITS_DIR, f"{campaign_id}.pkl")
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return pickle.load(f)
    return None


def load_all_bandits() -> Dict[int, Bandit]:
    bandits = {}
    for filename in os.listdir(BANDITS_DIR):
        if filename.endswith(".pkl"):
            campaign_id = int(filename[:-4])
            bandits[campaign_id] = load_bandit(campaign_id)
    return bandits
