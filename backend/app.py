import json
import random
from flask_cors import CORS
from flask import Flask, jsonify, send_from_directory
import os

# config the build folder path
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

# ...您的其他API端点代码...

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
    data = [
        { "name": "Melbourne", "latlng": [-37.8136, 144.9631] },
        { "name": "Sydney", "latlng": [-33.8688, 151.2093] },
        { "name": "Adelaide", "latlng": [-34.9285, 138.6007] },
        { "name": "Perth", "latlng": [-31.9505, 115.8605] },
        { "name": "Brisbane", "latlng": [-27.4698, 153.0251] }
    ]
    return jsonify(data)

@app.route('/api/statemap-data')
def get_state_data():
    data = [
        {"name": "New South Wales", "value": 730000000},
        {"name": "Queensland", "value": 5800000},
        {"name": "South Australia", "value": 1700000},
        {"name": "Tasmania", "value": 500000},
        {"name": "Victoria", "value": 6500000},
        {"name": "Western Australia", "value": 2500000},
        {"name": "Australian Capital Territory", "value": 400000},
        {"name": "Northern Territory", "value": 250000}
    ]
    return jsonify(data)

# @app.route('/api/histogram-data')
# def get_histogram_data():
#
#     data = [
#         ['score', 'amount', 'product'],
#         [89.3, 58212, 'Matcha Latte'],
#         [57.1, 78254, 'Milk Tea'],
#         [74.4, 41032, 'Cheese Cocoa'],
#         [50.1, 12755, 'Cheese Brownie'],
#         [89.7, 20145, 'Matcha Cocoa'],
#         [68.1, 79146, 'Tea'],
#         [19.6, 91852, 'Orange Juice'],
#         [10.6, 101852, 'Lemon Juice'],
#         [32.7, 20112, 'Walnut Brownie']
#     ]
#     return jsonify(data)

@app.route('/api/histogram-data')
def get_histogram_data():
    with open('../data/moData.json', 'r') as f:
        data = f.read()

    # 将JSON数据转换为Python对象
    data = json.loads(data)
    max_val = max(data, key=lambda i: i['value'])['value']

    res = []
    for d in data:
        tmp = []
        tmp.append(d['value'] / max_val * 100)
        tmp.append(d['value'])
        tmp.append(d['x'])
        res.append(tmp)
    res=sorted(res[1:],key=lambda i:i[1],reverse=True)[:50]
    res.insert(0,['score', 'amount', 'product'])

    return jsonify(res)

@app.route('/api/pie-data')
def get_pie_data():
    with open('../data/moData.json', 'r') as f:
        data = f.read()

    # 将JSON数据转换为Python对象
    data = json.loads(data)
    # max_val = max(data, key=lambda i: i['value'])['value']

    res = []
    for d in data:
        tmp = {}
        tmp['value']=d['value']
        tmp['name']=d['x']
        res.append(tmp)
    res = sorted(res[:], key=lambda i: i['value'], reverse=True)[:10]

    data = [
        { 'value': 40, 'name': 'rose 1' },
        { 'value': 38, 'name': 'rose 2' },
        { 'value': 32, 'name': 'rose 3' },
        { 'value': 30, 'name': 'rose 4' },
        { 'value': 28, 'name': 'rose 5' },
        { 'value': 26, 'name': 'rose 6' },
        { 'value': 22, 'name': 'rose 7' },
        { 'value': 18, 'name': 'rose 8' }
    ]
    return jsonify(res)


@app.route('/api/wordcloud-data')
def get_wordcloud_data():
    # 从文件中读取JSON数据
    with open('../data/moData.json', 'r') as f:
        data = f.read()

    # 将JSON数据转换为Python对象
    data = json.loads(data)

    # 返回JSON数据
    return jsonify(data)

@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

#     pip freeze > requirements.txt
