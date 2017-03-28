import random

# TODO 开放的穴位接口类，便于以后修改
class Acupoint:
    def __init__(self, name: str=None, score: float=0):
        self.name = name    # 穴位的名称，以后可能有所更改
        self.score = score  # 穴位的价值，以后可能有所更改

# 穴位汇总
class Body:
    def __init__(self, points: set=set(), size: int=20, choose_size: int=10, selected_size: int=0, selected_point: list=None):
        self.points = points  # 剩下没有用过的穴位
        self.size = size    # 总穴位数
        self.choose_size = choose_size  # 需要选择的总数
        self.selected_size = selected_size
        self.selected_point = selected_point if selected_point is not None else []  # 被选择的穴位(有先后顺序的)
        if len(self.points)  == 0:
            self.init_point()

    # 可能会根据穴位的要求有所修改
    def init_point(self):
        for i in range(self.size):
            self.points.add(Acupoint(str(i), float(i)))

    # TODO 选择一个穴位
    def choose_a_point(self):
        # 随机选择一个
        return random.choice(list(self.points))

    # TODO 选择一些穴位
    def choose_some_points(self, count: int):
        # 随机选择一些
        return random.sample(self.points, count)

    # 走一步
    def go_a_step(self, acupoint: Acupoint):
        self.selected_point.append(acupoint)
        self.selected_size += 1
        self.points.remove(acupoint)

    # TODO 评分函数
    def evaluate_score(self):
        return sum([acupoint.score for acupoint in self.selected_point])

    # 模拟至结束(simulation)
    def simulation_to_finish(self):
        while(self.selected_size < self.choose_size):
            next_point = self.choose_a_point()
            self.go_a_step(next_point)
        return self.evaluate_score()


class TreeNode:  # 树的结点
    def __init__(self, body: Body=None):
        self.body = body
        self.sum_score = 0
        self.test_times = 0
        self.average_score = 0
        self.child_nodes = []


class Tree:  # 树
    def __init__(self, body: Body, breadth: int=6, depth: int=3, simulation_times: int=1):
        self.root = TreeNode(body)
        self.breadth = breadth
        self.depth = depth
        self.create_tree(self.root, self.depth, simulation_times)

    # 建树可理解为扩展的过程 Expansion
    def create_tree(self, root: TreeNode, depth: int, bot_side: int=2, simulation_times: int=1):
        if depth == 0:  # 实现多次模拟
            for i in range(simulation_times):
                temp_body = Body(points=root.body.points, size=root.body.size, choose_size=root.body.choose_size, selected_size=root.body.selected_size, selected_point=root.body.selected_point)
                final_score = temp_body.simulation_to_finish()
                root.sum_score += final_score
                root.test_times += 1
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