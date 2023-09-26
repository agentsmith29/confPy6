import ruamel.yaml


def parse_yaml_with_comments(yaml_text):
    def add_comments(node, comments):
        for key, comment in comments.items():
            node.yaml_add_eol_comment(comment, key)

    def parse_node(node):
        if isinstance(node, ruamel.yaml.ScalarNode):
            return {
                'value': node.value,
                'comment': node.comment if hasattr(node, 'comment') else None
            }
        elif isinstance(node, ruamel.yaml.MappingNode):
            result = {}
            for key_node, value_node in node.value:
                key = key_node.value
                comments = {}
                if hasattr(key_node, 'comment'):
                    comments[key] = key_node.comment
                result[key] = parse_node(value_node)
                if hasattr(value_node, 'comment'):
                    comments[key] = value_node.comment
                add_comments(result[key], comments)
            return result
        elif isinstance(node, ruamel.yaml.SequenceNode):
            return [parse_node(item) for item in node.value]

    yaml = ruamel.yaml.YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096  # Ensure comments are preserved

    data = yaml.load(yaml_text)
    return parse_node(data)


yaml_text = """
application_config: # ApplicationConfig
    wafer_version: "ASDF" #     Wafer Version: The version of the wafer
    wafer_nr: "No Wafer Number" # wafer_nr: The version of the wafer
    
    # Configurations
    laser_config: # LaserConfig
      wavelength_range: 850 # wavelength_range: None
      port: "USB 0" # port: None
      # Configurations
      laser_config: # Testconfig
        test1: 850 # wavelength_range: None
        test2: 2 # velocity: None
"""

result = ruamel.yaml.round_trip_load(yaml_text)
#print(result.ca)
def parse_node(node,l = ""):
    print(f"{l}|-> Node {type(node)}")
    val = {}
    com = node.ca.comment
    print(com)
    for n in node:
        print(f"{l}|--> Examine node: {n} of type {type(node[n])}")
        if isinstance(node[n], ruamel.yaml.CommentedMap):
            print(f"{l}|--> {type(node[n])}: {n}")
            val[n] = parse_node(node[n], l="  ")
        else:
            print(f"{l}|--> ScalarNode: {node[n]} ({type(node[n])}, {n}")
            val[n] = get_comment(node, n, l)

    return {'value': val, 'comment': com}

def get_comment(comment_map, key, l=""):
    d = {c:comment_map.ca.items[c] for c in comment_map.ca.items}
    print(f"{l}||--> Comment map: {d}")
    if key in d:
        return {'value': comment_map[key], 'comment': convert_comment_map(d[key])}
    else:
        return {'value': comment_map[key], 'comment': None}

def convert_comment_map(comment_map):
    stripped_comment_map = [c for c in comment_map if isinstance(c, ruamel.yaml.CommentToken)][0]
    pcm: ruamel.yaml.CommentToken = stripped_comment_map
    return comment_map

parse_node(result)
comment = node.comment
print(f"{node}: {value}")

# get the comment
result.ca.comment[1][0].value
