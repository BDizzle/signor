import unittest
import sys

sys.path.insert(0, '..')

from signor.src import app as flask

def sign_request(self, data):
	return self.app.post('/sign', data=data, follow_redirects=True)


class Tests(unittest.TestCase):

	def setUp(self):
		flask.app.config['TESTING'] = True
		flask.app.config['WTF_CSRF_ENABLED'] = False
		self.app = flask.app.test_client()
		return

	def tearDown(self):
		pass

	def test_missing_access_key(self):
		response = sign_request(self, dict())
		self.assertEqual(response.status_code, 400, 'ACCESS_KEY is required')

	def test_missing_secret_access_key(self):
		response = sign_request(self, dict(
			ACCESS_KEY='foo'
		))
		self.assertEqual(response.status_code, 400, 'SECRET_ACCESS_KEY is required')

	def test_missing_session_token(self):
		response = sign_request(self, dict(
			ACCESS_KEY='foo',
			SECRET_ACCESS_KEY='bar'
		))
		self.assertEqual(response.status_code, 400, 'SESSION_TOKEN is required')

	def test_with_all_required_credentials(self):
		response = sign_request(self, dict(
			ACCESS_KEY='foo',
			SECRET_ACCESS_KEY='bar',
			SESSION_TOKEN='baz'
		))
		self.assertEqual(response.status_code, 200)



if __name__ == "__main__":
	unittest.main()

