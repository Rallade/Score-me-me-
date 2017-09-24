from flask import Flask, request, jsonify
import nexmo
from nexmo_keys import *
from majestic_key import *
import nltk
import urllib.request, json


client = nexmo.Client(key=api_key, secret=api_secret)
high_score = 0
top_player = ''

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def process():
    meme_score = 0
    if request.method == 'POST':
        print(request.get_json())
    else:
        message = dict(request.args)
        text = message['text']
        msisdn = message['msisdn']
        print(dict(request.args))
        sent = text[0]
        sent = nltk.word_tokenize(sent)
        sent = nltk.pos_tag(sent)

        sites = [word[0] + '.com' for word in sent if (word[1] == 'NN' or word[1] == 'JJ' or word[l] == 'RB' or word[1] == 'RBR')]

        for site in sites:
            with urllib.request.urlopen('https://api.majestic.com/api/json?app_api_key='+m_key+'&cmd=GetTopics&item='+site+'&datasource=fresh&count=10') as url:
                data = json.loads(url.read().decode())
                topics = data['DataTables']['Topics']['Data']
            for topic in topics:
                print(topic['Topic'])
                print('Computer' in topic['Topic'])
                if 'Computer' in topic['Topic']:
                    print(topic['TopicalTrustFlow'])
                    meme_score += topic['TopicalTrustFlow']
        text = 'Your meme score was ' + str(meme_score)
        if meme_score > high_score:
            top_player = msisdn
            text += '\nThat\'s a new high score!'
        
        response = client.send_message({'from': 'Meme Score', 'to': msisdn, 'text': text})
        response = response['messages'][0]

        if response['status'] == '0':
            print('Sent message', response['message-id'])
            print('Remaining balance is', response['remaining-balance'])
        else:
            print('Error:', response['error-text'])
                
    return ('ok', 200)


if __name__ == "__main__":
    app.run()
