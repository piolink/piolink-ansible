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

mostouter_params = [
    'status', 'primary-server', 'secondary-server', 'minpoll',
    'maxpoll'
]

module_args = make_module_args(mostouter_params)

name = 'ntp'


class PaskNtp(PaskModule):
    def __init__(self, name, module_args):
        super(PaskNtp, self).__init__(name, module_args)

    @try_except
    def run(self):
        data = self.make_data(self.module.params)
        self.resp = self.put(self.url, data)


def main():

    ntp = PaskNtp(name, module_args)
    ntp.set_param()
    ntp.run()
    ntp.set_result()

if __name__ == '__main__':
    main()
