import unittest

from store import Store


class StoreTest(unittest.TestCase):

    def setUp(self):
        self.store = Store()

    def test_set_with_retry(self):
        with self.assertLogs(level='INFO') as cm:
            with self.assertRaises(Exception) as exp:
                self.store.set_with_retry('key', 'value')

        self.assertTrue('Connection refused' in str(exp.exception))
        self.assertTrue('Retrying in' in '\n'.join(cm.output))

    def test_get_with_retry(self):
        with self.assertLogs(level='INFO') as cm:
            with self.assertRaises(Exception) as exp:
                self.store.get_with_retry('key')

        self.assertTrue('Connection refused' in str(exp.exception))
        self.assertTrue('Retrying in' in '\n'.join(cm.output))
