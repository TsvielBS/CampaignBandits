# Multi-Armed Bandit FastAPI Service

This repository contains a FastAPI microservice that implements a multi-armed bandit algorithm for different campaigns. The service allows you to:

1. **Get P arms**: Retrieve the top P arms for a given campaign using the Upper Confidence Bound (UCB) algorithm.
2. **Add new arms**: Add new arms to an existing campaign.
3. **Create a new campaign**: Initialize a new campaign with unexplored arms.
4. **Update a bandit**: Update the bandit model with new sentences and rewards for a given campaign.

## Installation

To install the necessary dependencies, run:

```bash
pip install -r requirements.txt
```

## Running the Service

To run the FastAPI service using Uvicorn, use the following command:

```bash
uvicorn app.main:app --reload
```

This will start the server on `http://127.0.0.1:8000`.

## API Endpoints

### 1. **Get Arms**

Retrieve the top P arms for a given campaign ID.

- **Endpoint**: `GET /api/v1/bandit/get-arms`
- **Parameters**:
    - `campaign_id` (int): The ID of the campaign.
    - `p` (int): The number of arms to retrieve.

**Response**:
```json
{
    "campaign_id": 1,
    "selected_arms": {
        "Arm1": {
            "predicted_reward": 0.5,
            "ucb_value": 1.2,
            "type": "Exploration"
        },
        ...
    }
}
```

### 2. **Add Arms**

Add new arms to an existing campaign.

- **Endpoint**: `POST /api/v1/bandit/add-arms`
- **Parameters**:
    - `campaign_id` (int): The ID of the campaign.
    - `new_arms` (list of str): The list of new arms to add.

**Response**:
```json
{
    "campaign_id": 1,
    "new_arms_added": ["NewArm1", "NewArm2"]
}
```

### 3. **Create New Campaign**

Initialize a new campaign with explored and unexplored arms.

- **Endpoint**: `POST /api/v1/bandit/new-campaign`
- **Request**:
    ```json
    {
        "campaign_id": 1,
        "unexplored_arms": ["UnexploredArm1"]
    }
    ```

**Response**:
```json
{
    "campaign_id": 1
}
```

### 4. **Update Bandit**

Update the bandit model with new sentences and rewards for a given campaign.

- **Endpoint**: `POST /api/v1/bandit/update-bandit`
- **Request**:
    ```json
    {
        "new_sentences_and_rewards": [
            ["Sentence1", 3.0],
            ["Sentence2", 4.0]
        ]
    }
    ```

**Response**:
```json
{
    "campaign_id": 1
}
```

## Testing

To run the tests, use:

```bash
pytest
```

This will execute the tests defined in the `tests` directory.