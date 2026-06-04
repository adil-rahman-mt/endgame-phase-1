from app import create_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import limits.storage
import os
from dotenv import load_dotenv

load_dotenv()

options = {}
redis_storage = limits.storage.storage_from_string(os.environ.get('REDIS_STORAGE_URI'), **options)

app = create_app()

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per 10 second"],
    storage_uri=os.environ.get('REDIS_STORAGE_URI'),
    strategy="fixed-window",
)

if __name__ == "__main__":
    app.run(debug=False)

@app.route('/')
def home():
    return """
    <p>Welcome to Endgame: Phase 1.</p>
    <p>For the API documentation, click <a href="https://github.com/adil-rahman-mt/endgame-phase-1">here</a></p>
    <p>Or visit https://github.com/adil-rahman-mt/endgame-phase-1</p>
    """