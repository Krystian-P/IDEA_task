import h5py
import numpy as np

lista = []
with h5py.File('C:/Users/Krystian/Desktop/IDEA_task/task_data.hdf5', 'r') as f:
    for hour in range(1, 25):
        print(hour)
        gens = np.array(f.get(f'/results/hour_{hour}/gens'))
        lista.append(gens[:, 2])
