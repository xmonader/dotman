import os
import os.path
from sys import argv
from typing import List, Tuple 
import argparse

def get_linkable_files(apppath : str, dest:str =os.path.expanduser("~")) -> List[Tuple[str, str]]: 
    """
    collects the linkable files in a certain app.

    apppath: application's dotfiles directory
        we expect dir to have the hierarchy.
        i3
        `-- .config
            `-- i3
            `-- config

    dest: destination of the link files : default is the home of user.
    """

    linkables = []
    for root, dirs, files in os.walk(apppath):
        # for d in dirs:
        #     dirpath = os.path.join(root, d)
        for f in files:
            filepath = os.path.join(root, f)
            linkpath =  os.path.join(dest, filepath.replace(apppath, ""))
            # remove leading /
            linkpath = linkpath[1:] if linkpath.startswith("/") else linkpath
            linkpath = os.path.join(dest, linkpath)
            linkables.append((filepath, linkpath))
        
    return linkables

def stow(linkables:List[Tuple[str, str]], simulate:bool =True, verbose:bool =True):
    """
    Creates symoblic links and related directories

    linkables is a list of tuples (filepath, linkpath) : List[Tuple[file_path, link_path]]
    simulate does simulation with no effect on the filesystem: bool
    verbose shows log messages: bool

    """
    for filepath, linkpath in linkables:
        if verbose:
            print("Will link {} -> {}".format(filepath, linkpath))

        if not simulate:
            os.makedirs(os.path.dirname(linkpath), exist_ok=True)
            os.symlink(filepath, linkpath)

def cli():
    parser =argparse.ArgumentParser()
    parser.add_argument("-s", "--simulate", action="store_true", default=False, help="Simulate, with no actions on the filesystem.")
    parser.add_argument("-v", "--verbose", action="store_true", default=True)
    parser.add_argument("-a", "--app", help="Application name to stow its configs.")
    parser.add_argument("-d", "--dest", default=os.path.expanduser("~"))
    res = parser.parse_args()
    apppath = os.path.realpath(res.app)

    stow(get_linkable_files(apppath, dest=res.dest), simulate=res.simulate, verbose=res.verbose)
    

if __name__ == "__main__":
    cli()