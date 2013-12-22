import sys, os
# append parent directory to PYTHONPATH so imports work
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
import flaskberry
import unittest
from nose.tools import assert_equal, assert_true, assert_in

class FlaskberryTestCase(unittest.TestCase):

    def setUp(self):
        self.app = flaskberry.app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        assert_in("Welcome", rv.data)
        assert_equal(rv.status, '200 OK')

    def test_system_page(self):
        rv = self.app.get('/system/')
        assert_in("System", rv.data)
        assert_in("Load Average", rv.data)
        assert_in("Shutdown", rv.data)
        assert_in("Reboot", rv.data)

    # testing disk module requires sudo
    def test_disks_page(self):
        rv = self.app.get('/disks/')
        assert_in("Disks", rv.data)
        assert_in("Unmount", rv.data)

if __name__ == '__main__':
    unittest.main()
