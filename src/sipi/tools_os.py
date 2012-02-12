"""
    Sipi - Simple OS functions
    
"""
import os, errno
import shutil
import tempfile

def path_status(path):
    """
    >>> path_status("invalid_path_%$&*!")
    
    """
    try:
        wok=os.access(path, os.W_OK)
        return ("ok", {"wok": wok})
    except Exception,e:
        return ("error", (e.__class__, str(e)))

def atomic_write(path, contents):
    """
    Atomic write to file
    
    Create temporary file and then move/rename to specified path.
    Rename operation in the same filesystem are atomic (at least in Linux).
    
    >>> atomic_write("/tmp/_jlddk_atomic_write", "test!")
    """
    fd, tfn=tempfile.mkstemp()
    
    try:
        ### part 1: write to temp file
        f=os.fdopen(fd, "w")
        f.write(contents)
        f.close()
    except Exception, e:
        try:    os.close(fd)
        except: pass
        return ("error", "write to temp file: %s" % str(e))        
        
    try:
        ### part 2: rename to specified path
        os.rename(tfn, path)
    except:
        return ("error", "rename to path '%s'" % path)
        
    return ("ok", tfn)

def move(src_path, dst_path):
    """
    Move file
    """
    try:
        shutil.move(src_path, dst_path)
        return ("ok", None)
    except Exception, e:
        return ("error", e)


def can_write(path):
    """
    Checks if the current user (i.e. the script) can delete the given path
    Must check both user & group level permissions
    
    FOR THIS TEST, NEED TO CREATE A DIRECTORY /tmp/_test_root_sipi THROUGH ROOT
    
    >>> p="/tmp/_test_sipi"
    >>> rm(p)
    ('ok', '/tmp/_test_sipi')
    >>> touch(p)
    ('ok', '/tmp/_test_sipi')
    >>> can_write(p)
    ('ok', True)
    >>> rm(p)
    ('ok', '/tmp/_test_sipi')
    >>> can_write("/tmp/_test_root_sipi/some_file")
    ('ok', False)
    """
    try:
        return ("ok", os.access(path, os.W_OK))
    except:
        return ("error", None)
    

def gen_walk(path, max_files=None):
    """
    os.walk generator with an optional limit on the number of files returned 
    """
    count=0
    done=False
    for root, _dirs, files in os.walk(path):
        
        for f in files:
            yield os.path.join(root, f)
        
            count=count+1
            if max_files is not None:
                if count==max_files:
                    done=True
                    break
            
        if done: break


def remove_common_prefix(common_prefix, path):
    """
    >>> remove_common_prefix("/tmp", "/tmp/some_dir/some_file.ext")
    ('ok', '/some_dir/some_file.ext')
    """
    try:
        _head, _sep, tail=path.partition(common_prefix)
        return ("ok", tail)
    except:
        return ("error", path)

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
    