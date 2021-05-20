# coding: utf-8
# 2021/5/20 @ tongshiwei
import networkx as nx
from EduNLP.Formula import Formula


# def inorder_traversal(ast: nx.DiGraph):
#     visit = set()
#     nodes = []
#
#     def _inorder_traversal(_node):
#         if _node in visit:
#             return
#         successors = list(ast.successors(_node))
#         if successors:
#             if len(successors) <= 2:
#                 _inorder_traversal(successors[0])
#                 nodes.append(_node)
#                 visit.add(_node)
#                 if len(successors) == 2:
#                     _inorder_traversal(successors[1])
#             else:
#                 nodes.append(_node)
#                 for successor in successors:
#                     if successor in visit:
#                         continue
#                     _inorder_traversal(successor)
#         else:
#             nodes.append(_node)
#
#     for node in ast.nodes:
#         if node in visit or list(ast.predecessors(node)):
#             continue
#         _inorder_traversal(node)
#     return nodes

def traversal_formula(ast, ord2token=False, var_numbering=False, *args, **kwargs):
    tokens = []
    for i in nx.dfs_postorder_nodes(ast):
        node = ast.nodes[i]
        if ord2token is True and node["type"] in ["mathord", "textord"]:
            if var_numbering is True and node["type"] == "mathord":
                tokens.append("%s_%s" % (node["type"], node.get("var", "con")))
            else:
                tokens.append(node["type"])
        else:
            tokens.append(node["text"])
    return tokens


def ast_tokenize(formula, ord2token=False, var_numbering=False, return_type="formula", *args, **kwargs):
    """

    Parameters
    ----------
    formula
    ord2token
    var_numbering
    return_type
    args
    kwargs

    Returns
    -------

    Examples
    --------
    >>> ast_tokenize(r"{x + y}^\\frac{\\pi}{2} + 1 = x", return_type="list")
    ['x', '+', 'y', '{ }', '\\\\pi', '{ }', '2', '{ }', '\\\\frac', '^', '+', '1', '=', 'x']
    >>> ast_tokenize(r"{x + y}^\\frac{\\pi}{2} + 1 = x", return_type="list", ord2token=True)
    ['mathord', '+', 'mathord', '{ }', 'mathord', '{ }', 'textord', '{ }', '\\\\frac', '^', '+', 'textord', \
'=', 'mathord']
    >>> ast_tokenize(r"{x + y}^\\frac{\\pi}{2} + 1 = x", return_type="list", ord2token=True, var_numbering=True)
    ['mathord_0', '+', 'mathord_1', '{ }', 'mathord_con', '{ }', 'textord', '{ }', '\\\\frac', '^', '+', 'textord', \
'=', 'mathord_0']
    >>> len(ast_tokenize(r"{x + y}^\\frac{\\pi}{2} + 1 = x", return_type="ast").nodes)
    14
    >>> ast_tokenize(r"{x + y}^\\frac{\\pi}{2} + 1 = x")
    <Formula: {x + y}^\\frac{\\pi}{2} + 1 = x>
    """
    if return_type == "list":
        ast = Formula(formula, variable_standardization=True).ast
        return traversal_formula(ast, ord2token=ord2token, var_numbering=var_numbering)
    elif return_type == "formula":
        return Formula(formula)
    elif return_type == "ast":
        return Formula(formula).ast
    else:
        raise ValueError()


if __name__ == '__main__':
    print(ast_tokenize(r"{x + y}^\frac{\pi}{2} + 1 = x", return_type="list", ord2token=True, var_numbering=True))