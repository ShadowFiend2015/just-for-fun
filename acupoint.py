import random, re


# TODO 开放的穴位接口类，便于以后修改
class Acupoint:
    def __init__(self, name: str=None, score: float=0):
        self.name = name    # 穴位的名称，以后可能有所更改
        self.score = score  # 穴位的价值，以后可能有所更改

# 穴位汇总
class Body:
    def __init__(self, points: set=set(), size: int=20, choose_size: int=10, selected_size: int=0, selected_point: list=list()):
        self.points = points  # 剩下没有用过的穴位
        self.size = size    # 总穴位数
        self.choose_size = choose_size  # 需要选择的总数
        self.selected_size = selected_size
        self.selected_point = selected_point  # 被选择的穴位(有先后顺序的)
        if bool(self.points) is False:
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
        self.acupoint = None
        self.child_nodes = []

    def modify_result_node(self, breadth: int, depth: int, simulation_times: int, current_score: float):
        remaining_simulation_times = (breadth ** depth) * simulation_times  # 若在扩展的过程中发现已经胜利，那么该点的胜利次数和测试次数计算公式如代码中所示
        self.sum_score += remaining_simulation_times * current_score
        self.test_times += remaining_simulation_times


class Tree:  # 树
    def __init__(self, body: Body, breadth: int=6, depth: int=3, simulation_times: int=1):
        self.root = TreeNode(body)
        self.breadth = breadth
        self.depth = depth
        self.create_tree(self.root, self.depth, simulation_times)

    # 建树可理解为扩展的过程 Expansion
    def create_tree(self, root: TreeNode, depth: int, simulation_times: int=1, judge_score: float=1):   # judge_score: 判定分数，低于这个分数则直接放弃。以后可能会有修改
        if depth == 0:  # 实现多次模拟
            for i in range(simulation_times):
                temp_body = Body(points=root.body.points, size=root.body.size, choose_size=root.body.choose_size, selected_size=root.body.selected_size, selected_point=root.body.selected_point)
                final_score = temp_body.simulation_to_finish()
                root.sum_score += final_score
                root.test_times += 1
            return root

        some_possible_next_points = root.body.choose_some_points(min(self.breadth, len(root.body.points))) # 扩展时可供针灸选择的下一个穴位的位置
        for i in range(min(self.breadth, len(root.body.points))):
            temp_body = Body(points=root.body.points.copy(), size=root.body.size, choose_size=root.body.choose_size,
                             selected_size=root.body.selected_size, selected_point=root.body.selected_point.copy())
            next_point = some_possible_next_points[i]  # 选择下一上穴位的位置
            temp_body.go_a_step(next_point)
            current_score = temp_body.evaluate_score()
            if current_score < judge_score:  # 剪枝的判定条件，以后可能会有修改
                new_root = TreeNode()
                new_root.modify_result_node(min(self.breadth, len(temp_body.points)), depth - 1, simulation_times, current_score)  # 当前depth - 1是当前结点的子结点的深度
                new_root.acupoint = next_point
                root.child_nodes.append(new_root)
                continue
            new_root = self.create_tree(TreeNode(temp_body), depth - 1, simulation_times, judge_score)
            new_root.acupoint = next_point
            new_root.body = None  # 不保留body，节省内存
            root.child_nodes.append(new_root)
        return root


    # 反馈过程 Back-Propagation
    def back_propagation(self, root: TreeNode):
        if root is None:
            return 0, 0
        for child_node in root.child_nodes:
            child_sum_score, child_test_times = self.back_propagation(child_node)
            root.sum_score += child_sum_score
            root.test_times += child_test_times
        return root.sum_score, root.test_times

    # 选择过程 Selection
    def selection(self):
        # 对于更复杂的情况，以后可能要多次选择
        # TODO
        selected_node = None
        max_average_score = 0
        for child_node in self.root.child_nodes:
            child_node.average_score = child_node.sum_score / child_node.test_times
            if child_node.average_score > max_average_score:
                selected_node = child_node
                max_average_score = child_node.average_score
        return selected_node

    # 后序遍历，测试用
    def post_order_traversal(self, root: TreeNode):
        global total
        if root is None:
            return
        for child_node in root.child_nodes:
            self.post_order_traversal(child_node)
        total += 1
        print(root.sum_score, total)


total = 0

def main():
    acupoint_size = 0
    choose_size = 0
    while 1:  # 输入总穴位数和需要的穴位数
        print('Please input the total size and the size you need, format like:1 2')
        player_input = input()
        match_group = re.match('^(\d+)[\s,;.]+(\d+).*$', player_input)  # 用正则表达式匹配的方法使输入可读的概率更高
        try:
            acupoint_size = int(match_group.group(1))
            choose_size = int(match_group.group(2))
        except AttributeError as e:
            print('Illegal input!')
        else:
            if choose_size > acupoint_size:
                print('the first number can not be little than the second number!')
                continue
            break
    body = Body(size=acupoint_size, choose_size=choose_size)
    for i in range(choose_size):
        mcts_tree = Tree(body)
        mcts_tree.back_propagation(mcts_tree.root)
        selected_node = mcts_tree.selection()
        if selected_node is None:
            print('Error!')
            return
        next_point = selected_node.acupoint
        if next_point is None:
            print('Error2!')
            return
        body.go_a_step(next_point)
    print(body.selected_point)


main()
