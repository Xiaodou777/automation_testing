"""
============================
Author:古一
Time:2020/11/10
E-mail:369799130@qq.com
============================
"""
import os
import allure
import pytest
import yaml
from loguru import logger
from common.handle_assert import HandleAssert as HA
from common.handle_path import DATA_DIR
from cases.case_loan.loan_case import LoanCase

case_data_path = os.path.join(DATA_DIR, 'loan_case_data.yaml')
datas = yaml.safe_load(open(case_data_path, encoding='utf-8'))


# @pytest.mark.zls
@allure.feature('项目')
class TestLoan(LoanCase):
    conf_mysql = LoanCase().mysql_conf

    @allure.story('添加项目')
    @allure.title('{data[title]}')
    # @pytest.mark.zls
    @pytest.mark.parametrize('connect_mysql', [conf_mysql], indirect=True)
    @pytest.mark.parametrize('data', datas['add_loan'])
    def test_add_loan(self, data, get_login_data, connect_mysql):
        """加标业务验证"""
        login_data = get_login_data
        db = connect_mysql
        result = self.case_add_loan(data, login_data, db)
        self.assert_equal(data['expected']['code'], result['code'])
        self.assert_equal(data['expected']['msg'], result['msg'])
        if data['sql']:
            self.assert_equal(1, result['add_num'])
        logger.info('用例通过！')

    @allure.story('审核项目')
    @allure.title('{data[title]}')
    # @pytest.mark.zls
    @pytest.mark.parametrize('connect_mysql', [conf_mysql], indirect=True)
    @pytest.mark.parametrize('data', datas['audit'])
    def test_audit(self, data, get_login_data, connect_mysql):
        """审核业务验证"""
        login_data = get_login_data
        db = connect_mysql
        result = self.case_audit(data, login_data, db)
        self.assert_equal(data['expected']['code'], result['code'])
        self.assert_equal(data['expected']['msg'], result['msg'])
        if data['sql']:
            self.assert_equal(data['expected']['status'], result['status'])
        logger.info('用例通过！')

    @allure.story('投资项目')
    @allure.title('{data[title]}')
    @pytest.mark.parametrize('connect_mysql', [conf_mysql], indirect=True)
    @pytest.mark.parametrize('data', datas['invest'])
    def test_invest(self, data, get_login_data, connect_mysql):
        """投资业务验证"""
        login_data = get_login_data
        db = connect_mysql
        result = self.case_invest(data, login_data, db)
        self.assert_equal(data['expected']['code'], result['code'])
        self.assert_equal(data['expected']['msg'], result['msg'])
        self.assert_equal(self.to_two_decimal(data['invest_json']['amount']), result['invest_amount'])
        if data['check_sql']:
            self.assert_equal(1, result['invest_num'])
            self.assert_equal(1, result['financeLog_num'])
        logger.info('用例通过！')
