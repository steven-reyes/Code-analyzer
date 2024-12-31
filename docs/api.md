# API Documentation

## 1. Introduction

The **Code Analyzer API** allows external clients to interact programmatically with the application for analysis, reporting, and real-time suggestions. It supports:

- Submitting project paths or repository URLs for analysis.
- Retrieving detailed analysis results.
- Interacting with ChatGPT for real-time suggestions.

---

## 2. Base URL

### Localhost:
If running locally:
```
http://localhost:5000
```

### Docker:
If using Docker Compose:
```
http://localhost:5000
```

Make sure to adjust the port as per your `docker-compose.yml` configuration if necessary.

---

## 3. Endpoints

### 3.1 `POST /analyze`
**Description**: Initiates an analysis on a given project path or GitHub repository.

#### Request:

**Local Project:**
```json
{
  "project_path": "/path/to/local/project"
}
```

**GitHub Repository:**
```json
{
  "github_url": "https://github.com/username/repo"
}
```

#### Response (200 OK):
```json
{
  "file_structure": {...},
  "requirements": {...},
  "docker_setup": {...},
  "ml_workflow": {...},
  "incomplete_logic": {...},
  "env_file": {...},
  "security": {...},
  "duplicates": {...},
  "logging_monitoring": {...},
  "testing": {...}
}
```

---

### 3.2 `POST /chat`
**Description**: Interacts with ChatGPT to provide suggestions or file edits based on user input.

#### Request:
```json
{
  "message": "What can you tell me about improving code structure?"
}
```

Optional Context:
```json
{
  "message": "How do I fix missing logic in main.py?",
  "context": "You are ChatGPT. Provide code suggestions."
}
```

#### Response (200 OK):
```json
{
  "response": "ChatGPT-01 suggests using a 'try-except' block for better error handling."
}
```

---

### 3.3 `GET /status`
**Description**: Checks if the server is running and returns basic status information.

#### Response (200 OK):
```json
{
  "status": "running",
  "version": "1.0.0"
}
```

---

## 4. Authentication (Optional)

You can enhance security by requiring an API key for all requests. Add the following to your `.env` file:
```
API_KEY=your_api_key
```

Then include the `x-api-key` header in your requests:
```json
{
  "headers": {
    "x-api-key": "your_api_key"
  }
}
```

---

## 5. Error Responses

| Status Code | Meaning                         | Example Message                 |
|-------------|---------------------------------|----------------------------------|
| 400         | Bad Request                    | "Invalid project path."         |
| 401         | Unauthorized                   | "Missing or invalid API key."   |
| 500         | Internal Server Error          | "Unexpected error during scan." |

---

## 6. Example Workflows

### Analyze a Local Project:
Send a `POST /analyze` request:
```json
{
  "project_path": "/home/user/my_project"
}
```

### Analyze a GitHub Repository:
Send a `POST /analyze` request:
```json
{
  "github_url": "https://github.com/username/repo"
}
```

### Interact with ChatGPT:
Send a `POST /chat` request:
```json
{
  "message": "How do I improve Dockerfile security?"
}
```

### Check Server Status:
Send a `GET /status` request:
```bash
curl -X GET http://localhost:5000/status
```

Expected response:
```json
{
  "status": "running",
  "version": "1.0.0"
}
```

### Using an API Key:
If authentication is enabled, include the `x-api-key` header:
```bash
curl -X POST http://localhost:5000/analyze \
  -H "x-api-key: your_api_key" \
  -d '{"project_path": "/home/user/project"}'
```

---

## 7. Notes and Best Practices

- **Security**:
  - Use HTTPS in production environments.
  - Avoid exposing sensitive API keys.

- **Scaling**:
  - Use a load balancer to handle multiple concurrent API requests.
  - Optimize server memory and CPU usage for large-scale analyses.

- **Timeouts**:
  - Ensure the client handles long-running requests gracefully.

For further details, consult the [Architecture Documentation](docs/architecture.md).

