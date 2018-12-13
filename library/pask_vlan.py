#!/usr/bin/python

import os
import logging
import requests
import copy
import ast
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pask_prestapi import PrestApi,\
    OP_DELETE, OP_GET, OP_POST, OP_PUT
from ansible.module_utils.pask_module import PaskModule, try_except


inner_port_args = dict(
    name=dict(type='str', required=True),
    type=dict(type='str', required=True),
)

module_args = dict(
    vid=dict(type='str', required=True),
    name=dict(type='str', required=True),
    port=dict(type='list', elements='dict', options=inner_port_args),
    state=dict(type='str'),
)

name = 'vlan'


class PaskVlan(PaskModule):
    def __init__(self, name, module_args):
        super(PaskVlan, self).__init__(name, module_args)

    @try_except
    def run(self):
        url = os.path.join(self.url, self.module.params['name'])
        if self.module.params['state'] == "absent":
            self.ok_error_msg['delete'] = ['There is no vlan']
            self.resp = self.delete(url)
        else:
            data = self.make_data(self.module.params)
            self.resp = self.put(url, data)


def main():
    vlan = PaskVlan(name, module_args)
    vlan.set_param()
    vlan.run()
    vlan.set_result()

if __name__ == '__main__':
    main()
