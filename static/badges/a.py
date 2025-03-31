import os
import random

folder = "."
files = [f for f in os.listdir(folder) if f.endswith(".png")]
original_paths = [os.path.join(folder, f) for f in files]

shuffled = files[:]
random.shuffle(shuffled)

temp_names = [f"tmp_{i}.tmp" for i in range(len(files))]
temp_paths = [os.path.join(folder, name) for name in temp_names]

for src, tmp in zip(original_paths, temp_paths):
    os.rename(src, tmp)

for tmp, new_name in zip(temp_paths, shuffled):
    os.rename(tmp, os.path.join(folder, new_name))
