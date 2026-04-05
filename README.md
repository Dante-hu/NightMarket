# NightMarket Backend

## Run

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Navigate to `http://localhost:8000`

## Project Structure

```
backend/
├── admin/
│   └── static/            # Admin UI (HTML, JS, CSS)
├── api/                   # API blueprints
├── database/              # DB connection and SQLite
│   └── hok_*.db          # SQLite databases
├── managers/              # Business logic
├── models/                # ML models (translation, TTS)
├── pytest/                # Tests
└── main.py                # Entry point
```

## Admin Panel

Go to `http://localhost:8000/admin` to manage dialogue trees.

### Adding NPCs
1. Go to NPCs tab
2. Enter name (required), ID is optional (auto-generated)
3. Click Create

### Adding Dialogue
1. Select NPC from dropdown
2. Click "+ Add Root Node" or "+ Child" on existing nodes
3. Enter dialogue text in the Dialogue field
4. Click "Generate Translations" to translate to HAN/POJ
5. Click "Generate Audio" to create TTS audio (requires POJ translation)

## API Endpoints

API is served at `http://localhost:8000` when started with above instructions

### Vendors
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/api/v1/vendors/<vendor_id>` | Get vendor profile and items |

### Dialogue (Game)
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/api/v1/dialogue/<node_id>` | Get dialogue node |
| GET | `/api/v1/dialogue/root-nodes/<npc_id>` | Get root nodes for NPC |

### Challenges
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/api/v1/challenges` | Get all challenges |
| GET | `/api/v1/challenges/<challenge_id>` | Get challenge |
| POST | `/api/v1/challenges/accept` | Accept challenge |
| POST | `/api/v1/challenges/inventory` | Add to inventory |
| POST | `/api/v1/challenges/verify` | Verify challenge |

### Admin - NPCs
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/api/admin/npcs` | Get all NPCs |
| POST | `/api/admin/npcs` | Create NPC |
| PUT | `/api/admin/npcs/<npc_id>` | Update NPC |
| DELETE | `/api/admin/npcs/<npc_id>` | Delete NPC |

### Admin - Dialogue Nodes
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/api/admin/dialogue-nodes?npc_id=X` | Get nodes for NPC |
| POST | `/api/admin/dialogue-nodes` | Create node |
| PUT | `/api/admin/dialogue-nodes/<node_id>` | Update node |
| DELETE | `/api/admin/dialogue-nodes/<node_id>` | Delete node |

### Admin - Dialogues
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/api/admin/dialogues/<node_id>` | Get dialogue |
| PUT | `/api/admin/dialogues/<node_id>` | Update dialogue |

### Admin - Options
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/api/admin/options/<node_id>` | Get options for node |
| POST | `/api/admin/options/<node_id>` | Create option |
| PUT | `/api/admin/options/<option_id>` | Update option |
| DELETE | `/api/admin/options/<option_id>` | Delete option |

### Admin - Translation
| Method | Endpoint | Description |
|--------|----------|--------------|
| POST | `/api/admin/model/translate/<node_id>` | Translate to HAN/POJ |

Request:
```json
{"input_text": "Hello!", "output_lang": "HAN"}
```

### Admin - TTS
| Method | Endpoint | Description |
|--------|----------|--------------|
| POST | `/api/admin/model/tts/<node_id>` | Generate audio |

Request:
```json
{"translation_text": "你好！"}
```

### Admin - Vendors
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/api/admin/vendors` | Get all vendors |
| POST | `/api/admin/vendors` | Create vendor |
| PUT | `/api/admin/vendors/<vendor_id>` | Update vendor |
| DELETE | `/api/admin/vendors/<vendor_id>` | Delete vendor |

### Admin - Items
| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/api/admin/items/<vendor_id>` | Get items for vendor |
| POST | `/api/admin/items/<vendor_id>` | Create item |
| PUT | `/api/admin/items/<item_id>` | Update item |
| DELETE | `/api/admin/items/<item_id>` | Delete item |
