def json_to_dict(json_path):
    '''
        Reads JSON file and returns a dict
    '''
    from json import loads

    with open(json_path) as raw:
        jdict = loads(raw.read())
    return jdict
