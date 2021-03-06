# -*- encoding: utf-8 -*-
import unittest

import requests
import json

URL = "http://121.199.9.187:8081/object_storage"
session = requests.session()

container = "cloudgatetestcon"
test_ob_container = "cloudgatetest"
object_test = "config.py"

class ObjectStorageTest(unittest.TestCase):
    def printJson(self, s):
        b = json.loads(s)
        print json.dumps(b, indent=4)

    def setUp(self):
        pass

    def tearDown(self):
        session.close()

    def test_example(self):
        pass

    def test_createContainer(self):
        response = session.put(URL + "/v1/tenant_id/" + container)
        print response.text

    def test_listContainers(self):
        response = session.get(URL + "/v1/tenant_id")
        self.printJson(response.text)

    def test_deleteContainer(self):
        response = session.delete(URL + "/v1/tenant_id/" + container)

    def test_listObjects(self):
        response = session.get(URL + "/v1/tenant_id/" + test_ob_container)
        self.printJson(response.text)

    def test_deleteObject(self):
        response = session.delete(URL + "/v1/tenant_id/" + test_ob_container + "/" + object_test)
        print response

    def test_copyObject(self):
        pass

    def test_createObject(self):
        pass

if __name__ == '__main__':
    unittest.main()
