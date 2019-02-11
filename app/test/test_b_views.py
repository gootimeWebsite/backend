# -*- coding: UTF-8 -*-
from app.test.base_test import BaseTestCase
from app import app, db
from app.models import User, Messages

import unittest
import pickle
import random, json


class UserTest(BaseTestCase):

    def test_a_message(self):
        self.begin("POST", "/message")

        response = self.app.post('/message', data = json.dumps({}, ensure_ascii = False))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "invalid request")

        response = self.app.post('/message', data = json.dumps({"phonenumber":"177"}, ensure_ascii = False))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "invalid request")

        response = self.app.post('/message', data = json.dumps({"phonenumber":"17799163760"}, ensure_ascii = False))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")

        response = self.app.post('/message', data = json.dumps({"phonenumber":"17799163760"}, ensure_ascii = False))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")


    def test_b_login(self):
        self.begin("POST", "/login")
        message = Messages.query.filter_by(phonenumber="17799163760").first().message

        response = self.app.post('/login', data = json.dumps({}, ensure_ascii = False))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["error"], ret["message"])
        self.assertEquals(ret["message"], "invalid request")

        response = self.app.post('/login', data = json.dumps({"type":"phone","phonenumber":"17799163761","message":str(random.randint(100000, 999999))}, ensure_ascii = False))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["error"], ret["message"])
        self.assertEquals(ret["message"], "need message")

        response = self.app.post('/login', data = json.dumps({"type":"phone","phonenumber":"17799163760","message":str(random.randint(100000, 999999))}, ensure_ascii = False))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["error"], ret["message"])
        self.assertEquals(ret["message"], "wrong message")

        response = self.app.post('/login', data = json.dumps({"type":"phone","phonenumber":"17799163760","message":message}, ensure_ascii = False))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"], ret["username"])
        self.assertEquals(ret["message"], "success")

        message = Messages(phonenumber="11111111111", message="111111")
        db.session.add(message)
        db.session.commit()
        response = self.app.post('/login', data = json.dumps({"type":"phone","phonenumber":"11111111111","message":"111111"}, ensure_ascii = False))
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"], ret["username"])
        self.assertEquals(ret["message"], "success")

        d = {"username":ret["username"], "token":ret["token"], "rftoken":ret["rftoken"]}
        with open("./app/test/.cache", "wb") as f:
            pickle.dump(d, f)


    def test_c_token(self):
        self.begin("GET", "/token")
        d = {}
        with open("./app/test/.cache", "rb") as f:
            d = pickle.load(f)

        response = self.app.get('/token')
        ret = response.data.decode('utf8')
        print (ret)
        self.assertEquals(ret, "Unauthorized Access")

        response = self.app.get('/token', headers = {"Authorization":"Bearer "+d["rftoken"]})
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")

        d["token"] = ret["token"]
        with open("./app/test/.cache", "wb") as f:
            pickle.dump(d, f)


    def test_d_logout(self):
        self.begin("POST", "/logout")
        d = {}
        with open("./app/test/.cache", "rb") as f:
            d = pickle.load(f)

        response = self.app.post('/logout')
        ret = response.data.decode('utf8')
        print (ret)
        self.assertEquals(ret, "Unauthorized Access")

        response = self.app.post('/logout', headers = {"Authorization":"Bearer "+d["token"]})
        ret = json.loads(response.data.decode('utf8'))
        print (ret["message"])
        self.assertEquals(ret["message"], "success")


    def test_z_default(self):
        self.begin("Any", "/   ")

        response = self.app.get('/')
        ret = response.data.decode('utf8')
        print (ret)
        self.assertEquals(ret, "Not Found")
