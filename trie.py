from UserDict import DictMixin

class Node(object):
    def __init__(self, *args, **kwargs):
        self.value = None
        self.children = {}

class PrefixTrie(DictMixin):
    def __init__(self):
        self._root = Node()

    def longest_prefix(self, key):
        node = self._root
        prefix = []
        valid_index = 0
        last_value = None
        for index, part in enumerate(key):
            n = node.children.get(part)
            if n is None:
                break
            prefix.append(part)
            if node.value != None:
                valid_index = index
                last_value = node.value
            node = n

        if node.value != None:
            return ("".join(prefix), node.value)
        elif last_value != None:
            return ("".join(prefix[0:valid_index]), last_value)
        else:
            raise KeyError

    def __setitem__(self, key, value):
        node = self._root

        for part in key:
            n = node.children.get(part)
            if not n:
                node = node.children.setdefault(part, Node())
            else:
                node = n

        node.value = value

    def __getitem__(self, key):
        node = self._find(key)
        if not node or node.value is None:
            raise KeyError
        return node.value

    def _find(self, key):
        node = self._root
        for part in key:
            node = node.children.get(part)
            if not node:
                break
        return node

    def __delitem__(self, key):
        nodes_parts = []
        append = nodes_parts.append
        node = self._root
        for part in key:
            append((node,part))
            node = node.children.get(part)
            if node is None:
                break
        if node is None or node.value is None:
            raise KeyError
        node.value = None
        pop = nodes_parts.pop
        while node.value is None and not node.children and nodes_parts:
            node,part = pop()
            del node.children[part]
