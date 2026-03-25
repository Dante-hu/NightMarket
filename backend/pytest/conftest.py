import pytest
import sys
import os

# Allow imports from the backend root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from flask import Flask, request, jsonify
from managers.dialogue_manager import Dialogue_Manager
from managers.vendor_manager import Vendor_Manager
from managers.challenge_manager import Challenge_Manager
import base64


def create_test_app():
    mode = 1
    dialogue_manager = Dialogue_Manager(mode)
    vendor_manager = Vendor_Manager(mode)
    challenge_manager = Challenge_Manager(mode)
    app = Flask(import_name="Hokkien Game Test")
    app.config["TESTING"] = True

    MOCK_USER_STATS = {
        "u123": {
            "user_id": "u123",
            "current_streak": 5,
            "last_active_date": "2026-02-20",
            "activity_heatmap": {
                "2026-02-18": 5,
                "2026-02-19": 12,
                "2026-02-20": 8
            },
            "preferred_language": "hokkien"
        }
    }

    @app.route("/api/v1/user/<user_id>/stats", methods=["GET"])
    def api_get_user_stats(user_id):
        user = MOCK_USER_STATS.get(user_id)
        if not user:
            user = {
                "user_id": user_id,
                "current_streak": 0,
                "last_active_date": None,
                "activity_heatmap": {},
                "preferred_language": "hokkien"
            }
        return jsonify(user), 200

    @app.route("/api/v1/vendors/<vendor_id>", methods=["GET"])
    def get_vendor_profile(vendor_id):
        vendor_data = vendor_manager.get_vendor_profile(vendor_id)
        return jsonify({"status": "success", "data": vendor_data, "meta": {"processTimeMS": 123}}), 200

    @app.route("/api/v1/dialogue/<node_id>", methods=["GET"])
    def get_dialogue_node(node_id):
        node_data = dialogue_manager.get_dialogue_node(node_id)
        return jsonify({"status": "success", "data": node_data, "meta": {"processTimeMS": 123}}), 200

    @app.route("/api/v1/dialogue/root-nodes/<npc_id>")
    def get_dialogue_root_nodes(npc_id):
        node_data = dialogue_manager.get_dialogue_root_nodes(npc_id)
        return jsonify({"status": "success", "data": node_data, "meta": {"processTimeMS": 123}}), 200

    @app.route("/api/v1/generate/sentences", methods=["POST"])
    def fetch_sentences():
        body = request.get_json()
        input_text = body.get("input_text")
        text = "this output is a test output"
        return jsonify({
            "status": "success",
            "data": {
                "input_text": input_text,
                "english_text": text,
                "chinese_text": text,
                "hokkien_text": text
            },
            "meta": {"processTimeMS": 123}
        }), 200

    @app.route("/api/v1/generate/translation", methods=["POST"])
    def fetch_translation():
        body = request.get_json()
        return jsonify({
            "status": "success",
            "data": {
                "source_lang": body.get("source_lang"),
                "output_lang": body.get("output_lang"),
                "parameters": body.get("parameters"),
                "input_text": body.get("input_text"),
                "translated_text": "this output is a test output"
            },
            "meta": {"processTimeMS": 123}
        }), 200

    @app.route("/api/v1/generate/romanizer", methods=["POST"])
    def fetch_romanizer():
        body = request.get_json()
        return jsonify({
            "status": "success",
            "data": {
                "source_lang": body.get("source_lang"),
                "output_lang": body.get("output_lang"),
                "input_text": body.get("input_text"),
                "romanized_text": "this output is a test output"
            },
            "meta": {"processTimeMS": 123}
        }), 200

    @app.route("/api/v1/generate/numeric-tones", methods=["POST"])
    def fetch_numeric_tones():
        body = request.get_json()
        return jsonify({
            "status": "success",
            "data": {
                "source_lang": body.get("source_lang"),
                "output_lang": body.get("output_lang"),
                "input_text": body.get("input_text"),
                "numeric_tones": "this output is a test output"
            },
            "meta": {"process_time_ms": 123}
        }), 200

    @app.route("/api/v1/generate/audio-url", methods=["POST"])
    def fetch_audio_url():
        body = request.get_json()
        return jsonify({
            "status": "success",
            "data": {
                "source_lang": body.get("source_lang"),
                "output_lang": body.get("output_lang"),
                "input_text": body.get("input_text"),
                "audio_url": "this output is a test output"
            },
            "meta": {"process_time_ms": 123}
        }), 200

    @app.route("/api/v1/generate/audio-blob", methods=["POST"])
    def fetch_audio_blob():
        body = request.get_json()
        return jsonify({
            "status": "success",
            "data": {
                "source_lang": body.get("source_lang"),
                "output_lang": body.get("output_lang"),
                "input_text": body.get("input_text"),
                "audio_blob": "this output is a test output"
            },
            "meta": {"process_time_ms": 123}
        }), 200

    @app.route("/cat-fact")
    def get_cat_fact():
        return jsonify({
            "status": "success",
            "data": {"cat_fact": "Adult cats rarely meow at each other; they developed this sound specifically to communicate with humans."},
            "meta": {"processTimeMS": 123}
        }), 200

    @app.route("/api/v1/challenges", methods=["GET"])
    def get_challenges():
        challenges = challenge_manager.get_all_challenges()
        return jsonify({
            "status": "success",
            "data": challenges,
            "meta": {"processTimeMS": 123}
        }), 200
 
    @app.route("/api/v1/challenges/accept", methods=["POST"])
    def accept_challenge():
        body = request.get_json()
        user_id = body.get("user_id")
        challenge_id = body.get("challenge_id")
        if not user_id or not challenge_id:
            return jsonify({
                "status": "error",
                "message": "user_id and challenge_id are required"
            }), 400
        result, error = challenge_manager.accept_challenge(user_id, challenge_id)
        if error:
            return jsonify({"status": "error", "message": error}), 400
        return jsonify({
            "status": "success",
            "data": result,
            "meta": {"processTimeMS": 123}
        }), 200
 
    @app.route("/api/v1/challenges/inventory", methods=["POST"])
    def add_to_inventory():
        body = request.get_json()
        user_id = body.get("user_id")
        item_id = body.get("item_id")
        challenge_id = body.get("challenge_id")
        if not user_id or not item_id or not challenge_id:
            return jsonify({
                "status": "error",
                "message": "user_id, item_id and challenge_id are required"
            }), 400
        result, error = challenge_manager.add_to_inventory(user_id, item_id, challenge_id)
        if error:
            return jsonify({"status": "error", "message": error}), 400
        return jsonify({
            "status": "success",
            "data": result,
            "meta": {"processTimeMS": 123}
        }), 200
 
    @app.route("/api/v1/challenges/verify", methods=["POST"])
    def verify_challenge():
        body = request.get_json()
        user_id = body.get("user_id")
        challenge_id = body.get("challenge_id")
        final_order = body.get("final_order")
        if not user_id or not challenge_id or final_order is None:
            return jsonify({
                "status": "error",
                "message": "user_id, challenge_id and final_order are required"
            }), 400
        is_success, reason = challenge_manager.verify_challenge(
            user_id, challenge_id, final_order)
        return jsonify({
            "status": "success",
            "data": {
                "is_success": is_success,
                "challenge_id": challenge_id,
                "reason": reason
            },
            "meta": {"processTimeMS": 123}
        }), 200
 
    @app.route("/api/v1/challenges/<challenge_id>", methods=["GET"])
    def get_challenge(challenge_id):
        challenge = challenge_manager.get_challenge(challenge_id)
        if not challenge:
            return jsonify({
                "status": "error",
                "message": "Challenge not found: %s" % challenge_id
            }), 404
        return jsonify({
            "status": "success",
            "data": challenge,
            "meta": {"processTimeMS": 123}
        }), 200
 
    @app.route("/api/v1/user/<user_id>/inventory", methods=["GET"])
    def get_user_inventory(user_id):
        inventory = challenge_manager.get_user_inventory(user_id)
        return jsonify({
            "status": "success",
            "data": inventory,
            "meta": {"processTimeMS": 123}
        }), 200
 
    return app


@pytest.fixture(scope="session")
def client():
    """Shared Flask test client for all tests."""
    app = create_test_app()
    with app.test_client() as client:
        yield client