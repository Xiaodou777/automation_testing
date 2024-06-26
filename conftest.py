"""
============================
Author:古一
Time:2020/10/28
E-mail:369799130@qq.com
============================
"""
import pytest
from loguru import logger

from apis.api_member.member_api import MemberApi
from common.handle_mysql import HandleMysql

# ma = MemberApi()


@pytest.fixture(scope='class')
def get_login_data():
    """获取登录数据"""
    data = MemberApi().get_login_data()
    return data


@pytest.fixture(scope='class')
def connect_mysql(request):
    """连接数据库"""
    db = HandleMysql(**request.param)
    yield db
    db.close()


@pytest.fixture(scope='session', autouse=True)
def task_mark():
    logger.debug("{:=^50}".format('测试任务start'))
    yield
    logger.debug("{:=^50}".format('测试任务结束'))


@pytest.fixture(autouse=True)
def case_mark():
    logger.debug("{:=^50}".format('用例开始'))
    yield
    logger.debug("{:=^50}".format('用例结束'))
