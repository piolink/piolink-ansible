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


outermost_param_str = [
    'config-password', 'description', 'level', 'log', 'password', 'state'
]
outermost_args = make_module_args(outermost_param_str)

module_args = dict(
    name=dict(type='str', required=True)
)
module_args.update(outermost_args)

name = 'user'


class PaskUser(PaskModule):
    def __init__(self, name, module_args):
        super(PaskUser, self).__init__(name, module_args)

    @try_except
    def run(self):
        url = os.path.join(self.url, self.module.params['name'])
        if self.module.params['state'] == 'absent':
            self.resp = self.delete(url)
        else:
            data = self.make_data(self.module.params, include_inner=True)
            self.resp = self.put(url, data)


def main():
    user = PaskUser(name, module_args)
    user.set_param()
    user.run()
    user.set_result()

if __name__ == '__main__':
    main()
