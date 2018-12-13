#!/usr/bin/python

import os
import logging
import requests
import copy
import ast
import pprint
import ast
import sys
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pask_prestapi import PrestApi,\
    OP_DELETE, OP_GET, OP_POST, OP_PUT
from ansible.module_utils.pask_module import PaskModule,\
    make_module_args, try_except


# make vip args
protocol_inner_args = dict(
    protocol=dict(type='str', required=True),
    vport=dict(type='str')
)

vip_inner_args = dict(
    ip=dict(type='str', required=True),
    protocol=dict(type='dict', options=protocol_inner_args)
)

# real inner args
real_inner_param = [
    'rport', 'status', 'graceful-shutdown'
]
real_inner_args = dict(
    id=dict(type='str', required=True),
)
d = make_module_args(real_inner_param)
real_inner_args.update(d)

slow_start_inner_args = dict(
    rate=dict(type='str'),
    timer=dict(type='str'),
)

# sticky param
sticky_inner_param = [
    'time', 'source-subnet'
]
sticky_inner_args = make_module_args(sticky_inner_param)

# make dynamic_proximity_args
dynamic_proximity_inner_args = dict(
    name=dict(type='str', required=True),
    ratio=dict(type='str')
)

# session_timeout inner_args
session_timeout_params = [
    'generic', 'icmp', 'udp-stream', 'udp-stream', 'tcp-syn-sent',
    'tcp-syn-recv', 'tcp-established', 'tcp-fin-wait', 'tcp-close-wait',
    'tcp-last-ack', 'tcp-wait', 'tcp-close', 'tcp-unassured'
]
session_timeout_inner_args = make_module_args(session_timeout_params)

# make filter args
filter_param = [
    'dip', 'dport', 'protocol', 'sip', 'sport', 'status', 'type'
]
filter_inner_args = dict(
    id=dict(type='str', required=True)
)
filter_inner_args.update(make_module_args(filter_param))

# make outermost of module_args
module_args = dict(
    name=dict(type='str', required=True),
    vip=dict(type='list', elements='dict', options=vip_inner_args),
    real=dict(type='list', elements='dict', options=real_inner_args),
    sticky=dict(type='dict', options=sticky_inner_args),
)
module_args['health-check'] = dict(type='list')
module_args['slow-start'] = dict(type='dict', options=slow_start_inner_args)
module_args['dynamic-proximity'] = dict(type='dict',
                                        options=dynamic_proximity_inner_args)
module_args['session-timeout'] = dict(type='dict',
                                      options=session_timeout_inner_args)
module_args['filter'] = dict(type='list',
                             elements='dict', options=filter_inner_args)

str_param_list = [
    'priority', 'nat-mode', 'lan-to-lan',
    'lb-method', 'session-sync',
    'fail-skip', 'backup', 'keep-backup', 'status',
    'snatip', 'state', 'passive-health-check', 'session-timeout-mode'
    'session-reset', 'active-nodest'
]

for p in str_param_list:
    module_args[p] = dict(type='str')

name = 'slb'


class PaskSlb(PaskModule):
    def __init__(self, name, module_args):
        super(PaskSlb, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = dict()
        if self.module.params['state'] == "absent":
            data[name] = {'name': self.module.params['name']}
            self.ok_error_msg['delete'] = ['EntryDoesNotExist']
            self.resp = self.delete(self.url, data)
        else:
            data = self.make_data(self.module.params, include_inner=True)
            filter_data = self.make_filter_data(data)
            data['filter'] = filter_data
            url = os.path.join(self.url, self.module.params['name'])
            self.resp = self.put(url, data)

    def make_filter_data(self, data):
        # module do not have filter data in playbook script
        vip_filter = self.make_filter_by_vip(data['vip'])

        if data.get('filter') is None:
            for _id in range(len(vip_filter)):
                vip_filter[_id]['id'] = str(_id + 1)
            return vip_filter

        # module have filter data in playbook script
        filter_data = list()
        used_filter_id = list()
        for param in data['filter']:
            used_filter_id.append(param['id'])

        f_compare_list = [
            'type', 'dip', 'sip', 'protocol', 'dport'
        ]

        append = False
        for vf in vip_filter:
            for df in data['filter']:
                for p in f_compare_list:
                    if vf.get(p) is None:
                        continue
                    if df.get(p) is None:
                        append = True
                    if vf[p] != df[p]:
                        append = True
            if append:
                for _id in range(1, 255):
                    if str(_id) not in used_filter_id:
                        vf['id'] = str(_id)
                        filter_data.append(vf)
                        used_filter_id.append(str(_id))
                        break

        return filter_data + data['filter']

    def make_filter_by_vip(self, vips):
        # make filter without id
        filter_list = list()

        for vip in vips:
            f_made_by_vip = {
                'type': 'include',
                'sip': '0.0.0.0/0',
                'protocol': 'all',
                'status': 'enable'
            }
            f_made_by_vip['dip'] = vip['ip'] + "/32"

            if vip.get('protocol') is not None:
                if vip['protocol'].get('vport') is not None:
                    f_made_by_vip['dport'] = vip['protocol'].get('vport')
                if vip['protocol'].get('protocol') is not None:
                    f_made_by_vip['protocol'] = vip['protocol'].get('protocol')
            filter_list.append(f_made_by_vip)
        return filter_list


def main():
    real = PaskSlb(name, module_args)
    real.set_param()
    real.run()
    real.set_result()

if __name__ == '__main__':
    main()
