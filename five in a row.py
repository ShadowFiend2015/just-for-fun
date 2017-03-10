import random, copy

class Piece:  # 棋子
    def __init__(self, row, col, side):
        self.row = row
        self.col = col
        self.side = side  # 先手是1， 后手是2


class Chessboard:  # 棋盘
    def __init__(self, row_size: int=15, col_size: int=15):
        self.row_size = row_size
        self.col_size = col_size
        self.total_size = row_size * col_size
        self.steps = 0  # 已走步数
        self.board = [[0 for y in range(col_size)] for x in range(row_size)]
        # self.exist_blocks = [(x, y) for x in range(row_size) for y in range(col_size)]
        self.possible_next_blocks = set()  # 下一步可能走的格子，只选择已存在的点周围3*3格子内的点

    def go_a_step(self, piece: Piece):
        if (piece.row < 0 or piece.row > self.row_size - 1 or piece.col < 0 or piece.col > self.col_size - 1 or self.board[piece.row][piece.col] != 0):
            print('the block you put is illegal!')
            return False
        else:
            self.board[piece.row][piece.col] = piece.side
            self.steps += 1
            # self.exist_blocks.remove((piece.row, piece.col))
            if (piece.row, piece.col) in self.possible_next_blocks:
                self.possible_next_blocks.remove((piece.row, piece.col))
            for i in range(-1, 2):
                for j in range(-1, 2):
                    position_row = piece.row + i
                    position_col = piece.col + j
                    if -1 < position_row < self.row_size and -1 < position_col < self.col_size and self.board[position_row][position_col] == 0:
                        self.possible_next_blocks.add((position_row, position_col))
            return True

    def choose_next_step(self):
        # 现在采用在possible_next_blocks中的随机找一个的算法，有待提高
        # TODO 使用更好的五子棋评分方法
        return random.choice(list(self.possible_next_blocks))

    # 专门用来扩展时选取几个可能的下一步用的
    def choose_some_next_step(self):
        # TODO 修改choose_next_step的同时也要修改这个函数
        return random.sample(self.possible_next_blocks)

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

    # 模拟 simulation
    def simulation_to_end(self, side):
        while self.steps < self.total_size:
            next_step = self.choose_next_step()
            current_piece = Piece(next_step[0], next_step[1], side)
            self.go_a_step(current_piece)
            if self.is_win(current_piece):
                return side
            side = int(3 - side)
        return 0  # 平了



class TreeNode:  # 树的结点
    def __init__(self, chessboard: Chessboard=None):
        self.win_times = 0
        self.test_times = 0
        self.winning_percentage = 0
        self.chessboard = chessboard
        self.child_nodes = []

    def modify_result_node(self, breadth: int, depth: int, simulation_times: int, is_bot: bool):
        remaining_simulation_times = (breadth ** depth) * simulation_times  # 若在扩展的过程中发现已经胜利，那么该点的胜利次数和测试次数计算公式如代码中所示
        self.win_times += remaining_simulation_times if is_bot else 0
        self.test_times += remaining_simulation_times


class Tree:  # 树
    def __init__(self, breadth: int=10, depth: int=5, bot_side: int=2, simulation_times: int=1):
        self.root = TreeNode()
        self.breadth = breadth
        self.depth = depth
        self.create_tree(self.root, self.depth, bot_side, simulation_times, 0)

    # 建树可理解为扩展的过程 Expansion
    def create_tree(self, root: TreeNode, depth: int, bot_side: int=2, simulation_times: int=1, recursion_degree: int=0):
        if depth == 0:
            new_root = TreeNode()
            temp_chessboard = copy.deepcopy(root.chessboard)
            win_side = temp_chessboard.simulation_to_end(bot_side)
            new_root.win_times += 1 if bot_side == win_side else 0
            new_root.test_times += 1 if win_side != 0 else 0
            return new_root

        some_possible_next_blocks = root.chessboard.choose_some_next_step() # 扩展时可供bot选择的下一步棋的位置
        for i in range(min(self.breadth, len(root.chessboard.possible_next_blocks))):
            temp_chessboard = copy.deepcopy(root.chessboard)
            next_step = some_possible_next_blocks[i]  # 选择下一步棋的位置
            bot_piece = Piece(next_step[0], next_step[1], bot_side)
            temp_chessboard.go_a_step(bot_piece)
            if temp_chessboard.is_win(bot_piece):
                new_root = TreeNode()
                new_root.modify_result_node(min(self.breadth, len(temp_chessboard.possible_next_blocks)), depth - 1, simulation_times, True)  # 当前depth - 1是当前结点的子结点的深度
                root.child_nodes.append(new_root)
                continue
            player_next_step = temp_chessboard.choose_next_step()
            player_piece = Piece(player_next_step[0], player_next_step[1], int(3 - bot_side))
            temp_chessboard.go_a_step(player_piece)  # side只分为1, 2因此非bot就是3 - bot_side
            if temp_chessboard.is_win(player_piece):
                new_root = TreeNode()
                new_root.modify_result_node(min(self.breadth, len(temp_chessboard.possible_next_blocks)), depth - 1, simulation_times, False)
                root.child_nodes.append(new_root)
                continue
            new_root = self.create_tree(TreeNode(temp_chessboard), depth - 1, bot_side, simulation_times)
            if recursion_degree != 0:
                new_root.chessboard = None  # 只保留第一层递归的chessboard，不保留其他的chessboard，节省内存
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


def main():
    chessboard = Chessboard()

    # after you've gone a step
    # TODO
