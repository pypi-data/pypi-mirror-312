# pyevabgp

`pyevabgp` is a Python package for monitoring and alerting BGP states and metrics of juniper  using snmp, NETCONF, and gNMI.

## Features
- Monitor BGP peer state.
- Retrieve bgp metrics using Juniper-specific MIBs,openconfig yang models,ietf and juniper native yang models
- Generate alerts for BGP state changes.(in built bettertack alerting method)
- Support bgp next hop encoding capablity.
- tested on junos 23.4R2-S2.1 

## Installation
Install `pyevabgp` via pip:
```bash
pip install pyevabgp

