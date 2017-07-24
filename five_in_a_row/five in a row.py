import random, copy, re


# 五子棋评分表
# 参照：http://blog.csdn.net/chaiwenjun000/article/details/50751792
# 第一排为没有棋子的得分
# 第二排为1~4个自己棋子的得分
# 第三排为1~4个对方棋子的得分
# 第四排为黑白都有情况的得分
score_table = (7,
               35, 800, 15000, 800000,
               15, 400, 1800, 100000,
               0, 0)

class Piece:  # 棋子
    def __init__(self, row, col, side):
        self.row = row
        self.col = col
        self.side = side  # 先手是1， 后手是2


class Chessboard:  # 棋盘
    def __init__(self, row_size: int=15, col_size: int=15, steps: int=0, board=None, possible_next_blocks: set=set()):
        self.row_size = row_size
        self.col_size = col_size
        self.total_size = row_size * col_size
        self.steps = steps  # 已走步数
        self.board = [[0 for y in range(col_size)] for x in range(row_size)] if board is None else board
        # self.exist_blocks = [(x, y) for x in range(row_size) for y in range(col_size)]
        self.possible_next_blocks = possible_next_blocks  # 下一步可能走的格子，只选择已存在的点周围3*3格子内的点

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

    def choose_next_step(self, side):
        # 使用五子棋评分算法
        possible_blocks_score = self.evaluate_score(side)
        return (possible_blocks_score[0][0], possible_blocks_score[0][1])
        # 采用在possible_next_blocks中的随机找一个的算法
        # return random.choice(list(self.possible_next_blocks))

    # 专门用来扩展时选取几个可能的下一步用的
    def choose_some_next_step(self, count, side):
        # 使用五子棋评分算法
        possible_blocks_score = self.evaluate_score(side)
        return [(possible_blocks_score[i][0], possible_blocks_score[i][1]) for i in range(count)]
        # 不再采用随机生成的方法
        # return random.sample(self.possible_next_blocks, count)

    # 用五子棋评分表算法算出当前可能最好的下棋位置
    def evaluate_score(self, side):
        possible_blocks_score = []
        for block in self.possible_next_blocks:
            block_row = block[0]
            block_col = block[1]
            current_score = 0
            for offset in range(5):
                row_piece_count = 0  # 计算黑白子的个数。同side + 10， 非同side + 1， 空 + 0。
                col_piece_count = 0  # 竖着的
                left_top_piece_count = 0  # 左上-右下
                right_top_piece_count = 0  # 右上-左下
                for i in range(5):
                    temp_row = block_row - offset + i
                    temp_col = block_col - offset + i
                    temp_col2 = block_col + offset - i
                    row_piece_count += 0 if (temp_col < 0 or temp_col > self.col_size - 1 or self.board[block_row][temp_col] == 0) else 10 if self.board[block_row][temp_col] == side else 1
                    col_piece_count += 0 if (temp_row < 0 or temp_row > self.row_size - 1 or self.board[temp_row][block_col] == 0) else 10 if self.board[temp_row][block_col] == side else 1
                    left_top_piece_count += 0 if (temp_row < 0 or temp_row > self.row_size - 1 or temp_col < 0 or temp_col > self.col_size - 1 or self.board[temp_row][temp_col] == 0) else 10 if self.board[temp_row][temp_col] == side else 1
                    right_top_piece_count += 0 if (temp_row < 0 or temp_row > self.row_size - 1 or temp_col2 < 0 or temp_col2 > self.col_size - 1 or self.board[temp_row][temp_col2] == 0) else 10 if self.board[temp_row][temp_col2] == side else 1
                row_score_index = 9 if (row_piece_count % 10 != 0 and row_piece_count // 10 != 0) else row_piece_count + 4 if row_piece_count % 10 != 0 else row_piece_count // 10
                current_score += score_table[row_score_index]
                col_score_index = 9 if (col_piece_count % 10 != 0 and col_piece_count // 10 != 0) else col_piece_count + 4 if col_piece_count % 10 != 0 else col_piece_count // 10
                current_score += score_table[col_score_index]
                left_top_score_index = 9 if (left_top_piece_count % 10 != 0 and left_top_piece_count // 10 != 0) else left_top_piece_count + 4 if left_top_piece_count % 10 != 0 else left_top_piece_count // 10
                current_score += score_table[left_top_score_index]
                right_top_score_index = 9 if (right_top_piece_count % 10 != 0 and right_top_piece_count // 10 != 0) else right_top_piece_count + 4 if right_top_piece_count % 10 != 0 else right_top_piece_count // 10
                current_score += score_table[right_top_score_index]
            possible_blocks_score.append((block_row, block_col, current_score))
        possible_blocks_score.sort(key=lambda x: x[2], reverse=True)
        return possible_blocks_score




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
            next_step = self.choose_next_step(side)
            current_piece = Piece(next_step[0], next_step[1], side)
            self.go_a_step(current_piece)
            if self.is_win(current_piece):
                return side
            side = int(3 - side)
        return 0  # 平了

    def print_board(self):
        print(end='   ')
        for i in range(self.col_size):
            print(i + 1, end=' ' if i + 1 < 10 else '')
        print()
        for i in range(self.row_size):
            print(i + 1, end='  ' if i + 1 < 10 else ' ')
            for j in range(self.col_size):
                print('.' if self.board[i][j] == 0 else 'X' if self.board[i][j] == 1 else 'O', end=' ')
            print()
        print()


class TreeNode:  # 树的结点
    def __init__(self, chessboard: Chessboard=None):
        self.win_times = 0
        self.test_times = 0
        self.winning_percentage = 0
        self.chessboard = chessboard
        self.piece = None  # 记录当前的结点是哪一步走过来的
        self.child_nodes = []

    def modify_result_node(self, breadth: int, depth: int, simulation_times: int, is_bot: bool):
        remaining_simulation_times = (breadth ** depth) * simulation_times  # 若在扩展的过程中发现已经胜利，那么该点的胜利次数和测试次数计算公式如代码中所示
        self.win_times += remaining_simulation_times if is_bot else 0
        self.test_times += remaining_simulation_times


class Tree:  # 树
    def __init__(self, chessboard: Chessboard, breadth: int=6, depth: int=3, bot_side: int=2, simulation_times: int=1):
        self.root = TreeNode(chessboard)
        self.breadth = breadth
        self.depth = depth
        self.create_tree(self.root, self.depth, bot_side, simulation_times)

    # 建树可理解为扩展的过程 Expansion
    def create_tree(self, root: TreeNode, depth: int, bot_side: int=2, simulation_times: int=1):
        if depth == 0:  # 实现多次模拟
            for i in range(simulation_times):
                temp_chessboard = Chessboard(steps=root.chessboard.steps, board=[[x for x in y] for y in root.chessboard.board], possible_next_blocks=root.chessboard.possible_next_blocks.copy())
                win_side = temp_chessboard.simulation_to_end(bot_side)
                root.win_times += 1 if bot_side == win_side else 0
                root.test_times += 1 if win_side != 0 else 0
            return root

        some_possible_next_blocks = root.chessboard.choose_some_next_step(min(self.breadth, len(root.chessboard.possible_next_blocks)), bot_side) # 扩展时可供bot选择的下一步棋的位置
        for i in range(min(self.breadth, len(root.chessboard.possible_next_blocks))):
            temp_chessboard = Chessboard(steps=root.chessboard.steps,
                                         board=[[x for x in y] for y in root.chessboard.board],
                                         possible_next_blocks=root.chessboard.possible_next_blocks.copy())
            next_step = some_possible_next_blocks[i]  # 选择下一步棋的位置
            bot_piece = Piece(next_step[0], next_step[1], bot_side)
            temp_chessboard.go_a_step(bot_piece)
            if temp_chessboard.is_win(bot_piece):
                new_root = TreeNode()
                new_root.modify_result_node(min(self.breadth, len(temp_chessboard.possible_next_blocks)), depth - 1, simulation_times, True)  # 当前depth - 1是当前结点的子结点的深度
                new_root.piece = bot_piece
                root.child_nodes.append(new_root)
                continue
            player_next_step = temp_chessboard.choose_next_step(int(3 - bot_side))
            player_piece = Piece(player_next_step[0], player_next_step[1], int(3 - bot_side))
            temp_chessboard.go_a_step(player_piece)  # side只分为1, 2因此非bot就是3 - bot_side
            if temp_chessboard.is_win(player_piece):
                new_root = TreeNode()
                new_root.modify_result_node(min(self.breadth, len(temp_chessboard.possible_next_blocks)), depth - 1, simulation_times, False)
                new_root.piece = bot_piece
                root.child_nodes.append(new_root)
                continue
            new_root = self.create_tree(TreeNode(temp_chessboard), depth - 1, bot_side, simulation_times)
            new_root.piece = bot_piece
            new_root.chessboard = None  # 不保留chessboard，节省内存
            root.child_nodes.append(new_root)
        return root

    # 反馈过程 Back-Propagation
    def back_propagation(self, root: TreeNode):
        if root is None:
            return 0, 0
        for child_node in root.child_nodes:
            child_win_times, child_test_times = self.back_propagation(child_node)
            root.win_times += child_win_times
            root.test_times += child_test_times
        return root.win_times, root.test_times

    # 选择过程 Selection
    def selection(self):
        # 对于更复杂的情况，以后可能要多次选择
        # TODO
        selected_node = None
        max_winning_percentage = -1
        for child_node in self.root.child_nodes:
            child_node.winning_percentage = child_node.win_times / child_node.test_times
            if child_node.winning_percentage > max_winning_percentage:
                selected_node = child_node
                max_winning_percentage = child_node.winning_percentage
        return selected_node

    # 后序遍历，测试用
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
    player_side = 0
    bot_side = 0
    while(1):  # 输入选择先手后手
        try:
            player_side = int(input('Choose your side. 1 means offensive position， 2 means defensive position\n'))
        except ValueError as e:
            print('Input a integer please!')
        else:
            if player_side != 1 and player_side != 2:
                print('Input 1 or 2 please!')
            else:
                bot_side = int(3 - player_side)
                break
    if player_side == 1:
        print('Please input your step, format like:1 2')
    if player_side == 2:
        chessboard.go_a_step(Piece(7, 7, 1))
        print('bot_step:', 8, 8)
        chessboard.print_board()
    while 1:  # 下棋过程
        while 1:  # 输入下棋位置
            player_input = input()
            match_group = re.match('^(\d+)[\s,;.]+(\d+).*$', player_input)  # 用正则表达式匹配的方法使输入可读的概率更高
            try:
                player_step = (int(match_group.group(1)), int(match_group.group(2)))
            except AttributeError as e:
                print('Illegal input!')
            else:
                player_piece = Piece(player_step[0] - 1, player_step[1] - 1, player_side)  # 数组从0开始，玩家输入习惯从1开始
                go_a_step_success = chessboard.go_a_step(player_piece)
                if go_a_step_success is True:
                    break
        chessboard.print_board()
        if chessboard.is_win(player_piece) is True:
            print('You Win!')
            break
        if chessboard.steps == chessboard.total_size:
            print('Draw!')
            break
        print('the bot is considering...')
        mcts_tree = Tree(chessboard=chessboard, bot_side=bot_side)
        mcts_tree.back_propagation(mcts_tree.root)
        selected_node = mcts_tree.selection()
        if selected_node is None:
            print('Error!')
            return
        bot_piece = selected_node.piece
        if bot_piece is None:
            print('Error2!')
            return
        chessboard.go_a_step(bot_piece)
        print('bot_step:', bot_piece.row + 1, bot_piece.col + 1)
        chessboard.print_board()
        if chessboard.is_win(bot_piece) is True:
            print('You Lose!')
            break
        if chessboard.steps == chessboard.total_size:
            print('Draw!')
            break


main()
