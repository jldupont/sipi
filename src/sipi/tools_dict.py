"""
    Created on 2012-01-27
    @author: jldupont
"""

def strip(d):
    """
    Strip each element in a dict
    
    >>> strip({"e1":" v1", "e2":" v2 "})
    {'e1': 'v1', 'e2': 'v2'}
    """
    for e in d:
        try:    d[e]=d[e].strip()
        except: pass
    return d


if __name__=="__main__":
    import doctest
    doctest.testmod()
    