#!/usr/bin/python
# coding: utf-8 -*-

# Copyright (C) 2020 Inspur Inc. All Rights Reserved.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
---
module: is_edit_priv_user
version_added: 1.0
author:
    - WangBaoshan
short_description: Change user privilege
description:
   - Change user privilege on Inspur server.
options:
    uname:
        description:
            - User name.
        type: str
        required: true
    role_id:
        description:
            - user role id of new user.
        default: NoAccess
        choices: ['Administrator', 'Operator', 'Commonuser','OEM','NoAccess']
        type: str
    priv:
        description:
            - user access, select one or more from None/KVM/VMM/SOL.
        type: list
        elements: str
        required: true
'''

EXAMPLES = '''
- name: edit user privilege test
  hosts: ism
  connection: local
  gather_facts: no
  vars:
    ism:
      host: "{{ ansible_ssh_host }}"
      username: "{{ username }}"
      password: "{{ password }}"

  tasks:

  - name: "change user privilege"
    is_edit_priv_user:
      uname: "wbs"
      role_id: "Administrator"
      priv: "KVM,SOL"
      provider: "{{ ism }}"
'''

RETURN = '''

message:
    description: messages returned after module execution
    returned: always
    type: str
state:
    description: status after module execution
    returned: always
    type: str
changed:
    description: check to see if a change was made on the device
    returned: always
    type: false
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.general.plugins.module_utils.ism import ism_argument_spec, get_connection


class User(object):
    def __init__(self, argument_spec):
        self.spec = argument_spec
        self.module = None
        self.init_module()
        self.results = dict()

    def init_module(self):
        """Init module object"""

        self.module = AnsibleModule(
            argument_spec=self.spec, supports_check_mode=True)

    def run_command(self):
        self.module.params['subcommand'] = 'setpriv'
        self.results = get_connection(self.module)

    def show_result(self):
        """Show result"""
        self.module.exit_json(**self.results)

    def work(self):
        """Worker"""
        self.run_command()
        self.show_result()


def main():
    argument_spec = dict(
        uname=dict(type='str', required=True),
        role_id=dict(type='str', default='NoAccess', choices=['Administrator', 'Operator', 'Commonuser', 'OEM', 'NoAccess']),
        priv=dict(type='list', elements='str', required=True),
    )
    argument_spec.update(ism_argument_spec)
    user_obj = User(argument_spec)
    user_obj.work()


if __name__ == '__main__':
    main()
