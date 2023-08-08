import os
import time
import itertools
from pathlib import Path
import uproot
import numpy as np
N = 100000

try:
    os.system('rm -r rs_output')
except:
    pass

os.mkdir('rs_output')
os.chdir('rs_output')

mother_particles = ["B"]

particles = ["K", "mu", "p", "e"]

# TODO: Do this a bit more nicely. Maybe use "particle" library?
particles_pid = {
    'K+': 321,
    'K-': -321,
    'mu+': 13,
    'mu-': -13,
    'p+': 2212,
    'p-': -2212,
    'e+': -11,
    'e-': 11,
    'B+': 521,
}

# Set the desired length of each combination
combination_length = 3

# Generate all combinations with repetitions allowed
all_combinations = list(itertools.product(particles, repeat=combination_length))

# Remove duplicates by converting each combination to a set
unique_combinations = {tuple(sorted(comb)) for comb in all_combinations}

# Convert back to a list of lists
unique_combinations = [list(comb) for comb in unique_combinations]

print(f"Running {len(unique_combinations)} channels")
rapid_sim_path = '~/RapidSim/RapidSim/build/src/RapidSim.exe'
if os.environ.get('RAPID_SIM_EXE_PATH') is not None:
    rapid_sim_path = os.environ.get('RAPID_SIM_EXE_PATH')

rs_idx = -1
for particle_m in mother_particles:
    for particle_combination in unique_combinations:
        particle_i = particle_combination[0]
        particle_j = particle_combination[1]
        particle_k = particle_combination[2]

        rs_idx += 1

        f = open('../BLANK.config', 'r')
        f_lines = f.readlines()
        with open(f'rs_{rs_idx}.config', 'a') as f_out:
            for idx, line in enumerate(f_lines):
                if 'BLANK0' in line:
                    line = line.replace('BLANK0', particle_m + '+')
                if 'BLANK1' in line:
                    line = line.replace('BLANK1', particle_i + '+')
                if 'BLANK2' in line:
                    line = line.replace('BLANK2', particle_j + '+')
                if 'BLANK3' in line:
                    line = line.replace('BLANK3', particle_k + '-')
                f_out.write(line)

        f = open('../BLANK.decay', 'r')
        f_lines = f.readlines()
        with open(f'rs_{rs_idx}.decay', 'a') as f_out:
            for idx, line in enumerate(f_lines):
                if 'BLANK0' in line:
                    line = line.replace('BLANK0', particle_m + '+')
                if 'BLANK1' in line:
                    line = line.replace('BLANK1', particle_i + '+')
                if 'BLANK2' in line:
                    line = line.replace('BLANK2', particle_j + '+')
                if 'BLANK3' in line:
                    line = line.replace('BLANK3', particle_k + '-')
                f_out.write(line)

time_A_full = time.time()
rs_idx = -1
for particle_m in mother_particles:
    for particle_combination in unique_combinations:
        particle_i = particle_combination[0]
        particle_j = particle_combination[1]
        particle_k = particle_combination[2]

        rs_idx += 1
        print(
            f"{rs_idx + 1}/{len(unique_combinations)}, Running RapidSim for {particle_m}+ -> {particle_i}+ {particle_j}+ {particle_k}-")
        time_A = time.time()
        os.system(f'{rapid_sim_path} rs_{rs_idx} {N} 1 > dump.txt  ')
        file = uproot.open(f'rs_{rs_idx}_tree.root')["DecayTree"]
        keys = file.keys()
        results = file.arrays(keys, library="np")
        file.close()

        results['mother_PID'] =  np.zeros(len(results['mother_E']), dtype=np.int32) + particles_pid[particle_m+'+']
        results['particle_1_PID'] = np.zeros(len(results['mother_E']), dtype=np.int32) + particles_pid[particle_i+'+']
        results['particle_2_PID'] = np.zeros(len(results['mother_E']), dtype=np.int32) + particles_pid[particle_j+'+']
        results['particle_3_PID'] = np.zeros(len(results['mother_E']), dtype=np.int32) + particles_pid[particle_k+'-']

        file2 = uproot.recreate(f'rs_{rs_idx}_tree2.root')
        file2['DecayTree'] = results
        file2.close()


        time_B = time.time()
time_B_full = time.time()

os.system('rm dump.txt')
os.system('hadd -fk output.root *_tree2.root')
os.system('rm *_tree.root')
os.system('rm *_hists.root')
os.system('rm *config')
os.system('rm *decay')
os.system('mv output.root ../.')
os.chdir(Path(os.getcwd()).parents[0])
os.system('rm -r rs_output')

print(f"\n\n\ntime: {time_B_full - time_A_full:.4f}")
os.system('ls -lh output.root')