""" change a batch of file names in one directory


@file change_batch_file_names.py
@author Bo Ma
@version 1.0
@date 2019.09.28


"""

import os

def rename_file():
    """
    function to rename a batch of files
    @param 
    @return 

    """
    i = 0

    path_dir = "/home/mabo/2019-now-work-bo/work/working-note-log/2016-2019-germany-wrok/2016-2019-working-note-log-latex/figure/"

    for file_name in os.listdir(path_dir):

        # old_name = path_dir + file_name
        # new_name = path_dir + file_name
        old_name = file_name
        print("the old name is: %s" %(old_name))

        
        #replace the symbol '.' with '-' for the first two '.'
        # old_sym = '.'
        old_sym = '_'
        new_sym = '-'
        new_name = str_replace_sym(old_name,old_sym,new_sym)
        print("the new name is: %s"%(new_name) )

        #rename() will rename all the files
        old_full_path = path_dir + old_name
        new_full_path = path_dir + new_name
        os.rename(old_full_path, new_full_path)

        i +=1

def str_replace_sym(old_string,old_sym,new_sym):
    """
    function to replace the old_sym in the old_sym with a new_sym

    @param old_string the input string 
    @param old_sym the symbol in the input string which will be replaced;
    @param new_sym the symbol which will replace the old_sym

    @return the new string 

    """
    # the number of symbols in the string
    sym_num =  old_string.count(old_sym)
    #omit the last '.' which is used in windows os to define the file property
    if old_sym=='.':
       print("notation: the old symbol is '.'!")
       sym_num -=1

    new_string = old_string.replace(old_sym,new_sym,sym_num)

    return new_string



# Driver code
if __name__ == '__main__':
    #calling the main function
    rename_file()

