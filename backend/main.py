from flask import Flask, request, jsonify
from database.dialogue_manager import Dialogue_Manger
import base64

class App:
    def __init__(self, mode):
        self.app_mode = mode
        self.app = Flask(import_name="Hokkien Game")
        self.dialogue_manager = Dialogue_Manger(mode)
        
    def run(self):
        print("\nStarting Flask app...")
      
        #local mock data + graph style dialogue test 
       
        VENDORS = {
            1: {
                "id": 1,
                "name": "Bubble Tea Stall",
                "specialty": "Bubble Tea",
                "personality": {
                    "politeness": 0.9,
                    "friendliness": 0.8,
                    "dialect": "Tâi-lâm"
                }
            },
            2: {
                "id": 2,
                "name": "Oyster Omelette Stall",
                "specialty": "Oyster Omelette",
                "personality": {
                    "politeness": 0.7,
                    "friendliness": 0.6,
                    "dialect": "Tâi-pak"
                }
            }
        }

        #mock data for contract apis
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

        # mock vendor profile from api testing
        MOCK_VENDOR_PROFILES = {
            "v001": {
                "vendor_id": "v001",
                "name": "A-Ging's Bubble Tea",
                "inventory": [
                    {
                        "item_id": "item_01",
                        "name": "Classic Milk Tea",
                        "base_price": 50
                    },
                    {
                        "item_id": "item_02",
                        "name": "Taro Milk Tea",
                        "base_price": 60
                    }
                ],
                "starting_node_id": "intro_001"
            }
        }

        @self.app.route("/vendors", methods=["GET"])
        def get_vendors():
            return jsonify({
                "status": "success",
                "vendors": list(VENDORS.values())
            }), 200

        @self.app.route("/vendors/<int:vendor_id>", methods=["GET"])
        def get_vendor(vendor_id):
            vendor = VENDORS.get(vendor_id)
            if not vendor:
                return jsonify({"status": "error", "message": "Vendor not found"}), 404
            return jsonify({"status": "success", "vendor": vendor}), 200

        @self.app.route("/api/v1/user/<user_id>/stats", methods=["GET"])
        def api_get_user_stats(user_id):
            user = MOCK_USER_STATS.get(user_id)
            if not user:
                # simple default if unknown user
                user = {
                    "user_id": user_id,
                    "current_streak": 0,
                    "last_active_date": None,
                    "activity_heatmap": {},
                    "preferred_language": "hokkien"
                }
            return jsonify(user), 200

        @self.app.route("/api/v1/vendors/<vendor_id>", methods=["GET"])
        def api_get_vendor_profile(vendor_id):
            vendor = MOCK_VENDOR_PROFILES.get(vendor_id)
            if not vendor:
                return jsonify({"error": "Vendor not found"}), 404
            return jsonify(vendor), 200

        @self.app.route("/api/v1/dialogue/<node_id>", methods=["GET"])
        def get_dialogue_node(node_id):
            node_data = self.dialogue_manager.get_dialogue_node(node_id)
            print(node_data)
            
            return jsonify({
                "status": "success",
                "data": node_data,
                "meta": {"processTimeMS": 123}
            }), 200

        @self.app.route("/api/v1/generate/sentences", methods=["POST"])
        def fetch_sentences():
            request_body = request.get_json()
            input_text = request_body.get("input_text")

            if self.app_mode == "test_mode":
                english_text = chinese_text = hokkien_text = "this output is a test output"
            else:
                english_text = chinese_text = hokkien_text = "calls model api for translation"
            
            return jsonify({
                "status": "success",
                "data": {
                    "input_text": input_text,
                    "english_text": english_text,
                    "chinese_text": chinese_text,
                    "hokkien_text": hokkien_text
                },
                "meta": {"processTimeMS": 123}
            }), 200

        @self.app.route("/api/v1/generate/translation", methods=["POST"])
        def fetch_translation():
            request_body = request.get_json()
            source_lang = request_body.get("source_lang")
            output_lang = request_body.get("output_lang")
            model_parameters = request_body.get("parameters")
            input_text = request_body.get("input_text")

            model_out = "this output is a test output" if self.app_mode == "test_mode" else "calls model api for translation"
            
            return jsonify({
                "status": "success",
                "data": {
                    "source_lang": source_lang,
                    "output_lang": output_lang,
                    "parameters": model_parameters,
                    "input_text": input_text,
                    "translated_text": model_out
                },
                "meta": {"processTimeMS": 123}
            }), 200
        
        @self.app.route("/api/v1/generate/romanizer", methods=["POST"])
        def fetch_romanizer():
            request_body = request.get_json()
            source_lang = request_body.get("source_lang")
            output_lang = request_body.get("output_lang")
            input_text = request_body.get("input_text")

            romanized_text = "this output is a test output" if self.app_mode == "test_mode" else "calls model api for romanization"

            return jsonify({
                "status": "success",
                "data": {
                    "source_lang": source_lang,
                    "output_lang": output_lang,
                    "input_text": input_text,
                    "romanized_text": romanized_text
                },
                "meta": {"processTimeMS": 123}
            }), 200

        # might not be used
        @self.app.route("/api/v1/generate/image", methods=["POST"])
        def generate_image():
            request_body = request.get_json()
            input_text = request_body.get("input_text")
            negative_prompt = request_body.get("negative_prompt")
            negative_prompt_style = request_body.get("negative_prompt_style")
            n_steps = request_body.get("n_steps")
            high_noise_frac = request_body.get("high_noise_frac")
            base64_string = request_body.get("base64_string")
            
            generate_image = "this output is a test output" if self.app_mode == "test_mode" else "calls model api for image generation"

            return jsonify({
                "status": "success",
                "data": {
                    "input_text": input_text,
                    "negative_prompt": negative_prompt,
                    "negative_prompt_style": negative_prompt_style,
                    "n_steps": n_steps,
                    "high_noise_frac": high_noise_frac,
                    "base64_string": base64_string,
                    "generate_image": generate_image
                },
                "meta": {"process_time_ms": 123}
            }), 200

        @self.app.route("/api/v1/generate/numeric-tones", methods=["POST"])
        def fetch_numeric_tones():
            request_body = request.get_json()
            input_text = request_body.get("input_text")
            source_lang = request_body.get("source_lang")
            output_lang = request_body.get("output_lang")

            numeric_tones = "this output is a test output" if self.app_mode == "test_mode" else "calls model api for numeric tones"

            return jsonify({
                "status": "success",
                "data": {
                    "source_lang": source_lang,
                    "output_lang": output_lang,
                    "input_text": input_text,
                    "numeric_tones": numeric_tones
                },
                "meta": {"process_time_ms": 123}
            }), 200
        
        @self.app.route("/api/v1/generate/audio-url", methods=["POST"])
        def fetch_audio_url():
            request_body = request.get_json()
            input_text = request_body.get("input_text")
            source_lang = request_body.get("source_lang")
            output_lang = request_body.get("output_lang")

            audio_url = "this output is a test output" if self.app_mode == "test_mode" else "aaaa"

            return jsonify({
                "status": "success",
                "data": {
                    "source_lang": source_lang,
                    "output_lang": output_lang,
                    "input_text": input_text,
                    "audio_url": audio_url
                },
                "meta": {"process_time_ms": 123}
            }), 200
        
        @self.app.route("/api/v1/generate/audio-blob", methods=["POST"])
        def fetch_audio_blob():
            request_body = request.get_json()
            input_text = request_body.get("input_text")
            source_lang = request_body.get("source_lang")
            output_lang = request_body.get("output_lang")

            audio_blob = "this output is a test output" if self.app_mode == "test_mode" else "aaaa"

            return jsonify({
                "status": "success",
                "data": {
                    "source_lang": source_lang,
                    "output_lang": output_lang,
                    "input_text": input_text,
                    "audio_blob": audio_blob
                },
                "meta": {"process_time_ms": 123}
            }), 200
        
        @self.app.route("/cat-fact")
        def get_cat_fact():
            return jsonify({
                "status": "success",
                "data": {
                    "cat_fact": "Adult cats rarely meow at each other; they developed this sound specifically to communicate with humans."
                },
                "meta": {"processTimeMS": 123}
            }), 200
        
        @self.app.route("/audio-test")
        def get_audio_test():
            with open("audio-clips/test_audio.mp3", 'rb') as f:
                encoded_string = base64.b64encode(f.read()).decode('utf-8')

            return jsonify({
                "status": "success",
                "data": {
                    "audio_clip": encoded_string
                },
                "meta": {"processTimeMS": 123}
            }), 200

        self.app.run(host="0.0.0.0", port=8000, debug=False)

def select_launch_mode():
    prompt = '''
Select launch mode...
        
> Press a | Launch in default mode
> Press s | Launch in test mode
'''      
    mode = input(prompt)
    match mode:
        case "a":
            return 0
        case "s":
            return 1
            

if __name__ == "__main__":
    mode = select_launch_mode()
    app = App(mode)
    app.run()