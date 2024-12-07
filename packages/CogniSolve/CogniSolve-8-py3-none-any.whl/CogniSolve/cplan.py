import requests, json

def ask(text_input, func):
    #https://dl.comss.org/download/controld.exe
    def get_message_from_gemini(api_keys, text_input):
        headers = {"Content-Type": "application/json"}
        data = {"contents":[{"parts":[{"text": text_input}]}]}
        for api_key in api_keys:
            #url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={}".format(api_key)
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-002:generateContent?key={}".format(api_key)
            try:
                response = requests.post(url, headers=headers, data=json.dumps(data))
                if response.status_code == 200:
                    response_data = response.json()
                    generated_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
                    return generated_text
                else:
                    print("Error: {0}".format(response.text))
                    if "400"in response.text:return"Failure!"
            except Exception as exc: print("Failure to connect: {0}".format(exc))
        return"Failure!"

    api_keys = ['MZj3khwnKuvFfr7=-vgm99bUcdIRs6WIDySazIA',
                '4fg_DQnHd*DXn7mtn7Su23n-4K75oz7Y.ySazIA',
                '4hT9t7RPkMjQTocMS53K*kfRXY8V=jEn+ySazIA',
                '8E3wEh+LE6KUhi*4otn0kTL6fi5h=jm..ySazIA']

    for i in range(len(api_keys)):
        api_keys[i] = func(api_keys[i])

    result = get_message_from_gemini(api_keys, text_input)
    print(result)
