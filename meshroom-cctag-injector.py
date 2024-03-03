import csv
import json
import os
import re

if __name__ == "__main__":
    
    mg_file_path = input("Enter the full path to the MeshRoom file [.mg]:")
    mg_file_path = mg_file_path.strip('&')
    mg_file_path = mg_file_path.strip()
    mg_file_path = mg_file_path.strip('\"')
    mg_file_path = mg_file_path.strip('\'')
    if not mg_file_path.endswith('.mg'):
        print("ERROR: Wrong file type!")
        exit(1)

    csv_file_path = input("Enter the full path to the coordinate file [.csv]:")
    csv_file_path = csv_file_path.strip('&')
    csv_file_path = csv_file_path.strip()
    csv_file_path = csv_file_path.strip('\"')
    csv_file_path = csv_file_path.strip('\'')
    if not csv_file_path.endswith('.csv'):
        print("ERROR: Wrong file type!")
        exit(1)
    
    with open(mg_file_path) as mf_file:
        mg_file_contents = mf_file.read()

    mg_file_json = json.loads(mg_file_contents)
    
    graph_keys = mg_file_json['graph'].keys()

    node_to_inject_points = ''

    for key in graph_keys:
        if re.match(r'SfMTransform_[0-9]+', key):
            print(f"Found {key}!")
            node_to_inject_points = key
            break # Only care about first node!
    
    coords = []
    
    with open(csv_file_path) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            coords.append(row)

    # Sort coords            
    coords = sorted(coords, key=lambda d: int(d['markerId']))

    for coord in coords:
        temp_coord = {  'x': float(coord['x']),
                        'y': float(coord['y']),
                        'z': float(coord['z']),}
        
        temp_marker = {'markerId': int(coord['markerId']),
                       'markerCoord': temp_coord,}
        
        mg_file_json['graph'][f'{node_to_inject_points}']['inputs']['markers'].append(temp_marker)

    json_output = json.dumps(mg_file_json, indent=4)

    # Keep for future, for now just overwrite
    
    #csv_file_name = csv_file_path.split(sep="\\")[-1].split(".")[0]
    #output_file_path = mg_file_path[:-3] + f" - {csv_file_name}" + mg_file_path[-3:]
    
    # Just overwrite the input file
    output_file_path = mg_file_path

    with open(output_file_path, 'w') as outfile:
        outfile.write(json_output)

    pass