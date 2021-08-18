from flask import Flask, json, request, abort, jsonify
from aws_requests_auth.aws_auth import AWSRequestsAuth
from requests import Request

app = Flask(__name__)

@app.route('/sign', methods=['POST'])
def validate_request():
  if 'ACCESS_KEY' not in request.form:
    abort(400, description='missing ACCESS_KEY')
  elif 'SECRET_ACCESS_KEY' not in request.form:
    abort(400, description='missing SECRET_ACCESS_KEY')
  elif 'SESSION_TOKEN' not in request.form:
    abort(400, description='missing SESSION_TOKEN')
  elif 'HOST' not in request.form:
    abort(400, description='missing HOST')
  elif 'REGION' not in request.form:
    abort(400, description='missing REGION')
  elif 'SERVICE' not in request.form:
    abort(400, description='missing SERVICE')
  else:
    return sign_request(), 200, {'Content-Type': 'application/json; charset=utf-8'}


#return errors as JSON, otherwise it would be HTML
@app.errorhandler(400)
def bad_request(message):
  return jsonify(error=str(message)), 400

def sign_request():
    host = request.form['HOST']
    auth = AWSRequestsAuth( aws_access_key=request.form['ACCESS_KEY'],
                            aws_secret_access_key=request.form['SECRET_ACCESS_KEY'],
                            aws_token=request.form['SESSION_TOKEN'],
                            aws_host=host,
                            aws_region=request.form['REGION'],
                            aws_service=request.form['SERVICE']
                            )

    #need to create an actual request in order to generate the headers, we do NOT actually send this request
    req = Request('GET', host, auth=auth)
    prepared = req.prepare();

    #convert the CaseInsensitiveDict that AWSRequestAuth gives us into a regular dict so that it can be serialized as JSON
    return json.dumps(dict(prepared.headers));

if __name__ == '__main__':
    app.run() 