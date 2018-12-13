#!/usr/bin/python

import os
import logging
import requests
import copy
import ast
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pask_prestapi import PrestApi,\
    OP_DELETE, OP_GET, OP_POST, OP_PUT
from ansible.module_utils.pask_module import PaskModule,\
    make_module_args, try_except


dns_id_params = ['id']
dns_id_args = make_module_args(dns_id_params)

outermost_param_str = [
    'retry', 'timeout'
]
module_args = dict(
    id=dict(type='list', options=dns_id_args)
)
module_args.update(make_module_args(outermost_param_str))

name = 'dns'


class PaskDns(PaskModule):
    def __init__(self, name, module_args):
        super(PaskDns, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.put(self.url, data)


def main():
    dns = PaskDns(name, module_args)
    dns.set_param()
    dns.run()
    dns.set_result()

if __name__ == '__main__':
    main()
