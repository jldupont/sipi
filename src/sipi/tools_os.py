"""
    OS related tools
"""

import os, errno

def touch(path):
    """
    >>> touch("/tmp/JustTouching")
    ('ok', '/tmp/JustTouching')
    >>> rm('/tmp/JustTouching')
    ('ok', '/tmp/JustTouching')
    """
    fhandle = file(path, 'a')
    try:
        os.utime(path, None)
        return ('ok', path)
    except OSError, exc:
        return ("error", (exc.errno, errno.errorcode[exc.errno]))
    finally:
        fhandle.close()        

def rm(path):
    """
    >>> rm("/tmp/NotAFile") ## no need to complain if there is no file
    ('ok', '/tmp/NotAFile')
    """
    try:
        os.remove(path)
        return ('ok', path)
    except OSError, exc:
        if exc.errno==errno.ENOENT:
            return ('ok', path)
        return ("error", (exc.errno, errno.errorcode[exc.errno]))
    

def rmdir(path):
    """
    Silently (i.e. no exception thrown) removes a directory if possible
    
    >>> rmdir("/tmp/JustATestDir")
    ('error', (2, 'ENOENT'))
    >>> mkdir_p("/tmp/JustATestDir")
    ('ok', '/tmp/JustATestDir')
    >>> rmdir("/tmp/JustATestDir")
    ('ok', '/tmp/JustATestDir')
    """
    try:
        os.rmdir(path)
        return ('ok', path)
    except OSError,exc:
        return ("error", (exc.errno, errno.errorcode[exc.errno]))

def mkdir_p(path):
    """
    Silently (i.e. no exception thrown) makes a directory structure if possible
    
    >>> mkdir_p("/tmp/JustATestDir")
    ('ok', '/tmp/JustATestDir')
    >>> mkdir_p("/tmp/JustATestDir")
    ('ok', '/tmp/JustATestDir')
    >>> rmdir("/tmp/JustATestDir")
    ('ok', '/tmp/JustATestDir')
    """
    try:
        os.makedirs(path)
        return ('ok', path)
    except OSError, exc:
        if exc.errno == errno.EEXIST:
            return ('ok', path)

        return ('error', (exc.errno, errno.errorcode[exc.errno]))
        
        
if __name__=="__main__":
    import doctest
    doctest.testmod()
    