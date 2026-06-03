# Clone Me Project 2.0

## Project Overview

This repository contains the backend for the "Clone Me Project 2.0" application. The backend is built using Flask and provides authentication, profile access, and a chat endpoint powered by the Ollama model. It uses MongoDB for user storage and JWT for token-based authentication.

## File Structure

```
backend/
  app.py
  app/
    __init__.py
    auth/
      controller.py
      routes.py
      utils.py
    chat/
      routes.py
    core/
      config.py
      db.py
    middleware/
      jwt_required.py
    models/
      history.py
      user.py
```

### Key files

- `backend/app.py` - Main Flask application entry point.
- `backend/app/core/config.py` - Configuration settings, including MongoDB and JWT secrets.
- `backend/app/auth/utils.py` - JWT token generation and validation utilities.
- `backend/app/auth/controller.py` - Authentication-related logic.
- `backend/app/auth/routes.py` - Authentication route definitions.
- `backend/app/chat/routes.py` - Chat API route using Ollama.
- `backend/app/middleware/jwt_required.py` - Middleware for protecting routes.
- `backend/app/models/user.py` - User model representation.
- `backend/app/models/history.py` - Chat history model representation.

## Tech Stack

- Python
- Flask
- Flask-CORS
- PyMongo
- MongoDB
- JWT (`PyJWT`)
- Ollama
- BSON (`bson`)

## Notes

- Database configuration is handled via environment variables: `DB_URI`, `DB_NAME`, and `SECRET_KEY`.
- The chat endpoint uses the Ollama client with the configured model.
- This README describes the backend structure; if there is a frontend or additional services, they are not included here.
