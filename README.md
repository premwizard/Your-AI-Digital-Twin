# CloneMe 2.0

## Project Overview

CloneMe 2.0 is a production-ready AI Digital Twin backend built with Python, Flask, MongoDB, and Ollama. The platform is designed to model a user's personality, memories, career interests, goals, and training data to deliver more meaningful, personalized interactions than a conventional chatbot.

The backend supports:
- user authentication with JWT and refresh tokens
- personality profile management
- long-term memory storage and retrieval
- training document ingestion and processing
- interview simulation and feedback
- future self projection
- analytics and usage reporting
- enriched prompt building with contextual data before invoking the LLM

## File Structure

```
backend/
  app.py
  requirements.txt
  .env.example
  app/
    __init__.py
    auth/
      __init__.py
      controller.py
      routes.py
      schemas.py
      service.py
      utils.py
    clone/
      __init__.py
      controller.py
      routes.py
      service.py
    memory/
      __init__.py
      controller.py
      routes.py
    training/
      __init__.py
      controller.py
      routes.py
    interview/
      __init__.py
      controller.py
      routes.py
    future_self/
      __init__.py
      controller.py
      routes.py
    analytics/
      __init__.py
      controller.py
      routes.py
    rag/
      __init__.py
      context_builder.py
    middleware/
      __init__.py
      jwt_required.py
      rate_limit.py
    models/
      __init__.py
      personality_profile.py
      memory.py
      training_document.py
      conversation_history.py
      interview_session.py
      future_profile.py
      clone_settings.py
    services/
      __init__.py
      llm.py
    utils/
      __init__.py
      logger.py
      responses.py
    core/
      __init__.py
      config.py
      db.py
```

## Main Features

- **Personality Profile Engine**: stores personality type, communication style, goals, strengths, weaknesses, skills, and preferences.
- **Long-Term Memory System**: stores memories, project notes, goals, and conversation history for later retrieval.
- **Clone Training System**: accepts resume/bio/project data and stores processed training documents.
- **Interview Simulator**: supports HR, technical, and behavioral interview session storage with feedback.
- **Future Self Mode**: creates a future persona based on career goals and timeline.
- **Enhanced Chat System**: builds context from profile, memories, and training data before sending enriched prompts to the LLM.
- **Analytics API**: returns counts for conversations, memories, training documents, and interview sessions.

## Tech Stack

- Python
- Flask
- Flask-CORS
- Flask-PyMongo
- PyMongo
- MongoDB
- PyJWT
- Ollama
- Werkzeug

## API Endpoints

- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/refresh`
- `POST /api/clone/respond`
- `GET /api/clone/personality`
- `POST /api/clone/personality`
- `GET /api/memory`
- `POST /api/memory`
- `POST /api/training/upload`
- `POST /api/training/process`
- `POST /api/training/train`
- `POST /api/interview/start`
- `GET /api/interview/sessions`
- `GET /api/interview/sessions/<session_id>/feedback`
- `POST /api/future-self/profile`
- `GET /api/future-self/profile`
- `POST /api/future-self/chat`
- `GET /api/analytics/overview`

## Environment Variables

- `SECRET_KEY`
- `REFRESH_SECRET_KEY`
- `DB_URI`
- `DB_NAME`
- `OLLAMA_MODEL`
- `FLASK_DEBUG`
- `PORT`
- `RATE_LIMIT_MAX_REQUESTS`
- `RATE_LIMIT_WINDOW_SECONDS`

## Notes

- The backend preserves existing user authentication and Ollama-powered response generation while extending the architecture to support AI digital twin workflows.
- Use `backend/app.py` as the Flask entrypoint.
- Load environment variables from `.env.example` and install dependencies from `backend/requirements.txt`.
