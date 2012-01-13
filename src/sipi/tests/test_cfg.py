"""
    sipi.cfg unit testing
"""

import unittest

import sipi.cfg as cfg
import sipi.tools_os as tos

class TestCfgJSON(unittest.TestCase):

    JSONFILE="/tmp/~jsonfile.json"

    def setUp(self):
        tos.rm(self.JSONFILE)
        tos.quick_write(self.JSONFILE, '''{"param2":"value2"}''')
        cfg.filename=self.JSONFILE

    def test_which(self):
        code, r=cfg.which()
        
        self.assertEqual(code, 'filename')
        self.assertEqual(r, self.JSONFILE)

        # should raise an exception for an immutable sequence
        #self.assertRaises(TypeError, random.shuffle, (1,2,3))

    def test_get1(self):
        code, value=cfg.get("param2")
        
        self.assertEqual(code, "ok")
        self.assertEqual(cfg._last_exception, None)
        self.assertEqual(value, "value2")

    def tearDown(self):
        tos.rm(self.JSONFILE)
        

class TestCfgYAML(unittest.TestCase):

    YAMLFILE="/tmp/~yamlfile.yaml"

    DATA='''
    param2:
        value2
        
    param3:
        value3        
    '''

    def setUp(self):
        tos.rm(self.YAMLFILE)
        tos.quick_write(self.YAMLFILE, self.DATA)
        cfg.filename=self.YAMLFILE

    def test_which(self):
        code, r=cfg.which()
        
        self.assertEqual(code, 'filename')
        self.assertEqual(r, self.YAMLFILE)

        # should raise an exception for an immutable sequence
        #self.assertRaises(TypeError, random.shuffle, (1,2,3))

    def test_get1(self):
        code, value=cfg.get("param2")
        
        self.assertEqual(code, "ok")
        self.assertEqual(cfg._last_exception, None)
        self.assertEqual(value, "value2")

    def test_get2(self):
        code, value=cfg.get("param3")
        
        self.assertEqual(code, "ok")
        self.assertEqual(cfg._last_exception, None)
        self.assertEqual(value, "value3")

    def tearDown(self):
        tos.rm(self.YAMLFILE)


if __name__ == '__main__':
    unittest.main()
