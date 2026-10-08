
# Allow importing student code from parent directory (outside of ./src)
import sys
from pathlib import Path
from typing import (
    Dict,
    Optional,
    Iterable,
)
import subprocess
import tempfile

sys.path.append(str(Path(__file__).parent.parent))
sys.setrecursionlimit(10_000)

from lark import Lark

import src.ski_prog as ski_prog
from ski_eval import eval as ski_eval_eval
from src.ski import S, K, I, App, Var, Expr, check_ast_is_wellformed

DIR = Path(__file__).resolve().parent

ski_syntax = Path('./src/ski_prog.lark').read_text()
ski_parser = Lark(ski_syntax, start='start', parser='lalr')
env: Dict[str, Expr] = {}

def normalize_expr(expr: Expr) -> str:
    with tempfile.NamedTemporaryFile('w') as f:
        print(expr, file=f, flush=True)
        try: 
            return subprocess.check_output([DIR / 'ski-normalizer', f.name], text=True, stderr=subprocess.DEVNULL).strip()
        except subprocess.CalledProcessError as e:
            if e.returncode == 1:
                return f'SKI expression is not fully evaluated: {expr}'
            elif e.returncode == 2:
                return f'SKI expression was exceeded execution num steps limit: {expr}'
            else:
                return f'Internal error. Please contact a TA if you hit this.'
                

def ski_to_prog(fname, execute: bool, normalize: bool):
    if fname is None: return

    # read ski file.
    try:
        text = Path(fname).read_text()
    except Exception as err:
        print(">>>>> Error occurs when reading SKI file: '{}' <<<<<\n".format(fname))
        print(err); exit(0)

    # parse ski file.
    try:
        tree = ski_parser.parse(text)
        # print(tree.pretty())
    except Exception as err:
        print(">>>>> Syntax error occurs when parsing SKI file: '{}' <<<<<\n".format(fname))
        print(err); exit(0)

    # convert `tree` to `prog`.
    prog = ski_prog.TreeToProg().transform(tree)

    # load defn block.
    if True:
        for defn in prog.defns:
            (s, e) = (defn.s, defn.e)
            e_subst = ski_prog.subst(e, env)
            env[s]  = e_subst

    # evaluate expr block.
    if execute:
        for e in prog.es:
            e_subst = ski_prog.subst(e, env)
            e_eval  = ski_eval_eval(e_subst)
            assert check_ast_is_wellformed(e_eval), f'Invalid evaluation result {e_eval}'
            if normalize:
                e_eval = normalize_expr(e_eval)
            print(e_eval)

if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("input", type=str, help="main ski file.")
    p.add_argument("-i", "--include", type=str, help="aux ski file to be imported before `input`.")
    p.add_argument("--normalize", action='store_true', help="Normalize SKI expression by fully evaluating it")
    args = p.parse_args()

    ski_to_prog(fname=args.include, execute=False, normalize=args.normalize)
    ski_to_prog(fname=args.input, execute=True, normalize=args.normalize)
