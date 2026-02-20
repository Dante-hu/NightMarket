from flask import Flask, request, jsonify

class App:
    def __init__(self):
        self.app = None
        self.app_mode = None

    def create_app(self):
        self.app = Flask("Hokkien Game")
        self.select_mode()
        self.run()

    def select_mode(self):
        prompt = '''
Select launch mode...
        
> Press a | Launch in default mode
> Press s | Launch in test mode
'''      
        if input(prompt) == 's':
            self.app_mode = "test_mode"

    def run(self):
        print("\nStarting Flask app...")

        @self.app.route("/")
        def hello_world():
            return "<p>Hello, World!</p>"

        @self.app.route("/generate/sentences", methods=["POST"])
        def fetch_sentences():
            if request.method != "POST":
                return jsonify({
                        "status": "error",
                        "message": "Invalid request method used"
                    }), 400

            request_body = request.get_json()
            input_text = request_body.get("input_text")

            if self.app_mode == "test_mode":
                english_text = "this output is a test output"
                chinese_text = "this output is a test output"
                hokkien_text = "this output is a test output"
            else:
                english_text = "calls model api for translation"
                chinese_text = "calls model api for translation"
                hokkien_text = "calls model api for translation"
            
            return jsonify({
                "status": "success",
                "data": {
                    "input_text": input_text,
                    "english_text": english_text,
                    "chinese_text": chinese_text,
                    "hokkien_text": hokkien_text
                },
                "meta": {
                    "processTimeMS": 123
                }
            }), 200

        @self.app.route("/generate/translation", methods=["POST"])
        def fetch_translation():
            if request.method != "POST":
                return jsonify({
                        "status": "error",
                        "message": "Invalid request method used"
                    }), 400

            request_body = request.get_json()
            source_lang = request_body.get("source_lang")
            output_lang = request_body.get("output_lang")
            model_parameters = request_body.get("parameters")

            input_text = request_body.get("input_text")

            if self.app_mode == "test_mode":
                model_out = "this output is a test output"
            else:
                model_out = "calls model api for translation"
            
            return jsonify({
                "status": "success",
                "data": {
                    "source_lang": source_lang,
                    "output_lang": output_lang,
                    "parameters": model_parameters,
                    "input_text": input_text,
                    "translated_text": model_out
                },
                "meta": {
                    "processTimeMS": 123
                }
            }), 200
        
        @self.app.route("/generate/romanizer", methods=["POST"])
        def fetch_romanizer():
            if request.method != "POST":
                return jsonify({
                        "status": "error",
                        "message": "Invalid request method used"
                    }), 400
            
            api_key = request.headers.get("API-KEY")

            request_body = request.get_json()
            source_lang = request_body.get("source_lang")
            output_lang = request_body.get("output_lang")
            input_text = request_body.get("input_text")

            if self.app_mode == "test_mode":
                romanized_text = "this output is a test output"
            else:
                romanized_text = "calls model api for romanization"

            return jsonify({
                "status": "success",
                "data": {
                    "source_lang": source_lang,
                    "output_lang": output_lang,
                    "input_text": input_text,
                    "romanized_text": romanized_text
                },
                "meta": {
                    "processTimeMS": 123
                }
            }), 200
        

                  
        @self.app.route("/generate/image", methods=["POST"])
        def generate_image():
            if request.method != "POST":
                return jsonify({
                        "status": "error",
                        "message": "Invalid request method used"
                    }), 400
            
            api_key = request.headers.get("API-KEY")

            request_body = request.get_json()
            input_text = request_body.get("input_text")
            negative_prompt = request_body.get("negative_prompt")
            negative_prompt_style = request_body.get("negative_prompt_style")
            n_steps = request_body.get("n_steps")
            high_noise_frac = request_body.get("high_noise_frac")
            base64_string = request_body.get("base64_string")
            
            if self.app_mode == "test_mode":
                generate_image = "this output is a test output"
            else:
                generate_image = "calls model api for image generation"

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
                "meta": {
                    "process_time_ms": 123
                }
            }), 200

        @self.app.route("/generate/numeric-tones", methods=["POST"])
        def fetch_numeric_tones():
            if request.method != "POST":
                return jsonify({
                        "status": "error",
                        "message": "Invalid request method used"
                    }), 400  
            
            request_body = request.get_json()
            input_text = request_body.get("input_text")
            source_lang = request_body.get("sourc_lang")
            output_lang = request_body.get("output_lang")

            if self.app_mode == "test_mode":
                numeric_tones = "this output is a test output"
            else:
                numeric_tones = "calls model api for numeric tones"

            return jsonify({
                "status": "success",
                "data": {
                    "source_lang": source_lang,
                    "output_lang": output_lang,
                    "input_text": input_text,
                    "numeric_tones": numeric_tones
                },
                "meta": {
                    "process_time_ms": 123
                }
            }), 200
        
        @self.app.route("/generate/audio-url", methods=["POST"])
        def fetch_audio_url():
            if request.method != "POST":
                return jsonify({
                        "status": "error",
                        "message": "Invalid request method used"
                    }), 400  
        
            request_body = request.get_json()
            input_text = request_body.get("input_text")
            source_lang = request_body.get("sourc_lang")
            output_lang = request_body.get("output_lang")

            if self.app_mode == "test_mode":
                audio_url = "this output is a test output"
            else:
                audio_url = "aaaa"

            return jsonify({
                "status": "success",
                "data": {
                    "source_lang": source_lang,
                    "output_lang": output_lang,
                    "input_text": input_text,
                    "ttsaudio_url_audio": audio_url
                },
                "meta": {
                    "process_time_ms": 123
                }
            }), 200
        
        @self.app.route("/generate/audio-blob", methods=["POST"])
        def fetch_audio_url():
            if request.method != "POST":
                return jsonify({
                        "status": "error",
                        "message": "Invalid request method used"
                    }), 400  
        
            request_body = request.get_json()
            input_text = request_body.get("input_text")
            source_lang = request_body.get("sourc_lang")
            output_lang = request_body.get("output_lang")

            if self.app_mode == "test_mode":
                audio_blob = "this output is a test output"
            else:
                audio_blob = "aaaa"

            return jsonify({
                "status": "success",
                "data": {
                    "source_lang": source_lang,
                    "output_lang": output_lang,
                    "input_text": input_text,
                    "ttsaudio_url_audio": audio_blob
                },
                "meta": {
                    "process_time_ms": 123
                }
            }), 200

        self.app.run(host="0.0.0.0", port=8000, debug=False)


if __name__ == "__main__":
    app = App()
    app.create_app()
