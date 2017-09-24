import urllib.request, json
import nltk


sent = 'this is an  example sentence; not that original'
sent = nltk.word_tokenize(sent)
sent = nltk.pos_tag(sent)

sites = [word[0] + '.com' for word in sent if word[1] == 'NN']
print(sites)

meme_score = 0

with urllib.request.urlopen('https://api.majestic.com/api/json?app_api_key=8672807C37B327B1F5FD871D82233D9A&cmd=GetTopics&item=majestic.com&datasource=fresh&count=10') as url:
    data = json.loads(url.read().decode())
    #print(data)
    topics = data['DataTables']['Topics']['Data']
    print (topics)
    for topic in topics:
        print(topic['Topic'])
        print('Computer' in topic['Topic'])
        if 'Computer' in topic['Topic']:
            print(topic['TopicalTrustFlow'])
            meme_score += topic['TopicalTrustFlow']
print(meme_score)

with urllib.request.urlopen('https://developer.majestic.com/api/json?app_api_key=8672807C37B327B1F5FD871D82233D9A&cmd=GetIndexItemInfo&items=1&item0=http://www.surrenderat20.net&datasource=fresh') as url:
    data = json.loads(url.read().decode())
    topics = data['DataTables']['Results']['Data'][0]
    topic1 = topics['TopicalTrustFlow_Topic_0']
    if 'Computer' in topic1:
        meme_score += topics['TopicalTrustFlow_Value_0']
    topic2 = topics['TopicalTrustFlow_Topic_1']
    if 'Computer' in topic2:
        meme_score += topics['TopicalTrustFlow_Value_1']
    topic3 = topics['TopicalTrustFlow_Topic_2']
    if 'Computer' in topic3:
        meme_score += topics['TopicalTrustFlow_Value_2']

print(meme_score)
    
