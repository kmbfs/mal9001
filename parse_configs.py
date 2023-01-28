import yaml

def read_config_value(key):
    stream = open("configs.yml", 'r')
    d = yaml.load(stream, Loader=yaml.FullLoader)
    for subgroup, map in d.items():
        if key in map:
            return map[key]
    return None
