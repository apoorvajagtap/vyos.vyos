#
# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The vyos_firewall_zones config file.
It is in this file where the current configuration (as dict)
is compared to the provided configuration (as dict) and the command set
necessary to bring the current configuration to its desired end-state is
created.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    dict_merge,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.resource_module import (
    ResourceModule,
)
from ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.facts.facts import (
    Facts,
)
from ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.rm_templates.firewall_zones import (
    Firewall_zonesTemplate,
)


class Firewall_zones(ResourceModule):
    """
    The vyos_firewall_zones config class
    """

    def __init__(self, module):
        super(Firewall_zones, self).__init__(
            empty_fact_val={},
            facts_module=Facts(module),
            module=module,
            resource="firewall_zones",
            tmplt=Firewall_zonesTemplate(),
        )
        self.parsers = [
            "name",
            "default_action",
            "description",
            "from_name",
            "firewall_name",
            "firewall_v6_name",
            "interfaces",
            "local_zone",
        ]

    def execute_module(self):
        """ Execute the module

        :rtype: A dictionary
        :returns: The result from module execution
        """
        if self.state not in ["parsed", "gathered"]:
            self.generate_commands()
            self.run_commands()
        return self.result

    def generate_commands(self):
        """ Generate configuration commands to send based on
            want, have and desired state.
        """
        # wantd = {entry['name']: entry for entry in self.want}
        # haved = {entry['name']: entry for entry in self.have}

        wantd = {}
        haved = {}
        for entry in self.want:
            wantd.update({entry["name"]: entry})
        for entry in self.have:
            haved.update({entry["name"]: entry})

        # turn all lists into dicts prior to merge
        for entry in wantd, haved:
            self._fz_dict_to_list(entry)

        print("wantd just before merging >>", wantd)
        print("haved just before merging >>", wantd)

        # if state is merged, merge want onto have and then compare
        if self.state == "merged":
            wantd = dict_merge(haved, wantd)

        print("wantd after merge, >> ", wantd)

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {
                k: v for k, v in iteritems(haved) if k in wantd or not wantd
            }
            wantd = {}

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in iteritems(haved):
                if k not in wantd:
                    self._compare(want={}, have=have)

        for k, want in iteritems(wantd):
            self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Firewall_zones network resource.
        """
        print("inside _compare >>>>>> ", want, "+++", have)
        self.compare(parsers=self.parsers, want=want, have=have)

    def _fz_dict_to_list(self, entry):
        for name, config in iteritems(entry):
            if "interfaces" in config:
                int_list = []
                for int in config["interfaces"]:
                    int_list.append(int["name"])
                config["interfaces"] = int_list
