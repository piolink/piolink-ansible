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


trap_host_params_str = [
    'community', 'des-passwd', 'engine-id', 'md5-passwd',
    'sha-passwd', 'aes-passwd', 'version', 'user'
]
inner_trap_host_args = dict(
    ip=dict(type='str', required=True),
)
inner_trap_host_args.update(make_module_args(trap_host_params_str))

trap_params = [
    'cold-start', 'failover', 'fan', 'health-check', 'link-down',
    'link-up', 'management-cpu', 'management-memory', 'packet-cpu',
    'packet-memory', 'power', 'temperature'
]
inner_trap_args = dict(
    host=dict(type='list', elements='dict', options=inner_trap_host_args),
)
inner_trap_args.update(make_module_args(trap_params))

community_params = ['policy', 'limit-oid']
inner_community_args = dict(
    name=dict(type='str', required=True),
)
inner_community_args.update(make_module_args(community_params))

system_params = ['name', 'contact', 'location']
inner_system_args = make_module_args(system_params)

outermost_param_str = ['status', 'load-timeout']

outermost_args = make_module_args(outermost_param_str)

module_args = dict(
    trap=dict(type='dict', options=inner_trap_args),
    community=dict(type='list', elements='dict', options=inner_community_args),
    system=dict(type='dict', options=inner_system_args),
)
module_args.update(outermost_args)

name = 'snmp'


class PaskSnmp(PaskModule):
    def __init__(self, name, module_args):
        super(PaskSnmp, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        self.resp = self.put(self.url, data)


def main():
    snmp = PaskSnmp(name, module_args)
    snmp.set_param()
    snmp.run()
    snmp.set_result()

if __name__ == '__main__':
    main()
