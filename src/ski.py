from dataclasses import dataclass
from typing import Type, Union

class Expr(object):
    pass

@dataclass(eq=True)
class S(Expr):
    """
    `S()` denotes the S combinator.
    """

    def __repr__(self) -> str:
        return 'S'

@dataclass(eq=True)
class K(Expr):
    """
    `K()` denotes the K combinator.
    """

    def __repr__(self) -> str:
        return 'K'

@dataclass(eq=True)
class I(Expr):
    """
    `I()` denotes the I combinator.
    """

    def __repr__(self) -> str:
        return 'I'

@dataclass(eq=True)
class Var(Expr):
    """
    `Var("x")` denotes the variable x.
    """

    s: str

    def __repr__(self) -> str:
        return str(self.s)

@dataclass(eq=True)
class App(Expr):
    """
    `App(e1,e2)` denotes the application (e1 e2).
    """

    e1: Expr
    e2: Expr

    def __repr__(self) -> str:
        return f'({self.e1} {self.e2})'

def check_ast_is_wellformed(e: Expr) -> bool:
    if not isinstance(e, Expr):
        return False

    if isinstance(e, App):
        return (check_ast_is_wellformed(e.e1) and check_ast_is_wellformed(e.e2))
    elif isinstance(e, Var):
        return isinstance(e.s, str)
    else:
        return isinstance(e, (S, K, I))
