# -*- coding: UTF-8 -*-
from app.test.base_test import BaseTestCase
from app import app, db
from app.models import User, Messages
from app.forum.models import Forum, ForumRole

import unittest
import pickle
import random, json


class ForumTest(BaseTestCase):

    def test_a_post(self):
        self.begin("POST", "/   ")
        d = {}
        with open("./app/test/.cache", "rb") as f:
            d = pickle.load(f)

        response = self.app.post('/forum/', data = json.dumps({"title":"Test", "content":"This is a test!"}))
        ret = response.data.decode('utf8')
        print (ret)
        self.assertEquals(ret, "Unauthorized Access")

        response = self.app.post('/forum/', headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "invalid request")

        response = self.app.post('/forum/', headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({"title":"Test", "content":"This is a test!"}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")

        d["id"] = ret["id"]
        with open("./app/test/.cache", "wb") as f:
            pickle.dump(d, f)


    def test_b_get(self):
        self.begin("GET", "/   ")
        d = {}
        with open("./app/test/.cache", "rb") as f:
            d = pickle.load(f)

        response = self.app.get('/forum/', headers = {"Authorization":"Bearer "+d["token"]})
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")


    def test_c_get_id(self):
        self.begin("GET", "/id")
        d = {}
        with open("./app/test/.cache", "rb") as f:
            d = pickle.load(f)

        response = self.app.get('/forum/'+str(d["id"]))
        ret = response.data.decode('utf8')
        print (ret)
        self.assertEquals(ret, "Unauthorized Access")

        response = self.app.get('/forum/'+str(random.randint(100000, 999999)), headers = {"Authorization":"Bearer "+d["token"]})
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "post not found")

        response = self.app.get('/forum/'+str(d["id"]), headers = {"Authorization":"Bearer "+d["token"]})
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")


    def test_d_put_id(self):
        self.begin("PUT", "/id")
        d = {}
        with open("./app/test/.cache", "rb") as f:
            d = pickle.load(f)

        response = self.app.put('/forum/'+str(d["id"]))
        ret = response.data.decode('utf8')
        print (ret)
        self.assertEquals(ret, "Unauthorized Access")

        response = self.app.put('/forum/'+str(random.randint(100000, 999999)), headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({"title":"PutTset","content":"This is a Put test!"}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "post not found")

        response = self.app.put('/forum/'+str(d["id"]), headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "invalid request")

        response = self.app.put('/forum/'+str(d["id"]), headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({"title":"PutTset","content":"This is a Put test!"}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")


    def test_e_patch_id(self):
        self.begin("PATCH", "/id")
        d = {}
        with open("./app/test/.cache", "rb") as f:
            d = pickle.load(f)

        response = self.app.patch('/forum/'+str(d["id"]))
        ret = response.data.decode('utf8')
        print (ret)
        self.assertEquals(ret, "Unauthorized Access")

        response = self.app.patch('/forum/'+str(random.randint(100000, 999999)), headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({"type":"title","title":"PatchTset"}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "post not found")

        response = self.app.patch('/forum/'+str(d["id"]), headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "invalid request")

        response = self.app.patch('/forum/'+str(d["id"]), headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({"type":"title","title":"PatchTset"}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")

        response = self.app.patch('/forum/'+str(d["id"]), headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({"type":"content","content":"This is a Patch test!"}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")


    def test_f_delete_id(self):
        self.begin("PATCH", "/id")
        d = {}
        with open("./app/test/.cache", "rb") as f:
            d = pickle.load(f)

        response = self.app.delete('/forum/'+str(d["id"]))
        ret = response.data.decode('utf8')
        print (ret)
        self.assertEquals(ret, "Unauthorized Access")

        response = self.app.delete('/forum/'+str(random.randint(100000, 999999)), headers = {"Authorization":"Bearer "+d["token"]})
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "post not found")

        response = self.app.delete('/forum/'+str(d["id"]), headers = {"Authorization":"Bearer "+d["token"]})
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")
