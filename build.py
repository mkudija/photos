# -*- coding: utf-8 -*- #

import os
import shutil
import sys
from pathlib import Path

# from config import *

def delete_folder_contents(dst):
    """Delete all contents of dst.
    """
    print('\tDeleting {}...'.format(dst))
    for item in os.listdir(dst):
        s = os.path.join(dst, item)
        # print('\t{}                  '.format(s))#, end='\r')
        if os.path.isdir(s):
            shutil.rmtree(s)
        else:
            os.remove(s)


def copytree(src, dst, symlinks=False, ignore=None):
    """Copy directory and all contents from src to dst.
    """
    print('\tCopying {}'.format(dst))
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        # print('\t{}                  '.format(d))#, end='\r')
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def copy_file(src, dst):
    """Copy file from src to dst.
    """
    shutil.copy(src, dst)
 

def insert_text_in_file(original, add, insertionPoint):
    """Inserts text from add into original at insertionPoint    
    """
    # read original 
    f = open(original, "r")
    contents = f.readlines()
    f.close()

    # read addition
    # f = open(add, "r")
    # contentsAdd = f.readlines()
    # f.close()

    # get index of insertionPoint
    i=0
    for line in contents:
        if insertionPoint in line:
            index = i
        i+=1

    # add text
    contents[index:index] = add

    # write original with addition
    f = open(original, "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()


def replace_text_in_file(original, add, replaceText):
    """Replaces replaceText with add in original file.
    """
    with open(original, 'r') as f:
      content = f.read()

    content = content.replace(replaceText, add)

    with open(original, 'w') as f:
      f.write(content)



def construct_index(photos, pathOutput):
    """Copies index.html to pathOutput, and constructs page using photos.
    """

    # copy index from template
    copy_file('theme/index.html', pathOutput)

    i = 999
    for photo in photos:
        print(str(photo))
        original = pathOutput/'index.html'
        name = str(photo).split('-')[-1].split('.')[0]
        date = str(photo).split('-')[0].split('/')[-1]+'-'+str(photo).split('-')[1]
      
        add = '<article class="thumb">\n\
                <a href="'+str(photo)+'" class="image"><img src="'+str(photo).replace(' ','%20').replace('images','images_low-res')+'" alt="" /></a>\n\
                <h2>'+name+' ('+date+')</h2>\n\
                </article>'

        insertionPoint = '<!-- #PHOTOS'+str(i)+'# -->'
        # insert_text_in_file(original, add=add, insertionPoint=insertionPoint)
        replace_text_in_file(original, add=add, replaceText=insertionPoint)

        i-=1

 
def resize_images(dst, height):
    """Resizes all images in dst by factor.
    """
    from PIL import Image
    from glob import glob
    import glob

    img_files = os.listdir(dst)  # list all files and directories

    i=1
    for file in img_files:
        print('\t{} images resized.  '.format(i), end='\r')
        foo = Image.open(dst/Path(file))
        size0 = foo.size[0]
        size1 = foo.size[1]
        resize_factor = height/size1
        size0_new = int(size0*resize_factor)
        size1_new = int(size1*resize_factor)
        foo = foo.resize((size0_new,size1_new),Image.ANTIALIAS)
        foo.save(dst/Path(file), optimize=True, quality=95)
        i+=1
    print('\t{} images resized.  '.format(i), end='\r')


# --------------------------------------------------------------------------------------------------------
if __name__ == "__main__":

    photos = list(Path('images/').glob('*'))
  
    pathOutput = Path('')
    print('Building index.html...')
    construct_index(photos, pathOutput)
    copytree(src='images', dst='images_low-res', symlinks=False, ignore=None)
    resize_images(dst='images_low-res', height=250)
    print('\nDone.\n')