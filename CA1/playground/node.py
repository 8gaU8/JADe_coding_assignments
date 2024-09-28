class TreeMap:
    def __init__(self) -> None:
        self.map: dict[frozenset, Node] = {}

    def register(self, node: "Node") -> None:
        self.map[node.itemset] = node

    def get(self, key: frozenset, default=None) -> "Node | None":
        return self.map.get(key, default)

    def clear(self):
        self.map.clear()

    def __repr__(self) -> str:
        return f"TreeMap({self.map})"


class Node:
    def __init__(self, itemset: frozenset, nb: int, tree_map: TreeMap) -> None:
        self.itemset: frozenset = itemset
        self.nb = nb
        self.parents: list[Node] = []

        self.is_singleton = len(itemset) == 1
        self._parent_pre: Node | None = None
        self._parent_suffix: Node | None = None
        self.children: list[Node] = []
        self.updated = False
        self.support = 0

        self.tree_map = tree_map
        self.tree_map.register(self)

    def calc_support(self) -> int:
        if not self.updated:
            support = self.nb
            for child in self.children:
                support += child.calc_support()
            self.support = support
        self.updated = True
        return self.support

    def _append_parent(self, node: "Node"):
        self.updated = False
        self.parents.append(node)

    def append_child(self, node: "Node"):
        self.updated = False
        self.children.append(node)

    def sort_children(self, counts: dict):
        children = sorted(self.children, key=lambda i: -counts[i])
        self.children = children

    @property
    def parent_pre(self) -> "Node|None":
        return self._parent_pre

    @parent_pre.setter
    def parent_pre(self, node: "Node"):
        self._parent_pre = node
        node.children.append(self)

    @property
    def parent_suffix(self) -> "Node|None":
        return self._parent_suffix

    @parent_suffix.setter
    def parent_suffix(self, node: "Node"):
        self._parent_suffix = node
        node.children.append(self)

    def mktree(self, i=1) -> str:
        msg = f"Node({''.join(list(self.itemset))}, {self.nb})\n"
        # msg = f"Node(items={self.items}, nb={self.nb})\n"
        for child in self.children:
            msg += "  " * i + child.mktree(i + 1)
        return msg

    def __repr__(self) -> str:
        return f"Node({''.join(list(self.itemset))}, {self.nb})"

    def repr_tree(self) -> str:
        return self.mktree().strip()

    def print_tree(self):
        print(self.repr_tree())


TREE_MAP = TreeMap()


def gen_node(itemset: frozenset, nb: int) -> tuple[Node, bool]:
    node = TREE_MAP.get(itemset, None)
    if node is not None:
        return node, True
    return Node(itemset, nb, TREE_MAP), False


# def main():
#     node_top = Node(None, 0)
#     node_d = Node("d", 0)
#     node_a = Node("a", 1)
#     node_b = Node("b", 0)
#     node_c = Node("c", 0)

#     tracts = [
#         frozenset(["c", "d"]),
#         frozenset(["a"]),
#         frozenset(["a", "b", "d"]),
#         frozenset(["b", "d"]),
#         frozenset(["a", "b", "c", "d"]),
#         frozenset(["a", "d"]),
#     ]
#     items = get_sorted_items(tracts)


# if __name__ == "__main__":
#     main()
