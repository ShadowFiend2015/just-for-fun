#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <sstream>
#include <iomanip>
#include<set>

using namespace std;

int models_array[12][5][2] =
{
    {{0, 0}, {0, 1}, {0, 2}, {1, 2}, {1, 3}},
    {{0, 0}, {0, 1}, {0, 2}, {1, 0}, {1, 1}},
    {{0, 0}, {0, 1}, {0, 2}, {1, 0}, {1, 3}},
    {{0, 0}, {0, 1}, {0, 2}, {1, 0}, {2, 0}},
    {{0, 0}, {0, 1}, {1, 1}, {1, 2}, {2, 1}},
    {{0, 0}, {0, 1}, {1, 1}, {1, 2}, {2, 2}},
    {{0, 0}, {0, 1}, {0, 2}, {0, 3}, {1, 1}},
    {{0, 0}, {0, 1}, {0, 2}, {0, 3}, {1, 0}},
    {{0, 0}, {0, 1}, {1, 1}, {1, 2}},
    {{0, 0}, {0, 1}, {0, 2}, {1, 1}},
    {{0, 0}, {0, 1}, {0, 2}, {1, 0}},
    {{0, 0}, {0, 1}, {1, 0}}
};
string types[8] = {"0&no_reverse", "90&no_reverse", "180&no_reverse", "270&no_reverse",
                   "0&reverse",    "90&reverse",    "180&reverse",    "270&reverse"
                  };

struct Point
{
    int x;
    int y;
};

struct Model
{
    int pos;    // 在数组中的位置，也就是编号
    vector<Point> points;
};

vector<vector<int> > initBoard()
{
    vector<vector<int> > board;
    for (int i = 0; i < 5; i++)
    {
        vector<int> temp(11, 0);
        board.push_back(temp);
    }
    return board;
}

vector<Model> initModels()
{
    vector<Model> models;
    for (int i = 0; i < 8; i++)
    {
        vector<Point> points;
        for (int j = 0; j < 5; j++)
        {
            Point p = {models_array[i][j][0], models_array[i][j][1]};
            points.push_back(p);
        }
        Model m = {i, points};
        models.push_back(m);
    }
    for (int i = 8; i < 11; i++)
    {
        vector<Point> points;
        for (int j = 0; j < 4; j++)
        {
            Point p = {models_array[i][j][0], models_array[i][j][1]};
            points.push_back(p);
        }
        Model m = {i, points};
        models.push_back(m);
    }
    for (int i = 11; i < 12; i++)
    {
        vector<Point> points;
        for (int j = 0; j < 3; j++)
        {
            Point p = {models_array[i][j][0], models_array[i][j][1]};
            points.push_back(p);
        }
        Model m = {i, points};
        models.push_back(m);
    }
    return models;
}

void printBoard(vector<vector<int> > board)
{
    for (int i = 0; i < board.size(); i++)
    {
        for (int j = 0; j < board[i].size(); j++)
        {
            cout << setw(2) << board[i][j] << " ";
        }
        cout << endl;
    }
    cout << endl;
}

void printModel(Model m)
{
    set<int> s;
    for(int i = 0; i < m.points.size(); i++)
    {
        s.insert(m.points[i].x * 100 + m.points[i].y);
    }
    cout << "   ";
    for(int i = -5; i <= 5; i++)    cout << setw(2) << i << " ";
    cout << endl;
    for(int i = -5; i <= 5; i++)
    {
        cout << setw(2) << i << " ";
        for(int j = -5; j <= 5; j++)
        {
            if(s.count(i * 100 + j) == 1) cout << setw(2) << 1 << " ";
            else cout << setw(2) << 0 << " ";
        }
        cout << endl;
    }
    cout << endl;
}

void printUsed(vector<int> used)
{
    for(int i = 0; i < used.size(); i++)
    {
        cout << setw(2) << used[i] << " ";
    }
    cout << endl << endl;
}

Point rotateAndReversePoint(Point target, Point base, int type)
{
    Point res = {target.x - base.x, target.y - base.y};
    int temp_x, temp_y;
    switch (type % 4)
    {
    case 0 :
        break;
    case 1 :
        temp_x = res.x;
        temp_y = res.y;
        res.x = temp_y;
        res.y = -temp_x;
        break;
    case 2 :
        temp_x = res.x;
        temp_y = res.y;
        res.x = -temp_x;
        res.y = -temp_y;
        break;
    case 3 :
        temp_x = res.x;
        temp_y = res.y;
        res.x = -temp_y;
        res.y = temp_x;
        break;
    }
    if(type / 4 == 1)
    {
        res.x = -res.x;
    }
    return res;
}

Model rotateAndReverseModel(Model m, int type, int point_pos)
{
    Point base = m.points[point_pos];
    vector<Point> ps;
    Model res = {m.pos, ps};
    for(int i = 0; i < m.points.size(); i++)
    {
        if(i == point_pos)
        {
            Point zero = {0, 0};
            res.points.push_back(zero);
            continue;
        }
        res.points.push_back(rotateAndReversePoint(m.points[i], base, type));
    }
    return res;
}

int checkUsed(vector<int> used)
{
    int total = 0;
    for(int i = 0; i < used.size(); i++)
    {
        total += used[i];
    }
    return total == 12;
}

// 确定该点为"角"，corner
// 查看(x, y)上下左右4个点哪几个被占用。0 - 2/3个点被占用，可以使用。1 - 0/1/2个不相连的点被占用，不可使用。2 - 4个点都被占用，递归中应直接返回。
int checkPoint(vector<vector<int> > board, int x, int y)
{
    // up - 1000, down - 100, left - 10, right - 1
    int in_used = 0, pos = 0;
    if(x == 0 || board[x-1][y] != 0)
    {
        pos += 1000;
        in_used++;
    }
    if(x == board.size() - 1 || board[x+1][y] != 0)
    {
        pos += 100;
        in_used++;
    }
    if(y == 0 || board[x][y-1] != 0)
    {
        pos += 10;
        in_used++;
    }
    if(y == board[0].size() - 1 || board[x][y+1] != 0)
    {
        pos += 1;
        in_used++;
    }
    if(in_used == 0 || in_used == 1) return 1;
    if(in_used == 3) return 0;
    if(in_used == 4) return 2;
    if(pos == 1100 || pos == 11) return 1;
    return 0;
}

// 0 - can use, 1 - can't use
int checkModelInBoard(vector<vector<int> > board, Point p, Model m)
{
    for(int i = 0; i < m.points.size(); i++)
    {
        Point temp = {p.x + m.points[i].x, p.y + m.points[i].y};
        if(temp.x < 0 || temp.x > board.size() || temp.y < 0 || temp.y > board[0].size() || board[temp.x][temp.y] != 0) return 1;
    }
    return 0;
}

vector<vector<int> > genModelInBoard(vector<vector<int> > board, Point p, Model m)
{
    for(int i = 0; i < m.points.size(); i++)
    {
        Point temp = {p.x + m.points[i].x, p.y + m.points[i].y};
        board[temp.x][temp.y] = m.pos;
    }
    return board;
}

vector<int> genUsedModels(vector<int> used, int pos)
{
    used[pos] = 1;
    return used;
}

void traverseBoard(const vector<Model>& models, vector<int> used, vector<vector<int> > board)
{
    if(checkUsed(used))
    {
        printBoard(board);
        return;
    }
    Point cur_board;
    for(int i = 0; i < board.size(); i++)
    {
        for(int j = 0; j < board[i].size(); j++)
        {
            if(board[i][j] != 0) continue;
            int flag = checkPoint(board, i, j);
            if(flag == 1) continue;
            if(flag == 2) return;
            cur_board = {i, j};
            break;
        }
    }
    for(int i = 0; i < used.size(); i++)
    {
        if(used[i] != 0) continue;
        Model m = models[i];
        for(int j = 0; j < m.points.size(); j++)
        {
            Point cur_model = m.points[j];
            for(int t = 0; t < 8; t++)
            {
                Model temp = rotateAndReverseModel(m, t, j);
                if(checkModelInBoard(board, cur_board, temp) == 0)
                {
                    traverseBoard(models, genUsedModels(used, i), genModelInBoard(board, cur_board, temp));
                }
            }
        }
    }
}

vector<string> split(string str) {
    vector<string> res;
    stringstream s(str);
    string word;
    while(s >> word)
        res.push_back(word);
    return res;
}

vector<vector<int> > initBoardFromFile(string filepath)
{
    fstream     f(filepath);
    vector<string>  items;
    string      line;
    vector<vector<int> > board;
    while(getline(f, line))
    {
        items = split(line);
        if(items.size() != 11)  continue;
        vector<int> temp;
        for(int i = 0; i < items.size(); i++)
        {
            temp.push_back(atoi(items[i].c_str()));
        }
        board.push_back(temp);
    }
    return board;
}

vector<int> initUsedFromFile(string filepath)
{
    fstream     f(filepath);
    vector<string>  items;
    string      line;
    vector<int> used;
    while(getline(f, line))
    {
        items = split(line);
        if(items.size() != 12)  continue;
        for(int i = 0; i < items.size(); i++)
        {
            used.push_back(atoi(items[i].c_str()));
        }
    }
    return used;
}

int main()
{
    string board_filepath = "D:\\board.txt";
    string used_filepath = "D:\\used.txt";
    vector<Model> models = initModels();
    vector<vector<int> > board = initBoardFromFile(board_filepath);
    vector<int> used = initUsedFromFile(used_filepath);
    printBoard(board);
    printUsed(used);
    traverseBoard(models, used, board);
    return 0;
}
