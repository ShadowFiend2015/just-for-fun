#include<stdio.h>
#include<math.h>
#include<algorithm>
#include<iostream>
//#include<windows.h>
#include<time.h>
#include<string.h>
using namespace std;
int result;
int top;
int cot;    // 已经下了多少个棋子了
int first = 0;
int DEG = 10000000;
int n;
int tx, ty;
int ans = 0;
bool w;
int tm[10][9];
bool tf[9];
bool flag;
int tp;
int map[10][9];
int line[8][3] = {
	1, 2, 3,
	4, 5, 6,
	7, 8, 9,
	1, 4, 7,
	2, 5, 8,
	3, 6, 9,
	1, 5, 9,
	3, 5, 7 };
int tem;
int ttem[2][80];
bool fin[9];
int p;
int x, y;
int res = 0;
int print()
{
	system("cls");
	for (int i = 1; i <= 3; i++)
	{
		for (int j = 1; j <= 3; j++)
		{
			for (int k = 1; k <= 3; k++)
			{
				for (int l = 1; l <= 3; l++)
				{
					switch (map[line[i - 1][k - 1]][line[j - 1][l - 1] - 1])
					{
					case 0:
					{
							  cout << ". ";
							  break;
					}
					case 1:
					{
							  cout << "O ";
							  break;
					}
					case 2:
					{
							  cout << "X ";
							  break;
					}
					default: cout << "error";
					}
				}
				cout << "|" << " ";
			}
			cout << endl;
		}
		cout << "-----------------------" << endl;
	}
	return 0;
}
int start()
{
	cot = 0;
	memset(map, 0, sizeof(map));
	memset(fin, 0, sizeof(fin));
	memset(ttem, 0, sizeof(ttem));
	srand((unsigned)time(NULL));
	p = 5;

	cout << "Algorithm : MCTS" << endl;
	cout << endl;

	cout << "----------------------------HELP--------------------------------" << endl;
	cout << "In fact ten is a super Tic-Tac-Toe.It has 9 blocks, each of them has 9 places to play. " << endl;
	cout << "The input should be like a b, which a means block,b means place." << endl;
	cout << "The rule is: you must play in the block that the place which another one plays in points to." << endl;
	cout << "For example, if you play in 9 2, ten must play in the block 2." << endl;
	cout << "If in one block you win,the block is yours. You will play until finish a Tic-Tac-Toe in general" << endl;
	cout << "If the block you should play in has finished,you can play everywhere." << endl;
	system("pause");
	system("cls");
	cout << "type in(0 to play first,1 to play the second): ";
	cin >> first;
	char ff;
	cout << "Would you set degree?(Recommend not)(Y/N): ";
	cin >> ff;
	if (ff == 'Y')
	{
		cout << "Degree:(default:10,000,000) ";
		cin >> DEG;
	}
	print();
	return 0;
}
int is_win(int m, int a, int side)
{
	int cxd = 0;
	int k = 0;
	int l = 0;
	for (int i = 1; i <= 8; i++)
	{
		for (int j = 1; j <= 3; j++)
		{
			if (m == 1)
			{
				if (map[a][line[i - 1][j - 1] - 1] == 1) k++;
				if (map[a][line[i - 1][j - 1] - 1] == 2) l++;
			}
			if (m == 2)
			{
				if (tm[a][line[i - 1][j - 1] - 1] == 1) k++;
				if (tm[a][line[i - 1][j - 1] - 1] == 2) l++;
			}
		}
		if (side == 1)
		{
			if (k >= cxd) cxd = k;
			k = 0;
		}
		else
		{
			if (l >= cxd) cxd = l;
			l = 0;
		}
	}
	return cxd;
}
int mcts(int u, int v)
{
	top = (int)DEG / pow(81 - cot, 2);  // 根据已经下的棋子数来设置循环次数
	int ran = 0;
	int num = 0;
	int ans = 0;
	for (int s = 1; s <= top; s++)
	{
		n = v;
		w = 0;
		tp = u;
		ty = v;
		memcpy(tf, fin, sizeof(fin));
		memcpy(tm, map, sizeof(map));
		tm[tp][v - 1] = 2;
		if (is_win(2, 0, 2) == 3) ans++;
		for (;;)
		{
			if (is_win(2, tp, 2) == 3)
			{
				tm[0][tp - 1] = 2;
				tf[tp - 1] = 1;
			}
			if (is_win(2, 0, 2) == 3)
			{
				ans++;
				break;
			}
			flag = 1;
			for (int i = 1; i <= 9; i++)
			{
				if (tm[tp][i - 1] == 0) flag = 0;
			}
			if (flag) tf[tp - 1] = 1;
			tp = ty;
			if (tf[tp - 1] == 1) tp = 0;
			flag = 1;
			for (int i = 1; i <= 9; i++)
			{
				if (tf[i - 1] == 0) flag = 0;
			}
			if (flag) break;
			num = 0;
			memset(ttem, 0, sizeof(ttem));
			if (tp == 0)
			{
				for (int i = 1; i <= 9; i++)
				{
					for (int j = 1; j <= 9; j++)
					{
						if ((tm[j][i - 1] == 0) && (tf[j - 1] == 0))
						{
							num++;
							ttem[0][num - 1] = j;
							ttem[1][num - 1] = i;
						}
					}
				}
			}
			else
			{
				for (int i = 1; i <= 9; i++)
				{
					if ((tm[tp][i - 1] == 0) && (tf[tp - 1] == 0))
					{
						num++;
						ttem[0][num - 1] = tp;
						ttem[1][num - 1] = i;
					}
				}
			}

			for (int i = 1; i <= num; i++)
			{
				tm[ttem[0][i - 1]][ttem[1][i - 1] - 1] = 1;
				if (is_win(2, ttem[0][i - 1], 1) == 3)
				{
					tm[0][ttem[0][i - 1] - 1] = 1;
					if (is_win(2, 0, 1) == 3) goto aa;
					tm[0][ttem[0][i - 1] - 1] = 0;
				}
				tm[ttem[0][i - 1]][ttem[1][i - 1] - 1] = 0;
			}
			ran = 0;
			ran = (rand() % num) + 1;
			tx = ttem[0][ran - 1];
			ty = ttem[1][ran - 1];
			tm[tx][ty - 1] = 1;
			tp = tx;

			if (is_win(2, tp, 1) == 3)
			{
				tm[0][tp - 1] = 1;
				tf[tp - 1] = 1;
			}
			flag = 1;
			for (int i = 1; i <= 9; i++)
			{
				if (tm[tp][i - 1] == 0) flag = 0;
			}
			if (flag) tf[tp - 1] = 1;
			flag = 1;
			for (int i = 1; i <= 9; i++)
			{
				if (tf[i - 1] == 0) flag = 0;
			}
			if (flag) break;
			tp = ty;
			if (tf[tp - 1] == 1) tp = 0;
			num = 0;
			memset(ttem, 0, sizeof(ttem));
			if (tp == 0)
			{
				for (int i = 1; i <= 9; i++)
				{
					for (int j = 1; j <= 9; j++)
					{
						if ((tm[j][i - 1] == 0) && (tf[j - 1] == 0))
						{
							num++;
							ttem[0][num - 1] = j;
							ttem[1][num - 1] = i;
						}
					}
				}
			}
			else
			{
				for (int i = 1; i <= 9; i++)
				{
					if ((tm[tp][i - 1] == 0) && (tf[tp - 1] == 0))
					{
						num++;
						ttem[0][num - 1] = tp;
						ttem[1][num - 1] = i;
					}
				}
			}

			for (int i = 1; i <= num; i++)
			{
				tm[ttem[0][i - 1]][ttem[1][i - 1] - 1] = 2;
				if (is_win(2, ttem[0][i - 1], 2) == 3)
				{
					tm[0][ttem[0][i - 1] - 1] = 2;
					if (is_win(2, 0, 2) == 3)
					{
						ans++;
						goto aa;
					}
					tm[0][ttem[0][i - 1] - 1] = 0;
				}
				tm[ttem[0][i - 1]][ttem[1][i - 1] - 1] = 0;
			}
			ran = 0;
			ran = (rand() % num) + 1;
			tx = ttem[0][ran - 1];
			ty = ttem[1][ran - 1];
			tm[tx][ty - 1] = 2;
			tp = tx;
		}
	aa:	    if (s % (top / 2) == 0) cout << "=";
	}
	return ans;
}
int main()
{
	start();
	for (;;)
	{
		if (first) goto mc;
	er:		cout << "type in: ";    // 玩家下
		cin >> x >> y;
		cot++;
		if ((x != p) && (p != 0))
		{
			cout << "you should play in the block " << p << endl;
			goto er;
		}
		if (map[x][y - 1] != 0)
		{
			cout << "you cannot play here!" << endl;
			goto er;
		}
		if (p == 0) p = x;
		if (fin[y - 1] == 1) p = 0;
		map[x][y - 1] = 1;
		print();
		if (is_win(1, x, 1) == 3)
		{
			map[0][x - 1] = 1;
			fin[x - 1] = 1;
			for (int q = 1; q <= 9; q++) map[x][q - 1] = 1;
		}
		if (is_win(1, 0, 1) == 3)
		{
			cout << "YOU WIN!!" << endl;
			break;
		}
		flag = 1;
		for (int i = 1; i <= 9; i++)
		{
			if (map[p][i - 1] == 0) flag = 0;
		}
		if (flag) fin[p - 1] = 1;
		p = y;
		if (fin[y - 1] == 1) p = 0;

	mc:    	int max = 0;    // bot用mcts查找该怎么下
		tem = 0;
		first = 0;
		int tt = 0;
		if (p == 0)     // 你下完了以后bot可以在随便一个格子里下(你输入的第2个数字，也就是你所指定的bot下的block已经被占满)
		{
			for (int i = 1; i <= 9; i++)
			{
				for (int j = 1; j <= 9; j++)
				{
					if ((map[i][j - 1] == 0) && (fin[i - 1] == 0))
					{
						tt = mcts(i, j);
						if (max <= tt)
						{
							max = tt;   // ans最多的结果
							tem = i;    // tem是bot应该下的block
							res = j;    // res是bot应该下的block中的第几个
						}
					}
				}
			}
			p = tem;
			goto pl;
		}
		for (int hh = 1; hh <= 9; hh++)     //与上面的if (p == 0)相对，Bot只能在你指定的block里下
		{
			if ((map[p][hh - 1] == 0) && (fin[p - 1] == 0))
			{
				tt = mcts(p, hh);
				if (max <= tt)
				{
					max = tt;
					res = hh;
				}
			}
		}
		result = max;

	pl:   	map[p][res - 1] = 2;//ten play
		cot++;

		if (is_win(1, p, 2) == 3)
		{
			map[0][p - 1] = 2;
			fin[p - 1] = 1;
			for (int q = 1; q <= 9; q++) map[p][q - 1] = 2;
		}
		if (is_win(1, 0, 2) == 3)
		{
			print();
			cout << "ten plays: " << p << " " << res << endl;
			cout << "YOU LOST!!" << endl;
			break;
		}
		flag = 1;
		for (int i = 1; i <= 9; i++)
		{
			if (map[p][i - 1] == 0) flag = 0;
		}
		if (flag) fin[p - 1] = 1;
		flag = 1;
		for (int i = 1; i <= 9; i++)
		{
			if (fin[i - 1] == 0) flag = 0;
		}
		if (flag)
		{
			cout << "YOU ARE EQUAL! " << endl;
			break;
		}
		print();
		cout << "ten plays: " << p << " " << res << endl;
		cout << "#INFORMATION:" << endl;
		cout << "# " << result << "/" << top << " = " << (double)result / top * 100 << "%" << endl;
		p = res;
		if (fin[p - 1] == 1) p = 0;
	}
	system("pause");
	return 0;
}

