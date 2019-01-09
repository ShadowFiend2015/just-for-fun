#include<stdio.h>
#include<stdlib.h>
#include<windows.h>
#include<conio.h>
#include<string.h>
#include<time.h>

struct
{
	int blocks[4][4];
}stack[10000];
int top = -1;

int board[4][4] = {{0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}, {0, 0, 0, 0}};
int score = 0;

void gotoxy(int x, int y) 
{
    COORD pos;
    pos.X = x - 1;
    pos.Y = y - 1;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE),pos);
}

void display()
{
	system("cls");
	int i, y = 4, j, k;
	char title[30] = "2048 Gift for little Orange";
	gotoxy(40-strlen(title)/2, 2);
	printf("%c%c%s%c%c\n", 3, 3, title, 3, 3);
	for(j = 0; j < 4; j++)
	{
		gotoxy(24, y++);	// 24 = 40 - 37/2 + 2 (+2是为了对齐)
		for(i = 0; i < 37; i++)	printf("%c", 4);
		gotoxy(24, y++);
		printf("%c        %c        %c        %c        %c", 4, 4, 4, 4, 4);
		gotoxy(24, y++);
		for(k = 0; k < 4; k++)
		{
			printf("%c  ", 4);
			if(board[j][k] == 0) printf("      ");
			else printf("%4d  ", board[j][k]);
		}
		printf("%c", 4);
		gotoxy(24, y++);
		printf("%c        %c        %c        %c        %c", 4, 4, 4, 4, 4);
	}
	gotoxy(24, y);
	for(i = 0; i < 37; i++)	printf("%c", 4);
	gotoxy(6, 4);
	printf("Highest Score");
	gotoxy(10, 6);
	printf("%d", score);
	gotoxy(1, 21);
	if(score >= 2) 	 printf("翠华牵手");
	if(score >= 4)	 printf("----华山日出");
	if(score >= 8)	 printf("----泰山1831");
	if(score >= 16)  printf("----青岛之夜");
	if(score >= 32)  printf("----长白之巅");
	if(score >= 64)  printf("----南京初恋");
	if(score >= 128) printf("----苏州情趣");
	if(score >= 256) printf("青海相携");
	if(score >= 512) printf("----巴蜀相随");
	if(score >= 1024)printf("----西安6.30相盼");
	if(score >= 2048)printf("----forever...");
}

void push()
{
	if(top > 9999)	return;
	int i, j;
	top++;
	for(i = 0; i < 4; i++)
		for(j = 0; j < 4; j++)
			stack[top].blocks[i][j] = board[i][j];
}

void pop()
{
	if(top < 0)	return;
	int i, j;
	for(i = 0; i < 4; i++)
		for(j = 0; j < 4; j++)
			board[i][j] = stack[top].blocks[i][j];
	top--;
}

void creatNewOne()
{
	int empty[16] = {0}, count = 0, i, j, randone;
	for(i = 0; i < 4; i++)
		for(j = 0; j < 4; j++)
			if(!board[i][j])	empty[count++] = i*10 + j;
	srand(time(NULL));
	randone = rand()%count;
	i = empty[randone] / 10;
	j = empty[randone] % 10;
	randone = rand()%10;
	board[i][j] = randone == 9 ? 4 : 2;
}

void getGreatestScore()
{
	int i, j;
	score = 0;
	for(i = 0; i < 4; i++)
		for(j = 0; j < 4; j++)
			if(board[i][j] > score)	score = board[i][j];
}

void initialize()
{
	memset(board, 0, sizeof(board));
	score = 0;
	top = -1;
	creatNewOne();
	creatNewOne();
	getGreatestScore();
}

int direction()
{
    fflush(stdin); //清除缓存数据 
    int key = 0;
	while(1)
	{
		key = getch();
		if(key == 8)	return 5;
		if(isascii(key))	continue;
		key = getch();
		switch(key)
		{
			case 72 : return 1;
			case 80 : return 2;
			case 75 : return 3;
			case 77 : return 4;
		}
	}
}

int testMoveUp()
{
	int i, j;
	for(i = 1; i < 4; i++)
		for(j = 0; j < 4; j++)
			if(board[i][j] && (!board[i-1][j] || board[i-1][j] == board[i][j]))	return 1;
	return 0;
}

int testMoveDown()
{
	int i, j;
	for(i = 2; i >= 0; i--)
		for(j = 0; j < 4; j++)
			if(board[i][j] && (!board[i+1][j] || board[i+1][j] == board[i][j]))	return 1;
	return 0;
}

int testMoveLeft()
{
	int i, j;
	for(i = 1; i < 4; i++)
		for(j = 0; j < 4; j++)
			if(board[j][i] && (!board[j][i-1] || board[j][i-1] == board[j][i]))	return 1;
	return 0;
}

int testMoveRight()
{
	int i, j;
	for(i = 2; i >= 0; i--)
		for(j = 0; j < 4; j++)
			if(board[j][i] && (!board[j][i+1] || board[j][i+1] == board[j][i]))	return 1;
	return 0;
}

void MoveUp()
{
	int i, j, k, temp[4] = {0};
	for(j = 0; j < 4; j++)
	{
		memset(temp, 0, sizeof(temp));
		for(i = 1; i < 4; i++)
		{
			if(!board[i][j])	continue;
			k = i;
			while(!board[k-1][j] && k >= 1)
			{
				board[k-1][j] = board[k][j];
				board[k][j] = 0;
				k--;
			}
			if(!temp[k-1] && board[k][j] == board[k-1][j])
			{
				temp[k-1] = 1;
				board[k-1][j] <<= 1;
				board[k][j] = 0;
			}
		}
	}		
}

void MoveDown()
{
	int i, j, k, temp[4] = {0};
	for(j = 0; j < 4; j++)
	{
		memset(temp, 0, sizeof(temp));
		for(i = 2; i >= 0; i--)
		{
			if(!board[i][j])	continue;
			k = i;
			while(!board[k+1][j] && k <= 2)
			{
				board[k+1][j] = board[k][j];
				board[k][j] = 0;
				k++;
			}
			if(!temp[k+1] && board[k][j] == board[k+1][j])
			{
				temp[k+1] = 1;
				board[k+1][j] <<= 1;
				board[k][j] = 0;
			}
		}
	}		
}

void MoveLeft()
{
	int i, j, k, temp[4] = {0};
	for(i = 0; i < 4; i++)
	{
		memset(temp, 0, sizeof(temp));
		for(j = 1; j < 4; j++)
		{
			if(!board[i][j])	continue;
			k = j;
			while(!board[i][k-1] && k >= 1)
			{
				board[i][k-1] = board[i][k];
				board[i][k] = 0;
				k--;
			}
			if(!temp[k-1] && board[i][k] == board[i][k-1])
			{
				temp[k-1] = 1;
				board[i][k-1] <<= 1;
				board[i][k] = 0;
			}
		}
	}
}

void MoveRight()
{
	int i, j, k, temp[4] = {0};
	for(i = 0; i < 4; i++)
	{
		memset(temp, 0, sizeof(temp));
		for(j = 2; j >= 0; j--)
		{
			if(!board[i][j])	continue;
			k = j;
			while(!board[i][k+1] && k <= 2)
			{
				board[i][k+1] = board[i][k];
				board[i][k] = 0;
				k++;
			}
			if(!temp[k+1] && board[i][k] == board[i][k+1])
			{
				temp[k+1] = 1;
				board[i][k+1] <<= 1;
				board[i][k] = 0;
			}
		}
	}
}

void playGame()
{
	display();
	int move;
	while(1)
	{
		if(!testMoveUp() && !testMoveDown() && !testMoveLeft() && !testMoveRight())	
		{
			char flag;
			gotoxy(1, 23);
			printf("little Orange, Game Over! Do you want to come back to last step?\n");
			scanf("%c", &flag);
			if(flag == 'y' || flag == 'Y')	{pop(); display();}
			else	break;
		}
		while(1)
		{
			move = direction();
			if(move == 5)
			{
				pop();
				break;
			}
			else if(move == 1)
			{
				if(!testMoveUp())	continue;
				push();
				MoveUp();
			}
			else if(move == 2)
			{
				if(!testMoveDown())	continue;
				push();
				MoveDown();
			}
			else if(move == 3)
			{
				if(!testMoveLeft())	continue;
				push();
				MoveLeft();
			}
			else if(move == 4)
			{
				if(!testMoveRight())	continue;
				push();
				MoveRight();
			}
			creatNewOne();
			break;
		}
		getGreatestScore();
		display();
	}
}

void heart()
{
	system("cls");
    for (float y = 1.5f; y > -1.5f; y -= 0.1f) {
        for (float x = -1.5f; x < 1.5f; x += 0.05f) {
            float a = x * x + y * y - 1;
            putchar(a * a * a - x * x * y * y * y <= 0.0f ? '*' : ' ');
        }
        putchar('\n');
    }
	gotoxy(60, 11);
	printf("little Orange");
	gotoxy(60, 12);
	printf("Happy Birthday!");
	gotoxy(1, 27);
}

int main()
{
	char flag;
	while(1)
	{
		initialize();
		playGame();
		display();
		fflush(stdin);
		gotoxy(1, 23);
		printf("Do you want to play again?\n");
		scanf("%c", &flag);
		if(flag == 'y' || flag == 'Y')	continue;
		else break;
	}
	heart();
	return 0;
}