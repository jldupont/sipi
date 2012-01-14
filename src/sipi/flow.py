"""
    Simple Flow tools
"""

def coroutine(func):
    """
    Decorator for coroutine creation & bootstrapping
    """
    def _(*args, **kwargs):
        cr=func(*args, **kwargs)
        cr.next()
        return cr
    _.__name__=func.__name__
    return _


def build_pipeline(blocks, pipe=None):
    """
    Build a pipeline from the list of blocks
    
    The first element of the list must correspond to the first `block` of the pipeline.
    
    Each `block` is a tuple `(handler_function, name)`.
    The `handler_function` must accept 1 tuple parameter of the following signature: `(next_block, (context, msg))`. 
    
    """
    rblocks=reversed(blocks)   
    for block in rblocks:
        handler, name=block
        if pipe is None:
            pipe=_processor((None, handler, name))
        else:
            pipe=_processor((pipe, handler, name))
    return pipe


### PRIVATE #################################################
#############################################################


def _processor((nxt, handler, name)):
    def loop():
        try:
            while True:
                ctx, msg=(yield)
                msg=handler(nxt, (ctx, msg))
                if msg is not None:
                    nxt.send(msg)
                    
        except KeyboardInterrupt:
            raise
        
        except Exception,e:
            try:    nxt.send((ctx, ("error", e)))
            except: nxt.send((None, ("error", e)))

    l=loop()
    l.next()    
    return l


