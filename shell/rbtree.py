import pdb

RB_RED = 0
RB_BLACK = 1

def COLOR(tmp):
    if not tmp:
        return ''
    if tmp.color == RB_RED:
        return 'R'
    if tmp.color == RB_BLACK:
        return 'B'
    return 'U'

class RBNode(object):
    def __init__(self, key):
        self.parent=None
        self.left=None
        self.right=None
        self.color=RB_RED
        self.key=key

    def set_parent_color(self, parent, color):
        self.parent = parent
        self.color = color

    def is_red(self):
        return self.color == RB_RED

    def __str__(self):
        return str(self.key)

class RBTree(object):
    def __init__(self):
        self.root = None

    def cout(self):
        cur = []
        cur.append(self.root)
        while any(cur):
            lvl = []
            for tmp  in cur:
                print tmp, '-', COLOR(tmp), 
                if tmp:
                    lvl.append(tmp.left)
                    lvl.append(tmp.right)
                cur = lvl
            print '.'

    def search(self, key):
        tmp = self.root
        while tmp:
            if tmp.key > key:
                tmp = tmp.left
            elif tmp.key < key:
                tmp = tmp.right
            else:
                return tmp
        return None

    def _left_rotate(self, rbnode):
        riser = rbnode.right
        if not riser:
            return
        rbnode.right = riser.left
        if riser.left:
            riser.left.parent = rbnode
        riser.left = rbnode
        riser.parent = rbnode.parent
        if rbnode.parent:
            if rbnode.parent.left == rbnode:
                rbnode.parent.left = riser
            else:
                rbnode.parent.right = riser
        rbnode.parent = riser

    def _right_rotate(self, rbnode):
        riser = rbnode.left
        if not riser:
            return
        rbnode.left = riser.right
        if riser.right:
            riser.right.parent = rbnode
        riser.right = rbnode
        riser.parent = rbnode.parent
        if rbnode.parent:
            if rbnode.parent.left == rbnode:
                rbnode.parent.left = riser
            else:
                rbnode.parent.right = riser
        rbnode.parent = riser

    def insert(self, key):
        exist = self.search(key)
        if exist:
            return exist
        new_node = RBNode(key)

        tmp = self.root
        papa = tmp
        while tmp:
            papa = tmp
            if tmp.key > key:
                tmp = tmp.left
            else:
                tmp = tmp.right
        new_node.parent = papa
        if not papa:
            self.root = new_node
        elif papa.key > key:
            papa.left = new_node
        else:
            papa.right = new_node

        self.insert_fixup(new_node)
        self.rejust_root()
        self.root.set_parent_color(None, RB_BLACK) #make sure root is black
        return new_node

    def rejust_root(self):
        while self.root.parent:
            self.root = self.root.parent

    def insert_fixup(self, new_node):
        if not new_node.parent:
            return
        if new_node.parent and new_node.parent.color == RB_BLACK:
            return

        node = new_node
        parent = node.parent

        while parent and parent.is_red():
            gparent = parent.parent
            if gparent.left == parent:
                uncle = gparent.right
                if uncle and uncle.is_red():#case 1
                    parent.color = uncle.color = RB_BLACK
                    gparent.color = RB_RED
                    node = gparent
                    parent = node.parent
                else:
                    if parent.right == node: #case 2
                        node = parent
                        self._left_rotate(node)
                        parent = node.parent
                    #case 3
                    parent.color = RB_BLACK
                    gparent.color = RB_RED
                    node = gparent
                    self._right_rotate(node)
                    parent = node.parent
            else: #gparent.right == parent
                uncle = gparent.left
                if uncle and uncle.is_red():#case 1
                    parent.color = uncle.color = RB_BLACK
                    gparent.color = RB_RED
                    node = gparent
                    parent = node.parent
                else:
                    if parent.left == node:#case 2
                        node = parent
                        self._right_rotate(node)
                        parent = node.parent
                    #case 3
                    parent.color = RB_BLACK
                    gparent.color = RB_RED
                    node = gparent
                    self._left_rotate(node)
                    parent = node.parent

    def successor(self, node):
        if node.right:
            successor = node.right
            tmp = successor.left
            while tmp:
                successor = tmp
                tmp = tmp.left
            return successor

        tmp = node
        parent = tmp.parent
        while parent and parent.right == tmp:
            tmp = parent
            parent = parent.parent
        return parent

    def delete(self, key):
        node = self.search(key)
        if not node:
            return None
        if not node.left or not node.right:
            succ = node
        else:
            succ = self.successor(node)
        if succ.left:
            son = succ.left
        else:
            son = succ.right
        if son: #tips:
            son.parent = succ.parent
        if not succ.parent:
            self.root = son
        else:
            if succ == succ.parent.left:
                succ.parent.left = son
            else:
                succ.parent.right = son
        if succ != node:
            node.key = succ.key
        if not succ.is_red():
            self.delete_fixup(son)
        return succ

    def delete_fixup(self, node):
        while node != self.root and not node.is_red():
            if node == node.parent.left:
                brother = node.parent.right
                if brother.is_red():
                    brother.color = RB_BLACK
                    node.parent.color = RB_RED
                    self._left_rotate(node.parent)
                if not brother.left.is_red() and not brother.right.is_red():
                    brother.color = RB_RED
                    node = node.parent
                else:
                    if not brother.right.is_red():
                        brother.left.color = RB_BLACK
                        brother.color = RB_RED
                        self._right_rotate(brother)
                        brother = node.parent.right
                    brother.color = node.parent.color
                    node.parent.color = RB_BLACK
                    brother.right.color = RB_BLACK
                    self._left_rotate(node.parent)
                    node = self.root
            else:
                pass




if __name__ == '__main__':
    rbtree = RBTree()
    #pdb.set_trace()
    rbtree.insert(1)
    rbtree.insert(2)
    rbtree.insert(4)
    rbtree.insert(5)
    rbtree.insert(7)
    rbtree.insert(8)
    rbtree.insert(11)
    rbtree.insert(14)
    rbtree.insert(15)
    rbtree.cout()
    n4 = rbtree.search(4)
    print rbtree.successor(n4)
    n8 = rbtree.search(8)
    print rbtree.successor(n8)
    n15 = rbtree.search(15)
    print rbtree.successor(n15)

