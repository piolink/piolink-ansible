#!/usr/bin/python

import os
import logging
import requests
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pask_prestapi import PrestApi,\
    OP_DELETE, OP_GET, OP_POST, OP_PUT
from ansible.module_utils.pask_module import PaskModule, try_except

param_list = [
    'id', 'type', 'recover', 'timeout', 'interval', 'status', 'state', 'retry',
    'sip', 'tip', 'uri', 'host', 'user-agent', 'status-code', 'expect', 'unexpect',
    'content-length', 'increase-icmp-id', 'tolerance', 'update-delay', 'oid',
    'half-open', 'send', 'filename', 'packets', 'radius-auth-name', 'port',
    'radius-auth-passwd', 'radius-auth-secret', 'radius-acct-secret', 'version',
    'validate', 'common-name', 'description', 'source-port-min', 'source-port-max',
    'mac', 'community', 'record-type', 'query'
]

str_param_list = list(set(param_list) - set(['prest_ip', 'prest_port', 'id']))

module_args = dict(
    id=dict(type='str', required=True),
)

for p in str_param_list:
    module_args[p] = dict(type='str')

name = 'health-check'


class PaskHealthcheck(PaskModule):
    def __init__(self, name, module_args):
        super(PaskHealthcheck, self).__init__(name, module_args)

    @try_except
    def run(self):
        if self.module.params['state'] == "absent":
            data = dict()
            url = os.path.join(self.url, self.module.params['id'])
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            self.resp = self.delete(url, data)
        else:
            data = self.make_data(self.module.params)
            url = os.path.join(self.url, self.module.params['id'])
            self.resp = self.put(url, data)


def main():
    hc = PaskHealthcheck(name, module_args)
    hc.set_param()
    hc.run()
    hc.set_result()

if __name__ == '__main__':
    main()
