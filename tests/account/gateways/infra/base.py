import unittest
from os.path import dirname, join

import firebase_admin
from firebase_admin import credentials


class InfraTestCase(unittest.TestCase):
    _app = None

    @classmethod
    def setUpClass(cls):
        root_path = dirname(dirname(dirname(dirname(dirname(__file__)))))

        certificate_path = join(root_path, '.firebase.json')

        cred = credentials.Certificate(certificate_path)

        InfraTestCase._app = firebase_admin.initialize_app(cred)

    @classmethod
    def tearDownClass(cls):
        firebase_admin.delete_app(InfraTestCase._app)
