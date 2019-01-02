# coding: utf-8
import os


class URL:

    def __init__(self, ip=None):
        if ip:
            self.ip = ip
        else:
            self.ip = "127.0.0.1:8081"

    def login_url(self):
        loginURL = "http://" + self.ip + "/api/accounts/login/"
        return loginURL

    def logout_url(self):
        logoutURL = "http://" + self.ip + "/api/accounts/logout/"
        return logoutURL

    def zone_url(self):
       zoneURL = "http://" + self.ip + "/api/zones"
       return zoneURL

    def del_zone_url(self):
        delZoneURL = "http://" + self.ip + "/iclock/data/company/?action=del"
        return delZoneURL

    def department_url(self):
       departmentURL = "http://" + self.ip + "/api/departments"
       return departmentURL

    def del_department_url(self):
       departmentURL = "http://" + self.ip + "/api/delete/departments/"
       return departmentURL

    def employee_url(self):
        empURL = "http://" + self.ip + "/api/employees"
        return empURL

    def del_employee_url(self):
        delEmpURL = "http://" + self.ip + "/api/delete/employees/"
        return delEmpURL

    def device_url(self):
        deviceURL = "http://" + self.ip + "/api/devices"
        return deviceURL

    def del_device_url(self):
        delDeviceURL = "http://" + self.ip + "/api/delete/devices/"
        return delDeviceURL

    def schedule_url(self):
        scheduleURL = "http://" + self.ip + "/api/employeeschedules"
        return scheduleURL

    def DStime_url(self):
        DStimeURLL = "http://" + self.ip + "/api/dstime"
        return DStimeURLL

    def send_emp_url(self):
        sendEmpURL = "http://" + self.ip + "/api/empstodevs"
        return sendEmpURL