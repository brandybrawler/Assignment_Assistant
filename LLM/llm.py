from flask import Flask, request
from pathlib import Path
from gpt4all import GPT4All
import requests

app = Flask(__name__)

current_directory = Path.cwd()
model_path = current_directory / "Chat_Models"
model_path.mkdir(parents=True, exist_ok=True)

model_name = 'orca-mini-3b-gguf2-q4_0.gguf'
#Other models include:
# wizardlm-13b-v1.2.Q4_0.gguf           #really huge model(have not tried it so far)
# mistral-7b-openorca.gguf2.Q4_0.gguf       #fast and uncensored, best for chat based conversations
# gpt4all-falcon-newbpe-q4_0.gguf       #fastest model overall, instruction based
# orca-mini-3b-gguf2-q4_0.gguf      #dumbest model

model = GPT4All(model_name, model_path=model_path)
#
@app.route('/incoming_text', methods=['POST'])
def transcribe():
    try:
        print("Received Transcribed Text:-->  " + request.json['transcribed_text'])
        text_prompt = request.json.get('transcribed_text', '')
        system_template = "A chat between a user and an artificial intelligence assistant called ProxmaAI, who was created by Proxima.\n"
        # prompt_template = 'USER: {0}\nASSISTANT: '
        with model.chat_session():
            response = model.generate(
                text_prompt,
                max_tokens=200,
                temp=0.7,
                top_k=40,
                top_p=0.4,
                min_p=0.0,
                repeat_penalty=1.18,
                repeat_last_n=64,
                n_batch=8,
                n_predict=None,
                streaming=False
            )

            TextResponse = response
            print(TextResponse)

            # Send TextResponse to http://localhost:8088/tts
            tts_response = requests.post('http://localhost:8088/ttsText', json={'TextResp': TextResponse})
            print("Response status code:", tts_response.status_code)  
            
            # Add this line for debugging# Text to print after sending the response
            print("Text after sending the response")
        if tts_response.ok:
            return {"response": "Sent text response to the endpoint"}, 200
        else:
            return {"error": 'Failed to send TextResponse to the endpoint'}, 500

    except Exception as e:
        return {"error": str(e)}, 500

  

if __name__ == '__main__':
    app.run(host='localhost', port=8089)