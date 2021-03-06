#!/bin/env python
import unittest
from unittest.mock import Mock
from ats.topology import Device

from genie.metaparser.util.exceptions import SchemaEmptyParserError,\
                                             SchemaMissingKeyError

from genie.libs.parser.iosxe.show_l2vpn import ShowBridgeDomain, \
                                               ShowEthernetServiceInstanceDetail, \
                                               ShowEthernetServiceInstanceStats, \
                                               ShowEthernetServiceInstanceSummary, \
                                               ShowL2vpnVfi, \
                                               ShowL2vpnServiceAll


class test_show_bridge_domain(unittest.TestCase):

    device = Device(name='aDevice')

    empty_output = {'execute.return_value': ''}

    golden_parsed_output_full = {
        'bridge_domain': {
            2051: {
                'state': 'UP',
                'member_ports': ['vfi VPLS-2051 neighbor 10.120.202.64 2051', 'Port-channel1 service instance 2051'],
                'bd_domain_id': 2051,
                'aging_timer': 3600,
                'mac_table': {
                    'VPLS-2051.10200e6': {
                        'pseudoport': 'VPLS-2051.10200e6',
                        'mac_address': {
                            '0000.57C4.A8D9': {
                                'tag': 'dynamic',
                                'mac_address': '0000.57C4.A8D9',
                                'age': 3153,
                                'policy': 'forward',
                                'aed': 0,
                                },
                            },
                        },
                    'Port-channel1.EFP2051': {
                        'pseudoport': 'Port-channel1.EFP2051',
                        'mac_address': {
                            '0000.A000.0027': {
                                'tag': 'dynamic',
                                'mac_address': '0000.A000.0027',
                                'age': 3142,
                                'policy': 'forward',
                                'aed': 0,
                                },
                            '0000.A000.0097': {
                                'tag': 'dynamic',
                                'mac_address': '0000.A000.0097',
                                'age': 3153,
                                'policy': 'forward',
                                'aed': 0,
                                },
                            '0000.A000.013A': {
                                'tag': 'dynamic',
                                'mac_address': '0000.A000.013A',
                                'age': 3137,
                                'policy': 'forward',
                                'aed': 0,
                                },
                            '0000.A000.00BF': {
                                'tag': 'dynamic',
                                'mac_address': '0000.A000.00BF',
                                'age': 3125,
                                'policy': 'forward',
                                'aed': 0,
                                },
                            '0000.A000.010C': {
                                'tag': 'dynamic',
                                'mac_address': '0000.A000.010C',
                                'age': 3133,
                                'policy': 'forward',
                                'aed': 0,
                                },
                            '0000.A000.010F': {
                                'tag': 'dynamic',
                                'mac_address': '0000.A000.010F',
                                'age': 3133,
                                'policy': 'forward',
                                'aed': 0,
                                },
                            },
                        },
                    },
                'mac_learning_state': 'Enabled',
                'split-horizon_group': {
                    '0': {
                        'interfaces': ['Port-channel1 service instance 2051'],
                        'num_of_ports': '1',
                        },
                    },
                'number_of_ports_in_all': 2,
                },
            2052: {
                'state': 'UP',
                'member_ports': ['vfi VPLS-2052 neighbor 10.120.202.64 2052', 'Port-channel1 service instance 2052'],
                'bd_domain_id': 2052,
                'aging_timer': 3600,
                'mac_table': {
                    'Port-channel1.EFP2052': {
                        'pseudoport': 'Port-channel1.EFP2052',
                        'mac_address': {
                            '0000.A000.002C': {
                                'tag': 'dynamic',
                                'mac_address': '0000.A000.002C',
                                'age': 3143,
                                'policy': 'forward',
                                'aed': 0,
                                },
                            '0000.A000.0015': {
                                'tag': 'dynamic',
                                'mac_address': '0000.A000.0015',
                                'age': 3141,
                                'policy': 'forward',
                                'aed': 0,
                                },
                            },
                        },
                    },
                'mac_learning_state': 'Enabled',
                'split-horizon_group': {
                    '0': {
                        'interfaces': ['Port-channel1 service instance 2052'],
                        'num_of_ports': '1',
                        },
                    },
                'number_of_ports_in_all': 2,
                },
            },
        }

    golden_output_full = {'execute.return_value': '''\
        Router#show bridge-domain
        Load for five secs: 55%/0%; one minute: 15%; five minutes: 10%
        Time source is NTP, 20:29:29.871 EST Fri Nov 11 2016

        Bridge-domain 2051 (2 ports in all)
        State: UP                    Mac learning: Enabled
        Aging-Timer: 3600 second(s)
            vfi VPLS-2051 neighbor 10.120.202.64 2051
        1 ports belonging to split-horizon group 0
            Port-channel1 service instance 2051 (split-horizon)
           AED MAC address    Policy  Tag       Age  Pseudoport
           0   0000.A000.0027 forward dynamic   3142 Port-channel1.EFP2051
           0   0000.A000.00BF forward dynamic   3125 Port-channel1.EFP2051
           0   0000.A000.013A forward dynamic   3137 Port-channel1.EFP2051
           0   0000.A000.010F forward dynamic   3133 Port-channel1.EFP2051
           0   0000.57C4.A8D9 forward dynamic   3153 VPLS-2051.10200e6
           0   0000.A000.0097 forward dynamic   3153 Port-channel1.EFP2051
           0   0000.A000.010C forward dynamic   3133 Port-channel1.EFP2051

        Bridge-domain 2052 (2 ports in all)
        State: UP                    Mac learning: Enabled
        Aging-Timer: 3600 second(s)
            vfi VPLS-2052 neighbor 10.120.202.64 2052
        1 ports belonging to split-horizon group 0
            Port-channel1 service instance 2052 (split-horizon)
           AED MAC address    Policy  Tag       Age  Pseudoport
           0   0000.A000.0015 forward dynamic   3141 Port-channel1.EFP2052
           0   0000.A000.002C forward dynamic   3143 Port-channel1.EFP2052
    '''
    }

    golden_parsed_output_bridge_domain = {
        'bridge_domain': {
            3051: {
                'number_of_ports_in_all': 2,
                'state': 'UP',
                'member_ports': ['vfi VPLS-3051 neighbor 192.168.36.220 3051', 'GigabitEthernet0/0/3 service instance 3051'],
                'mac_table': {
                    'GigabitEthernet0/0/3.EFP3051': {
                        'pseudoport': 'GigabitEthernet0/0/3.EFP3051',
                        'mac_address': {
                            '0000.A000.0118': {
                                'tag': 'dynamic',
                                'age': 3441,
                                'aed': 0,
                                'mac_address': '0000.A000.0118',
                                'policy': 'forward',
                                },
                            '0000.A000.0077': {
                                'tag': 'dynamic',
                                'age': 3426,
                                'aed': 0,
                                'mac_address': '0000.A000.0077',
                                'policy': 'forward',
                                },
                            '0000.A000.011C': {
                                'tag': 'dynamic',
                                'age': 3442,
                                'aed': 0,
                                'mac_address': '0000.A000.011C',
                                'policy': 'forward',
                                },
                            '0000.A000.001F': {
                                'tag': 'dynamic',
                                'age': 3416,
                                'aed': 0,
                                'mac_address': '0000.A000.001F',
                                'policy': 'forward',
                                },
                            '0000.A000.0068': {
                                'tag': 'dynamic',
                                'age': 3424,
                                'aed': 0,
                                'mac_address': '0000.A000.0068',
                                'policy': 'forward',
                                },
                            '0000.A000.00C5': {
                                'tag': 'dynamic',
                                'age': 3433,
                                'aed': 0,
                                'mac_address': '0000.A000.00C5',
                                'policy': 'forward',
                                },
                            '0000.A000.0108': {
                                'tag': 'dynamic',
                                'age': 3440,
                                'aed': 0,
                                'mac_address': '0000.A000.0108',
                                'policy': 'forward',
                                },
                            '0000.A000.0010': {
                                'tag': 'dynamic',
                                'age': 3415,
                                'aed': 0,
                                'mac_address': '0000.A000.0010',
                                'policy': 'forward',
                                },
                            '0000.A000.000F': {
                                'tag': 'dynamic',
                                'age': 3415,
                                'aed': 0,
                                'mac_address': '0000.A000.000F',
                                'policy': 'forward',
                                },
                            '0000.A000.007F': {
                                'tag': 'dynamic',
                                'age': 3426,
                                'aed': 0,
                                'mac_address': '0000.A000.007F',
                                'policy': 'forward',
                                },
                            '0000.A000.007B': {
                                'tag': 'dynamic',
                                'age': 3426,
                                'aed': 0,
                                'mac_address': '0000.A000.007B',
                                'policy': 'forward',
                                },
                            '0000.A000.0087': {
                                'tag': 'dynamic',
                                'age': 3427,
                                'aed': 0,
                                'mac_address': '0000.A000.0087',
                                'policy': 'forward',
                                },
                            '0000.A000.00AA': {
                                'tag': 'dynamic',
                                'age': 3430,
                                'aed': 0,
                                'mac_address': '0000.A000.00AA',
                                'policy': 'forward',
                                },
                            '0000.A000.012C': {
                                'tag': 'dynamic',
                                'age': 3443,
                                'aed': 0,
                                'mac_address': '0000.A000.012C',
                                'policy': 'forward',
                                },
                            '0000.A000.00D0': {
                                'tag': 'dynamic',
                                'age': 3434,
                                'aed': 0,
                                'mac_address': '0000.A000.00D0',
                                'policy': 'forward',
                                },
                            '0000.A000.00F6': {
                                'tag': 'dynamic',
                                'age': 3438,
                                'aed': 0,
                                'mac_address': '0000.A000.00F6',
                                'policy': 'forward',
                                },
                            '0000.A000.00F7': {
                                'tag': 'dynamic',
                                'age': 3438,
                                'aed': 0,
                                'mac_address': '0000.A000.00F7',
                                'policy': 'forward',
                                },
                            '0000.A000.00F2': {
                                'tag': 'dynamic',
                                'age': 3438,
                                'aed': 0,
                                'mac_address': '0000.A000.00F2',
                                'policy': 'forward',
                                },
                            '0000.A000.0129': {
                                'tag': 'dynamic',
                                'age': 3443,
                                'aed': 0,
                                'mac_address': '0000.A000.0129',
                                'policy': 'forward',
                                },
                            },
                        },
                    },
                'aging_timer': 3600,
                'bd_domain_id': 3051,
                'split-horizon_group': {
                    '0': {
                        'num_of_ports': '1',
                        'interfaces': ['GigabitEthernet0/0/3 service instance 3051'],
                        },
                    },
                'mac_learning_state': 'Enabled',
                },
            },
        }


    golden_output_bridge_domain = {'execute.return_value': '''\
        Router#show bridge-domain 3051
        Load for five secs: 10%/1%; one minute: 11%; five minutes: 12%
        Time source is NTP, 19:54:46.940 EST Wed Nov 2 2016

        Bridge-domain 3051 (2 ports in all)
        State: UP                    Mac learning: Enabled
        Aging-Timer: 3600 second(s)
            vfi VPLS-3051 neighbor 192.168.36.220 3051
        1 ports belonging to split-horizon group 0
            GigabitEthernet0/0/3 service instance 3051 (split-horizon)
           AED MAC address    Policy  Tag       Age  Pseudoport
           0   0000.A000.00F2 forward dynamic   3438 GigabitEthernet0/0/3.EFP3051
           0   0000.A000.00AA forward dynamic   3430 GigabitEthernet0/0/3.EFP3051
           0   0000.A000.0077 forward dynamic   3426 GigabitEthernet0/0/3.EFP3051
           0   0000.A000.00D0 forward dynamic   3434 GigabitEthernet0/0/3.EFP3051
           0   0000.A000.001F forward dynamic   3416 GigabitEthernet0/0/3.EFP3051
           0   0000.A000.0129 forward dynamic   3443 GigabitEthernet0/0/3.EFP3051
           0   0000.A000.00F6 forward dynamic   3438 GigabitEthernet0/0/3.EFP3051
           0   0000.A000.007B forward dynamic   3426 GigabitEthernet0/0/3.EFP3051
           0   0000.A000.0068 forward dynamic   3424 GigabitEthernet0/0/3.EFP3051
           0   0000.A000.00C5 forward dynamic   3433 GigabitEthernet0/0/3.EFP3051
           0   0000.A000.0087 forward dynamic   3427 GigabitEthernet0/0/3.EFP3051
           0   0000.A000.00F7 forward dynamic   3438 GigabitEthernet0/0/3.EFP3051
           0   0000.A000.0118 forward dynamic   3441 GigabitEthernet0/0/3.EFP3051
           0   0000.A000.0108 forward dynamic   3440 GigabitEthernet0/0/3.EFP3051
           0   0000.A000.007F forward dynamic   3426 GigabitEthernet0/0/3.EFP3051
           0   0000.A000.011C forward dynamic   3442 GigabitEthernet0/0/3.EFP3051
           0   0000.A000.012C forward dynamic   3443 GigabitEthernet0/0/3.EFP3051
           0   0000.A000.0010 forward dynamic   3415 GigabitEthernet0/0/3.EFP3051
           0   0000.A000.000F forward dynamic   3415 GigabitEthernet0/0/3.EFP3051
    '''
    }

    golden_parsed_output_count = {'lines_match_regexp': 32102}

    golden_output_count = {'execute.return_value': '''\
        Router#show bridge-domain | count Port-channel1\.EFP2.*
        Number of lines which match regexp = 32102
    '''
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        platform_obj = ShowBridgeDomain(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = platform_obj.parse()    

    def test_golden_full(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output_full)
        platform_obj = ShowBridgeDomain(device=self.device)
        parsed_output = platform_obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output_full)

    def test_golden_bridge_domain(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output_bridge_domain)
        platform_obj = ShowBridgeDomain(device=self.device)
        parsed_output = platform_obj.parse(bd_id='3051')
        self.assertEqual(parsed_output, self.golden_parsed_output_bridge_domain)

    def test_golden_count(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output_count)
        platform_obj = ShowBridgeDomain(device=self.device)
        parsed_output = platform_obj.parse(word='Port-channel1\.EFP2.*')
        self.assertEqual(parsed_output, self.golden_parsed_output_count)


class test_show_ethernet_service_instance_detail(unittest.TestCase):

    device = Device(name='aDevice')

    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        'service_instance': {
            400: {
                'l2protocol_drop': False,
                'associated_interface': 'GigabitEthernet0/0/2',
                'efp_statistics': {
                    'bytes_in': 0,
                    'bytes_out': 0,
                    'pkts_in': 0,
                    'pkts_out': 0,
                    },
                'associated_evc': '50',
                'ce_vlans': '30',
                'state': 'AdminDown',
                },
            2051: {
                'l2protocol_drop': True,
                'associated_interface': 'GigabitEthernet0/0/3',
                'efp_statistics': {
                    'bytes_in': 0,
                    'bytes_out': 0,
                    'pkts_in': 0,
                    'pkts_out': 0,
                    },
                'description': 'xxx',
                'associated_evc': '',
                'dot1q_tunnel_ethertype': '0x8100',
                'encapsulation': 'dot1q 2051 vlan protocol type 0x8100',
                'state': 'Up',
                'rewrite': 'egress tag translate 1-to-1 dot1q 2051 vlan-type 0x8100',
                'ce_vlans': '',
                'type': 'Static',
                },
            2052: {
                'l2protocol_drop': True,
                'associated_interface': 'GigabitEthernet0/0/3',
                'efp_statistics': {
                    'bytes_in': 0,
                    'bytes_out': 0,
                    'pkts_in': 0,
                    'pkts_out': 0,
                    },
                'description': 'xxx',
                'associated_evc': '',
                'dot1q_tunnel_ethertype': '0x8100',
                'encapsulation': 'dot1q 2052 vlan protocol type 0x8100',
                'state': 'Up',
                'rewrite': 'egress tag translate 1-to-1 dot1q 2052 vlan-type 0x8100',
                'ce_vlans': '',
                'type': 'Static',
                },
            2053: {
                'l2protocol_drop': True,
                'associated_interface': 'GigabitEthernet0/0/3',
                'efp_statistics': {
                    'bytes_in': 0,
                    'bytes_out': 0,
                    'pkts_in': 0,
                    'pkts_out': 0,
                    },
                'description': 'xxx',
                'associated_evc': '',
                'dot1q_tunnel_ethertype': '0x8100',
                'encapsulation': 'dot1q 2053 vlan protocol type 0x8100',
                'state': 'Up',
                'rewrite': 'egress tag translate 1-to-1 dot1q 2053 vlan-type 0x8100',
                'ce_vlans': '',
                'type': 'Static',
                },
            2054: {
                'l2protocol_drop': True,
                'associated_interface': 'GigabitEthernet0/0/3',
                'efp_statistics': {
                    'bytes_in': 0,
                    'bytes_out': 0,
                    'pkts_in': 0,
                    'pkts_out': 0,
                    },
                'description': 'xxx',
                'associated_evc': '',
                'dot1q_tunnel_ethertype': '0x8100',
                'encapsulation': 'dot1q 2054 vlan protocol type 0x8100',
                'state': 'Up',
                'rewrite': 'egress tag translate 1-to-1 dot1q 2054 vlan-type 0x8100',
                'ce_vlans': '',
                'type': 'Static',
                },
            2055: {
                'l2protocol_drop': True,
                'associated_interface': 'GigabitEthernet0/0/3',
                'efp_statistics': {
                    'bytes_in': 0,
                    'bytes_out': 0,
                    'pkts_in': 0,
                    'pkts_out': 0,
                    },
                'description': 'xxx',
                'associated_evc': '',
                'dot1q_tunnel_ethertype': '0x8100',
                'encapsulation': 'dot1q 2055 vlan protocol type 0x8100',
                'state': 'Up',
                'rewrite': 'egress tag translate 1-to-1 dot1q 2055 vlan-type 0x8100',
                'ce_vlans': '',
                'type': 'Static',
                },
            },
        }

    golden_output = {'execute.return_value': '''\
        Router#show ethernet service instance detail
        Load for five secs: 4%/0%; one minute: 5%; five minutes: 4%
        Time source is NTP, 16:31:09.701 EST Tue Nov 8 2016

        Service Instance ID: 2051
        Service Instance Type: Static
        Description: xxx
        Associated Interface: GigabitEthernet0/0/3
        Associated EVC: 
        L2protocol drop
        CE-Vlans:                                                                        
        Encapsulation: dot1q 2051 vlan protocol type 0x8100
        Rewrite: egress tag translate 1-to-1 dot1q 2051 vlan-type 0x8100
        Interface Dot1q Tunnel Ethertype: 0x8100
        State: Up
        EFP Statistics:
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance ID: 2052
        Service Instance Type: Static
        Description: xxx
        Associated Interface: GigabitEthernet0/0/3
        Associated EVC: 
        L2protocol drop
        CE-Vlans:                                                                        
        Encapsulation: dot1q 2052 vlan protocol type 0x8100
        Rewrite: egress tag translate 1-to-1 dot1q 2052 vlan-type 0x8100
        Interface Dot1q Tunnel Ethertype: 0x8100
        State: Up
        EFP Statistics:
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance ID: 2053
        Service Instance Type: Static
        Description: xxx
        Associated Interface: GigabitEthernet0/0/3
        Associated EVC: 
        L2protocol drop
        CE-Vlans:                                                                        
        Encapsulation: dot1q 2053 vlan protocol type 0x8100
        Rewrite: egress tag translate 1-to-1 dot1q 2053 vlan-type 0x8100
        Interface Dot1q Tunnel Ethertype: 0x8100
        State: Up
        EFP Statistics:
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance ID: 2054
        Service Instance Type: Static
        Description: xxx
        Associated Interface: GigabitEthernet0/0/3
        Associated EVC: 
        L2protocol drop
        CE-Vlans:                                                                        
        Encapsulation: dot1q 2054 vlan protocol type 0x8100
        Rewrite: egress tag translate 1-to-1 dot1q 2054 vlan-type 0x8100
        Interface Dot1q Tunnel Ethertype: 0x8100
        State: Up
        EFP Statistics:
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance ID: 2055
        Service Instance Type: Static
        Description: xxx
        Associated Interface: GigabitEthernet0/0/3
        Associated EVC: 
        L2protocol drop
        CE-Vlans:                                                                        
        Encapsulation: dot1q 2055 vlan protocol type 0x8100
        Rewrite: egress tag translate 1-to-1 dot1q 2055 vlan-type 0x8100
        Interface Dot1q Tunnel Ethertype: 0x8100
        State: Up
        EFP Statistics:
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance ID: 400
        Associated Interface: GigabitEthernet0/0/2
        Associated EVC: 50
        CE-Vlans: 30
        State: AdminDown
        EFP Statistics:
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0
    '''
    }

    golden_parsed_output_interface = {
        'service_instance': {
            1: {
                'type': 'L2Context',
                'ce_vlans': '',
                'l2protocol_drop': True,
                'efp_statistics': {
                    'pkts_in': 0,
                    'bytes_in': 0,
                    'pkts_out': 0,
                    'bytes_out': 0,
                    },
                'encapsulation': 'dot1q 200-300 vlan protocol type 0x8100',
                'associated_evc': '',
                'dot1q_tunnel_ethertype': '0x8100',
                'state': 'Up',
                'associated_interface': 'Ethernet0/0',
                'control_policy': 'ABC',
                'intiators': 'unclassified vlan',
                },
            2: {
                'type': 'Dynamic',
                'ce_vlans': '10-20',
                'l2protocol_drop': True,
                'efp_statistics': {
                    'pkts_in': 0,
                    'bytes_in': 0,
                    'pkts_out': 0,
                    'bytes_out': 0,
                    },
                'encapsulation': 'dot1q 201 vlan protocol type 0x8100',
                'associated_evc': '',
                'dot1q_tunnel_ethertype': '0x8100',
                'state': 'Up',
                'associated_interface': 'Ethernet0/0',
                },
            3: {
                'type': 'static',
                'ce_vlans': '10-20',
                'l2protocol_drop': True,
                'efp_statistics': {
                    'pkts_in': 0,
                    'bytes_in': 0,
                    'pkts_out': 0,
                    'bytes_out': 0,
                    },
                'encapsulation': 'dot1q 201 vlan protocol type 0x8100',
                'associated_evc': '',
                'dot1q_tunnel_ethertype': '0x8100',
                'state': 'Up',
                'associated_interface': 'Ethernet0/0',
                },
            },
        }

    golden_output_interface = {'execute.return_value': '''\
        Device# show ethernet service instance interface ethernet 0/0 detail

        Service Instance ID: 1
        Service instance type: L2Context
        Intiators: unclassified vlan
        Control policy: ABC
        Associated Interface: Ethernet0/0
        Associated EVC:
        L2protocol drop
        CE-Vlans:
        Encapsulation: dot1q 200-300 vlan protocol type 0x8100
        Interface Dot1q Tunnel Ethertype: 0x8100
        State: Up
        EFP Statistics:
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance ID: 2
        Service instance type: Dynamic

        Associated Interface: Ethernet0/0
        Associated EVC:
        L2protocol drop
        CE-Vlans: 10-20
        Encapsulation: dot1q 201 vlan protocol type 0x8100
        Interface Dot1q Tunnel Ethertype: 0x8100
        State: Up
        EFP Statistics:
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance ID: 3
        Service instance type: static
        Associated Interface: Ethernet0/0
        Associated EVC:
        L2protocol drop
        CE-Vlans: 10-20
        Encapsulation: dot1q 201 vlan protocol type 0x8100
        Interface Dot1q Tunnel Ethertype: 0x8100
        State: Up
        EFP Statistics:
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0
    '''
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        platform_obj = ShowEthernetServiceInstanceDetail(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = platform_obj.parse()    

    def test_golden_full(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        platform_obj = ShowEthernetServiceInstanceDetail(device=self.device)
        parsed_output = platform_obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output)

    def test_golden_interface(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output_interface)
        platform_obj = ShowEthernetServiceInstanceDetail(device=self.device)
        parsed_output = platform_obj.parse(interface='ethernet 0/0')
        self.assertEqual(parsed_output, self.golden_parsed_output_interface)


class test_show_ethernet_service_instance_stats(unittest.TestCase):

    device = Device(name='aDevice')

    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        'max_num_of_service_instances': 32768,
        'service_instance': {
            2051: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2052: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2053: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2054: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2055: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2056: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2057: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2058: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2059: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2060: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2061: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2062: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2063: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2064: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2065: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2066: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2067: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2068: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2069: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2070: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2071: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2072: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2073: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2074: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2075: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2076: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2077: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2078: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2079: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2080: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2081: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2082: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2083: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2084: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2085: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2086: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2087: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2088: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2089: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2090: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            2091: {
                'pkts_out': 0,
                'pkts_in': 0,
                'interface': 'GigabitEthernet0/0/3',
                'bytes_in': 0,
                'bytes_out': 0,
                },
            },
        }

    golden_output = {'execute.return_value': '''\
        Router#show ethernet service instance stats
        Load for five secs: 2%/0%; one minute: 5%; five minutes: 4%
        Time source is NTP, 16:31:09.138 EST Tue Nov 8 2016

        System maximum number of service instances: 32768
        Service Instance 2051, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2052, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2053, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2054, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2055, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2056, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2057, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2058, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2059, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2060, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2061, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2062, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2063, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2064, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2065, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2066, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2067, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2068, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2069, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2070, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2071, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2072, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2073, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2074, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2075, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2076, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2077, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2078, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2079, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2080, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2081, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2082, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2083, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2084, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2085, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2086, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2087, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2088, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2089, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2090, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0

        Service Instance 2091, Interface GigabitEthernet0/0/3
           Pkts In   Bytes In   Pkts Out  Bytes Out
                 0          0          0          0
    '''
    }

    golden_parsed_output_interface = {
        'service_instance': {
            1: {
                'bytes_in': 15408,
                'pkts_out': 97150,
                'interface': 'GigabitEthernet0/0/13',
                'pkts_in': 214,
                'bytes_out': 6994800,
                },
            2: {
                'bytes_in': 6768,
                'pkts_out': 9090,
                'interface': 'GigabitEthernet0/0/13',
                'pkts_in': 654,
                'bytes_out': 34565,
                },
            },
        }

    golden_output_interface = {'execute.return_value': '''\
        Router# show ethernet service instance interface gigabitEthernet 0/0/13 stats
        Service Instance 1, Interface GigabitEthernet0/0/13
        Pkts In   Bytes In   Pkts Out  Bytes Out
               214      15408      97150    6994800
        Service Instance 2, Interface GigabitEthernet0/0/13
        Pkts In   Bytes In   Pkts Out  Bytes Out
               654      6768      9090    34565
    '''
    }

    golden_parsed_output_shrinked = {
        'max_num_of_service_instances': 32768,
    }

    golden_output_shrinked = {'execute.return_value': '''\
        1006#show ethernet service instance stats
        Load for five secs: 1%/0%; one minute: 0%; five minutes: 0%
        Time source is NTP, 15:44:40.696 EST Fri Nov 11 2016

        System maximum number of service instances: 32768
    '''
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        platform_obj = ShowEthernetServiceInstanceStats(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = platform_obj.parse()    

    def test_golden_full(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        platform_obj = ShowEthernetServiceInstanceStats(device=self.device)
        parsed_output = platform_obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output)

    def test_golden_interface(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output_interface)
        platform_obj = ShowEthernetServiceInstanceStats(device=self.device)
        parsed_output = platform_obj.parse(interface='gigabitEthernet 0/0/13')
        self.assertEqual(parsed_output, self.golden_parsed_output_interface)

    def test_golden_shrinked(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output_shrinked)
        platform_obj = ShowEthernetServiceInstanceStats(device=self.device)
        parsed_output = platform_obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output_shrinked)

class test_show_ethernet_service_instance_summary(unittest.TestCase):

    device = Device(name='aDevice')

    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
        'system_summary': {
            'xconnect': {
                'deleted': 0,
                'down': 0,
                'total': 0,
                'bd_adm_do': 0,
                'admin_do': 0,
                'error_di': 0,
                'unknown': 0,
                'up': 0,
                },
            'bdomain': {
                'deleted': 0,
                'down': 0,
                'total': 201,
                'bd_adm_do': 0,
                'admin_do': 0,
                'error_di': 0,
                'unknown': 0,
                'up': 201,
                },
            'local sw': {
                'deleted': 0,
                'down': 0,
                'total': 0,
                'bd_adm_do': 0,
                'admin_do': 0,
                'error_di': 0,
                'unknown': 0,
                'up': 0,
                },
            'other': {
                'deleted': 0,
                'down': 0,
                'total': 201,
                'bd_adm_do': 0,
                'admin_do': 0,
                'error_di': 0,
                'unknown': 0,
                'up': 201,
                },
            'all': {
                'deleted': 0,
                'down': 0,
                'total': 402,
                'bd_adm_do': 0,
                'admin_do': 0,
                'error_di': 0,
                'unknown': 0,
                'up': 402,
                },
            },
        'GigabitEthernet0/0/3': {
            'bdomain': {
                'deleted': 0,
                'down': 0,
                'total': 0,
                'bd_adm_do': 0,
                'admin_do': 0,
                'error_di': 0,
                'unknown': 0,
                'up': 0,
                },
            'local sw': {
                'deleted': 0,
                'down': 0,
                'total': 0,
                'bd_adm_do': 0,
                'admin_do': 0,
                'error_di': 0,
                'unknown': 0,
                'up': 0,
                },
            'all': {
                'deleted': 0,
                'down': 0,
                'total': 201,
                'bd_adm_do': 0,
                'admin_do': 0,
                'error_di': 0,
                'unknown': 0,
                'up': 201,
                },
            'other': {
                'deleted': 0,
                'down': 0,
                'total': 201,
                'bd_adm_do': 0,
                'admin_do': 0,
                'error_di': 0,
                'unknown': 0,
                'up': 201,
                },
            'xconnect': {
                'deleted': 0,
                'down': 0,
                'total': 0,
                'bd_adm_do': 0,
                'admin_do': 0,
                'error_di': 0,
                'unknown': 0,
                'up': 0,
                },
            },
        'Port-channel1': {
            'xconnect': {
                'deleted': 0,
                'down': 0,
                'total': 0,
                'bd_adm_do': 0,
                'admin_do': 0,
                'error_di': 0,
                'unknown': 0,
                'up': 0,
                },
            'bdomain': {
                'deleted': 0,
                'down': 0,
                'total': 201,
                'bd_adm_do': 0,
                'admin_do': 0,
                'error_di': 0,
                'unknown': 0,
                'up': 201,
                },
            'local sw': {
                'deleted': 0,
                'down': 0,
                'total': 0,
                'bd_adm_do': 0,
                'admin_do': 0,
                'error_di': 0,
                'unknown': 0,
                'up': 0,
                },
            'other': {
                'deleted': 0,
                'down': 0,
                'total': 0,
                'bd_adm_do': 0,
                'admin_do': 0,
                'error_di': 0,
                'unknown': 0,
                'up': 0,
                },
            'all': {
                'deleted': 0,
                'down': 0,
                'total': 201,
                'bd_adm_do': 0,
                'admin_do': 0,
                'error_di': 0,
                'unknown': 0,
                'up': 201,
                },
            },
        }

    golden_output = {'execute.return_value': '''\
        Router#show ethernet service instance summary
        Load for five secs: 2%/0%; one minute: 5%; five minutes: 4%
        Time source is NTP, 16:31:09.005 EST Tue Nov 8 2016

        System summary
                    Total       Up  AdminDo     Down  ErrorDi  Unknown  Deleted  BdAdmDo  
        bdomain       201      201        0        0        0        0        0        0  
        xconnect        0        0        0        0        0        0        0        0  
        local sw        0        0        0        0        0        0        0        0  
        other         201      201        0        0        0        0        0        0  
        all           402      402        0        0        0        0        0        0  
        Associated interface: GigabitEthernet0/0/3
                    Total       Up  AdminDo     Down  ErrorDi  Unknown  Deleted  BdAdmDo  
        bdomain         0        0        0        0        0        0        0        0  
        xconnect        0        0        0        0        0        0        0        0  
        local sw        0        0        0        0        0        0        0        0  
        other         201      201        0        0        0        0        0        0  
        all           201      201        0        0        0        0        0        0  
        Associated interface: Port-channel1
                    Total       Up  AdminDo     Down  ErrorDi  Unknown  Deleted  BdAdmDo  
        bdomain       201      201        0        0        0        0        0        0  
        xconnect        0        0        0        0        0        0        0        0  
        local sw        0        0        0        0        0        0        0        0  
        other           0        0        0        0        0        0        0        0  
        all           201      201        0        0        0        0        0        0  
    '''
    }


    def test_empty(self):
        self.device = Mock(**self.empty_output)
        platform_obj = ShowEthernetServiceInstanceSummary(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = platform_obj.parse()    

    def test_golden_full(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        platform_obj = ShowEthernetServiceInstanceSummary(device=self.device)
        parsed_output = platform_obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output)


class test_show_l2vpn_vfi(unittest.TestCase):

    device = Device(name='aDevice')

    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
    'vfi': {
        'VPLS-2052': {
            'vpn_id': 2052,
            'rd': '65109:2052',
            'type': 'multipoint',
            'bd_vfi_name': 'VPLS-2052',
            've_range': 10,
            'signaling': 'BGP',
            'bridge_domain': {
                '2052': {
                    'pseudo_port_interface': 'pseudowire100002',
                    'attachment_circuits': {
                        },
                    'vfi': {
                        '10.120.202.64': {
                            'pw_id': {
                                'pseudowire100203': {
                                    'local_label': 26,
                                    'remote_label': 327818,
                                    've_id': 1,
                                    'split_horizon': True,
                                    },
                                },
                            },
                        },
                    },
                },
            've_id': 2,
            'rt': ['65109:2052', '65109:2052'],
            'state': 'up',
            },
        'VPLS-2055': {
            'vpn_id': 2055,
            'rd': '65109:2055',
            'type': 'multipoint',
            'bd_vfi_name': 'VPLS-2055',
            've_range': 10,
            'signaling': 'BGP',
            'bridge_domain': {
                '2055': {
                    'pseudo_port_interface': 'pseudowire100005',
                    'attachment_circuits': {
                        },
                    'vfi': {
                        '10.120.202.64': {
                            'pw_id': {
                                'pseudowire100206': {
                                    'local_label': 56,
                                    'remote_label': 327842,
                                    've_id': 1,
                                    'split_horizon': True,
                                    },
                                },
                            },
                        },
                    },
                },
            've_id': 2,
            'rt': ['65109:2055', '65109:2055'],
            'state': 'up',
            },
        'VPLS-2051': {
            'vpn_id': 2051,
            'rd': '65109:2051',
            'type': 'multipoint',
            'bd_vfi_name': 'VPLS-2051',
            've_range': 10,
            'signaling': 'BGP',
            'bridge_domain': {
                '2051': {
                    'pseudo_port_interface': 'pseudowire100001',
                    'attachment_circuits': {
                        },
                    'vfi': {
                        '10.120.202.64': {
                            'pw_id': {
                                'pseudowire100202': {
                                    'local_label': 16,
                                    'remote_label': 327810,
                                    've_id': 1,
                                    'split_horizon': True,
                                    },
                                },
                            },
                        },
                    },
                },
            've_id': 2,
            'rt': ['65109:2051', '65109:2051'],
            'state': 'up',
            },
        'VPLS-2053': {
            'vpn_id': 2053,
            'rd': '65109:2053',
            'type': 'multipoint',
            'bd_vfi_name': 'VPLS-2053',
            've_range': 10,
            'signaling': 'BGP',
            'bridge_domain': {
                '2053': {
                    'pseudo_port_interface': 'pseudowire100003',
                    'attachment_circuits': {
                        },
                    'vfi': {
                        '10.120.202.64': {
                            'pw_id': {
                                'pseudowire100204': {
                                    'local_label': 36,
                                    'remote_label': 327826,
                                    've_id': 1,
                                    'split_horizon': True,
                                    },
                                },
                            },
                        },
                    },
                },
            've_id': 2,
            'rt': ['65109:2053', '65109:2053'],
            'state': 'up',
            },
        'VPLS-2054': {
            'vpn_id': 2054,
            'rd': '65109:2054',
            'type': 'multipoint',
            'bd_vfi_name': 'VPLS-2054',
            've_range': 10,
            'signaling': 'BGP',
            'bridge_domain': {
                '2054': {
                    'pseudo_port_interface': 'pseudowire100004',
                    'attachment_circuits': {
                        },
                    'vfi': {
                        '10.120.202.64': {
                            'pw_id': {
                                'pseudowire100205': {
                                    'local_label': 46,
                                    'remote_label': 327834,
                                    've_id': 1,
                                    'split_horizon': True,
                                    },
                                },
                            },
                        },
                    },
                },
            've_id': 2,
            'rt': ['65109:2054', '65109:2054'],
            'state': 'up',
            },
        },
    }

    golden_output = {'execute.return_value': '''\
        Router#sh l2vpn vfi
        Load for five secs: 20%/0%; one minute: 5%; five minutes: 5%
        Time source is NTP, 11:33:13.680 EST Wed Nov 9 2016

        Legend: RT=Route-target, S=Split-horizon, Y=Yes, N=No

        VFI name: VPLS-2051, state: up, type: multipoint, signaling: BGP
          VPN ID: 2051, VE-ID: 2, VE-SIZE: 10
          RD: 65109:2051, RT: 65109:2051, 65109:2051,
          Bridge-Domain 2051 attachment circuits:
          Pseudo-port interface: pseudowire100001
          Interface          Peer Address    VE-ID  Local Label  Remote Label    S
          pseudowire100202   10.120.202.64   1      16           327810          Y

        VFI name: VPLS-2052, state: up, type: multipoint, signaling: BGP
          VPN ID: 2052, VE-ID: 2, VE-SIZE: 10
          RD: 65109:2052, RT: 65109:2052, 65109:2052,
          Bridge-Domain 2052 attachment circuits:
          Pseudo-port interface: pseudowire100002
          Interface          Peer Address    VE-ID  Local Label  Remote Label    S
          pseudowire100203   10.120.202.64   1      26           327818          Y

        VFI name: VPLS-2053, state: up, type: multipoint, signaling: BGP
          VPN ID: 2053, VE-ID: 2, VE-SIZE: 10
          RD: 65109:2053, RT: 65109:2053, 65109:2053,
          Bridge-Domain 2053 attachment circuits:
          Pseudo-port interface: pseudowire100003
          Interface          Peer Address    VE-ID  Local Label  Remote Label    S
          pseudowire100204   10.120.202.64   1      36           327826          Y

        VFI name: VPLS-2054, state: up, type: multipoint, signaling: BGP
          VPN ID: 2054, VE-ID: 2, VE-SIZE: 10
          RD: 65109:2054, RT: 65109:2054, 65109:2054,
          Bridge-Domain 2054 attachment circuits:
          Pseudo-port interface: pseudowire100004
          Interface          Peer Address    VE-ID  Local Label  Remote Label    S
          pseudowire100205   10.120.202.64   1      46           327834          Y

        VFI name: VPLS-2055, state: up, type: multipoint, signaling: BGP
          VPN ID: 2055, VE-ID: 2, VE-SIZE: 10
          RD: 65109:2055, RT: 65109:2055, 65109:2055,
          Bridge-Domain 2055 attachment circuits:
          Pseudo-port interface: pseudowire100005
          Interface          Peer Address    VE-ID  Local Label  Remote Label    S
          pseudowire100206   10.120.202.64   1      56           327842          Y
    '''
    }

    golden_parsed_output_2 = {
    'vfi': {
        'vfi-sample': {
            'bd_vfi_name': 'vfi-sample',
            'signaling': 'LDP',
            'bridge_domain': {
                '30': {
                    'vfi': {
                        '10.16.2.2': {
                            'pw_id': {
                                'pseudowire1': {
                                    'split_horizon': True,
                                    'vc_id': 12,
                                    },
                                },
                            },
                        '10.64.4.4': {
                            'pw_id': {
                                'pseudowire3': {
                                    'split_horizon': True,
                                    'vc_id': 14,
                                    },
                                },
                            },
                        '10.36.3.3': {
                            'pw_id': {
                                'pseudowire2': {
                                    'split_horizon': True,
                                    'vc_id': 13,
                                    },
                                },
                            },
                        },
                    'pseudo_port_interface': 'pseudowire100004',
                    'attachment_circuits': {
                        },
                    },
                },
            'vpn_id': 2000,
            'state': 'up',
            'type': 'multipoint',
            },
        },
    }

    golden_output_2 = {'execute.return_value': '''\
    R1_csr1kv#show l2vpn vfi
    Legend: RT=Route-target, S=Split-horizon, Y=Yes, N=No

    VFI name: vfi-sample, state: up, type: multipoint, signaling: LDP
      VPN ID: 2000
      Bridge-Domain 30 attachment circuits:
      Pseudo-port interface: pseudowire100004
      Interface          Peer Address     VC ID        S
      pseudowire3        10.64.4.4        14           Y
      pseudowire2        10.36.3.3        13           Y
      pseudowire1        10.16.2.2        12           Y
    '''
    }

    golden_parsed_output_3 = {
    'vfi': {
        'vfi-sample': {
            've_range': 15,
            've_id': 1,
            'type': 'multipoint',
            'bd_vfi_name': 'vfi-sample',
            'state': 'up',
            'bridge_domain': {
                '30': {
                    'vfi': {
                        '10.36.3.3': {
                            'pw_id': {
                                'pseudowire100006': {
                                    'local_label': 29,
                                    'remote_label': 20,
                                    've_id': 3,
                                    'split_horizon': True,
                                    },
                                },
                            },
                        '10.64.4.4': {
                            'pw_id': {
                                'pseudowire100007': {
                                    'local_label': 30,
                                    'remote_label': 24015,
                                    've_id': 4,
                                    'split_horizon': True,
                                    },
                                },
                            },
                        '10.16.2.2': {
                            'pw_id': {
                                'pseudowire100005': {
                                    'local_label': 28,
                                    'remote_label': 24,
                                    've_id': 2,
                                    'split_horizon': True,
                                    },
                                },
                            },
                        },
                    'attachment_circuits': {
                        },
                    },
                },
            'rt': ['100:2000', '100:100'],
            'vpn_id': 2000,
            'signaling': 'BGP',
            'rd': '100:2000',
            },
        },
    }

    golden_output_3 = {'execute.return_value': '''\
    R1_csr1kv#show l2vpn vfi
    Legend: RT=Route-target, S=Split-horizon, Y=Yes, N=No

    VFI name: vfi-sample, state: up, type: multipoint, signaling: BGP
      VPN ID: 2000, VE-ID: 1, VE-SIZE: 15 
      RD: 100:2000, RT: 100:2000, 100:100, 
      Bridge-Domain 30 attachment circuits:
      Neighbors connected via pseudowires:
      Interface          Peer Address    VE-ID  Local Label  Remote Label    S
      pseudowire100007   10.64.4.4       4      30           24015           Y
      pseudowire100006   10.36.3.3       3      29           20              Y
      pseudowire100005   10.16.2.2       2      28           24              Y
    '''
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        platform_obj = ShowL2vpnVfi(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = platform_obj.parse()    

    def test_golden_full(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        platform_obj = ShowL2vpnVfi(device=self.device)
        parsed_output = platform_obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output)

    def test_golden_full_2(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output_2)
        platform_obj = ShowL2vpnVfi(device=self.device)
        parsed_output = platform_obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output_2)

    def test_golden_full_3(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output_3)
        platform_obj = ShowL2vpnVfi(device=self.device)
        parsed_output = platform_obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output_3)


class test_show_l2vpn_service_all(unittest.TestCase):

    device = Device(name='aDevice')

    empty_output = {'execute.return_value': ''}

    golden_parsed_output = {
    'vpls_name': {
        'VPLS-2053': {
            'state': 'UP',
            'interface': {
                'pw100003': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': 'VPLS-2053(VFI)',
                    'state_in_l2vpn_service': 'UP',
                    },
                'pw100216': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': '1:2053(MPLS)',
                    'group': 'core_pw',
                    'state_in_l2vpn_service': 'UP',
                    },
                },
            },
        'VPLS-2052': {
            'state': 'UP',
            'interface': {
                'pw100002': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': 'VPLS-2052(VFI)',
                    'state_in_l2vpn_service': 'UP',
                    },
                'pw100215': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': '1:2052(MPLS)',
                    'group': 'core_pw',
                    'state_in_l2vpn_service': 'UP',
                    },
                },
            },
        'VPLS-2071': {
            'state': 'UP',
            'interface': {
                'pw100209': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': '1:2071(MPLS)',
                    'group': 'core_pw',
                    'state_in_l2vpn_service': 'UP',
                    },
                'pw100021': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': 'VPLS-2071(VFI)',
                    'state_in_l2vpn_service': 'UP',
                    },
                },
            },
        'VPLS-2058': {
            'state': 'UP',
            'interface': {
                'pw100008': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': 'VPLS-2058(VFI)',
                    'state_in_l2vpn_service': 'UP',
                    },
                'pw100221': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': '1:2058(MPLS)',
                    'group': 'core_pw',
                    'state_in_l2vpn_service': 'UP',
                    },
                },
            },
        'VPLS-2067': {
            'state': 'UP',
            'interface': {
                'pw100205': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': '1:2067(MPLS)',
                    'group': 'core_pw',
                    'state_in_l2vpn_service': 'UP',
                    },
                'pw100017': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': 'VPLS-2067(VFI)',
                    'state_in_l2vpn_service': 'UP',
                    },
                },
            },
        'VPLS-2061': {
            'state': 'UP',
            'interface': {
                'pw100224': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': '1:2061(MPLS)',
                    'group': 'core_pw',
                    'state_in_l2vpn_service': 'UP',
                    },
                'pw100011': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': 'VPLS-2061(VFI)',
                    'state_in_l2vpn_service': 'UP',
                    },
                },
            },
        'VPLS-2069': {
            'state': 'UP',
            'interface': {
                'pw100019': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': 'VPLS-2069(VFI)',
                    'state_in_l2vpn_service': 'UP',
                    },
                'pw100207': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': '1:2069(MPLS)',
                    'group': 'core_pw',
                    'state_in_l2vpn_service': 'UP',
                    },
                },
            },
        'VPLS-2064': {
            'state': 'UP',
            'interface': {
                'pw100202': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': '1:2064(MPLS)',
                    'group': 'core_pw',
                    'state_in_l2vpn_service': 'UP',
                    },
                'pw100014': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': 'VPLS-2064(VFI)',
                    'state_in_l2vpn_service': 'UP',
                    },
                },
            },
        'VPLS-2070': {
            'state': 'UP',
            'interface': {
                'pw100020': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': 'VPLS-2070(VFI)',
                    'state_in_l2vpn_service': 'UP',
                    },
                'pw100208': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': '1:2070(MPLS)',
                    'group': 'core_pw',
                    'state_in_l2vpn_service': 'UP',
                    },
                },
            },
        'VPLS-2057': {
            'state': 'UP',
            'interface': {
                'pw100220': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': '1:2057(MPLS)',
                    'group': 'core_pw',
                    'state_in_l2vpn_service': 'UP',
                    },
                'pw100007': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': 'VPLS-2057(VFI)',
                    'state_in_l2vpn_service': 'UP',
                    },
                },
            },
        'VPLS-2055': {
            'state': 'UP',
            'interface': {
                'pw100005': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': 'VPLS-2055(VFI)',
                    'state_in_l2vpn_service': 'UP',
                    },
                'pw100218': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': '1:2055(MPLS)',
                    'group': 'core_pw',
                    'state_in_l2vpn_service': 'UP',
                    },
                },
            },
        'VPLS-2056': {
            'state': 'UP',
            'interface': {
                'pw100006': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': 'VPLS-2056(VFI)',
                    'state_in_l2vpn_service': 'UP',
                    },
                'pw100219': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': '1:2056(MPLS)',
                    'group': 'core_pw',
                    'state_in_l2vpn_service': 'UP',
                    },
                },
            },
        'VPLS-2051': {
            'state': 'UP',
            'interface': {
                'pw100001': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': 'VPLS-2051(VFI)',
                    'state_in_l2vpn_service': 'UP',
                    },
                'pw100214': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': '1:2051(MPLS)',
                    'group': 'core_pw',
                    'state_in_l2vpn_service': 'UP',
                    },
                },
            },
        'VPLS-2059': {
            'state': 'UP',
            'interface': {
                'pw100009': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': 'VPLS-2059(VFI)',
                    'state_in_l2vpn_service': 'UP',
                    },
                'pw100222': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': '1:2059(MPLS)',
                    'group': 'core_pw',
                    'state_in_l2vpn_service': 'UP',
                    },
                },
            },
        'VPLS-2063': {
            'state': 'UP',
            'interface': {
                'pw100226': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': '1:2063(MPLS)',
                    'group': 'core_pw',
                    'state_in_l2vpn_service': 'UP',
                    },
                'pw100013': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': 'VPLS-2063(VFI)',
                    'state_in_l2vpn_service': 'UP',
                    },
                },
            },
        'VPLS-2060': {
            'state': 'UP',
            'interface': {
                'pw100010': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': 'VPLS-2060(VFI)',
                    'state_in_l2vpn_service': 'UP',
                    },
                'pw100223': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': '1:2060(MPLS)',
                    'group': 'core_pw',
                    'state_in_l2vpn_service': 'UP',
                    },
                },
            },
        'VPLS-2068': {
            'state': 'UP',
            'interface': {
                'pw100018': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': 'VPLS-2068(VFI)',
                    'state_in_l2vpn_service': 'UP',
                    },
                'pw100206': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': '1:2068(MPLS)',
                    'group': 'core_pw',
                    'state_in_l2vpn_service': 'UP',
                    },
                },
            },
        'VPLS-2066': {
            'state': 'UP',
            'interface': {
                'pw100016': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': 'VPLS-2066(VFI)',
                    'state_in_l2vpn_service': 'UP',
                    },
                'pw100204': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': '1:2066(MPLS)',
                    'group': 'core_pw',
                    'state_in_l2vpn_service': 'UP',
                    },
                },
            },
        'VPLS-2062': {
            'state': 'UP',
            'interface': {
                'pw100012': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': 'VPLS-2062(VFI)',
                    'state_in_l2vpn_service': 'UP',
                    },
                'pw100225': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': '1:2062(MPLS)',
                    'group': 'core_pw',
                    'state_in_l2vpn_service': 'UP',
                    },
                },
            },
        'VPLS-2065': {
            'state': 'UP',
            'interface': {
                'pw100015': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': 'VPLS-2065(VFI)',
                    'state_in_l2vpn_service': 'UP',
                    },
                'pw100203': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': '1:2065(MPLS)',
                    'group': 'core_pw',
                    'state_in_l2vpn_service': 'UP',
                    },
                },
            },
        'VPLS-2054': {
            'state': 'UP',
            'interface': {
                'pw100217': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': '1:2054(MPLS)',
                    'group': 'core_pw',
                    'state_in_l2vpn_service': 'UP',
                    },
                'pw100004': {
                    'priority': 0,
                    'state': 'UP',
                    'encapsulation': 'VPLS-2054(VFI)',
                    'state_in_l2vpn_service': 'UP',
                    },
                },
            },
        },
    }

    golden_output = {'execute.return_value': '''\
        Router#show l2vpn service all
        Load for five secs: 2%/0%; one minute: 7%; five minutes: 9%
        Time source is NTP, 20:31:05.928 EST Fri Nov 11 2016

        Legend: St=State    XC St=State in the L2VPN Service      Prio=Priority
                UP=Up       DN=Down            AD=Admin Down      IA=Inactive
                SB=Standby  HS=Hot Standby     RV=Recovering      NH=No Hardware
                m=manually selected

          Interface          Group       Encapsulation                   Prio  St  XC St
          ---------          -----       -------------                   ----  --  -----
        VPLS name: VPLS-2051, State: UP
          pw100001                       VPLS-2051(VFI)                  0     UP  UP   
          pw100214           core_pw     1:2051(MPLS)                    0     UP  UP   
        VPLS name: VPLS-2052, State: UP
          pw100002                       VPLS-2052(VFI)                  0     UP  UP   
          pw100215           core_pw     1:2052(MPLS)                    0     UP  UP   
        VPLS name: VPLS-2053, State: UP
          pw100003                       VPLS-2053(VFI)                  0     UP  UP   
          pw100216           core_pw     1:2053(MPLS)                    0     UP  UP   
        VPLS name: VPLS-2054, State: UP
          pw100004                       VPLS-2054(VFI)                  0     UP  UP   
          pw100217           core_pw     1:2054(MPLS)                    0     UP  UP   
        VPLS name: VPLS-2055, State: UP
          pw100005                       VPLS-2055(VFI)                  0     UP  UP   
          pw100218           core_pw     1:2055(MPLS)                    0     UP  UP   
        VPLS name: VPLS-2056, State: UP
          pw100006                       VPLS-2056(VFI)                  0     UP  UP   
          pw100219           core_pw     1:2056(MPLS)                    0     UP  UP   
        VPLS name: VPLS-2057, State: UP
          pw100007                       VPLS-2057(VFI)                  0     UP  UP   
          pw100220           core_pw     1:2057(MPLS)                    0     UP  UP   
        VPLS name: VPLS-2058, State: UP
          pw100008                       VPLS-2058(VFI)                  0     UP  UP   
          pw100221           core_pw     1:2058(MPLS)                    0     UP  UP   
        VPLS name: VPLS-2059, State: UP
          pw100009                       VPLS-2059(VFI)                  0     UP  UP   
          pw100222           core_pw     1:2059(MPLS)                    0     UP  UP   
        VPLS name: VPLS-2060, State: UP
          pw100010                       VPLS-2060(VFI)                  0     UP  UP   
          pw100223           core_pw     1:2060(MPLS)                    0     UP  UP   
        VPLS name: VPLS-2061, State: UP
          pw100011                       VPLS-2061(VFI)                  0     UP  UP   
          pw100224           core_pw     1:2061(MPLS)                    0     UP  UP   
        VPLS name: VPLS-2062, State: UP
          pw100012                       VPLS-2062(VFI)                  0     UP  UP   
          pw100225           core_pw     1:2062(MPLS)                    0     UP  UP   
        VPLS name: VPLS-2063, State: UP
          pw100013                       VPLS-2063(VFI)                  0     UP  UP   
          pw100226           core_pw     1:2063(MPLS)                    0     UP  UP   
        VPLS name: VPLS-2064, State: UP
          pw100014                       VPLS-2064(VFI)                  0     UP  UP   
          pw100202           core_pw     1:2064(MPLS)                    0     UP  UP   
        VPLS name: VPLS-2065, State: UP
          pw100015                       VPLS-2065(VFI)                  0     UP  UP   
          pw100203           core_pw     1:2065(MPLS)                    0     UP  UP   
        VPLS name: VPLS-2066, State: UP
          pw100016                       VPLS-2066(VFI)                  0     UP  UP   
          pw100204           core_pw     1:2066(MPLS)                    0     UP  UP   
        VPLS name: VPLS-2067, State: UP
          pw100017                       VPLS-2067(VFI)                  0     UP  UP   
          pw100205           core_pw     1:2067(MPLS)                    0     UP  UP   
        VPLS name: VPLS-2068, State: UP
          pw100018                       VPLS-2068(VFI)                  0     UP  UP   
          pw100206           core_pw     1:2068(MPLS)                    0     UP  UP   
        VPLS name: VPLS-2069, State: UP
          pw100019                       VPLS-2069(VFI)                  0     UP  UP   
          pw100207           core_pw     1:2069(MPLS)                    0     UP  UP   
        VPLS name: VPLS-2070, State: UP
          pw100020                       VPLS-2070(VFI)                  0     UP  UP   
          pw100208           core_pw     1:2070(MPLS)                    0     UP  UP   
        VPLS name: VPLS-2071, State: UP
          pw100021                       VPLS-2071(VFI)                  0     UP  UP   
          pw100209           core_pw     1:2071(MPLS)                    0     UP  UP   
    '''
    }


    def test_empty(self):
        self.device = Mock(**self.empty_output)
        platform_obj = ShowL2vpnServiceAll(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = platform_obj.parse()    

    def test_golden_full(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        platform_obj = ShowL2vpnServiceAll(device=self.device)
        parsed_output = platform_obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output)


if __name__ == '__main__':
    unittest.main()