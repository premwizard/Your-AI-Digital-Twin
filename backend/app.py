import os
from app import create_app
from app.utils.logger import logger

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() in ["1", "true", "yes"]
    logger.info("Starting CloneMe 2.0 backend on port %s", port)
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
