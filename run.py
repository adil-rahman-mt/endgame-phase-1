from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/')
def home():
    return """
    <p>Welcome to Endgame: Phase 1.</p>
    <p>For the API documentation, click <a href="https://github.com/adil-rahman-mt/endgame-phase-1">here</a></p>
    <p>Or visit https://github.com/adil-rahman-mt/endgame-phase-1</p>
    """