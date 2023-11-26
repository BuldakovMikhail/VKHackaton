from nn_framework.Response import Response


class ANode:
    """
    Реализация узла произвольного дерева
    """

    def __init__(self, val=None, handler=None) -> None:
        self.childs = []
        self.val = val
        self.handler = handler


class AnyNode(ANode):
    def __init__(self):
        super().__init__()


class HandlersContainer:
    def __init__(self):
        self.root = ANode("/")  # root is always empty

    def __insert_seq(self, seq: list[str], handler):  # [abs,bds,<asd>]
        seq_id = 0
        cur_node = self.root

        while seq_id < len(seq):
            is_template = False
            if seq[seq_id].endswith(">") and seq[seq_id].startswith("<"):
                is_template = True

            cur_node_childs_vals = [child.val for child in cur_node.childs]
            
            if seq[seq_id] in cur_node_childs_vals:
                child_ind = cur_node_childs_vals.index(seq[seq_id])
                cur_node = cur_node.childs[child_ind]
            elif len(cur_node.childs) > 0 and isinstance(cur_node.childs[-1], AnyNode) and is_template:
                cur_node = cur_node.childs[-1]
            else:
                if is_template:
                    if (
                        len(cur_node.childs) > 0
                        and not isinstance(cur_node.childs[-1], AnyNode)
                    ) or len(cur_node.childs) == 0:
                        any_node = AnyNode()
                        if seq_id == len(seq) - 1:
                            any_node.handler = handler

                        cur_node.childs.append(any_node)
                        cur_node = cur_node.childs[-1]

                else:
                    val_node = ANode()
                    if seq_id == len(seq) - 1:
                        val_node.handler = handler
                    val_node.val = seq[seq_id]
                    cur_node.childs.insert(0, val_node)
                    cur_node = cur_node.childs[0]

            seq_id += 1

    def __get_handler(self, seq: list[str]):
        seq_id = 0
        cur_node = self.root

        while cur_node.childs and seq_id < len(seq):
            childs_vals = [c.val for c in cur_node.childs]

            if seq[seq_id] in childs_vals:
                child_ind = childs_vals.index(seq[seq_id])
                cur_node = cur_node.childs[child_ind]
                seq_id += 1
            elif isinstance(cur_node.childs[-1], AnyNode):
                cur_node = cur_node.childs[-1]
                seq_id += 1
            else:
                return None

        return cur_node.handler

    def __contains__(self, key: str) -> bool:
        handler = self.__get_handler(key.split("/")[1:])
        return handler is not None

    def add_handler(self, url, func):
        self.__insert_seq(url.split("/")[1:], func)

    def try_call_handler(self, url) -> (bool, Response):
        return self.__get_handler(url.split("/")[1:])