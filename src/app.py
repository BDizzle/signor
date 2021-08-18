from flask import Flask, json, request, abort

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
    return json.dumps(companies)

if __name__ == '__main__':
    app.run() 