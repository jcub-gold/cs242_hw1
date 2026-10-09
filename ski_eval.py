import src.ski as ski

##########
# PART 1 #
##########
# TASK: Implement the below function `eval`.

MIN_LINEAGE_LENGTH = {"S": 4, "K": 3, "I":2, }
    
def eval(e: ski.Expr) -> ski.Expr:
    return reduce(e, [])

"""
reduce:
Iterates down the left spine of the expression tree until it reaches the leaf node, performing head reduction.
"""
def reduce(e, lineage):
    lineage.append(e)
    if isinstance(e, ski.Var):
        return lineage[0]
    type = get_type(e)
    if type != "":
        return handle_SKI_leaf(lineage, type)
    return reduce(e.e1, lineage)

"""
handle_SKI_leaf:
Only called assuming the leaf node (lienage[-1]) is an SKI leaf node. Here we perform the SKI
rewrite if there are enough arguments, update the tree, and continue to reduce.
"""
def handle_SKI_leaf(lineage, type):
    if len(lineage) < MIN_LINEAGE_LENGTH[type]:
        return lineage[0]
    e = None
    if type == "S":
        S, x, y, z = lineage.pop(), lineage.pop().e2, lineage.pop().e2, lineage.pop().e2
        e = ski.App(ski.App(x, z), ski.App(y, z))
    if type == "K":
        K, x, y = lineage.pop(), lineage.pop().e2, lineage.pop().e2
        e = x
    if type == "I":
        I, x = lineage.pop(), lineage.pop().e2
        e = x
    if len(lineage) > 0:
        lineage[-1].e1 = e
    return reduce(e, lineage)


def get_type(e):
    if isinstance(e, ski.S):
        return "S"
    if isinstance(e, ski.K):
        return "K"
    if isinstance(e, ski.I):
        return "I"
    return ""

