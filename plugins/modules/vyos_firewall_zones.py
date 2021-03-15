#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""
The module file for vyos_firewall_zones
"""

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
module: vyos_firewall_zones
short_description: Firewall zones resource module
description: This module manages firewall zones on VyOS devices
author:
  - Apoorva Jagtap (@apoorvajagtap)
options:
  config:
    description: A dictionary of Firewall zone options.
    type: list
    elements: dict
    suboptions:
      name: 
        description:
          - Specifies the name of the zone.
        type: str
        required: True
      default_action:
        description:
          - Default-action for traffic coming into this zone.
          - drop (Drop silently (default))
          - reject (Drop and notify source)
        type: str
        choices: ['drop', 'reject']
      description:
        description:
          - Zone description.
        type: str
      from:
        description:
          - Zone from which to filter traffic.
        type: list
        elements: dict
        suboptions:
          from_zone:
            description:
              - Zone from which to filter traffic.
            type: str
            required: True
          afi:
            description:
              - Address Family Identifier (AFI) for firewall options.
            type: str
            choices: ['ipv4', 'ipv6']
            required: True
          rule_set_name:
            description:
              - Firewall ruleset.
            type: str
            required: True 
      interfaces:
        description:
          - Interface associated with zone.
        type: dict
        suboptions:
          name:
            description:
              - Specify the name of the interface.
            type: list
            required: True  
      local_zone:
        description:
          - Zone to be local-zone.
        type: bool        
  state:
    description:
    - The state the configuration should be left in
    type: str
    choices:
    - merged
    - replaced
    - overridden
    - deleted
    - gathered
    - rendered
    - parsed  
    default: merged
"""
EXAMPLES = """
# Using merged
#
# Before state:
# -------------
#
# vyos@vyos:~$ show configuration commands | match zone-policy
# set zone-policy zone test interface 'eth3'                    ## issue-aj

  - name: Merge the provided configuration with the exisiting running configuration
    vyos.vyos.vyos_firewall_zones:
      config:
        - name: 'zone1'
          description: 'Added zone named zone1'
          interfaces:
            - eth1
          default_action: 'drop'

        - name: 'zone2'
          description: 'Added zone named zone2'
          interfaces:
            - eth2
            - eth4

      state: merged
      
# After State:
# --------------
# vyos@vyos:~$ show configuration commands | match zone-policy
# set zone-policy zone test interface 'eth3'
# set zone-policy zone zone1 default-action 'drop'
# set zone-policy zone zone1 description 'Added zone named zone1'
# set zone-policy zone zone1 interface 'eth1'
# set zone-policy zone zone2 description 'Added zone named zone2'
# set zone-policy zone zone2 interface 'eth2'
# set zone-policy zone zone2 interface 'eth4'

# Module Execution:
# ----------------
#     "after": [
#         {
#             "default_action": "drop",
#             "interfaces": [
#                 "eth3"
#             ],
#             "name": "test"
#         },
#         {
#             "interfaces": [
#                 "eth1"
#             ],
#             "name": "zone1"
#         },
#         {
#             "interfaces": [
#                 "eth4"            // issue-aj (eth2 not being displayed)
#             ],
#             "name": "zone2"
#         }
#     ],
#     "before": [
#         {
#             "interfaces": [
#                 "eth3"
#             ],
#             "name": "test"
#         }
#     ],
#     "changed": true,
#     "commands": [
#         "set zone-policy zone zone1 interface eth1",
#         "set zone-policy zone zone1 description 'Added zone named zone1'",
#         "set zone-policy zone zone1 default-action 'drop'",
#         "set zone-policy zone zone2 interface eth2",
#         "set zone-policy zone zone2 interface eth4",
#         "set zone-policy zone zone2 description 'Added zone named zone2'"
#     ],


# Using Gathered:
# --------------

# Native Config:

# vyos@vyos:~$ show configuration commands | match zone-policy
# set zone-policy zone test interface 'eth3'
# set zone-policy zone zone1 default-action 'drop'
# set zone-policy zone zone1 description 'Added zone named zone1'
# set zone-policy zone zone1 interface 'eth1'
# set zone-policy zone zone2 description 'Added zone named zone2'
# set zone-policy zone zone2 interface 'eth2'
# set zone-policy zone zone2 interface 'eth4'
# vyos@vyos:~$ 

 - name: Gather config details
    vyos.vyos.vyos_firewall_zones:
      state: gathered
      
# Module Execution:
# -----------------

    # "gathered": [
    #     {
    #         "default_action": "drop",     //issue-aj (default_action set for zone1)
    #         "interfaces": [
    #             "eth3"
    #         ],
    #         "name": "test"
    #     },
    #     {
    #         "interfaces": [
    #             "eth1"
    #         ],
    #         "name": "zone1"
    #     },
    #     {
    #         "interfaces": [
    #             "eth4"
    #         ],
    #         "name": "zone2"
    #     }
    # ],

# Using deleted:
# -------------

# before state:
# -------------

# vyos@vyos:~$ show configuration commands | match zone-policy
# set zone-policy zone test interface 'eth3'
# set zone-policy zone zone1 default-action 'drop'
# set zone-policy zone zone1 description 'Added zone named zone1'
# set zone-policy zone zone1 interface 'eth1'
# set zone-policy zone zone2 description 'Added zone named zone2'
# set zone-policy zone zone2 interface 'eth2'
# set zone-policy zone zone2 interface 'eth4'
# vyos@vyos:~$

    - name: Delete device configuration
      vyos_firewall_zones:
        config:
          - name: 'zone2'
            interfaces:
              - eth2
                          
      state: deleted     
      
# After State:
# -----------

# vyos@vyos:~$ show configuration commands | match zone-policy
# set zone-policy zone test interface 'eth3'
# set zone-policy zone zone1 default-action 'drop'
# set zone-policy zone zone1 description 'Added zone named zone1'
# set zone-policy zone zone1 interface 'eth1'
# set zone-policy zone zone2 description 'Added zone named zone2'
# set zone-policy zone zone2 interface 'eth2'       
# vyos@vyos:~$ 
#
#
    # "after": [
    #     {
    #         "default_action": "drop",
    #         "interfaces": [
    #             "eth3"
    #         ],
    #         "name": "test"
    #     },
    #     {
    #         "interfaces": [
    #             "eth1"
    #         ],
    #         "name": "zone1"
    #     },
    #     {
    #         "interfaces": [
    #             "eth2"
    #         ],
    #         "name": "zone2"
    #     }
    # ],
    # "before": [
    #     {
    #         "default_action": "drop",
    #         "interfaces": [
    #             "eth3"
    #         ],
    #         "name": "test"
    #     },
    #     {
    #         "interfaces": [
    #             "eth1"
    #         ],
    #         "name": "zone1"
    #     },
    #     {
    #         "interfaces": [
    #             "eth4"
    #         ],
    #         "name": "zone2"
    #     }
    # ],
    # "changed": true,
    # "commands": [
    #     "delete zone-policy zone zone2 interface eth4"       // issue-aj (should have deleted eth2, but deleted eth4)
    # ],

"""

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.argspec.firewall_zones.firewall_zones import (
    Firewall_zonesArgs,
)
from ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.config.firewall_zones.firewall_zones import (
    Firewall_zones,
)


def main():
    """
    Main entry point for module execution

    :returns: the result form module invocation
    """
    module = AnsibleModule(
        argument_spec=Firewall_zonesArgs.argument_spec,
        mutually_exclusive=[["config", "running_config"]],
        required_if=[
            ["state", "merged", ["config"]],
            ["state", "replaced", ["config"]],
            ["state", "overridden", ["config"]],
            ["state", "rendered", ["config"]],
            ["state", "parsed", ["running_config"]],
        ],
        supports_check_mode=True,
    )

    result = Firewall_zones(module).execute_module()
    module.exit_json(**result)


if __name__ == "__main__":
    main()
