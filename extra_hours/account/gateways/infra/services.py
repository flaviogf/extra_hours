import requests


class FirebaseUserService:
    def sign_with_email_and_password(self, email, password):
        url_api = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={}'

        data = {
            'email': email,
            'password': password,
        }

        response = requests.post(url_api.format('AIzaSyBSutdXuiHNq9JqSkN8Zqx9EpAhcQY7g9M'), data=data)

        if response.status_code != 200:
            return

        return response.json()['idToken']
