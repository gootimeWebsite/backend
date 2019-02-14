# -*- coding: UTF-8 -*-
from app.test.base_test import BaseTestCase
from app import app, db
from app.article.models import Article, ArticleRole

import unittest
import pickle
import random, json


class UserTest(BaseTestCase):

    def test_a_get(self):
        self.begin("GET", "/user/    ")
        d = {}
        with open("./app/test/.cache", "rb") as f:
            d = pickle.load(f)

        response = self.app.get('/user/')
        ret = response.data.decode('utf8')
        print (ret)
        self.assertEquals(ret, "Unauthorized Access")

        response = self.app.get('/user/', headers = {"Authorization":"Bearer "+d["token"]})
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")


    def test_b_put(self):
        self.begin("PUT", "/user/    ")
        d = {}
        with open("./app/test/.cache", "rb") as f:
            d = pickle.load(f)

        response = self.app.put('/user/', data = json.dumps({"username":"adil","phonenumber":"12345678911"}))
        ret = response.data.decode('utf8')
        print (ret)
        self.assertEquals(ret, "Unauthorized Access")

        response = self.app.put('/user/', headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "invalid request")

        response = self.app.put('/user/', headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({"username":"adil","phonenumber":"12345678910"}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "phonenumber already exist")

        response = self.app.put('/user/', headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({"username":"admin","phonenumber":"12345678911"}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "username already exist")

        response = self.app.put('/user/', headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({"username":"adil","phonenumber":"12345678911"}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")

        d = {"username":"adil", "token":ret["token"], "rftoken":ret["rftoken"]}
        with open("./app/test/.cache", "wb") as f:
            pickle.dump(d, f)


    def test_c_patch(self):
        self.begin("PATCH", "/user/    ")
        d = {}
        with open("./app/test/.cache", "rb") as f:
            d = pickle.load(f)

        response = self.app.patch('/user/', data = json.dumps({}))
        ret = response.data.decode('utf8')
        print (ret)
        self.assertEquals(ret, "Unauthorized Access")

        response = self.app.patch('/user/', headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "invalid request")

        response = self.app.patch('/user/', headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({"phonenumber":"12345678910"}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "phonenumber already exist")

        response = self.app.patch('/user/', headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({"username":"admin"}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "username already exist")

        response = self.app.patch('/user/', headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({"phonenumber":"12345678911"}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")

        response = self.app.patch('/user/', headers = {"Authorization":"Bearer "+d["token"]}, data = json.dumps({"username":"adil"}))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")

        d = {"username":"adil", "token":ret["token"], "rftoken":ret["rftoken"]}
        with open("./app/test/.cache", "wb") as f:
            pickle.dump(d, f)
