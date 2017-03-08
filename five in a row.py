

class Piece:  # 棋子
    def __init__(self, row, col, side):
        self.row = row
        self.col = col
        self.side = side


class Chessboard:  # 棋盘
    def __init__(self, row_size: int=15, col_size: int=15):
        self.row_size = row_size
        self.col_size = col_size
        self.total_size = row_size * col_size
        self.steps = 0  # 已走步数
        self.board = [[0 for y in range(col_size)] for x in range(row_size)]
        self.exist_blocks = [(x, y) for x in range(row_size) for y in range(col_size)]

    def go_a_step(self, piece: Piece):
        if (piece.row < 0 or piece.row > self.row_size - 1 or piece.col < 0 or piece.col > self.col_size - 1 or self.board[piece.row][piece.col] != 0):
            print('the block you put is illegal!')
            return False
        else:
            self.board[piece.row][piece.col] = piece.side
            self.steps += 1
            return True

    def is_win(self, piece: Piece):
        count = 1  # count of column to 5 竖5
        for i in range(1, 5):
            if piece.row - i < 0 or self.board[piece.row - i][piece.col] != piece.side:
                break
            else:
                count += 1
        if count >= 5:
            return True
        for i in range(1, 5):
            if piece.row + i > self.row_size - 1 or self.board[piece.row + i][piece.col] != piece.side:
                break
            else:
                count += 1
        if count >= 5:
            return True
        count = 1  # count of row to 5 横5
        for i in range(1, 5):
            if piece.col - i < 0 or self.board[piece.row][piece.col - i] != piece.side:
                break
            else:
                count += 1
        if count >= 5:
            return True
        for i in range(1, 5):
            if piece.col + i > self.col_size - 1 or self.board[piece.row][piece.col + i] != piece.side:
                break
            else:
                count += 1
        if count >= 5:
            return True
        count = 1  # count of left top to right bottom to 5  左上-右下5
        for i in range(1, 5):
            if piece.row - i < 0 or piece.col - i < 0 or self.board[piece.row - i][piece.col - i] != piece.side:
                break
            else:
                count += 1
        if count >= 5:
            return True
        for i in range(1, 5):
            if piece.row + i > self.row_size - 1 or piece.col + i > self.col_size - 1 or self.board[piece.row + i][piece.col + i] != piece.side:
                break
            else:
                count += 1
        if count >= 5:
            return True
        count = 1  # count of left bottom to right top to 5  左下-右上5
        for i in range(1, 5):
            if piece.row + i > self.row_size - 1 or piece.col - i < 0 or self.board[piece.row + i][piece.col - i] != piece.side:
                break
            else:
                count += 1
        if count >= 5:
            return True
        for i in range(1, 5):
            if piece.row - i < 0 or piece.col + i > self.col_size - 1 or self.board[piece.row - i][piece.col + i] != piece.side:
                break
            else:
                count += 1
        if count >= 5:
            return True
        return False


class TreeNode:  # 树的结点
    def __init__(self):
        self.win_times = 0
        self.test_times = 0
        self.winning_percentage = 0
        self.child_nodes = []


class Tree:  # 树
    def __init__(self, breadth: int, depth: int):
        self.root = TreeNode()
        self.breadth = breadth
        self.depth = depth
        self.create_tree(self.root, self.depth)

    def create_tree(self, root: TreeNode, depth: int):
        if depth == 0:
            return
        for i in range(self.breadth):
            new_root = self.create_tree(TreeNode(), depth - 1)
            root.child_nodes.append(new_root)
        return root

    def post_order_traversal(self, root: TreeNode):
        global total
        if root is None:
            return
        total += 1
        for child_node in root.child_nodes:
            self.post_order_traversal(child_node)
        print(root.win_times, total)


total = 0


tree = Tree(3, 5)
tree.post_order_traversal(tree.root)