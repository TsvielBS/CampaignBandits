from fastapi.testclient import TestClient
from app.main import app, load_bandits
import pytest
import os
from app.core import storage
from app.models.bandit import Bandit, BanditReward

client = TestClient(app)


@pytest.fixture
def clean_bandits_dir():
    yield
    for file in os.listdir(storage.BANDITS_DIR):
        os.remove(os.path.join(storage.BANDITS_DIR, file))


@pytest.fixture
def example_campaign_id(clean_bandits_dir):
    return 1


def test_get_arms(example_campaign_id):
    bandit = Bandit({"Arm1": BanditReward(5)}, {"Arm2"})
    storage.save_bandit(example_campaign_id, bandit)
    load_bandits()
    response = client.get(f"/api/v1/bandit/get-arms?campaign_id={example_campaign_id}&p=2")
    assert response.status_code == 200
    result = response.json()
    assert result["campaign_id"] == example_campaign_id
    assert "selected_arms" in result
    assert len(result["selected_arms"]) == 2


def test_add_arms(example_campaign_id):
    bandit = Bandit({"Arm1": BanditReward(5)}, {"Arm2"})
    storage.save_bandit(example_campaign_id, bandit)
    load_bandits()
    new_arms = ["NewArm1", "NewArm2"]
    response = client.post(f"/api/v1/bandit/add-arms?campaign_id={example_campaign_id}", json={"new_arms": new_arms})
    assert response.status_code == 200
    result = response.json()
    assert result["campaign_id"] == example_campaign_id
    assert result["new_arms_added"] == new_arms


def test_new_campaign(clean_bandits_dir):
    campaign_id = 2
    unexplored_arms = ["UnexploredArm1", "UnexploredArm2"]
    response = client.post("/api/v1/bandit/new-campaign", json={
        "campaign_id": campaign_id,
        "unexplored_arms": unexplored_arms
    })
    assert response.status_code == 200
    result = response.json()
    assert result["campaign_id"] == campaign_id
    saved_bandit = storage.load_bandit(campaign_id)
    assert saved_bandit.explored_arms_rwds == {}


def test_update_bandit(example_campaign_id):
    bandit = Bandit({"Arm1": BanditReward(5)}, {"Arm2"})
    storage.save_bandit(example_campaign_id, bandit)
    load_bandits()
    new_sentences_and_rewards = [("NewSentence1", 3.0), ("NewSentence2", 4.0)]
    response = client.post(f"/api/v1/bandit/update-bandit?campaign_id={example_campaign_id}",
                           json={"new_sentences_and_rewards": new_sentences_and_rewards})
    assert response.status_code == 200
    result = response.json()
    assert result["campaign_id"] == example_campaign_id
    updated_bandit = storage.load_bandit(example_campaign_id)
    assert "NewSentence1" in updated_bandit.explored_arms
    assert updated_bandit.explored_arms["NewSentence1"].mean_reward == 3.0
    assert "NewSentence2" in updated_bandit.explored_arms
    assert updated_bandit.explored_arms["NewSentence2"].mean_reward == 4.0


def test_persistence_between_runs(clean_bandits_dir):
    bandit_db = {
        1: Bandit({"Arm1": BanditReward(5)}, {"Arm2"})
    }
    storage.save_bandit(1, bandit_db[1])
    loaded_bandit = storage.load_bandit(1)
    assert loaded_bandit.explored_arms_rwds == {"Arm1": 5}


def test_load_non_existent_bandit(clean_bandits_dir):
    assert storage.load_bandit(999) is None


def test_save_and_load_multiple_bandits(clean_bandits_dir):
    bandits = {
        1: Bandit({"Arm1": BanditReward(5)}, {"Arm2"}),
        2: Bandit({"ArmA": BanditReward(10)}, {"ArmB"})
    }
    for campaign_id, bandit in bandits.items():
        storage.save_bandit(campaign_id, bandit)

    load_bandits()

    for campaign_id, expected_bandit in bandits.items():
        loaded_bandit = storage.load_bandit(campaign_id)
        assert loaded_bandit.explored_arms_rwds == expected_bandit.explored_arms_rwds
