#!/usr/bin/python

import os
import logging
import copy
import ast
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pask_prestapi import PrestApi,\
        OP_DELETE, OP_GET, OP_POST, OP_PUT
from ansible.module_utils.pask_module import PaskModule, try_except


inner_nat_args = dict(
    nat=dict(type='str'),
    type=dict(type='str'),
    priority=dict(type='str'),
    sip=dict(type='str'),
    dip=dict(type='str'),
    protocol=dict(type='str'),
    natip=dict(type='str'),
    status=dict(type='str'),
)
inner_nat_args['external-ip'] = dict(type='str')
inner_nat_args['internal-ip'] = dict(type='str')

req_param_list = [
    'id', 'rip'
]
param_list = [
    'name', 'rport', 'mac', 'interface', 'priority', 'weight',
    'graceful-shutdown', 'max-connection', 'upload-bandwidth',
    'download-bandwidth', 'health-check', 'domain-filter', 'pool-size',
    'pool-age', 'pool-reuse', 'pool-srcmask', 'src-natip', 'backup',
    'state', 'status'
]

module_args = dict()

for p in req_param_list:
    module_args[p] = dict(type='str', required=True)

for p in param_list:
    module_args[p] = dict(type='str')

module_args['nat'] = dict(type='list', options=inner_nat_args)

name = 'real'


class PaskReal(PaskModule):
    def __init__(self, name, module_args):
        super(PaskReal, self).__init__(name, module_args)

    @try_except
    def run(self):
        if self.module.params['state'] == "absent":
            data = dict()
            data['real'] = self.make_data(self.module.params)
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            resp = self.delete(self.url, data)
        else:
            data = dict()
            data = self.make_data(self.module.params, include_inner=True)
            url = os.path.join(self.url, self.module.params['id'])
            resp = self.put(url, data)
        self.resp = resp


def main():
    real = PaskReal(name, module_args)
    real.set_param()
    real.run()
    real.set_result()

if __name__ == '__main__':
    main()
