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


module_args = dict(
    hostname=dict(type="str", required=True)
)

name = 'hostname'


class PaskHostname(PaskModule):
    def __init__(self, name, module_args):
        super(PaskHostname, self).__init__(name, module_args)

    @try_except
    def run(self):
        resp = None

        data = self.make_data(self.module.params)
        resp = self.put(self.url, data)
        self.resp = resp


def main():
    hostname = PaskHostname(name, module_args)
    hostname.set_param()
    hostname.run()
    hostname.set_result()

if __name__ == '__main__':
    main()
