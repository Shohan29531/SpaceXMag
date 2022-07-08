import shutil
import os
 
# path to source directory
src_dir = 'fol1'
 
# path to destination directory
dest_dir = 'fol2'


rico_sca_files = []

with open('rico_sca_filter.txt') as f:
    rico_sca_files = [line.rstrip() for line in f]

# getting all the files in the source directory
files = os.listdir(src_dir)
 
shutil.copytree(src_dir, dest_dir)