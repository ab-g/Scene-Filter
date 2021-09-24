import sys
import os
import json


def get_first_scene_id(resource_pack_data):
    return resource_pack_data['scenes']['map'][0]['value']['id']['uuid']


def should_keep_node(node):
    if node['object3D']['name'] in ['UserRootObject', 'MainCamera', 'MainCharacter']:
        return True
    return False


def filter_node_children(scene_data, node):
    if 'children' not in node:
        return node

    node['children'] = [
        node_id for node_id in node['children']
        if should_keep_node(next(node for node in scene_data['nodes'] if node['object3D']['id']['uuid'] == node_id))
    ]
    return node


def main(game_project_dir_path):
    resource_pack_file_path = os.path.join(game_project_dir_path, 'resource-pack.json')
    with open(resource_pack_file_path, 'r') as resource_pack_file:
        resource_pack_data = json.load(resource_pack_file)

    scene_id = get_first_scene_id(resource_pack_data)
    scene_file_path = os.path.join(game_project_dir_path, 'scenes/{0}.json'.format(scene_id))

    with open(scene_file_path, 'r') as scene_file:
        scene_data = json.load(scene_file)

    scene_data['nodes'] = [
        filter_node_children(scene_data, node) for node in scene_data['nodes'] if should_keep_node(node)
    ]
    print(json.dumps(scene_data, indent=4))

    with open(scene_file_path, 'w') as scene_file:
        json.dump(scene_data, scene_file, indent=4, sort_keys=False)


if __name__ == '__main__':
    main(sys.argv[1])
