# Author: Tomas Hodan (hodantom@cmp.felk.cvut.cz)
# Center for Machine Perception, Czech Technical University in Prague

import os
import sys
import yaml

sys.path.append(os.path.abspath('..'))
from pysixd import inout

model_mpath = '/local/datasets/tlod/imperial/tejani/models/obj_{:02d}.ply'
bbox_cens_path = '../output/tejani_bbox_cens.yml' # File to save bbox centers

bbox_cens = []
obj_ids = range(1, 7)
for obj_id in obj_ids:
    print('Processing obj: ' + str(obj_id))
    model_path = model_mpath.format(obj_id)
    model = inout.load_ply(model_path)

    # Scale
    model['pts'] *= 1000.0  # Convert to [mm]

    # Translate the bounding box center to the origin
    bb_cen = 0.5 * (model['pts'].min(axis=0) + model['pts'].max(axis=0))
    model['pts'] -= bb_cen
    bbox_cens.append(bb_cen.flatten().tolist())

    # Save the transformed model
    inout.save_ply(model_path, model['pts'], model['colors'], model['normals'],
                   model['faces'])

with open(bbox_cens_path, 'w') as f:
    yaml.dump(bbox_cens, f, width=10000)
