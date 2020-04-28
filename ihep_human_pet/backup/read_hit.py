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


def read_ascii_file_coin(path_file_ascii, list_time_diff):
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


def read_ascii_file_hit(path_file_ascii, path_saved_ascii):
    f = open(path_file_ascii, 'rt', encoding='ascii')
    fw = open(path_saved_ascii, 'wt', encoding='ascii')
    # list_t1 = []
    # num_saved_lines = 200
    # index_start = 0

    try:
        lines = f.readlines()
        for i in range(0, len(lines)):
            print('i is: %d' % (i))
            current_hit = lines[i]
            next_hit_index = i + 1
            if next_hit_index > len(lines):
                print('error!! infecious loop!!')
                break
            next_hit = lines[next_hit_index]

            current_hit_sp = current_hit.split()
            next_hit_sp = next_hit.split()
            #   line_sp = single_line.split(',')
            current_hit_event_id = Decimal(current_hit_sp[1])
            current_hit_par_id = Decimal(current_hit_sp[2])
            next_hit_event_id = Decimal(next_hit_sp[1])
            next_hit_par_id = Decimal(next_hit_sp[2])
            print('hit1_event is: %d, hit2_event is %d' %
                  (current_hit_event_id, next_hit_event_id))

            while current_hit_event_id == next_hit_event_id:
                print('hit1_event is: %d, hit2_event is %d' %
                      (current_hit_event_id, next_hit_event_id))
                # if same event and same particle
                if current_hit_par_id == next_hit_par_id:
                    print('hit1_par_id is: %d, hit2_par_id is %d' %
                          (current_hit_par_id, next_hit_par_id))
                    # print('same event! same patical!')
                    next_hit_index += 1
                    next_hit = lines[next_hit_index]
                    next_hit_sp = next_hit.split()
                    next_hit_event_id = Decimal(next_hit_sp[1])
                    next_hit_par_id = Decimal(next_hit_sp[2])
                    # if next_hit_index > 199:
                    #     print('error!! infecious loop!!')
                    #     break
                # if same event but diff particle, meaning coincidence
                else:
                    print('same event! coincidence!')
                    i = next_hit_index
                    fw.write(current_hit)
                    fw.write(next_hit)
                    break
                # continue
                #     else:
                #         print('same event! coincidence!')
                #         i = next_hit_index
                #         fw.write(current_hit)
                #         fw.write(next_hit)
                #         break
                # if index_start > num_saved_lines:
                # break
                # line_sp = single_line.split()
                # hit_1 = line_sp[6])
                #   convert to picoseconds
                # list_t1.append(t1)
                # print(single_line)
                # fw.write(current_hit)
                # index_start += 1
    finally:
        f.close()
        fw.close()
        # for i in range(1, 10):
        # print(list_t1[i])
        # # print(list_t2[i])
        # # print('the time difference is: % .2f' % (list_time_diff[i]))
        # print('tof-1 is: %.15f ' % (list_t1[i]))


if __name__ == '__main__':
    # path_file_ascii_coin = '/home/mabo/software/data/gate/ihep_human_tof_pet_sz/ihep_cluster/cyl_sphere_activ_ration_1to4_tof_30ps/human_szpet_cyl_to_sphere_1to4_source_tof_30ps_1Coincidences.dat'

    # path_file_ascii_hit = '/home/mabo/software/src/gate/gate_macros/ihep_human_tof_pet_sz/results/human_szpet_tof_30ps_0Hits.dat'
    path_file_ascii_hit = '/home/mabo/software/src/gate/gate_macros/ihep_human_tof_pet_sz/results/test_hits.dat'
    path_file_ascii_saved = '/home/mabo/software/src/gate/gate_macros/ihep_human_tof_pet_sz/results/test_hits_true.dat'
    #     time difference of tofk
    # list_time_diff = []
    # get the time diff
    # read_ascii_file_coin(path_file_ascii_coin, list_time_diff)
    read_ascii_file_hit(path_file_ascii_hit, path_file_ascii_saved)
    # read_ascii_file_hit(path_file_ascii_saved)
    # for i in range(1, 10):
    #     print('the time difference is: % .2f' % (list_time_diff[i]))
