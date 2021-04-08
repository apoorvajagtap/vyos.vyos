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
          afi:
            description:
              - Address Family Identifier (AFI) for firewall options.
            type: str
            choices: ['ipv4', 'ipv6']
          rule_set_name:
            description:
              - Firewall ruleset.
            type: str
          remove_from:
            description:
              - Delete the "from" section for a zone.
            type: bool
      interfaces:
        description:
          - Interface associated with zone.
        type: list 
      local_zone:
        description:
          - Zone to be local-zone.
        type: bool
      remove_zone:        
        description:
          - Set to True in order to delete all the configurations specifc to a particular zone
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
# set zone-policy zone zone1 interface 'eth1'

  - name: Merge the provided configuration with the exisiting running configuration
    vyos_firewall_zones:
      config:
        - name: 'zone1'
          default_action: 'drop'
          description: 'Merging configurations for zone1'
        - name: 'zone2'
          interfaces:
            - eth2
            - eth3
          description: 'Added zone named zone2'
      state: merged
      
# After State:
# --------------

# vyos@vyos:~$ show configuration commands | match zone-policy
# set zone-policy zone zone1 default-action 'drop'
# set zone-policy zone zone1 description 'Merging configurations for zone1'
# set zone-policy zone zone1 interface 'eth1'
# set zone-policy zone zone2 description 'Added zone named zone2'
# set zone-policy zone zone2 interface 'eth2'
# set zone-policy zone zone2 interface 'eth3'

# Module Execution:
# ----------------
#     "after": [
#         {
#             "default_action": "drop",
#             "description": "Merging configurations for zone1",
#             "interfaces": [
#                 "eth1"
#             ],
#             "name": "zone1"
#         },
#         {
#             "description": "Added zone named zone2",
#             "interfaces": [
#                 "eth3",
#                 "eth2"
#             ],
#             "name": "zone2"
#         }
#     ],
#     "before": [
#         {
#             "interfaces": [
#                 "eth1"
#             ],
#             "name": "zone1"
#         }
#     ],
#     "changed": true,
#     "commands": [
#         "set zone-policy zone zone1 description 'Merging configurations for zone1'",
#         "set zone-policy zone zone1 default-action drop",
#         "set zone-policy zone zone2 interface eth2",
#         "set zone-policy zone zone2 interface eth3",
#         "set zone-policy zone zone2 description 'Added zone named zone2'"
#     ],


# Using replaced:

# Before State:
# ------------

# vyos@vyos:~$ show configuration commands | match zone-policy
# set zone-policy zone zone1 default-action 'drop'
# set zone-policy zone zone1 description 'Merging configurations for zone1'
# set zone-policy zone zone1 interface 'eth1'
# set zone-policy zone zone2 description 'Added zone named zone2'
# set zone-policy zone zone2 interface 'eth2'
# set zone-policy zone zone2 interface 'eth3'

  - name: Replace provided configuration with device configuration
    vyos_firewall_zones:
      config:
        - name: 'zone1'
          interfaces:
            - eth4
        - name: 'zone2'
          interfaces:
            - eth2
          description: 'Replaced the description for zone2'
      state: replaced
      
# After State:
# -----------

# vyos@vyos:~$ show configuration commands | match zone-policy
# set zone-policy zone zone1 interface 'eth1'
# set zone-policy zone zone1 interface 'eth4'
# set zone-policy zone zone2 description 'Replaced the description for zone2'
# set zone-policy zone zone2 interface 'eth2'
# set zone-policy zone zone2 interface 'eth3'

# Module Execution
# ----------------
#     "after": [
#         {
#             "interfaces": [
#                 "eth4",
#                 "eth1"
#             ],
#             "name": "zone1"
#         },
#         {
#             "description": "Replaced the description for zone2",
#             "interfaces": [
#                 "eth2",
#                 "eth3"
#             ],
#             "name": "zone2"
#         }
#     ],
#     "before": [
#         {
#             "default_action": "drop",
#             "description": "Merging configurations for zone1",
#             "interfaces": [
#                 "eth1"
#             ],
#             "name": "zone1"
#         },
#         {
#             "description": "Added zone named zone2",
#             "interfaces": [
#                 "eth2",
#                 "eth3"
#             ],
#             "name": "zone2"
#         }
#     ],
#     "changed": true,
#     "commands": [
#         "set zone-policy zone zone1 interface eth4",
#         "delete zone-policy zone zone1 description 'Merging configurations for zone1'",
#         "delete zone-policy zone zone1 default-action drop",
#         "set zone-policy zone zone2 interface eth2",
#         "set zone-policy zone zone2 description 'Replaced the description for zone2'"
#     ],
#

# Using Overridden:
# -----------------

# Before State:
# ------------

# vyos@vyos:~$ show configuration commands | match zone-policy
# set zone-policy zone zone1 default-action 'drop'
# set zone-policy zone zone1 description 'Merging configurations for zone1'
# set zone-policy zone zone1 interface 'eth1'
# set zone-policy zone zone2 description 'Added zone named zone2'
# set zone-policy zone zone2 interface 'eth2'

  - name: Override device configuration with provided configuration
    vyos_firewall_zones:
      config:
        - name: 'zone1'
          interfaces:
            - eth1
        - name: 'zone2'
          interfaces:
            - eth2
        - name: 'zone3'
          description: 'Adding new zone zone3'
          interfaces:
            - eth4
      
      state: overridden
      
# After State:
# -----------

# vyos@vyos:~$ show configuration commands | match zone-policy
# set zone-policy zone zone1 interface 'eth1'
# set zone-policy zone zone2 interface 'eth2'
# set zone-policy zone zone3 description 'Adding new zone zone3'
# set zone-policy zone zone3 interface 'eth4'

# Module Execution:
# ----------------

#       "after": [
#           {
#               "interfaces": [
#                   "eth1"
#               ],
#               "name": "zone1"
#           },
#           {
#               "interfaces": [
#                   "eth2"
#               ],
#               "name": "zone2"
#           },
#           {
#               "description": "Adding new zone zone3",
#               "interfaces": [
#                   "eth4"
#               ],
#               "name": "zone3"
#           }
#       ],
#       "before": [
#           {
#               "default_action": "drop",
#               "description": "Merging configurations for zone1",
#               "interfaces": [
#                   "eth1"
#               ],
#               "name": "zone1"
#           },
#           {
#               "description": "Added zone named zone2",
#               "interfaces": [
#                   "eth2"
#               ],
#               "name": "zone2"
#           }
#       ],
#       "changed": true,
#       "commands": [
#           "delete zone-policy zone zone1 description 'Merging configurations for zone1'",
#           "delete zone-policy zone zone1 default-action drop",
#           "delete zone-policy zone zone2 description 'Added zone named zone2'",
#           "set zone-policy zone zone3 interface eth4",
#           "set zone-policy zone zone3 description 'Adding new zone zone3'"
#       ],

# Using deleted:
# -------------

# Before State:
# -------------

# vyos@vyos:~$ show configuration commands | match zone-policy
# set zone-policy zone zone1 default-action 'drop'
# set zone-policy zone zone1 description 'Merging configurations for zone1'
# set zone-policy zone zone1 interface 'eth1'
# set zone-policy zone zone2 description 'Added zone named zone2'
# set zone-policy zone zone2 from zone1 firewall name 'Downlink'
# set zone-policy zone zone2 interface 'eth2'
# set zone-policy zone zone2 interface 'eth3'
# set zone-policy zone zone3 from zone2 firewall ipv6-name 'V6-LOCAL'
# set zone-policy zone zone3 interface 'eth4'

  - name: Delete the specified configurations
    vyos_firewall_zones:
      config:
        - name: 'zone3'
          from:
            - remove_from: True
        - name: 'zone2'
          interfaces:
            - eth3
          description: 'Added zone named zone2'
      state: deleted

# After State:
# ------------

# vyos@vyos:~$ show configuration commands | match zone-policy
# set zone-policy zone zone1 default-action 'drop'
# set zone-policy zone zone1 description 'Merging configurations for zone1'
# set zone-policy zone zone1 interface 'eth1'
# set zone-policy zone zone2 from zone1 firewall name 'Downlink'
# set zone-policy zone zone2 interface 'eth2'
# set zone-policy zone zone3 interface 'eth4'

# Module Execution:
# -----------------
 
#     "after": [
#         {
#             "default_action": "drop",
#             "description": "Merging configurations for zone1",
#             "interfaces": [
#                 "eth1"
#             ],
#             "name": "zone1"
#         },
#         {
#             "from": [
#                 "zone1",
#                 "ipv4",
#                 "Downlink"
#             ],
#             "interfaces": [
#                 "eth2"
#             ],
#             "name": "zone2"
#         },
#         {
#             "interfaces": [
#                 "eth4"
#             ],
#             "name": "zone3"
#         }
#     ],
#     "before": [
#         {
#             "default_action": "drop",
#             "description": "Merging configurations for zone1",
#             "interfaces": [
#                 "eth1"
#             ],
#             "name": "zone1"
#         },
#         {
#             "description": "Added zone named zone2",
#             "from": [
#                 "zone1",
#                 "ipv4",
#                 "Downlink"
#             ],
#             "interfaces": [
#                 "eth3",
#                 "eth2"
#             ],
#             "name": "zone2"
#         },
#         {
#             "from": [
#                 "zone2",
#                 "ipv6",
#                 "V6-LOCAL"
#             ],
#             "interfaces": [
#                 "eth4"
#             ],
#             "name": "zone3"
#         }
#     ],
#     "changed": true,
#     "commands": [
#         "delete zone-policy zone zone3 from",
#         "delete zone-policy zone zone2 interface eth3",
#         "delete zone-policy zone zone2 description 'Added zone named zone2'"
#     ],


# Using Gathered:
# --------------

# Native Config:

# vyos@vyos:~$ show configuration commands | match zone-policy
# set zone-policy zone zone1 default-action 'drop'
# set zone-policy zone zone1 description 'Merging configurations for zone1'
# set zone-policy zone zone1 interface 'eth1'
# set zone-policy zone zone2 from zone1 firewall name 'Downlink'
# set zone-policy zone zone2 interface 'eth2'
# set zone-policy zone zone3 description 'This is zone3'
# set zone-policy zone zone3 interface 'eth4'

 - name: Gather config details
    vyos.vyos.vyos_firewall_zones:
      state: gathered
      
# Module Execution:
# -----------------
# 
#      "gathered": [
#         {
#             "default_action": "drop",
#             "description": "Merging configurations for zone1",
#             "interfaces": [
#                 "eth1"
#             ],
#             "name": "zone1"
#         },
#         {
#             "from": [
#                 "zone1",
#                 "ipv4",
#                 "Downlink"
#             ],
#             "interfaces": [
#                 "eth2"
#             ],
#             "name": "zone2"
#         },
#         {
#             "description": "This is zone3",
#             "interfaces": [
#                 "eth4"
#             ],
#             "name": "zone3"
#         }
#     ],


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
