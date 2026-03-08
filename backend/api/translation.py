from flask import Blueprint, request, jsonify, current_app

# Create the blueprint
translation_bp = Blueprint('translation', __name__)

@translation_bp.route("/sentences", methods=["POST"])
def fetch_sentences():
    request_body = request.get_json()
    input_text = request_body.get("input_text")

    # Use current_app to access your "test_mode" config
    if current_app.config.get("APP_MODE") == "test_mode":
        english_text = "test output"
    else:
        # This is where you will call your actual Service later
        english_text = "calls model api"
    
    return jsonify({"status": "success", "data": {"english_text": english_text}})