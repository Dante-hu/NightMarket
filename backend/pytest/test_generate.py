"""
Tests for POST /api/v1/generate/* endpoints:
  - /sentences
  - /translation
  - /romanizer
  - /numeric-tones
  - /audio-url
  - /audio-blob
"""

TEST_OUTPUT = "this output is a test output"


class TestGenerateSentences:

    def test_returns_200(self, client):
        res = client.post("/api/v1/generate/sentences", json={"input_text": "Hello"})
        assert res.status_code == 200

    def test_response_has_success_status(self, client):
        res = client.post("/api/v1/generate/sentences", json={"input_text": "Hello"})
        assert res.get_json()["status"] == "success"

    def test_response_has_data_and_meta(self, client):
        res = client.post("/api/v1/generate/sentences", json={"input_text": "Hello"})
        data = res.get_json()
        assert "data" in data
        assert "meta" in data

    def test_input_text_is_echoed_back(self, client):
        res = client.post("/api/v1/generate/sentences", json={"input_text": "Hello"})
        assert res.get_json()["data"]["input_text"] == "Hello"

    def test_english_text_is_present(self, client):
        res = client.post("/api/v1/generate/sentences", json={"input_text": "Hello"})
        assert res.get_json()["data"]["english_text"] == TEST_OUTPUT

    def test_chinese_text_is_present(self, client):
        res = client.post("/api/v1/generate/sentences", json={"input_text": "Hello"})
        assert res.get_json()["data"]["chinese_text"] == TEST_OUTPUT

    def test_hokkien_text_is_present(self, client):
        res = client.post("/api/v1/generate/sentences", json={"input_text": "Hello"})
        assert res.get_json()["data"]["hokkien_text"] == TEST_OUTPUT


class TestGenerateTranslation:

    def test_returns_200(self, client):
        res = client.post("/api/v1/generate/translation", json={
            "source_lang": "EN",
            "output_lang": "HAN",
            "parameters": {},
            "input_text": "Good morning"
        })
        assert res.status_code == 200

    def test_response_has_success_status(self, client):
        res = client.post("/api/v1/generate/translation", json={
            "source_lang": "EN", "output_lang": "HAN",
            "parameters": {}, "input_text": "Good morning"
        })
        assert res.get_json()["status"] == "success"

    def test_source_lang_is_echoed(self, client):
        res = client.post("/api/v1/generate/translation", json={
            "source_lang": "EN", "output_lang": "HAN",
            "parameters": {}, "input_text": "Good morning"
        })
        assert res.get_json()["data"]["source_lang"] == "EN"

    def test_output_lang_is_echoed(self, client):
        res = client.post("/api/v1/generate/translation", json={
            "source_lang": "EN", "output_lang": "HAN",
            "parameters": {}, "input_text": "Good morning"
        })
        assert res.get_json()["data"]["output_lang"] == "HAN"

    def test_input_text_is_echoed(self, client):
        res = client.post("/api/v1/generate/translation", json={
            "source_lang": "EN", "output_lang": "HAN",
            "parameters": {}, "input_text": "Good morning"
        })
        assert res.get_json()["data"]["input_text"] == "Good morning"

    def test_translated_text_is_present(self, client):
        res = client.post("/api/v1/generate/translation", json={
            "source_lang": "EN", "output_lang": "HAN",
            "parameters": {}, "input_text": "Good morning"
        })
        assert res.get_json()["data"]["translated_text"] == TEST_OUTPUT


class TestGenerateRomanizer:

    def test_returns_200(self, client):
        res = client.post("/api/v1/generate/romanizer", json={
            "source_lang": "HAN",
            "output_lang": "POJ",
            "input_text": "你好"
        })
        assert res.status_code == 200

    def test_response_has_success_status(self, client):
        res = client.post("/api/v1/generate/romanizer", json={
            "source_lang": "HAN", "output_lang": "POJ", "input_text": "你好"
        })
        assert res.get_json()["status"] == "success"

    def test_source_lang_is_echoed(self, client):
        res = client.post("/api/v1/generate/romanizer", json={
            "source_lang": "HAN", "output_lang": "POJ", "input_text": "你好"
        })
        assert res.get_json()["data"]["source_lang"] == "HAN"

    def test_input_text_is_echoed(self, client):
        res = client.post("/api/v1/generate/romanizer", json={
            "source_lang": "HAN", "output_lang": "POJ", "input_text": "你好"
        })
        assert res.get_json()["data"]["input_text"] == "你好"

    def test_romanized_text_is_present(self, client):
        res = client.post("/api/v1/generate/romanizer", json={
            "source_lang": "HAN", "output_lang": "POJ", "input_text": "你好"
        })
        assert res.get_json()["data"]["romanized_text"] == TEST_OUTPUT


class TestGenerateNumericTones:

    def test_returns_200(self, client):
        res = client.post("/api/v1/generate/numeric-tones", json={
            "source_lang": "POJ",
            "output_lang": "numeric",
            "input_text": "lí hó"
        })
        assert res.status_code == 200

    def test_response_has_success_status(self, client):
        res = client.post("/api/v1/generate/numeric-tones", json={
            "source_lang": "POJ", "output_lang": "numeric", "input_text": "lí hó"
        })
        assert res.get_json()["status"] == "success"

    def test_input_text_is_echoed(self, client):
        res = client.post("/api/v1/generate/numeric-tones", json={
            "source_lang": "POJ", "output_lang": "numeric", "input_text": "lí hó"
        })
        assert res.get_json()["data"]["input_text"] == "lí hó"

    def test_numeric_tones_is_present(self, client):
        res = client.post("/api/v1/generate/numeric-tones", json={
            "source_lang": "POJ", "output_lang": "numeric", "input_text": "lí hó"
        })
        assert res.get_json()["data"]["numeric_tones"] == TEST_OUTPUT


class TestGenerateAudioUrl:

    def test_returns_200(self, client):
        res = client.post("/api/v1/generate/audio-url", json={
            "source_lang": "HAN",
            "output_lang": "audio",
            "input_text": "你好"
        })
        assert res.status_code == 200

    def test_response_has_success_status(self, client):
        res = client.post("/api/v1/generate/audio-url", json={
            "source_lang": "HAN", "output_lang": "audio", "input_text": "你好"
        })
        assert res.get_json()["status"] == "success"

    def test_input_text_is_echoed(self, client):
        res = client.post("/api/v1/generate/audio-url", json={
            "source_lang": "HAN", "output_lang": "audio", "input_text": "你好"
        })
        assert res.get_json()["data"]["input_text"] == "你好"

    def test_audio_url_is_present(self, client):
        res = client.post("/api/v1/generate/audio-url", json={
            "source_lang": "HAN", "output_lang": "audio", "input_text": "你好"
        })
        assert res.get_json()["data"]["audio_url"] == TEST_OUTPUT


class TestGenerateAudioBlob:

    def test_returns_200(self, client):
        res = client.post("/api/v1/generate/audio-blob", json={
            "source_lang": "HAN",
            "output_lang": "audio",
            "input_text": "你好"
        })
        assert res.status_code == 200

    def test_response_has_success_status(self, client):
        res = client.post("/api/v1/generate/audio-blob", json={
            "source_lang": "HAN", "output_lang": "audio", "input_text": "你好"
        })
        assert res.get_json()["status"] == "success"

    def test_input_text_is_echoed(self, client):
        res = client.post("/api/v1/generate/audio-blob", json={
            "source_lang": "HAN", "output_lang": "audio", "input_text": "你好"
        })
        assert res.get_json()["data"]["input_text"] == "你好"

    def test_audio_blob_is_present(self, client):
        res = client.post("/api/v1/generate/audio-blob", json={
            "source_lang": "HAN", "output_lang": "audio", "input_text": "你好"
        })
        assert res.get_json()["data"]["audio_blob"] == TEST_OUTPUT