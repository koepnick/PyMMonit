# -*- coding: utf-8 -*-

import requests
import json

__version__ = '0.1.0'
__author__ = 'Sam Koepnick'


class MMonit(object):

    def __init__(self, mmonit_url, username, password):
        self.mmonit_url = mmonit_url
        self.username = username
        self.password = password

        self.login()

    def login(self):
        self.session = requests.session()
        self._get('/index.csp')
        login_data = {
            "z_username": self.username,
            "z_password": self.password,
            "z_csrf_protection": "off"
        }
        self._post('/z_security_check', data=login_data)

    def _get(self, url):
        result = self.session.get(self.mmonit_url + url)
        #b=json.loads(result.content.decode('latin-1'))
        #print(b)
        return result.content

    def _post(self, url, data=None):
        result = self.session.post(self.mmonit_url + url, data)
        return result.content

    """
    http://mmonit.com/documentation/http-api/Methods/Status
    """
    def hosts_list(self, **kwargs):
        """
        Returns the current status of all hosts registered in M/Monit.
        """
        data = {}

        if 'hostid' in kwargs:
            data['hostid'] = kwargs['hostid']

        if 'hostgroupid' in kwargs:
            data['hostgroupid'] = kwargs['hostgroupid']

        if 'status' in kwargs:
            data['status'] = kwargs['status']

        if 'platform' in kwargs:
            data['platform'] = kwargs['platform']

        if 'led' in kwargs:
            data['led'] = kwargs['led']

        if not data:
            return json.loads(self._get("/status/hosts/list").decode('utf-8'))
        return json.loads(self._post("/status/hosts/list", data).decode('utf-8'))

    def hosts_get(self, host_id):
        """
        Returns detailed status of the given host.
        """
        return json.loads(self._get("/status/hosts/get?id={}".format(host_id)).decode('utf-8'))

    def hosts_summary(self):
        """
        Returns a status summary of all hosts.
        """
        return  json.loads(self._get("/status/hosts/summary").decode('utf-8'))

    """
    http://mmonit.com/documentation/http-api/Methods/Uptime
    """
    def uptime_hosts(self):
        return json.loads(self._get("/reports/uptime/list").decode('utf-8'))

    def uptime_services(self):
        return json.loads(self._get("/reports/uptime/get").decode('utf-8'))

    """
    http://mmonit.com/documentation/http-api/Methods/Events
    """
    def events_list(self):
        return json.loads(self._get("/reports/events/list").decode('utf-8'))

    def events_get(self, event_id):
        return json.loads(self._get("/reports/events/get?id={}".format(event_id)).decode('utf-8'))

    def events_summary(self):
        return json.loads(self._get("/reports/events/summary").decode('utf-8'))

    def events_dismiss(self, event_id):
        return json.loads(self._post("/reports/events/dismiss", event_id).decode('utf-8'))

    """
    http://mmonit.com/documentation/http-api/Methods/Admin_Hosts
    """
    def admin_hosts_list(self):
        return json.loads(self._get("/admin/hosts/list").decode('utf-8'))

    def admin_hosts_get(self, host_id):
        return json.loads(self._get("/admin/hosts/get?id={}".format(host_id)).decode('utf-8'))

    def admin_hosts_upadte(self, host_id, **kwargs):
        return NotImplemented

    def admin_hosts_delete(self, host_id):
        return json.loads(self._post("/admin/hosts/delete", {"id": host_id}).decode('utf-8'))

    def admin_hosts_test(self, ipaddr, port, ssl, monituser, monitpassword):
        data = {
            "ipaddr": ipaddr,
            "port": port,
            "ssl": ssl,
            "monituser": monituser,
            "monitpassword": monitpassword
        }
        return json.loads(self._post("/admin/hosts/test", data).decode('utf-8'))

    def admin_hosts_action(self, id, action, service):
        data = {
            "id": id,
            "action": action,
            "service": service
        }
        return json.loads(self._post("/admin/hosts/action", data).decode('utf-8'))
