#!/usr/bin/python
import os
import shutil
import stat
from typing import Type, List


def copytree(src: str, dst: str, symlinks: bool = False, ignore: Type[List] = None):
    """ https://stackoverflow.com/a/22331852 """

    if not os.path.exists(dst):
        os.makedirs(dst)
        shutil.copystat(src, dst)
  
    lst = os.listdir(src)
  
    if ignore:
        excl = ignore(src, lst)
        lst = [x for x in lst if x not in excl]
    
    for item in lst:
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if symlinks and os.path.islink(s):
            if os.path.lexists(d):
                os.remove(d)
            os.symlink(os.readlink(s), d)
            try:
                st = os.lstat(s)
                mode = stat.S_IMODE(st.st_mode)
                os.lchmod(d, mode)
            except:
                pass # lchmod not available
        elif os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)