import requests
import json
from data.url_data import URL


class Login:
    def __init__(self, s):
        self.s = s
        self.url = URL()

    def login(self, data=None):
        """
        登录
        """
        if data:
            data = data
        else:
            data = {"username": "admin", "password": "admin"}
        data = json.dumps(data)
        res = self.s.post(url=self.url.login_url(), data=data).json()
        return res
        # print(res)
        # print(type(res))

    def logout(self, data=None):
        """
        退出登录
        """
        res = self.s.post(url=self.url.logout_url(), data=data).json()
        return res

    def create_zone(self, data):
        """
        创建或更新区域
        """
        data = json.dumps(data)
        res = self.s.post(url=self.url.zone_url(), data=data).json()
        return res

    def get_zone(self, data=None):
        """
        获取区域
        """
        res = self.s.get(url=self.url.zone_url(), params=data).json()
        return res

    def del_zone(self, zones):
        """
        删除区域
        """
        if isinstance(zones, int):
            data = 'K=%s' % zones
        else:
            zone_list = []
            data = []
            for i in zones:
                # 转为 K=格式
                zone = 'K=%s' % i
                zone_list.append(zone)
                str = '&'
                # 将list转为str，并以&连接
                data = str.join(zone_list)
        res2 = self.s.post(url=self.url.del_zone_url(), data=data)
        return res2

    def create_department(self, data):
        """
        创建部门
        """
        data = json.dumps(data)
        res = self.s.post(url=self.url.department_url(), data=data).json()
        return res

    def get_department(self, data):
        """
        获取部门
        """
        res = self.s.get(url=self.url.department_url(), params=data).json()
        return res

    def del_department(self, data):
        """
        删除部门
        """
        data = json.dumps(data)
        res = self.s.post(url=self.url.del_department_url(), data=data).json()
        return res

    def create_emp(self, data):
        """
        添加人员
        """
        data = json.dumps(data)
        res = self.s.post(url=self.url.employee_url(), data=data).json()
        return res

    def del_emp(self, data):
        """
        删除人员
        """
        data = json.dumps(data)
        res = self.s.post(url=self.url.del_employee_url(), data=data).json()
        return res

    def create_device(self, data):
        """
        添加设备
        """
        data = json.dumps(data)
        res = self.s.post(url=self.url.device_url(), data=data).json()
        return res

    def del_device(self, data):
        """
        添加设备
        """
        data = json.dumps(data)
        res = self.s.post(url=self.url.del_device_url(), data=data).json()
        return res

# if __name__ == '__main__':
#     s = requests.session()
#     A = Login(s)
#     r = A.login()
#     data = {"zoneNumber": 1}
#     res = A.get_department(data)
#     print(res)
#     data2 = {"zoneNumber": 1, "departmentCode": ["df"]}
#     res2 = A.del_department(data2)
