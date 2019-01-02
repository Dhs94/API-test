import requests
import unittest
import ddt
from case.login_wdms import Login


class Test(unittest.TestCase):

    def setUp(self):
        s = requests.session()
        self.wdms = Login(s)
        self.wdms.login()
        self.zones_num = []
        self.departments = []
        self.emps = []
        self.devices = []

    def tearDown(self):
        if self.zones_num:
            self.wdms.del_zone(self.zones_num)
        if self.departments:
            for dep in self.departments:
                self.wdms.del_department(dep)
        if self.emps:
            for emp in self.emps:
                self.wdms.del_emp(emp)
        if self.devices:
            self.wdms.del_device(self.devices)

    def test_login_success(self):
        u"""登录成功"""
        # 创建区域
        data = {'username': 'admin', 'password': 'admin'}
        res = self.wdms.login(data=data)
        expect_zone = self.wdms.get_zone()['data']
        self.assertEqual(res['message'], 'Login Successful')
        self.assertEqual(res['code'], 200)
        self.assertEqual(res['supervisor'], True)
        self.assertEqual(res['zone'], expect_zone)

    def test_login_username_blank(self):
        u"""用户名为空"""
        data = {'username': '', 'password': 'admin'}
        res = self.wdms.login(data=data)
        self.assertEqual(res['message'], 'Username Or Password Is Incorrect')

    def test_login_password_blank(self):
        u"""密码为空"""
        data = {'username': 'admin', 'password': ''}
        res = self.wdms.login(data=data)
        self.assertEqual(res['message'], 'Username Or Password Is Incorrect')

    def test_login_username_password_balnk(self):
        u"""用户密码为空"""
        data = {'username': '', 'password': ''}
        res = self.wdms.login(data=data)
        self.assertEqual(res['message'], 'Username Or Password Is Incorrect')

    def test_login_username_incorrect(self):
        u"""用户名错误"""
        data = {'username': '1234', 'password': 'admin'}
        res = self.wdms.login(data=data)
        self.assertEqual(res['message'], 'Username Or Password Is Incorrect')

    def test_login_password_incorrect(self):
        u"""密码错误"""
        data = {'username': 'admin', 'password': '1234'}
        res = self.wdms.login(data=data)
        self.assertEqual(res['message'], 'Username Or Password Is Incorrect')

    def test_login_username_password_incorrect(self):
        u"""用户名密码错误"""
        data = {'username': '1234', 'password': '1234'}
        res = self.wdms.login(data=data)
        self.assertEqual(res['message'], 'Username Or Password Is Incorrect')

    def test_logout_success(self):
        u"""成功退出登录"""
        res = self.wdms.logout()
        self.assertEqual(res['message'], 'Logout Successful')
        self.assertEqual(res['code'], 200)

    def test_create_zone_success(self):
        u"""成功添加区域"""
        data = {"Data": [{"zoneNumber": 11, "zoneName": "11"}]}
        self.zones_num = [11]
        res = self.wdms.create_zone(data=data)
        self.assertEqual(res['message'], 'Succeed')
        self.assertEqual(res['code'], 200)

    # @ddt.data({"Data": [{"zoneNumber": 2, "zoneName": "2"}]},
    #           {"Data": [{"zoneNumber": 100, "zoneName": "100"}]})
    def test_create_zone_zoneNumber_is_string(self):
        u"""zoneNumber为字符串"""
        data = {"Data": [{"zoneNumber": 'abc', "zoneName": "1"}]}
        res = self.wdms.create_zone(data=data)
        self.assertEqual(res['message'], "global name 'emp_dict' is not defined")
        self.assertEqual(res['code'], 4001)

    def test_create_zone_zoneNumber_contains_escapeChar(self):
        u"""zoneNumber含转义符"""
        data = {"Data": [{"zoneNumber": '/n', "zoneName": "1"}]}
        res = self.wdms.create_zone(data=data)
        self.assertEqual(res['message'], "global name 'emp_dict' is not defined")
        self.assertEqual(res['code'], 4001)

    def test_create_zone_zoneNumber_is_blank(self):
        u"""zoneNumber为空"""
        data = {"Data": [{"zoneNumber": '', "zoneName": "1"}]}
        res = self.wdms.create_zone(data=data)
        self.assertEqual(res['message'], "global name 'emp_dict' is not defined")
        self.assertEqual(res['code'], 4001)

    def test_create_zone_zoneName_is_int(self):
        u"""zoneName为数字"""
        data = {"Data": [{"zoneNumber": 13, "zoneName": 13}]}
        res = self.wdms.create_zone(data=data)
        self.assertEqual(res['message'], 'Parameter Not Found')
        self.assertEqual(res['code'], 3002)

    def test_create_zone_zoneName_is_string(self):
        u"""zoneName为字符串"""
        data = {"Data": [{"zoneNumber": 11, "zoneName": "abc,."}]}
        self.zones_num = [11]
        res = self.wdms.create_zone(data=data)
        self.assertEqual(res['message'], 'Succeed')
        self.assertEqual(res['code'], 200)

    def test_create_zone_zoneName_contains_escapeChar(self):
        u"""zoneName含转义符"""
        data = {"Data": [{"zoneNumber": 11, "zoneName": "/n"}]}
        res = self.wdms.create_zone(data=data)
        self.assertEqual(res['message'], "Parameter Not Found")
        self.assertEqual(res['code'], 3002)

    def test_create_zone_zoneName_is_blank(self):
        u"""zoneName为空"""
        data = {"Data": [{"zoneNumber": 11, "zoneName": ""}]}
        res = self.wdms.create_zone(data=data)
        self.assertEqual(res['message'], "global name 'emp_dict' is not defined")
        self.assertEqual(res['code'], 4001)

    def test_create_zone_both_are_blank(self):
        u"""zoneNumber、zoneName为空"""
        data = {"Data": [{"zoneNumber": "", "zoneName": ""}]}
        res = self.wdms.create_zone(data=data)
        self.assertEqual(res['message'], "global name 'emp_dict' is not defined")
        self.assertEqual(res['code'], 4001)

    def test_update_zone(self):
        u"""编辑区域"""
        # 软件中存在zoneNUmber=1，zoneName=zone1
        data = {"Data": [{"zoneNumber": 1, "zoneName": "1"}]}
        res = self.wdms.create_zone(data=data)
        self.assertEqual(res['message'], 'Succeed')
        self.assertEqual(res['code'], 200)

    def test_create_zone_in_batch(self):
        u"""批量添加区域"""
        data = {"Data": [{"zoneNumber": 11, "zoneName": "11"},
                         {"zoneNumber": 12, "zoneName": "12"},
                         {"zoneNumber": 13, "zoneName": "13"}]}
        self.zones_num = [11, 12, 13]
        res = self.wdms.create_zone(data=data)
        self.assertEqual(res['message'], 'Succeed')
        self.assertEqual(res['code'], 200)

    def test_get_zone_default(self):
        u"""没有设置page和perpage获取区域"""
        res = self.wdms.get_zone()
        self.assertEqual(res['message'], 'Succeed')
        self.assertEqual(res['code'], 200)
        self.assertEqual(res['pageSize'], 100)
        self.assertEqual(res['totalItems'], 3)
        self.assertEqual(res['totalPages'], 1)
        self.assertEqual(res['next_url'], '')
        self.assertEqual(res['page'], 1)

    def test_get_zone_success(self):
        u"""获取区域，page=2,perPage=2"""
        data = {'page': 2, 'per_page': 2}
        res = self.wdms.get_zone(data=data)
        self.assertEqual(res['pageSize'], 2)
        self.assertEqual(res['totalItems'], 3)
        self.assertEqual(res['totalPages'], 2)
        self.assertEqual(res['next_url'], 'http://127.0.0.1:8081/api/zones&page=3&per_page=2')
        self.assertEqual(res['page'], 2)

    def test_get_zone_page_is_zero(self):
        u"""获取区域，page=1"""
        data = {'page': 0}
        res = self.wdms.get_zone(data=data)
        self.assertEqual(res['pageSize'], 100)
        self.assertEqual(res['totalItems'], 3)
        self.assertEqual(res['totalPages'], 1)
        self.assertEqual(res['next_url'], '')
        self.assertEqual(res['page'], 1)

    def test_get_zone_page_is_beyond_totalPage(self):
        u"""获取区域，page超出总页数"""
        # 当前自由1页
        data = {'page': 2}
        res = self.wdms.get_zone(data=data)
        self.assertEqual(res['pageSize'], 100)
        self.assertEqual(res['totalItems'], 3)
        self.assertEqual(res['totalPages'], 1)
        self.assertEqual(res['next_url'], '')
        self.assertEqual(res['page'], 2)

    def test_get_zone_perPage_is_zero(self):
        u"""获取区域，perPage=0"""
        data = {'per_page': 0}
        res = self.wdms.get_zone(data=data)
        self.assertEqual(res['pageSize'], 100)
        self.assertEqual(res['totalItems'], 3)
        self.assertEqual(res['totalPages'], 1)
        self.assertEqual(res['next_url'], '')
        self.assertEqual(res['page'], 1)

    def test_get_zone_perPage_is_beyond_totalPage(self):
        u"""获取区域，perPage超出默认值(100)"""
        data = {'per_page': 200}
        res = self.wdms.get_zone(data=data)
        self.assertEqual(res['pageSize'], 100)
        self.assertEqual(res['totalItems'], 3)
        self.assertEqual(res['totalPages'], 1)
        self.assertEqual(res['next_url'], '')
        self.assertEqual(res['page'], 1)

    def test_create_department_success(self):
        u"""成功添加部门"""
        data = {"Data": [{"zoneNumber": 1, "departmentCode": "3", "departmentName": "3"},
                         {"zoneNumber": 1, "departmentCode": "2", "departmentName": "2"}]}
        self.departments = [{"zoneNumber": 1, "departmentCode": [2, 3]}]
        res = self.wdms.create_department(data)
        self.assertEqual(res['message'], "Succeed")
        self.assertEqual(res['code'], 200)

    def test_create_department_zoneNum_no_exist(self):
        u"""部门所属区域不存在"""
        data = {"Data": [{"zoneNumber": 6, "departmentCode": "3", "departmentName": "3"},
                         {"zoneNumber": 6, "departmentCode": "2", "departmentName": "2"}]}
        self.departments = [{"zoneNumber": 1, "departmentCode": [2, 3]}]
        res = self.wdms.create_department(data)
        self.assertEqual(res['message'], "Zone 6 doesn't existed")
        self.assertEqual(res['code'], 4002)

    def test_create_department_zoneNum_is_blank(self):
        u"""部门所属区域未填"""
        data = {"Data": [{"zoneNumber": "", "departmentCode": "3", "departmentName": "3"},
                         {"zoneNumber": "", "departmentCode": "2", "departmentName": "2"}]}
        self.departments = [{"zoneNumber": 1, "departmentCode": [2, 3]}]
        res = self.wdms.create_department(data)
        self.assertEqual(res['message'], "Zone  doesn't existed")
        self.assertEqual(res['code'], 4002)

    def test_create_department_depCode_is_string(self):
        u"""部门code为字符串 """
        data = {"Data": [{"zoneNumber": "1", "departmentCode": "abc", "departmentName": "3"},
                         {"zoneNumber": "1", "departmentCode": "def", "departmentName": "2"}]}
        self.departments = [{"zoneNumber": 1, "departmentCode": ["abc", "def"]}]
        res = self.wdms.create_department(data)
        self.assertEqual(res['message'], "Succeed")
        self.assertEqual(res['code'], 200)

    def test_create_department_depCode_is_blank(self):
        u"""部门code为空 """
        data = {"Data": [{"zoneNumber": "1", "departmentCode": " ", "departmentName": "3"}]}
        self.departments = [{"zoneNumber": 1, "departmentCode": [" "]}]
        res = self.wdms.create_department(data)
        self.assertEqual(res['message'], "Succeed")
        self.assertEqual(res['code'], 200)

    def test_create_department_depname_in_char_limit(self):
        u"""部门name字符数在限制内"""
        data = {"Data": [{"zoneNumber": "1", "departmentCode": "2", "departmentName": "123456789012345678901234567890123456789012345678901234567890"}]}
        self.departments = [{"zoneNumber": 1, "departmentCode": ["2"]}]
        res = self.wdms.create_department(data)
        self.assertEqual(res['message'], "Succeed")
        self.assertEqual(res['code'], 200)

    def test_create_department_depname_beyond_char_limit(self):
        u"""部门name在字符数超出限制"""
        data = {"Data": [{"zoneNumber": "1", "departmentCode": "2", "departmentName": "1234567890123456789012345678901234567890123456789012345678901"}]}
        self.departments = [{"zoneNumber": 1, "departmentCode": ["2"]}]
        res = self.wdms.create_department(data)
        self.assertEqual(res['code'], 4001)

    def test_create_department_depname_is_blank(self):
        u"""部门name为空"""
        data = {"Data": [{"zoneNumber": "1", "departmentCode": "2", "departmentName": " "}]}
        self.departments = [{"zoneNumber": 1, "departmentCode": ["2"]}]
        res = self.wdms.create_department(data)
        self.assertEqual(res['message'], "Succeed")
        self.assertEqual(res['code'], 200)

    def test_create_department_in_batch(self):
        u"""批量添加部门"""
        data = {"Data": [{"zoneNumber": 1, "departmentCode": "600", "departmentName": "600"},
                         {"zoneNumber": 1, "departmentCode": "601", "departmentName": "601"},
                         {"zoneNumber": 2, "departmentCode": "700", "departmentName": "700"},
                         {"zoneNumber": 2, "departmentCode": "701", "departmentName": "701"}]}
        self.departments = [{"zoneNumber": 1, "departmentCode": [600, 601]},
                            {"zoneNumber": 2, "departmentCode": [700, 701]}]
        res = self.wdms.create_department(data)
        self.assertEqual(res['message'], "Succeed")
        self.assertEqual(res['code'], 200)

    def test_create_emp_success(self):
        u"""成功添加人员"""
        data = {"Data": [{"zoneNumber": 1, "ID": "000001010", "departmentCode": "1"},
                         {"zoneNumber": 1, "ID": "000001011", "departmentCode": "1"},
                         {"zoneNumber": 2, "ID": "000001012", "departmentCode": "1"},
                         {"zoneNumber": 2, "ID": "000001013", "departmentCode": "1"}]}
        self.emps = [{"zoneNumber": 1, "empID": ["000001010", "000001011"]},
                     {"zoneNumber": 2, "empID": ["000001012", "000001013"]}]
        res = self.wdms.create_emp(data)
        self.assertEqual(res['message'], "Succeed")
        self.assertEqual(res['code'], 200)

    def test_create_device_success(self):
        u"""成功添加设备 """
        data = {"Data":
                [{"sn": "3368152100001", "zoneNumber": 1, "departmentCode": "1", "alias": "3368152100001", "masterDevice": "yes", "facialDevice": "yes"},
                 {"sn": "3368152100001", "zoneNumber": 2, "departmentCode": "1", "alias": "3368152100002", "masterDevice": "yes", "facialDevice": "yes"}]}
        self.devices = {"sn": ["3368152100001", "3368152100001"]}
        res = self.wdms.create_device(data)
        self.assertEqual(res['message'], "Succeed")
        self.assertEqual(res['code'], 200)

if __name__ == '__main__':
    unittest.main()




