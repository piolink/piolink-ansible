#!/usr/bin/python

import pprint
import os
import logging
import requests
import ast
import json
import traceback
from functools import wraps
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pask_prestapi import PrestApi,\
    OP_DELETE, OP_GET, OP_POST, OP_PUT


def make_module_args(param):
    d = dict()
    for p in param:
        d[p] = dict(type='str')
    return d


def try_except(func):
    @wraps(func)
    def applicator(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            return result
        except Exception as e:
            result = dict()
            result['failed'] = True
            result['message'] = 'pask module error'
            self.module.exit_json(**result)

    return applicator


class PaskModule(PrestApi):
    def __init__(self, name, module_args):
        super(PaskModule, self).__init__()
        self.module_args = module_args
        self.basic_module_args = dict(
            prest_ip=dict(type='str', required=True),
            prest_port=dict(type='str', required=True),
            user_id=dict(type='str', required=True),
            user_pw=dict(type='str', required=True)
        )
        self.param = None

        self.path_name = name
        self.data_name = name
        self.init_ansible()
        self.exclude_params = [
            'prest_ip', 'prest_port', 'state', 'user_id', 'user_pw'
        ]
        self.resp = None
        self.user_id = 'root'
        self.user_pw = 'admin'
        self.ok_error_msg = dict()

    def init_ansible(self):
        self.module_args.update(self.basic_module_args)
        result = dict(
            original_message='',
            message='',
            debug=''
        )

        module = AnsibleModule(
            argument_spec=self.module_args,
            supports_check_mode=True
        )
        self.result = result
        self.module = module
        self.set_param()

        if self.module.check_mode:
            return self.result

    def set_param(self):
        self.user_id = self.module.params['user_id']
        self.user_pw = self.module.params['user_pw']
        self.set_headers(self.user_id, self.user_pw)
        self.prefix_url = 'https://{}:{}/prestapi/v2/conf/'.format(
            self.module.params['prest_ip'], self.module.params['prest_port'])

        self.url = os.path.join(self.prefix_url, self.path_name)

    def make_delete_data(self, module_name, key, value):
        d = {
            module_name: {key: value}
        }
        return d

    def make_data(self, params, include_inner=False):
        data = dict()
        for k, v in params.iteritems():
            if k in self.exclude_params:
                continue
            if type(v) is dict:
                if include_inner:
                    inner_dict = self.make_data(v, include_inner)
                    data[k] = inner_dict
                else:
                    pass
            elif type(v) is list:
                if include_inner:
                    inner_list = list()
                    for _v in v:
                        if type(_v) is dict:
                            inner_dict = self.make_data(_v, include_inner)
                            inner_list.append(inner_dict)
                        else:
                            inner_list.append(_v)
                    data[k] = inner_list
            elif v is not None and v != "None":
                data.update({k: v})
        return data

    def run(self):
        resp = None
        if self.module.params['state'] == "absent":
            data = self.make_data(self.module.params)
            resp = self.delete(self.url, data)
        else:
            data = dict()
            if self.is_exist(self.url, self.module.params['id']):
                data[self.data_name] = self.make_data(self.module.params)
                resp = self.put(self.url, data)
            else:
                data[self.data_name] = self.make_data(self.module.params)
                resp = self.post(self.url, data)
        if resp is not None:
            self.result['message'] = resp.text
        else:
            self.result['message'] = 'Fail'
        self.resp = resp

    def is_ok_error_msg(self, msg):
        if len(self.used_method) < 0:
            return False
        if len(self.ok_error_msg.keys()) <= 0:
            return False

        for method, is_ok_msg in self.ok_error_msg.iteritems():
            if method == self.used_method[-1]:
                for ok_msg in is_ok_msg:
                    if ok_msg in msg:
                        return True
        return False

    def set_result(self):
        if self.resp is None:
            self.result['failed'] = True
            self.result['message'] = 'Prest request is failed'
            self.module.exit_json(**self.result)
            return

        resp_dic = json.loads(self.resp.text)
        if 'header' in resp_dic.keys():
            self.result['message'] = resp_dic['header']['resultMessage']
            if resp_dic['header']['resultCode'] > 0:
                self.result['changed'] = True
            elif resp_dic['header']['resultCode'] < 0:
                if not self.is_ok_error_msg(self.result['message']):
                    self.result['failed'] = True
        else:
            self.result['message'] = str(resp_dic)
        self.module.exit_json(**self.result)
