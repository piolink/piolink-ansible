#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: my_sample_module

short_description: This is my sample module

version_added: "2.4"

description:
    - "This is my longer description explaining my sample module"

options:
    name:
        description:
            - This is the message to send to the sample module
        required: true
    new:
        description:
            - Control to demo if the result of this module is changed or not
        required: false

extends_documentation_fragment
    - azure

author:
    - Your Name (@yourhandle)
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  my_new_test_module:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_new_test_module:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_new_test_module:
    name: fail me
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: The output message that the sample module generates
'''

import os
import logging
import requests
import copy
import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.pask_prestapi import PrestApi,\
    OP_DELETE, OP_GET, OP_POST, OP_PUT
from ansible.module_utils.pask_module import PaskModule


module_args = dict(
    uri=dict(type='str', required=True),
    data=dict(type='str'),
    method=dict(type='str')
)

name = 'prest'


class PaskPrest(PaskModule):
    def __init__(self, name, module_args):
        super(PaskPrest, self).__init__(name, module_args)

    def run(self):
        resp = None
        rest_method = ['get', 'post', 'put', 'delete']
        if self.module.params['method'] not in rest_method:
            return self.result
        url = 'https://{}:{}{}'.format(self.module.params['prest_ip'],
                                       self.module.params['prest_port'],
                                       self.module.params['uri'])
        if self.module.params['data'] is not None:
            data = json.loads(self.module.params['data'])

        if self.module.params['method'] == 'get':
            resp = self.get(url)
        elif self.module.params['method'] == 'post':
            resp = self.post(url, data)
        elif self.module.params['method'] == 'put':
            resp = self.put(url, data)
        elif self.module.params['method'] == 'delete':
            resp = self.delete(url, data)

        if resp is not None:
            self.resp = resp


def main():
    prest = PaskPrest(name, module_args)
    prest.set_param()
    prest.run()
    prest.set_result()


if __name__ == '__main__':
    main()
