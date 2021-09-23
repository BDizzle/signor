from flask import Flask, json, request, abort, jsonify
from aws_requests_auth.aws_auth import AWSRequestsAuth
from requests import Request

app = Flask(__name__)

@app.route('/sign', methods=['POST'])
def validate_request():
  data = request.json
  if 'ACCESS_KEY' not in data:
    abort(400, description='missing ACCESS_KEY')
  elif 'SECRET_ACCESS_KEY' not in data:
    abort(400, description='missing SECRET_ACCESS_KEY')
  elif 'SESSION_TOKEN' not in data:
    abort(400, description='missing SESSION_TOKEN')
  elif 'HOST' not in data:
    abort(400, description='missing HOST')
  elif 'REGION' not in data:
    abort(400, description='missing REGION')
  elif 'SERVICE' not in data:
    abort(400, description='missing SERVICE')
  else:
    return sign_request(), 200, {'Content-Type': 'application/json; charset=utf-8'}


#return errors as JSON, otherwise it would be HTML
@app.errorhandler(400)
def bad_request(message):
  return jsonify(error=str(message)), 400

def sign_request():
    data = request.json
    auth = AWSRequestsAuth( aws_access_key=data['ACCESS_KEY'],
                            aws_secret_access_key=data['SECRET_ACCESS_KEY'],
                            aws_token=data['SESSION_TOKEN'],
                            aws_host=data['HOST'],
                            aws_region=data['REGION'],
                            aws_service=data['SERVICE']
                            )

    #need to create an actual request in order to generate the headers, we do NOT actually send this request
    req = Request('GET', data['HOST'], auth=auth)
    prepared = req.prepare();

    #convert the CaseInsensitiveDict that AWSRequestAuth gives us into a regular dict so that it can be serialized as JSON
    headers = dict(prepared.headers);

    #add hyphen-less versions of headers that have hyphens in their name
    headers["XAmzSecurityToken"] = headers["X-Amz-Security-Token"]
    headers["xamzcontentsha256"] = headers["x-amz-content-sha256"]
    headers["xamzdate"] = headers["x-amz-date"]

    return json.dumps(headers);

if __name__ == '__main__':
    app.run() 