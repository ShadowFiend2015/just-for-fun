#include <iostream>
#include <vector>
#include <fstream>
#include <string>
#include <sstream>
#include <iomanip>

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
                   "0&reverse",    "90&reverse",    "180&reverse",    "270&reverse"}

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
}

Point rotateAndReversePoint(Point target, Point base, int type)
{
}

Model rotateAndReverseModel(Model m, int type, int point_pos)
{
    Point p = m.points[point_pos];

}

int main()
{
    vector<vector<int> > board = initBoard();
    vector<Model> models = initModels();
    printBoard(board);
    return 0;
}
