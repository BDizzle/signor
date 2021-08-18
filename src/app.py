from flask import Flask, json, request, abort, make_response, jsonify
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
    abort(make_response(jsonify(message='missing ACCESS_KEY', 400)))
  elif request.form['SECRET_ACCESS_KEY'] == None:
    abort(400, 'missing SECRET_ACCESS_KEY')
  elif request.form['SESSION_TOKEN'] == None:
    abort(400, 'missing SESSION_TOKEN')
  elif request.form['HOST'] == None:
    abort(400, 'missing HOST')
  elif request.form['REGION'] == None:
    abort(400, 'missing REGION')
  elif request.form['SERVICE'] == None:
    abort(400, 'missing SERVICE')
  else:
    return sign_request(request.form['ACCESS_KEY'], request.form['SECRET_ACCESS_KEY'])

def sign_request(access_key, secret_key):
    host = request.form['HOST']
    auth = AWSRequestsAuth( aws_access_key=request.form['ACCESS_KEY'],
                            aws_secret_access_key=request.form['SECRET_ACCESS_KEY'],
                            aws_token=request.form['SESSION_TOKEN'],
                            aws_host=host,
                            aws_region=request.form['REGION'],
                            aws_service=request.form['SERVICE']
                            )
    req = Request('GET', host, auth=auth)
    prepared = req.prepare();

    #convert the CaseInsensitiveDict that AWSRequestAuth gives us into a regular dict so that it can be serialized as JSON
    return json.dumps(dict(prepared.headers));


if __name__ == '__main__':
    app.run() 