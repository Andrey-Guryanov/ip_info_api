def _ripe_unpack_org_name(resp_org):
    try:
        org_attributes = resp_org['objects']['object'][0]['attributes']
        for attribute in org_attributes['attribute']:
            if attribute['name'] == 'org-name':
                result_org_name = attribute['value']
                break
    except KeyError:
        result_org_name = False
    return result_org_name

def ripe_unpack_ip_range(resp_ip):
    try:
        result_ip = resp_ip['objects']['object'][0]['primary-key']['attribute'][0]['value']
    except KeyError:
        result_ip = False
    return result_ip

def ripe_ip_resp_convert(extra_objs, result_ip, resp_org=None):
    result = result_ip
    result['netname'] = extra_objs['netname']
    result['country_code'] = extra_objs['country']
    if resp_org:
        result['org_name'] = _ripe_unpack_org_name(resp_org)
    else:
        result['org_name'] = None
    if 'descr' in extra_objs.keys():
        result['descr'] = extra_objs['descr']
    else:
        result['descr'] = None
    return result



def ripe_unpack_extra_objs(resp_ip):
    result_obj = {}
    try:
        extra_objs = resp_ip['objects']['object'][0]['attributes']['attribute']
    except KeyError:
        result_obj = False
    else:
        for obj in extra_objs:
            if obj['name'] in result_obj.keys():
                if isinstance(obj['value'], str):
                    result_obj[obj['name']] += ' ' + obj['value']
            else:
                if isinstance(obj['value'], str):
                    result_obj[obj['name']] = obj['value']
    return result_obj
