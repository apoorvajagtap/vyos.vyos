# -*- coding: utf-8 -*-
# Copyright 2021 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

"""
The vyos firewall_zones fact class
It is in this file the configuration is collected from the device
for a given resource, parsed, and the facts tree is populated
based on the configuration.
"""

from copy import deepcopy

from ansible.module_utils.six import iteritems
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common import (
    utils,
)
from ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.rm_templates.firewall_zones import (
    Firewall_zonesTemplate,
)
from ansible_collections.vyos.vyos.plugins.module_utils.network.vyos.argspec.firewall_zones.firewall_zones import (
    Firewall_zonesArgs,
)

class Firewall_zonesFacts(object):
    """ The vyos firewall_zones facts class
    """

    def __init__(self, module, subspec='config', options='options'):
        self._module = module
        self.argument_spec = Firewall_zonesArgs.argument_spec
        spec = deepcopy(self.argument_spec)
        if subspec:
            if options:
                facts_argument_spec = spec[subspec][options]
            else:
                facts_argument_spec = spec[subspec]
        else:
            facts_argument_spec = spec

        self.generated_spec = utils.generate_dict(facts_argument_spec)

    def populate_facts(self, connection, ansible_facts, data=None):
        """ Populate the facts for Firewall_zones network resource

        :param connection: the device connection
        :param ansible_facts: Facts dictionary
        :param data: previously collected conf

        :rtype: dictionary
        :returns: facts
        """
        facts = {}
        objs = []

        if not data:
            data = connection.get("show configuration commands | match zone-policy")

        # parse native config using the Firewall_zones template
        firewall_zones_parser = Firewall_zonesTemplate(lines=data.splitlines())
        objs = list(firewall_zones_parser.parse().values())

        ansible_facts['ansible_network_resources'].pop('firewall_zones', None)

        params = utils.remove_empties(
            utils.validate_config(self.argument_spec, {"config": objs})
        )

        facts['firewall_zones'] = params['config']
        ansible_facts['ansible_network_resources'].update(facts)

        return ansible_facts
