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

	def test_missing_host(self):
		response = sign_request(self, dict(
			ACCESS_KEY='foo',
			SECRET_ACCESS_KEY='bar',
			SESSION_TOKEN='baz'
		))
		self.assertEqual(response.status_code, 400, 'HOST is required')

	def test_missing_region(self):
		response = sign_request(self, dict(
			ACCESS_KEY='foo',
			SECRET_ACCESS_KEY='bar',
			SESSION_TOKEN='baz',
			HOST='https://hosty.mchostface'
		))
		self.assertEqual(response.status_code, 400, 'REGION is required')

	def test_missing_service(self):
		response = sign_request(self, dict(
			ACCESS_KEY='foo',
			SECRET_ACCESS_KEY='bar',
			SESSION_TOKEN='baz',
			HOST='https://hosty.mchostface',
			REGION='yes'
		))
		self.assertEqual(response.status_code, 400, 'SERVICE is required')

	def test_valid_request(self):
		response = sign_request(self, dict(
			ACCESS_KEY='foo',
			SECRET_ACCESS_KEY='bar',
			SESSION_TOKEN='baz',
			HOST='https://hosty.mchostface',
			REGION='yes',
			SERVICE='please'
		))
		self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
	unittest.main()

