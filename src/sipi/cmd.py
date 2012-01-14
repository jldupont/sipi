"""
    Simple Command Line tools
"""

import argparse
import fileinput


def process(line_proc, input_ctx={}, parser_args=None, desc=""):
    """
    Process input files
    
    `line_proc` must be a callable which takes 1 tuple as input:
    (ctx, (code, data))
    
    The parameter `ctx` contains contextual information:
    
    * `args`: processed command line arguments (from argparse)
    * `file`: path of current file being processed
    * `lineno`: line number in current file
    * `line`: actual string of the line
    * `total_files`: the current total of files processed (starts at 1)
    * `total_lines`: the current total of lines processed for all files processed
    
    Codes sent to `line_proc`:
    
    * *open*:  processing starts
    * *close*: processing ends
    * *file start*: processing of a new file starts
    * *file end*:   processing of current file ends
    * *line*: actual line of a file
    
    The parameter `parser_args` is a list of tuples `(pargs, kargs)` for `parser.add_argument` of the standard library module `argparse`.
    
    The parameter `desc` is a string description of the command line processor.
    """
    parser=argparse.ArgumentParser(desc)
    if parser_args is not None:
        for action in parser_args:
            pargs, kargs=action
            parser.add_argument(*pargs, **kargs)
            
    parser.add_argument('files', metavar='files', type=str, nargs='+',
                        help='list of files')
            
    args = parser.parse_args()
    
    ctxs={}
    total_files=0
    total_lines=0
    first_file=True

    try:
        line_proc((ctxs, ("open", None)))
        
        fi=fileinput.input(files=args.files)
        #current=fi.filename()
        current=None
        for line in fi:
            total_lines=total_lines+1

            ctxs={
                  "args":       args,
                  "file":       current,
                  "lineno":     fi.filelineno(),
                  "line":       line,
                  "total_files": total_files,
                  "total_lines": total_lines
                  }

            if fi.filename()!=current:
                current=fi.filename()
               
                if not first_file: 
                    line_proc((ctxs, ("file end", None)))
                else:
                    first_file=False
                    
                total_files=total_files+1
                line_proc((ctxs, ("file start", None)))
                
            ctxs.update(input_ctx)
                 
            line_proc((ctxs, ("line", line)))
            
    except Exception,e:
        ### try to abort cleanly, if possible           
        try:
            line_proc((ctxs, ("file end", None)))
            line_proc((ctxs, ("close", None)))
        except:
            ## no use alarming more!
            pass
        raise e
            
    return ctxs

    
