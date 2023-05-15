import json
import random
from flask_cors import CORS
from flask import Flask, jsonify, send_from_directory
import os
import requests

if os.environ["DEV"] == "true":
    url_prefix = "http://admin:666@couchdb-app-172-26-135-249.nip.io"
else:
    url_prefix = "http://couch-1-couchdb:5984"


state_mapping = {
    'default': "New South Wales",
    'western australia': "Western Australia",
    'new south wales': "New South Wales",
    'northern territory': "Northern Territory",
    'tasmania': "Tasmania",
    'victoria': "Victoria",
    'queensland': "Queensland",
    'australian capital territory': "Australian Capital Territory",
    'south australia': "South Australia"
}

params = {
    'reduce': 'true',
    'group_level': '1'
}
auth = ('admin', '666')

# heatmap_url = os.environ['HEATMAP_URL']
# income_heatmap_url = os.environ['INCOME_HEATMAP_URL']
# transport_heatmap_url = os.environ['TRANSPORT_HEATMAP_URL']

# state_avg_sentiment_url = os.environ['STATE_AVG_SENTIMENT_URL']
# income_state_avg_sentiment_url = os.environ['INCOME_STATE_AVG_SENTIMENT_URL']
# transport_state_avg_sentiment_url = os.environ['TRANSPORT_STATE_AVG_SENTIMENT_URL']

# token_count_url = os.environ['TOKEN_COUNT_URL']
# income_token_count_url = os.environ['INCOME_TOKEN_COUNT_URL']
# transport_token_count_url = os.environ['TRANSPORT_TOKEN_COUNT_URL']

# pie_data_url = os.environ['PIE_DATA_URL']
# income_pie_data_url = os.environ['INCOME_PIE_DATA_URL']
# transport_pie_data_url = os.environ['TRANSPORT_PIE_DATA_URL']

# wordcloud_data_url = os.environ['WORDCLOUD_DATA_URL']
# income_wordcloud_data_url = os.environ['INCOME_WORDCLOUD_DATA_URL']
# transport_wordcloud_data_url = os.environ['TRANSPORT_WORDCLOUD_DATA_URL']


# 合并URL和路由
heatmap_url = url_prefix + "/test_housing_twitter/_design/full/_view/location_point"
income_heatmap_url = url_prefix + "/test_income_twitter/_design/full/_view/location_point"
transport_heatmap_url = url_prefix + "/test_transport_twitter/_design/full/_view/location_point"

state_avg_sentiment_url = url_prefix + "/test_housing_twitter/_design/full/_view/state_avg_sentiment"
income_state_avg_sentiment_url = url_prefix + "/test_income_twitter/_design/full/_view/state_avg_sentiment"
transport_state_avg_sentiment_url = url_prefix + "/test_transport_twitter/_design/full/_view/state_avg_sentiment"

token_count_url = url_prefix + "/test_housing_twitter/_design/full/_view/token_count"
income_token_count_url = url_prefix + "/test_income_twitter/_design/full/_view/token_count"
transport_token_count_url = url_prefix + "/test_transport_twitter/_design/full/_view/token_count"

pie_data_url = url_prefix + "/test_housing_twitter/_design/full/_view/token_count"
income_pie_data_url = url_prefix + "/test_income_twitter/_design/full/_view/token_count"
transport_pie_data_url = url_prefix + "/test_transport_twitter/_design/full/_view/token_count"

wordcloud_data_url = url_prefix + "/test_housing_twitter/_design/full/_view/token_count"
income_wordcloud_data_url = url_prefix + "/test_income_twitter/_design/full/_view/token_count"
transport_wordcloud_data_url = url_prefix + "/test_transport_twitter/_design/full/_view/token_count"

# config the build1 folder path
app = Flask(__name__, static_folder="../frontend/build")
CORS(app)

"""
@app.route("/", defaults={"path": ""}) and @app.route("/<path:path>") 
are used to serve the React app's index.html file for any route requested by the user.
React's Single Page Application (SPA) is responsible for handling these routes.
<path:path> is a variable representing the requested path. 
defaults={"path": ""} indicates that when the user visits the root path (/), the default path is an empty string.
"""
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(app.static_folder + "/" + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")



@app.route('/api/bar-data')
def get_bar_data():
    # 50个和经济有关的英语名词
    words = [
        'Inflation', 'Deflation', 'Recession', 'Depression', 'Stagflation',
        'Boom', 'Bust', 'Growth', 'Development', 'Expansion',
        'Contraction', 'Fiscal policy', 'Monetary policy', 'Interest rates', 'Exchange rates',
        'Taxation', 'Subsidy', 'Tariff', 'Quota', 'Embargo'
    ]
    # 随机生成每个词对应的数值（0-100）
    data = {word: random.randint(0, 100) for word in words}
    print(data)
    return jsonify(list(data.items()))
@app.route('/api/heatmap-data')
def get_heatmap_data():
    url = heatmap_url

    response = requests.get(url, params=params, auth=auth)

    if response.status_code == 200:
        data = response.json()
        rows = data['rows']
        print(rows[:5])
    data=[]
    for i in rows:
        tmp={}
        tmp['name']=i['key']
        tmp['latlng']=i['value']
        data.append(tmp)
    return jsonify(data)
@app.route('/api/income/heatmap-data')
def get_income_heatmap_data():
    url = income_heatmap_url

    response = requests.get(url, params=params, auth=auth)

    if response.status_code == 200:
        data = response.json()
        rows = data['rows']
        print(rows[:5])
    data=[]
    for i in rows:
        tmp={}
        tmp['name']=i['key']
        tmp['latlng']=i['value']
        data.append(tmp)
    return jsonify(data)
@app.route('/api/transport/heatmap-data')
def get_transport_heatmap_data():
    url = transport_heatmap_url

    response = requests.get(url, params=params, auth=auth)

    if response.status_code == 200:
        data = response.json()
        rows = data['rows']
        print(rows[:5])
    data=[]
    for i in rows:
        tmp={}
        tmp['name']=i['key']
        tmp['latlng']=i['value']
        data.append(tmp)
    return jsonify(data)
@app.route('/api/statemap-data')
def get_state_data():
    url = state_avg_sentiment_url

    response = requests.get(url, params=params, auth=auth)

    if response.status_code == 200:
        data = response.json()
        rows = data['rows']
        rows.sort(key=lambda x: x['value'], reverse=True)
        top30 = rows[:30]
        print(top30)
    else:
        print('Request failed with status code:', response.status_code)
    print(top30)
    data=[]
    for i in top30:
        tmp={}
        tmp['name']=state_mapping[i['key']]
        tmp['value']=(i['value'][0])
        data.append(tmp)
    print(data)
    return jsonify(data)
@app.route('/api/income/statemap-data')
def get_income_state_data():
    url = income_state_avg_sentiment_url

    response = requests.get(url, params=params, auth=auth)

    if response.status_code == 200:
        data = response.json()
        rows = data['rows']
        rows.sort(key=lambda x: x['value'], reverse=True)
        top30 = rows[:30]
    else:
        print('Request failed with status code:', response.status_code)
    data=[]
    for i in top30:
        tmp={}
        tmp['name']=state_mapping[i['key']]
        tmp['value']=(i['value'][0])
        data.append(tmp)
    return jsonify(data)
@app.route('/api/transport/statemap-data')
def get_transport_state_data():
    url = transport_state_avg_sentiment_url

    response = requests.get(url, params=params, auth=auth)

    if response.status_code == 200:
        data = response.json()
        rows = data['rows']
        rows.sort(key=lambda x: x['value'], reverse=True)
        top30 = rows[:30]
    else:
        print('Request failed with status code:', response.status_code)
    data=[]
    for i in top30:
        tmp={}
        tmp['name']=state_mapping[i['key']]
        tmp['value']=(i['value'][0])
        data.append(tmp)
    return jsonify(data)
@app.route('/api/histogram-data')
def get_histogram_data():

    url = token_count_url

    response = requests.get(url, params=params, auth=auth)

    if response.status_code == 200:
        data = response.json()
        rows = data['rows']
        rows.sort(key=lambda x: x['value'], reverse=True)
        top30 = rows[60:120]
    else:
        print('Request failed with status code:', response.status_code)

    # 将JSON数据转换为Python对象
    data = top30
    max_val = max(data, key=lambda i: i['value'])['value']

    res = []
    for d in data:
        tmp = []
        tmp.append(d['value'] / max_val * 100)
        tmp.append(d['value'])
        tmp.append(d['key'])
        res.append(tmp)
    res=sorted(res[1:],key=lambda i:i[1],reverse=True)
    res.insert(0,['score', 'amount', 'product'])

    return jsonify(res)
@app.route('/api/income/histogram-data')
def get_income_histogram_data():
    url = income_token_count_url

    response = requests.get(url, params=params, auth=auth)

    if response.status_code == 200:
        data = response.json()
        rows = data['rows']
        rows.sort(key=lambda x: x['value'], reverse=True)
        top30 = rows[60:120]
    else:
        print('Request failed with status code:', response.status_code)

    # 将JSON数据转换为Python对象
    data = top30
    max_val = max(data, key=lambda i: i['value'])['value']

    res = []
    for d in data:
        tmp = []
        tmp.append(d['value'] / max_val * 100)
        tmp.append(d['value'])
        tmp.append(d['key'])
        res.append(tmp)
    res=sorted(res[1:],key=lambda i:i[1],reverse=True)
    res.insert(0,['score', 'amount', 'product'])

    return jsonify(res)
@app.route('/api/transport/histogram-data')
def get_transport_histogram_data():
    url = transport_token_count_url

    response = requests.get(url, params=params, auth=auth)

    if response.status_code == 200:
        data = response.json()
        rows = data['rows']
        rows.sort(key=lambda x: x['value'], reverse=True)
        top30 = rows[60:120]
    else:
        print('Request failed with status code:', response.status_code)

    # 将JSON数据转换为Python对象
    data = top30
    max_val = max(data, key=lambda i: i['value'])['value']

    res = []
    for d in data:
        tmp = []
        tmp.append(d['value'] / max_val * 100)
        tmp.append(d['value'])
        tmp.append(d['key'])
        res.append(tmp)
    res=sorted(res[1:],key=lambda i:i[1],reverse=True)
    res.insert(0,['score', 'amount', 'product'])

    return jsonify(res)
@app.route('/api/pie-data')
def get_pie_data():
    url = pie_data_url

    response = requests.get(url, params=params, auth=auth)

    if response.status_code == 200:
        data = response.json()
        rows = data['rows']
        rows.sort(key=lambda x: x['value'], reverse=True)
        top30 = rows[90:120]
    else:
        print('Request failed with status code:', response.status_code)

    # 将JSON数据转换为Python对象
    data = top30
    # max_val = max(data, key=lambda i: i['value'])['value']

    res = []
    for d in data:
        tmp = {}
        tmp['value']=d['value']
        tmp['name']=d['key']
        res.append(tmp)
    res = sorted(res[:], key=lambda i: i['value'], reverse=True)[:10]

    return jsonify(res)
@app.route('/api/income/pie-data')
def get_income_pie_data():
    url = income_pie_data_url

    response = requests.get(url, params=params, auth=auth)

    if response.status_code == 200:
        data = response.json()
        rows = data['rows']
        rows.sort(key=lambda x: x['value'], reverse=True)
        top30 = rows[90:120]
    else:
        print('Request failed with status code:', response.status_code)

    # 将JSON数据转换为Python对象
    data = top30
    # max_val = max(data, key=lambda i: i['value'])['value']

    res = []
    for d in data:
        tmp = {}
        tmp['value']=d['value']
        tmp['name']=d['key']
        res.append(tmp)
    res = sorted(res[:], key=lambda i: i['value'], reverse=True)[:10]

    return jsonify(res)
@app.route('/api/transport/pie-data')
def get_transport_pie_data():
    url = transport_pie_data_url

    response = requests.get(url, params=params, auth=auth)

    if response.status_code == 200:
        data = response.json()
        rows = data['rows']
        rows.sort(key=lambda x: x['value'], reverse=True)
        top30 = rows[90:120]
    else:
        print('Request failed with status code:', response.status_code)

    # 将JSON数据转换为Python对象
    data = top30
    # max_val = max(data, key=lambda i: i['value'])['value']

    res = []
    for d in data:
        tmp = {}
        tmp['value']=d['value']
        tmp['name']=d['key']
        res.append(tmp)
    res = sorted(res[:], key=lambda i: i['value'], reverse=True)[:10]

    return jsonify(res)
@app.route('/api/wordcloud-data')
def get_wordcloud_data():
    url = wordcloud_data_url

    response = requests.get(url, params=params, auth=auth)

    if response.status_code == 200:
        data = response.json()
        rows = data['rows']
        rows.sort(key=lambda x: x['value'], reverse=True)
        top30 = rows[60:120]
    else:
        print('Request failed with status code:', response.status_code)

    return jsonify(top30)
@app.route('/api/income/wordcloud-data')
def get_income_wordcloud_data():
    url = income_wordcloud_data_url

    response = requests.get(url, params=params, auth=auth)

    if response.status_code == 200:
        data = response.json()
        rows = data['rows']
        rows.sort(key=lambda x: x['value'], reverse=True)
        top30 = rows[60:120]
    else:
        print('Request failed with status code:', response.status_code)

    return jsonify(top30)
@app.route('/api/transport/wordcloud-data')
def get_transport_wordcloud_data():
    url = transport_wordcloud_data_url

    response = requests.get(url, params=params, auth=auth)

    if response.status_code == 200:
        data = response.json()
        rows = data['rows']
        rows.sort(key=lambda x: x['value'], reverse=True)
        top30 = rows[60:120]
    else:
        print('Request failed with status code:', response.status_code)

    return jsonify(top30)
@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

#     pip freeze > requirements.txt
