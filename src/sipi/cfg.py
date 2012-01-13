"""
    Simple Configuration Information API

    Configuration files are kept in *~/.config/*. Configuration parameters are treated as "read-only".
    Configuration file format can either be *.json* or *.yaml* , the priority being given to *.json*.
    
    Configuration file names can either be:
    
    1. specified using the *filename* parameter
    2. specified using the *ns* parameter
    3. inferred using the command line argument #0
    4. inferred using the command line argument #1
    
    The options are listed in order of priority.
    
    >>> which()
    ('ns', 'cfg')
"""
import os
import sys
import json
try:
    import yaml
except:
    yaml=None

### GLOBALS - CONFIGURATION
base_dir="~/.config"
ns=None
filename=None

### GLOBALS - private
_resolved_type=None
_resolved_filepath=None
_config_data=None
#####################

def which():
    """
    Reports which file will be used to provide configuration
    
    *file* and *ns* are optional.
    
    >>> which()
    ('ns', 'cfg')
    """
    global ns, filename
    global _resolved_type

    if filename is not None:
        _resolved_type=("filename", filename)
    else:
        if ns is not None:
            _resolved_type=("ns", ns)
            
    if _resolved_type is None:
        
        b0=os.path.basename(sys.argv[0])
        n0=b0.split('.')[0]
        
        ### if there is only 1 sys.argv, then it must be it!
        if len(sys.argv)==1:
            _resolved_type=("ns", n0)
        else:
            ### at least 2 arguments on the command-line?
            ### is the first one "python" in some way?
            if not n0.startswith("python"):
                _resolved_type=("ns", n0)
        
            b1=os.path.basename(sys.argv[1])
            n1=b1.split('.')[0]
        
            _resolved_type=("ns", n1)
    
    return _resolved_type    

def get(param, default=None):
    """
    Get a configuration parameter
    
    >>> get("param1")
    """
    global _config_data
    
    if _config_data:
        return _config_data.get(param, default)
    
    typ, value=_maybe_if_ns_then_generate_path(which())
    typ, value=_maybe_if_file_then_resolve_path((typ, value))
    
    return typ, value

#################################################################################    
### PRIVATE
#################################################################################

    
def _maybe_if_ns_then_generate_path((typ, value), sjson=False, syaml=False):
    """
    In order of priority:
    
    1. json
    2. yaml
    
    >>> _maybe_if_ns_then_generate_path(("ns", "cfg"), sjson=True)  # doctest:+ELLIPSIS
    ('json', '/home/.../.config/cfg.json')
    >>> _maybe_if_ns_then_generate_path(("ns", "cfg"), syaml=True)  # doctest:+ELLIPSIS
    ('yaml', '/home/.../.config/cfg.yaml')
    """
    global base_dir
    
    if typ!="ns":
        return (typ, value)
    
    r_base_dir=_resolve(base_dir)
    base_path=os.path.join(r_base_dir, value)
    
    json_path=base_path+".json"   
    json_exists=os.path.exists(json_path)
    if json_exists or sjson:
        return ("json", json_path)

    yaml_path=base_path+".yaml"
    yaml_exists=os.path.exists(yaml_path)
    if yaml_exists or syaml:
        return ("yaml", yaml_path)
    
    return ("error", ("file not found", (typ, value)))
        
    
def _maybe_if_file_then_resolve_path((typ, value)):
    if typ=="filename":
        return (typ, _resolve(value))
    return (typ, value)

def _resolve(path):
    return os.path.expanduser(os.path.expandvars(path))



if __name__=="__main__":
    import doctest
    doctest.testmod()
