import unittest
from pyramid.config import Configurator
from pyramid import testing

def _initTestingDB():
    from sqlalchemy import create_engine
    from papyrussample.models import initialize_sql
    session = initialize_sql(create_engine('sqlite://'))
    return session

class TestMyView(unittest.TestCase):
    def setUp(self):
        self.config = Configurator(autocommit=True)
        self.config.begin()
        _initTestingDB()

    def tearDown(self):
        self.config.end()

    def test_it(self):
        from papyrussample.views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['root'].name, 'root')
        self.assertEqual(info['project'], 'PapyrusSample')
