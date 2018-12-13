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


inner_ip_args = dict(
    address=dict(type='str', required=True),
    broadcast=dict(type='str'),
    overlapped=dict(type='str')
)

inner_ip6_args = dict(
    address=dict(type='str', required=True),
    broadcast=dict(type='str'),
)

inner_ip6_args['adv-on-link'] = dict(type='str')
inner_ip6_args['adv-autonomous'] = dict(type='str')
inner_ip6_args['adv-router-addr'] = dict(type='str')
inner_ip6_args['adv-valid-lifetime'] = dict(type='str')
inner_ip6_args['adv-preferred-lifetime'] = dict(type='str')

module_args = dict(
    name=dict(type='str', required=True),
    ip=dict(type='dict', options=inner_ip_args),
    ip6=dict(type='dict', options=inner_ip6_args),
    mtu=dict(type='str'),
    rpf=dict(type='str'),
    status=dict(type='str'),
)

module_args['adv-cur-hop-limit'] = dict(type='str')
module_args['adv-default-lifetime'] = dict(type='str')
module_args['adv-reachable-time'] = dict(type='str')
module_args['adv-retrans-timer'] = dict(type='str')
module_args['adv-send-advert'] = dict(type='str')
module_args['max-rtr-adv-interval'] = dict(type='str')
module_args['min-rtr-adv-interval'] = dict(type='str')

name = 'interface'


class PaskInterface(PaskModule):
    def __init__(self, name, module_args):
        super(PaskInterface, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params, include_inner=True)
        url = os.path.join(self.url, self.module.params['name'])
        self.resp= self.put(url, data)


def main():
    interface = PaskInterface(name, module_args)
    interface.set_param()
    interface.run()
    interface.set_result()

if __name__ == '__main__':
    main()
