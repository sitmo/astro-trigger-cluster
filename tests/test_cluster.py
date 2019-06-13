import unittest
import astrotc as atc


class TestCluster(unittest.TestCase):

    def setUp(self):
        self.cluster = atc.Cluster(atc.apertif)

    def test_config_name(self):
        self.assertEqual(self.cluster.config.name, 'apertif')


if __name__ == '__main__':
    unittest.main()
