"""
    Simple String tools
"""
import re

def trim_leading_0(x):
    """
    Trim leading 0 from a string
    """
    return re.sub('^0+',"", x)


def bulk_replace(x, patterns):
    """
    Bulk replace
    
    Parameter `x` is the input string.  
    Parameters `patterns` must be a list of tuples of the sort `(old, new)` where `old` is the original character to replace with `new`.
    """
    try:
        for old, new in patterns:
            x=x.replace(old, new)
    except:
        pass
    return x


REGEX_ALPHA_INT=re.compile( r'^([a-zA-Z]+)([0-9]+)$' )
def split_alpha(x, default_head=""):
    """
    Splits the alphabetical and numerical parts of a string
    
    >>> split_alpha("w080")
    ('w', '080')
    """
    try:
        result=REGEX_ALPHA_INT.match(x)
        groups=result.groups()
        return (groups[0].strip(), groups[1])
    except:
        return (default_head, x)


if __name__=="__main__":
    import doctest
    doctest.testmod()
