#!/usr/bin/python

import os
import logging
import requests
import copy
import ast
import pprint
import netaddr
import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pask_prestapi import PrestApi,\
    OP_DELETE, OP_GET, OP_POST, OP_PUT
from ansible.module_utils.pask_module import PaskModule,\
    make_module_args, try_except

inner_interface_params = ['interface']
inner_interface_args = make_module_args(inner_interface_params)
inner_gateway_params = ['gateway']
inner_gateway_args = make_module_args(inner_gateway_params)

inner_network_args = dict(
    dest=dict(type='str', required=True),
    interface=dict(type='list', options=inner_interface_args),
    gateway=dict(type='list', options=inner_gateway_args)
)
inner_defaultgw_params = ['priority', 'gatway']
inner_health_check_args = dict(
    id=dict(type="str", required=True)
)
inner_defaultgw_args = dict()
inner_defaultgw_args['health-check'] = dict(type='list',
                                            options=inner_health_check_args)
module_args = dict(
    network=dict(type='list', options=inner_network_args),
)
module_args['default-gateway'] = dict(type='list',
                                      options=inner_defaultgw_args)

name = 'route'


class PaskRoute(PaskModule):
    def __init__(self, name, module_args):
        super(PaskRoute, self).__init__(name, module_args)

    @try_except
    def run(self):
        interface_url = self.url.replace(name, 'interface')
        resp = self.get(interface_url)
        resp_dict = json.loads(resp.text)

        if_list = self.get_if_and_ip(resp_dict['interface'])

        route_data = self.make_route_data_from_interface(if_list)

        data = self.make_data(self.module.params, include_inner=True)

        if data.get('network') is None:
            data['network'] = route_data
        else:
            data['network'].extend(route_data)

        self.resp = self.put(self.url, data)

    def get_if_and_ip(self, data):
        """
            return value example
        [
            {'interface': 'mgmt', 'ip': '192.168.214.145/24'},
            {'interface': 'v2933', 'ip': '10.10.10.100/24'},
            {'interface': 'v2933', 'ip': '10.10.10.100/28'}
        ]
        """
        if_list = list()
        for interface in data:
            if interface.get('ip') is None:
                continue

            if type(interface['ip']) == list:
                for ip in interface['ip']:
                    d = {
                        'ip': ip['address'],
                        'interface': interface['name']
                    }
                    if_list.append(d)
            else:
                d = {
                    'ip': interface['ip']['address'],
                    'interface': interface['name']
                }
                if_list.append(d)
        return if_list

    def make_route_data_from_interface(self, if_list):
        network = list()
        for _if in if_list:
            net = netaddr.IPNetwork(_if['ip'])
            dest = str(net.network) + "/" + str(net.prefixlen)
            d = {
                "dest": dest,
                "interface": {
                    "interface": _if['interface']
                }
            }
            network.append(d)
        return network


def main():
    route = PaskRoute(name, module_args)
    route.set_param()
    route.run()
    route.set_result()

if __name__ == '__main__':
    main()
