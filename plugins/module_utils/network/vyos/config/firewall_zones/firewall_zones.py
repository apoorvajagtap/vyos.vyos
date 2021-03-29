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
    get_from_dict,
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
            "interfaces",
            "description",
            "default_action",
            "from",
            "local_zone",
            "remove_zone",
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
        wantd = {entry['name']: entry for entry in self.want}
        haved = {entry['name']: entry for entry in self.have}

        print("wantd ---------->", wantd, "haved --------------->", haved)

        ### commented out following, as we just need wantd configurations to be set,
        ### and no referance with wantd,,, but commenting out following is a problem for
        ### 'from' parser with merged state. (Alternative from line 87)
        # if state is merged, merge want onto have and then compare
        # if self.state == "merged":
        #     wantd = dict_merge(haved, wantd)

        if self.state == "merged":
            for parser in self.parsers:
                if parser != "interfaces":
                    print("NOPE !!!", parser)
                    wantd = dict_merge(haved, wantd)
                    continue

        # if state is deleted, empty out wantd and set haved to wantd
        if self.state == "deleted":
            haved = {
                k: v for k, v in iteritems(haved) if k in wantd or not wantd
            }
            #wantd = {}

        # remove superfluous config for overridden and deleted
        if self.state in ["overridden", "deleted"]:
            for k, have in iteritems(haved):
                if k not in wantd:
                    self._compare(want={}, have=have)

        for k, want in iteritems(wantd):
            if self.state == "deleted":
                self._compare_for_deleted_state(want=want, have=haved.pop(k, {}))
                # for parser in self.parsers:
                #     if parser == "interfaces":
                #         self.addcmd(want, parser, True)
            else:
                self._compare(want=want, have=haved.pop(k, {}))

    def _compare(self, want, have):
        """Leverages the base class `compare()` method and
           populates the list of commands to be run by comparing
           the `want` and `have` data with the `parsers` defined
           for the Firewall_zones network resource.
        """
        self.compare(parsers=self.parsers, want=want, have=have)

    def _compare_for_deleted_state(self, want=None, have=None):
        for parser in self.parsers:
            compval = self._tmplt.get_parser(parser).get("compval")
            if not compval:
                compval = parser
            _inw = get_from_dict(want, compval)
            _inh = get_from_dict(have, compval)

            print("want inside config-fw-zone ------->", want, "have inside config-fw-zone ------>", have)
            print("_inw inside config-fw-zone ------>", _inw, "_inh inside config-fw-zone ------>", _inh)
            print("=========================================================")

            ## If inw is not none, delete the entries. otherwise skip
            if _inw is not None: #and _inw != _inh:
                print("######################## check 1 +++++++ ")
                if isinstance(_inw, bool):
                    if _inw is False and _inh is None:
                        continue
                    self.addcmd(want, parser, not _inw)
                else:
                    self.addcmd(want, parser, True)
            # elif _inw is None and _inh is not None:
            #     print("######################## check 2---------------- ")
            #     if isinstance(_inh, bool):
            #         self.addcmd(have, parser, _inh)
            #     else:
            #         self.addcmd(have, parser, False)