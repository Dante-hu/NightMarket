# NightMarket Backend

A Python Flask backend for the NightMarket Taiwanese Hokkien language learning game world.

---

## Prerequisites

- Python 3.10 or higher
- pip

---

## Getting Started

### 1. Navigate to the backend folder

```bash
cd backend
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

You should see `(venv)` appear at the start of your terminal line once it's active.

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Server

```bash
python main.py
```

You will be prompted to select a launch mode:

```
> Press 0 | Launch in default mode
> Press 1 | Launch in test mode
```

- **Mode 0** — Production mode, connects to the main database and calls real APIs.
- **Mode 1** — Test mode, connects to `hok_test_data.db` and returns placeholder responses instead of calling real APIs.

The server will start on `http://localhost:8000`.

---

## Running the Tests

Make sure your virtual environment is activated and dependencies are installed before running tests.

```bash
pytest testing/ -v
```

The `-v` flag gives verbose output so you can see each individual test result.

The tests use Flask's built-in test client — **you do not need to start the server before running them.**

---

## Project Structure

```
backend/
├── api/
│   └── translation.py          # Unused blueprint (legacy)
├── audio-clips/
│   └── test_audio.mp3          # Test audio file
├── database/
│   ├── hok_db.py               # Database connection manager
│   ├── hok_test_data.db        # SQLite test database
│   └── sql_db.py               # Low-level SQL helper
├── managers/
│   ├── dialogue_manager.py     # Dialogue node logic
│   └── vendor_manager.py       # Vendor and item logic
├── models/
│   └── hok_translation_model.py # Hokkien translation model (not yet wired up)
├── testing/
│   ├── conftest.py             # Pytest fixtures and app setup
│   ├── test_dialogue.py        # Dialogue endpoint tests
│   ├── test_generate.py        # Generate endpoint tests
│   ├── test_misc.py            # Miscellaneous endpoint tests
│   ├── test_user_stats.py      # User stats endpoint tests
│   └── test_vendor.py          # Vendor endpoint tests
├── app_factory.py              # (Reserved for future use)
├── main.py                     # Main Flask app and all endpoints
└── requirements.txt            # Python dependencies
```

---

## API Endpoints

| Method | Endpoint                               | Description                            |
| ------ | -------------------------------------- | -------------------------------------- |
| GET    | `/api/v1/user/<user_id>/stats`         | Get user stats and activity            |
| GET    | `/api/v1/vendors/<vendor_id>`          | Get vendor profile and items           |
| GET    | `/api/v1/dialogue/<node_id>`           | Get a dialogue node                    |
| GET    | `/api/v1/dialogue/root-nodes/<npc_id>` | Get root dialogue nodes for an NPC     |
| POST   | `/api/v1/generate/sentences`           | Generate sentences (translation model) |
| POST   | `/api/v1/generate/translation`         | Translate text                         |
| POST   | `/api/v1/generate/romanizer`           | Romanize Hokkien text                  |
| POST   | `/api/v1/generate/numeric-tones`       | Convert to numeric tones               |
| POST   | `/api/v1/generate/audio-url`           | Get TTS audio URL                      |
| POST   | `/api/v1/generate/audio-blob`          | Get TTS audio as blob                  |
| GET    | `/cat-fact`                            | Returns a cat fact                     |
| GET    | `/audio-test`                          | Returns a base64 encoded test MP3      |
