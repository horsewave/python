"""
@file your_file_name.py
@detail :write your Description
@author Bo Ma
@date 2019.09.28
Email:mabo@ihep.ac.cn
Tel:010-88235869
Cell:15210606357
@version 1.0
"""

import subprocess
import time
from decimal import Decimal

# read ascii file


def read_ascii_file(path_file_ascii, list_time_diff):
    f = open(path_file_ascii, 'rt', encoding='ascii')
    list_t1 = []
    list_t2 = []

    try:
        for single_line in f.readlines():
            # do something
            line_sp = single_line.split()
            #   line_sp = single_line.split(',')
            t1 = Decimal(line_sp[6])
            t2 = Decimal(line_sp[29])
            #   convert to picoseconds
            time_diff = (t1-t2)*10**12
            #   list_t1.append(Decimal(t1))
            list_t1.append(t1)
            list_t2.append(t2)
            list_time_diff.append(time_diff)
    finally:
        f.close()
        for i in range(1, 10):
            # print(list_t1[i])
            # # print(list_t2[i])
            # # print('the time difference is: % .2f' % (list_time_diff[i]))
            print('tof-1 is: %.15f, tof-2 is: %.15f , the time difference is: %.15f ' %
                  (list_t1[i], list_t2[i], list_time_diff[i]))


if __name__ == '__main__':
    path_file_ascii = '/home/mabo/software/data/gate/ihep_human_tof_pet_sz/ihep_cluster/cyl_sphere_activ_ration_1to4_tof_30ps/human_szpet_cyl_to_sphere_1to4_source_tof_30ps_1Coincidences.dat'
    #     time difference of tof
    list_time_diff = []
    # get the time diff
    read_ascii_file(path_file_ascii, list_time_diff)
    for i in range(1, 10):
        print('the time difference is: % .2f' % (list_time_diff[i]))
