"""
    Simple OS functions
    
"""

import os, errno

def resolve_path(path):
    """
    Resolves a path with user and environment variables
    
    >>> resolve_path("~/.config") # doctest:+ELLIPSIS
    '/home/.../.config'
    """
    return os.path.expanduser(os.path.expandvars(path))


def quick_write(path, contents):
    """
    Best effort "write contents to file" 
    
    >>> quick_write("/tmp/QuickWriteTest", "{'param': 'value'}") # doctest:+ELLIPSIS
    ('ok', ...)
    >>> file_contents("/tmp/QuickWriteTest")
    ('ok', "{'param': 'value'}")
    >>> rm('/tmp/QuickWriteTest') # doctest:+ELLIPSIS
    ('ok', ...)
    """
    try:
        fh=open(resolve_path(path), "w")
        fh.write(contents)
        fh.close()
        return ('ok', path)
    except Exception, e:
        return ("error", str(e))
    finally:
        try:
            fh.close()
        except:
            pass

def file_contents(path):
    """
    Simple "get file contents"
    
    >>> rm('/tmp/JustTouching')
    ('ok', '/tmp/JustTouching')
    >>> touch("/tmp/JustTouching")
    ('ok', '/tmp/JustTouching')
    >>> file_contents("/tmp/JustTouching")
    ('ok', '')
    >>> rm('/tmp/JustTouching')
    ('ok', '/tmp/JustTouching')
    >>> file_contents("/tmp/JustTouching")
    ('error', None)
    """
    try:
        fh=open(path, "r")
        return ('ok', fh.read())
    except:
        return ("error", None)
    finally:
        try:
            fh.close()
        except:
            pass
    


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
    Silently (i.e. no exception thrown) removes a path if possible
    
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
    