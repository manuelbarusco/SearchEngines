# Calculates the differences among files
# author: Riccardo Forzan

import itertools
from os import listdir, popen

# folder with all the runs
runs_folder = input("Copy here the full path to the runs folder: ")

all_run_names = listdir(runs_folder)

# generate all possible combinations of 2 files
pairs = list(itertools.combinations(all_run_names, 2))

'''
Iterate over all possible combinations and print the number of different lines
'''

diff_list = []

index = 1

for pair in pairs:
    print(str(index) + "/" + str(len(pairs)))
    index = index + 1
    file_1 = runs_folder + "/" + pair[0]
    file_2 = runs_folder + "/" + pair[1]
    cmd = "diff -y --suppress-common-lines {0} {1} | wc -l".format(file_1, file_2)
    diff = int(popen(cmd).read().strip())
    diff_list.append((pair[0], pair[1], diff))

print(diff_list)