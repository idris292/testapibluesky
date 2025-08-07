# app.py
from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

# Auth
@app.route('/auth', methods=['POST'])
def auth_user():
    data = request.json
    res = requests.post("https://bsky.social/xrpc/com.atproto.server.createSession", json={
        "identifier": data['identifier'],
        "password": data['password']
    })
    return jsonify(res.json()), res.status_code

# add
@app.route('/post', methods=['POST'])
def post_message():
    data = request.json
    headers = {
        "Authorization": f"Bearer {data['access_token']}"
    }
    payload = {
        "repo": data['repo'],
        "collection": "app.bsky.feed.post",
        "record": {
            "text": data['text'],
            "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
    }
    res = requests.post("https://bsky.social/xrpc/com.atproto.repo.createRecord", headers=headers, json=payload)
    return jsonify(res.json()), res.status_code

# list
@app.route('/posts', methods=['GET'])
def get_user_posts():
    handle = request.args.get('handle')
    limit = request.args.get('limit', 100)
    access_token = request.headers.get('Authorization')

    headers = {}
    if access_token:
        headers['Authorization'] = access_token

    res = requests.get(
        f"https://bsky.social/xrpc/app.bsky.feed.getAuthorFeed?actor={handle}&limit={limit}",
        headers=headers
    )
    return jsonify(res.json()), res.status_code
# delete
@app.route('/delete-post', methods=['POST'])
def delete_post():
    data = request.json
    headers = {
        "Authorization": f"Bearer {data['access_token']}"
    }
    payload = {
        "repo": data['repo'],  # DID
        "collection": "app.bsky.feed.post",
        "rkey": data['rkey']   # ID unique du post
    }
    res = requests.post("https://bsky.social/xrpc/com.atproto.repo.deleteRecord", headers=headers, json=payload)
    return jsonify(res.json()), res.status_code


if __name__ == '__main__':
    app.run(debug=True)
