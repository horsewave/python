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
from matplotlib import pyplot as plt
import numpy as np
from pandas import DataFrame, Series
import pandas as pd
import pylab as plb
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
from scipy.signal import chirp, find_peaks, peak_widths
import random
# read ascii file


def read_ascii_file_coin(path_file_ascii):
    """read ascii file of the gate simulated coincidences 
    Arguments:
        path_file_ascii {[string]} -- [absolute path for the ascii file ]
    """
    f = open(path_file_ascii, 'rt', encoding='ascii')
    list_t1 = []
    list_t2 = []
    list_time_diff = []

    try:
        """using try: finally is a good way to prevent opening error.
        """
        for single_line in f.readlines():
            # do something
            line_sp = single_line.split()
            # get the absolute time for single 1 and two
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
            """check if it is right.
            """
            # # print('the time difference is: % .2f' % (list_time_diff[i]))
            print('tof-1 is: %.15f, tof-2 is: %.15f , the time difference is: %.15f ' %
                  (list_t1[i], list_t2[i], list_time_diff[i]))


def read_ascii_file_hit(path_file_ascii, path_saved_ascii):
    """read the gate simulated hit in ascii format, and extract the first hit for each gamma photons and Save the extracted file

    Arguments:
        path_file_ascii {[string]} -- [path for the gated generated hit ascii file]
        path_saved_ascii {[string]} -- [saved path for the extracted hit file]
    """
    f = open(path_file_ascii, 'rt', encoding='ascii')
    fw = open(path_saved_ascii, 'wt', encoding='ascii')
    try:
        lines = f.readlines()
        line_num=len(lines)
        i = 0
        while i < len(lines):
            # print('i is: %d' % (i))
            current_hit = lines[i]
            next_hit_index = i + 1
            if next_hit_index >= len(lines):
                """make sure the index is in the list range.
                """
                print('data reading finished!!! ')
                break
            next_hit = lines[next_hit_index]

            current_hit_sp = current_hit.split()
            next_hit_sp = next_hit.split()
            #get the event id and the particle id for current line
            current_hit_event_id = Decimal(current_hit_sp[1])
            current_hit_par_id = Decimal(current_hit_sp[2])
            #get the event id and the particle id for the next line
            next_hit_event_id = Decimal(next_hit_sp[1])
            next_hit_par_id = Decimal(next_hit_sp[2])

            while current_hit_event_id == next_hit_event_id:
                """1:make sure the current and the next hit is from the same event
                    2:if the event id and the particle id is the same, then drop the following hits,only keeping the first hit; 
                    3: if the event id is the same, and the partical id is different, then saveing both the two hits which are the first hits from the two back to back gamma photons. At this step you can exit the loop.
                    4: move the hit pointer to the latest position.
                """
                # if same event and same particle
                if current_hit_par_id == next_hit_par_id:
                    next_hit_index += 1
                    if next_hit_index >= len(lines):
                        print('data reading finished!!!')
                        break
                    next_hit = lines[next_hit_index]
                    next_hit_sp = next_hit.split()
                    next_hit_event_id = Decimal(next_hit_sp[1])
                    next_hit_par_id = Decimal(next_hit_sp[2])
                else:
                    fw.write(current_hit)
                    fw.write(next_hit)
                    break

            i = next_hit_index

    finally:
        f.close()
        fw.close()
        print('date read finished sucessfully!!')

def get_time_diff_hits(path_file_ascii,cut_count_threshold=5):
    """get the histgram of the processed hits which is in ascii format.
       The way to process the data is to use the pandas library.

    Arguments:
        path_file_ascii {[string]} -- [the path of the hit ascii file. This file is not the original GATE simulated file, but the hits file which only includes the first hit for each particle for TOF evaluation.]

    Keyword Arguments:
        cut_count_threshold {int} -- [the cut value for the time diff counts bellow which the time diff is drop.] (default: {5})

    Returns:
        [pandas.Series] -- [a series data whose index is the time difference in picoseconds and the value is the sum of the hit counts falling in this time diff. ]
    """
    # 1:read hit data into dataframe
    # df_hit = pd.read_table(path_file_ascii, sep='\s',  header=None)
    df_hit = pd.read_table(
        ###read part of the file according to the nrows.
        # path_file_ascii, delim_whitespace=True,  header=None,nrows=10000)
        path_file_ascii, delim_whitespace=True,  header=None)
    li_hit_header = ['1_run_id', '2_event_id', '3_particle_id', '4_source_id',
                 '5_base_id', '6_rsector_id', '7_module_id', '8_submodule_id','9_crystal_id','10_layer_id','11_time','12_dep_energy','13_par_range','14_pos_x','15_pos_y','16_pos_z','17_geant4_hit','18_hit_mother_id','19_par_mother_id','20_photon_id','21_compton_phantom_num','22_rayleigh_phantom_num','23_physics_interaction','24_compton_volume','25_rayleigh_volume']
    df_hit.columns=li_hit_header
    # use pivot to check specified data
    df_hit_pivot=pd.pivot_table(df_hit,index=['2_event_id'],columns=['3_particle_id'],values=['11_time'])
    
    """1:note partical_id 1 and 2 is int, not string, so you can not add quotations.
       2:time difference in picoseconds 
       3: this is a multiIndex DataFrame.
    Returns:
        [type] -- [description]
    """
    df_hit_pivot['11_time','time_diff'] =np.round((df_hit_pivot['11_time',1] - df_hit_pivot['11_time',2])*10**12)
    se_hist_tof=df_hit_pivot['11_time','time_diff'].value_counts()
    """get the counts for each time diff

    Returns:
        [pandas.Series] -- [a series data whose index is the time difference in picoseconds and the value is the sum of the hit counts falling in this time diff.]
    """
    #remove rows whose counts smaller than cut_count_threshold, and sort the series ascendingly
    se_hist_tof=(se_hist_tof[se_hist_tof[:]>cut_count_threshold]).sort_index()
    # print(se_hist_tof)
    return se_hist_tof

def get_time_diff_coincidences_single_cpu(path_file_ascii,cut_count_threshold=10):
    """read the GATE simulated coincidence data which is in ascii format into pandas dateframe, and get the event counts for different TOF bins

    Arguments:
        path_file_ascii {[string]} -- [path for the original GATE simulated coincidences file]

    Keyword Arguments:
        cut_count_threshold {int} -- [the cut value for the time diff counts bellow which the time diff is drop] (default: {10})

    Returns:
        [pandas.Series] -- [a series data whose index is the time difference in picoseconds and the value is the sum of the hit counts falling in this time diff. ]
    """
    df_coincidence = pd.read_table(
        path_file_ascii, delim_whitespace=True,  header=None,nrows=100000)
        # path_file_ascii, delim_whitespace=True,  header=None)
    
    """1:generate a new line for the time difference in picoseconds.
       2: use iloc to slice the dateframe. This took me more than 20 mins. 
    
    Returns:
        [dataframe?] -- [the time difference in int format which are all negative values]
    """
    df_coincidence['time_diff'] =np.round((df_coincidence.iloc[:,6]-df_coincidence.iloc[:,29])*10**12)
    
    #the values of the column of time difference are all negative values.now randomly set the values with both positive and negative values which will make the time curve more elengate, using the random generater: random.getrandbits(1) or random.choice([-1,1]:). I prefer the later one.
    coin_num=df_coincidence['time_diff'].size
    for i in range(0,coin_num,1):
        df_coincidence['time_diff'].values[i]=df_coincidence['time_diff'].values[i]*random.choice([-1,1])
    
    se_hist_tof=df_coincidence['time_diff'].value_counts()
    # #remove rows whose counts smaller than cut_count_threshold
    se_hist_tof=(se_hist_tof[se_hist_tof[:]>cut_count_threshold]).sort_index()
    # print(se_hist_tof)
    return se_hist_tof

def get_peak_fwhm(se_hist_tof):
    """get the fwhm of a peak

    Arguments:
        se_hist_tof {[pandas.Series]} -- [the index is the time difference in picoseconds, the value is the counts for each time diff.]
        path_save_img {[string]} -- [the pave for the saved image]

    Returns:
        [ndarray] -- [return:4*N array, where N is the number of peiclo: 0::FWHM, 1:heigh of the FWHM, 3: left pos;4: right pos]
    """
    #get the max of the series values.
    tof_max=se_hist_tof.max()
    
    # peaks, _ = find_peaks(se_hist_tof.values)
    ar_width=np.array(se_hist_tof.index.array)
    peak_prominence=tof_max-100
    peaks, _ = find_peaks(se_hist_tof.values,width=ar_width,prominence=peak_prominence)
    """find the peaks of the curve.
       1: the width parameter does not work accordingly. the peak index is always from 0~length.
       2: the prominence parameter is used to make sure only choose the most prominent peak. Otherwise there will be a lot of peaks.
    Returns:
        [type] -- [the positions of all the peaks]
    """
    peak_fwhm_pos=peak_widths(se_hist_tof.values,peaks,rel_height=0.5)
    """get the widths of all the peaks

    Returns:
        [multi-dimention arrays,4*N] -- [where N is the number of peiclo: 0::FWHM, 1:heigh of the FWHM, 3: left pos;4: right pos]
    """
    # print(se_hist_tof.values.shape)
    print(peak_fwhm_pos)
     
    return peak_fwhm_pos

def draw_peak(li_curve_data,li_peak_fwhm_pos,li_curve_name,path_save_img):
    """Draw multiple curves in one figure and show the position of the FWHM

    Arguments:
        li_curve_data {[list]} -- [a list of pandas.Series data, each of which contains the tof in ps(index), and the counts(values)]
        li_peak_fwhm_pos {[list]} -- [a list of peak_widths, each of which contains 4*N arrays:0:FWHM;1:the height;3 and 4 are the left and right position seperately]
        li_curve_name {[list]} -- [a list of names which to lable each curve in the legend]
        path_save_img {[string]} -- [path to save the genereated image.]
    """
    #get the length of the list
    num_peak_data=len(li_curve_data)
    num_peak_fwhm=len(li_peak_fwhm_pos)
    if num_peak_data!=num_peak_fwhm:
        print('the number of peak data: %d is not equal to the number of peak_fwhm: %d!Please check!! \n' %(num_peak_data,num_peak_fwhm))
        return
    
    # 创建一个画板
    fig = plt.figure()
    # 修改画板的大小
    fig.set_size_inches(10, 10)
    # 在画板上添加一个Axes绘图区域
    ax = fig.add_subplot(111)
    
    # to contain the legends for each curve.
    li_fwhm_legend=[]
    
    for i in range(0,num_peak_data):
        se_hist_tof=li_curve_data[i]
        peak_fwhm_pos=li_peak_fwhm_pos[i]
        str_curve_name=li_curve_name[i]
        # plot_tof = ax.plot(se_hist_tof.values)
        # plt.plot(se_hist_tof.index,se_hist_tof.values)
        plot_tof = ax.plot(se_hist_tof.index,se_hist_tof.values)
        plt.setp(plot_tof,marker='o', linestyle='-', linewidth=1, markersize=6)
        # plt.plot(se_hist_tof.index[peaks], se_hist_tof.values[peaks], "x")
        
        plt.hlines(peak_fwhm_pos[1][0],se_hist_tof.index[round(peak_fwhm_pos[2][0])],se_hist_tof.index[round(peak_fwhm_pos[3][0])])
        print('the left x point is:%d \n '%(se_hist_tof.index[round(peak_fwhm_pos[2][0])]))
        print('the right x point is:%d \n '%(se_hist_tof.index[round(peak_fwhm_pos[3][0])]))
        fwhw_value=se_hist_tof.index[round(peak_fwhm_pos[3][0])]-se_hist_tof.index[round(peak_fwhm_pos[2][0])]
        # li_fwhm_legend.append('FWHM:'+str(int(fwhw_value))+'ps')
        li_fwhm_legend.append(str_curve_name+'\n'+'FWHM:'+str(int(fwhw_value))+'ps')
    
    plt.legend(li_fwhm_legend,loc='best')
    plt.title('time diff')
    plt.xlabel('tof(ps)')
    plt.ylabel('counts')
    
    plt.savefig(path_save_img)
    plt.show()


def get_time_diff_coincidences_multi_cpu(path_base_name,file_suffix='Coincidences.dat',file_number=5):
    # path_base_name='/home/mabo/software/data/gate/ihep_human_tof_pet_sz/ihep_cluster/point_source/diff_cry_length/human_szpet_point_source_central_single_slice_cry_len_2mm_ew_50kev_tof_0ps_'
    file_suffix='Coincidences.dat'
    # file_number=3
    se_hist_tof=pd.Series()
    
    for i in range(1,file_number+1):
            path_full=path_base_name+str(i)+file_suffix
            se_hist_temp=get_time_diff_coincidences_single_cpu(path_full)
            se_hist_tof=se_hist_tof.radd(se_hist_temp,fill_value=0)
            # se_hist_tof.add(se_hist_temp,fill_value=0)
            # print('the sum after is \n')
            # print(se_hist_tof[-5:5])
    return se_hist_tof
    
def main_coincidence_process_single_cpu():
    """this is the main function for displaying the EVENT distributions for different TOF for multiple input files to compare
       1: there are three fields needed to fill: 
         1) the original path for the GATE simulated coincidence data which is in ASCII format; 
         2) the name for each curve which will show in the legend; 
         3) the path to save the image.
    
    """
    li_file_path=[]
    li_curve_name=[]
    li_file_path.append('/home/mabo/software/data/gate/ihep_human_tof_pet_sz/ihep_cluster/point_source/diff_cry_length/human_szpet_point_source_central_single_slice_cry_len_10mm_ew_50kev_tof_0ps_1Coincidences.dat')
    li_curve_name.append('cry_len_10mm_tof_0ps')
    
    li_file_path.append('/home/mabo/software/data/gate/ihep_human_tof_pet_sz/ihep_cluster/point_source/diff_cry_length/human_szpet_point_source_central_single_slice_cry_len_10mm_ew_50kev_tof_10ps_1Coincidences.dat')
    li_curve_name.append('cry_len_10mm_tof_10ps')
    
    li_file_path.append('/home/mabo/software/data/gate/ihep_human_tof_pet_sz/ihep_cluster/point_source/diff_cry_length/human_szpet_point_source_central_single_slice_cry_len_10mm_ew_50kev_tof_20ps_1Coincidences.dat')
    li_curve_name.append('cry_len_10mm_tof_20ps')
    
    
    path_saved_img_coin ='/home/mabo/software/data/gate/ihep_human_tof_pet_sz/ihep_cluster/point_source/diff_cry_length/Coincidences_tof_saved_cry_len_10mm_img.jpg'
    
    li_curve_data=[]
    li_peak_fwhm_pos=[]
    for i in range(0,len(li_file_path)):
        se_hist_tof = get_time_diff_coincidences_single_cpu(li_file_path[i])
        peak_fwhm_pos=get_peak_fwhm(se_hist_tof)
        
        li_curve_data.append(se_hist_tof)
        li_peak_fwhm_pos.append(peak_fwhm_pos)
    
    draw_peak(li_curve_data,li_peak_fwhm_pos,li_curve_name,path_saved_img_coin)

def main_coincidence_process_multi_cpu():
    """this is the main function for displaying the EVENT distributions for different TOF for multiple input files to compare
       1: there are three fields needed to fill: 
         1) the original path for the GATE simulated coincidence data which is in ASCII format; 
         2) the name for each curve which will show in the legend; 
         3) the path to save the image.
    
    """
    li_file_path=[]
    li_curve_name=[]
    li_cpu_num=[]
    li_file_path.append('/home/mabo/software/data/gate/ihep_human_tof_pet_sz/ihep_cluster/point_source/diff_cry_length/human_szpet_point_source_central_single_slice_cry_len_2mm_ew_50kev_tof_0ps_')
    li_curve_name.append('cry_len_2mm_tof_0ps')
    li_cpu_num.append(5)
    
    li_file_path.append('/home/mabo/software/data/gate/ihep_human_tof_pet_sz/ihep_cluster/point_source/diff_cry_length/human_szpet_point_source_central_single_slice_cry_len_3.6mm_ew_50kev_tof_0ps_')
    li_curve_name.append('cry_len_3.6mm_tof_0ps')
    li_cpu_num.append(5)
    
    li_file_path.append('/home/mabo/software/data/gate/ihep_human_tof_pet_sz/ihep_cluster/point_source/diff_cry_length/human_szpet_point_source_central_single_slice_cry_len_5mm_ew_50kev_tof_0ps_')
    li_curve_name.append('cry_len_5mm_tof_0ps')
    li_cpu_num.append(5)
    
    li_file_path.append('/home/mabo/software/data/gate/ihep_human_tof_pet_sz/ihep_cluster/point_source/diff_cry_length/human_szpet_point_source_central_single_slice_cry_len_10mm_ew_50kev_tof_0ps_')
    li_curve_name.append('cry_len_10mm_tof_0ps') 
    li_cpu_num.append(5)
    
    li_file_path.append('/home/mabo/software/data/gate/ihep_human_tof_pet_sz/ihep_cluster/point_source/diff_cry_length/human_szpet_point_source_central_single_slice_cry_len_20mm_ew_50kev_tof_0ps_')
    li_curve_name.append('cry_len_20mm_tof_0ps')
    li_cpu_num.append(5)
    
    path_saved_img_coin ='/home/mabo/software/data/gate/ihep_human_tof_pet_sz/ihep_cluster/point_source/diff_cry_length/Coincidences_tof_saved_img.jpg'
    
    li_curve_data=[]
    li_peak_fwhm_pos=[]
    for i in range(0,len(li_file_path)):
        se_hist_tof = get_time_diff_coincidences_multi_cpu(li_file_path[i],file_number=li_cpu_num[i])
        peak_fwhm_pos=get_peak_fwhm(se_hist_tof)
        
        li_curve_data.append(se_hist_tof)
        li_peak_fwhm_pos.append(peak_fwhm_pos)
    
    draw_peak(li_curve_data,li_peak_fwhm_pos,li_curve_name,path_saved_img_coin) 

def main_hit_process():
    """this is the main function for displaying the EVENT distributions for different TOF for multiple input files to compare
       1: there are four fields needed to fill: 
         1) the original path for the GATE simulated hit  data which is in ASCII format; 
         2) the name for each curve which will show in the legend; 
         3) the path to save the image.
         4) the path to save the extracted hits which contains only the first hit for each gamma photon 
    
    """
    li_file_path=[]
    li_file_saved_path=[]
    li_curve_name=[]
    li_file_path.append('/home/mabo/software/data/gate/ihep_human_tof_pet_sz/ihep_cluster/point_source/diff_cry_length/human_szpet_point_source_central_single_slice_cry_len_10mm_tof_0ps_1Hits.dat')
    li_file_saved_path.append('/home/mabo/software/data/gate/ihep_human_tof_pet_sz/ihep_cluster/point_source/diff_cry_length/human_szpet_point_source_central_single_slice_cry_len_10mm_tof_0ps_1Hits_saved_true.dat')
    li_curve_name.append('cry_len_10mm_tof_0ps')

    li_file_path.append('/home/mabo/software/data/gate/ihep_human_tof_pet_sz/ihep_cluster/point_source/diff_cry_length/human_szpet_point_source_central_single_slice_cry_len_5mm_tof_0ps_1Hits.dat')
    li_file_saved_path.append('/home/mabo/software/data/gate/ihep_human_tof_pet_sz/ihep_cluster/point_source/diff_cry_length/human_szpet_point_source_central_single_slice_cry_len_5mm_tof_0ps_1Hits_saved_true.dat')
    li_curve_name.append('cry_len_5mm_tof_0ps')


    path_saved_img ='/home/mabo/software/data/gate/ihep_human_tof_pet_sz/ihep_cluster/point_source/diff_cry_length/hits_tof_saved_img.jpg'

    li_curve_data=[]
    li_peak_fwhm_pos=[]
    for i in range(0,len(li_file_path)):
        read_ascii_file_hit(li_file_path[i], li_file_saved_path[i])
        se_hist_tof = get_time_diff_hits(li_file_saved_path[i])
        peak_fwhm_pos=get_peak_fwhm(se_hist_tof)
        
        li_curve_data.append(se_hist_tof)
        li_peak_fwhm_pos.append(peak_fwhm_pos)

    draw_peak(li_curve_data,li_peak_fwhm_pos,li_curve_name,path_saved_img)
 
        
   
if __name__ == '__main__':

    
    # main_coincidence_process()
    # main_hit_process() 
    # read_multi_ascii_file_coin()
    main_coincidence_process_single_cpu() 
   # main_coincidence_process_multi_cpu()

        
    
    # series_add_test()