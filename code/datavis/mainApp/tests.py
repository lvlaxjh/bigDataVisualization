from django.test import TestCase, Client
from . import models


class DataPutTest(TestCase):
    c = Client()

    def setUp(self):
        # 所有test运行前运行一次
        print('=====发送数据接口测试=====')

    def test_returnData_test(self):
        content = {
            "content": "test",
        }
        response = self.c.post('/returnData', data=content,
                               content_type='application/json').json()
        self.assertEqual(response['test'], 's')
