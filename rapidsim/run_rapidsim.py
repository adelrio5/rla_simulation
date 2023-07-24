import os

N = 100000

try:
    os.system('rm -r rs_output')
except:
    pass

os.mkdir('rs_output')
os.chdir('rs_output')

particles = ["K", "mu"]

rs_idx = -1
for particle_i in particles:
    for particle_j in particles:
        for particle_k in particles:

            rs_idx += 1

            f = open('../BLANK.config', 'r')
            f_lines = f.readlines()
            with open(f'rs_{rs_idx}.config', 'a') as f_out:
                for idx, line in enumerate(f_lines):
                    if 'BLANK1' in line:
                        line = line.replace('BLANK1', particle_i)
                    if 'BLANK2' in line:
                        line = line.replace('BLANK2', particle_j)
                    if 'BLANK3' in line:
                        line = line.replace('BLANK3', particle_k)
                    f_out.write(line)

            f = open('../BLANK.decay', 'r')
            f_lines = f.readlines()
            with open(f'rs_{rs_idx}.decay', 'a') as f_out:
                for idx, line in enumerate(f_lines):
                    if 'BLANK1' in line:
                        line = line.replace('BLANK1', particle_i)
                    if 'BLANK2' in line:
                        line = line.replace('BLANK2', particle_j)
                    if 'BLANK3' in line:
                        line = line.replace('BLANK3', particle_k)
                    f_out.write(line)

rs_idx = -1
for particle_i in particles:
    for particle_j in particles:
        for particle_k in particles:

            rs_idx += 1

            os.system(f'~/RapidSim/RapidSim/build/src/RapidSim.exe rs_{rs_idx} {N} 1')

os.system('hadd -fk output.root *_tree.root')
os.system('rm *_tree.root')
os.system('rm *_hists.root')
os.system('rm *config')
os.system('rm *decay')
os.system('mv output.root ../.')
os.system('cd ..')
os.system('rm -r rs_output')

