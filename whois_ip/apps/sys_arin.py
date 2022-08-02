def _arin_unpack(arin_dict, key_one, key_two):
    value = list(arin_dict[key_one][key_two].values())[0]
    return value


def _arin_conver_comment(comments_obj):
    result_comment = ''
    if isinstance(comments_obj['line'], list):
        for comment_obj in comments_obj['line']:
            result_comment += ' ' + comment_obj['$']
    else:
        result_comment += comments_obj['line']['$']
    return result_comment


def _arin_unpack_net(arin_netblocks):
    network = {}
    cidr_length = _arin_unpack(arin_netblocks, 'netBlock', 'cidrLength')
    network['ip_first'] = _arin_unpack(arin_netblocks, 'netBlock', 'startAddress')
    network['ip_last'] = _arin_unpack(arin_netblocks, 'netBlock', 'endAddress')
    network['network'] = f"{network['ip_first']}/{cidr_length}"
    return network


def arin_ip_resp_convert(resp_ip, resp_org, resp_customer):
    result = {}
    resp_ip = resp_ip['net']
    arin_netblocks = resp_ip['netBlocks']
    arin_networks = []
    if isinstance(arin_netblocks['netBlock'], dict):
        arin_networks.append(_arin_unpack_net(arin_netblocks))
    else:
        for net_block in arin_netblocks['netBlock']:
            arin_networks.append(_arin_unpack_net({'netBlock':net_block}))
    result['arin_networks'] = arin_networks
    result['netname'] = resp_ip['name']['$']
    if resp_org:
        resp_owner = resp_org['org']
    elif resp_customer:
        resp_owner = resp_customer['customer']
    if resp_owner:
        result['country_code'] = _arin_unpack(resp_owner, 'iso3166-1', 'code2')
        result['org_name'] = resp_owner['name']['$']
    else:
        result['country_code'] = None
        result['org_name'] = None
    if 'comment' in resp_ip.keys():
        result['descr'] = _arin_conver_comment(resp_ip['comment'])
    else:
        result['descr'] = None
    return result
