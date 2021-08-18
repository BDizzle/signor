from flask import Flask, json, request, abort
from aws_requests_auth.aws_auth import AWSRequestsAuth
from requests import Request

companies = [{"id": 1, "name": "Company One"}, {"id": 2, "name": "Company Two"}]

app = Flask(__name__)

@app.route('/')
def index():
  return json.dumps({'hello': 'world'})

@app.route('/sign', methods=['POST'])
def validate_request():
  if request.form['ACCESS_KEY'] == None:
    abort(400, 'missing ACCESS_KEY')
  elif request.form['SECRET_ACCESS_KEY'] == None:
    abort(400, 'missing SECRET_ACCESS_KEY')
  elif request.form['SESSION_TOKEN'] == None:
    abort(400, 'missing SESSION_TOKEN')
  else:
    return sign_request(request.form['ACCESS_KEY'], request.form['SECRET_ACCESS_KEY'])

def sign_request(access_key, secret_key):
    auth = AWSRequestsAuth( aws_access_key=request.form['ACCESS_KEY'],
                            aws_secret_access_key=request.form['SECRET_ACCESS_KEY'],
                            aws_host='foo',
                            aws_region='bar',
                            aws_service='baz'
                            )
    req = Request('GET', 'https://url.com', auth=auth)
    prepared = req.prepare();

    print(prepared.headers)

    return json.dumps(dict(prepared.headers));


if __name__ == '__main__':
    app.run() 