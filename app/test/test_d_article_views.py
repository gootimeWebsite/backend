# -*- coding: UTF-8 -*-
from app.test.base_test import BaseTestCase
from app import app, db
from app.article.models import Article, ArticleRole

import unittest
import pickle
import random, json


class ArticleTest(BaseTestCase):

    def test_a_post(self):
        self.begin("POST", "/article/")
        d = {}
        with open("./app/test/.cache", "rb") as f:
            d = pickle.load(f)

        response = self.app.post('/article/', data = json.dumps({"title":"Test", "content":"This is a test!", "category":"Test"}))
        ret = response.data.decode('utf8')
        print (ret)
        self.assertEquals(ret, "Unauthorized Access")

        response = self.app.post('/article/', headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "invalid request")

        response = self.app.post('/article/', headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({"title":"Test", "content":"This is a test!", "category":"Test"}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")

        d["Aid"] = ret["id"]
        with open("./app/test/.cache", "wb") as f:
            pickle.dump(d, f)


    def test_b_get(self):
        self.begin("GET", "/article/")
        d = {}
        with open("./app/test/.cache", "rb") as f:
            d = pickle.load(f)

        response = self.app.get('/article/', headers = {"Authorization":"Bearer "+d["token"]})
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")


    def test_c_get_id(self):
        self.begin("GET", "/article/id")
        d = {}
        with open("./app/test/.cache", "rb") as f:
            d = pickle.load(f)

        response = self.app.get('/article/'+str(d["Aid"]))
        ret = response.data.decode('utf8')
        print (ret)
        self.assertEquals(ret, "Unauthorized Access")

        response = self.app.get('/article/'+str(random.randint(100000, 999999)), headers = {"Authorization":"Bearer "+d["token"]})
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "post not found")

        response = self.app.get('/article/'+str(d["Aid"]), headers = {"Authorization":"Bearer "+d["token"]})
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")


    def test_d_put_id(self):
        self.begin("PUT", "/article/id")
        d = {}
        with open("./app/test/.cache", "rb") as f:
            d = pickle.load(f)

        response = self.app.put('/article/'+str(d["Aid"]))
        ret = response.data.decode('utf8')
        print (ret)
        self.assertEquals(ret, "Unauthorized Access")

        response = self.app.put('/article/'+str(random.randint(100000, 999999)), headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({"title":"PutTset", "content":"This is a Put test!", "category":"PutTest"}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "post not found")

        response = self.app.put('/article/'+str(d["Aid"]), headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "invalid request")

        response = self.app.put('/article/'+str(d["Aid"]), headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({"title":"PutTset", "content":"This is a Put test!", "category":"PutTest"}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")


    def test_e_patch_id(self):
        self.begin("PATCH", "/article/id")
        d = {}
        with open("./app/test/.cache", "rb") as f:
            d = pickle.load(f)

        response = self.app.patch('/article/'+str(d["Aid"]))
        ret = response.data.decode('utf8')
        print (ret)
        self.assertEquals(ret, "Unauthorized Access")

        response = self.app.patch('/article/'+str(random.randint(100000, 999999)), headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({"title":"PatchTset"}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "post not found")

        response = self.app.patch('/article/'+str(d["Aid"]), headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "invalid request")

        response = self.app.patch('/article/'+str(d["Aid"]), headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({"title":"PatchTset"}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")

        response = self.app.patch('/article/'+str(d["Aid"]), headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({"category":"PatchTset"}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")

        response = self.app.patch('/article/'+str(d["Aid"]), headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({"content":"This is a Patch test!"}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")


    def test_f_delete_id(self):
        self.begin("DELETE", "/article/id")
        d = {}
        with open("./app/test/.cache", "rb") as f:
            d = pickle.load(f)

        response = self.app.delete('/article/'+str(d["Aid"]))
        ret = response.data.decode('utf8')
        print (ret)
        self.assertEquals(ret, "Unauthorized Access")

        response = self.app.delete('/article/'+str(random.randint(100000, 999999)), headers = {"Authorization":"Bearer "+d["token"]})
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "post not found")

        response = self.app.delete('/article/'+str(d["Aid"]), headers = {"Authorization":"Bearer "+d["token"]})
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")
