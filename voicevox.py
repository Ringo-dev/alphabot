import requests
import random
import json
from pathlib import Path

with open('config.json', 'r') as f:
    config = json.load(f)

ip = config['ip']
port = config['port']
url = f'http://{ip}:{port}/'
speaker_id = config['speaker_id']

def voice_generate(messages):
    params = {
        'text': messages,
        'speaker': speaker_id
    }

    audio_query = requests.post(url + 'audio_query', params=params)
    if audio_query.status_code == 200:
        print("クエリ作成に成功しました。")
        print(audio_query.status_code)
        print(audio_query.json())

        synthesis = requests.post(url + 'synthesis', params=params, json=audio_query.json())
        print(synthesis.status_code)

        if synthesis.status_code == 200:
            ramdom_files = random.randrange(1000, 9999)
            file_path = f'temp_voice/voice_{ramdom_files}.mp3'
            with open(file_path, 'wb') as f:
                f.write(synthesis.content)

            print("音声合成に成功しました。")

            return file_path

        elif 400 <= synthesis.status_code <= 499:
            print("(音声合成)クライアント側にエラーが発生しました。")

        elif 500 <= synthesis.status_code <= 599:
            print("(音声合成)サーバー側にエラーが発生しました。")

        else:
            print("(音声合成)予期せぬエラーが発生しました。")

    elif 400 <= audio_query.status_code <= 499:
        print("(クエリ)クライアント側にエラーが発生しました。")

    elif 500 <= audio_query.status_code <= 599:
        print("(クエリ)サーバー側にエラーが発生しました。")

    else:
        print("(クエリ)予期せぬエラーが発生しました。")

#voice_generate()