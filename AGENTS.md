# Poke & Opencode Integration

This repository provides a standardized way for external agents, such as Opencode, to send notifications and data to Poke via the Inbound Webhook API.

## API Endpoint

The integration utilizes the following endpoint:

`POST https://poke.com/api/v1/inbound-sms/webhook`

## Setup

### 1. Obtain API Key
Ensure you have a valid API Key from your Poke dashboard.

### 2. Configure Environment
Store your API key securely. It is recommended to use an environment variable:

```bash
export POKE_API_KEY='your_bearer_token_here'
```

## Request Specification

### Headers
| Header | Value |
| :--- | :--- |
| `Authorization` | `Bearer <YOUR_API_KEY>` |
| `Content-Type` | `application/json` |

### Payload Schema
The request body must be a JSON object containing a `message` field.

```json
{
  "message": "The notification text to be sent."
}
```

## Usage for Agents

Other agents (like Opencode) can execute the provided `send_poke.py` script or implement the POST request directly following the schema above.

### Python Example
```bash
python send_poke.py "Deployment successful for project 'alpha'"
```

## Error Handling
The script includes basic error handling for network issues and non-200 HTTP response codes. When implementing this in other environments, ensure that you handle `401 Unauthorized` (invalid token) and `400 Bad Request` (invalid payload) errors appropriately.
