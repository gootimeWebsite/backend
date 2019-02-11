# -*- coding: UTF-8 -*-
from app.test.base_test import BaseTestCase
from app import app, db
from app.models import User
from app.article.models import ArticleRole
from app.forum.models import ForumRole

import unittest
import json

class DataTest(BaseTestCase):
    def test_database(self):
        self.begin("", "Database")

        db.drop_all()
        db.create_all()

        ForumRole.insert_roles()
        ArticleRole.insert_roles()

        admin = User(username="admin", phonenumber="12345678910", forum_roleID=2, article_roleID=2)
        db.session.add(admin)

        user = User(username="Tel72250567", phonenumber="17799163760", forum_roleID=1, article_roleID=1)
        db.session.add(user)

        db.session.commit()
