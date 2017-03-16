import sys

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QDesktopWidget, QButtonGroup, QRadioButton, QHBoxLayout, QVBoxLayout, QMessageBox)

from five_in_a_row_with_gui.fiverow import *

class ChessUI(QWidget):

    def __init__(self, chessboard):
        super().__init__()
        self.player_side = 1
        self.bot_side = 2
        self.chessboard = chessboard
        self.initUI()

    def initUI(self):

        self.resize(380, 380)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(210, 180, 140))
        self.setAutoFillBackground(True)
        self.setPalette(p)
        self.show()

    def paintEvent(self, event):
        qpainter = QPainter()
        qpainter.begin(self)
        self.drawChessBoard(event, qpainter)
        qpainter.end()

    def drawChessBoard(self, event, qp):
        width = 25
        startVertical = 15
        startHorizental = 15
        lineNum = 15
        pieceSize = 20
        #划横线
        for i in range(0, lineNum):
            qp.drawLine(startVertical+i*width, startHorizental, startVertical+i*width, startHorizental+(lineNum-1)*width)
        for i in range(0, lineNum):
            qp.drawLine(startVertical, startHorizental+i*width, startVertical+(lineNum-1)*width, startHorizental+i*width)
        for i in range(0, lineNum):
            for j in range(0, lineNum):
                if self.chessboard.board[i][j] == 1:
                    qp.setPen(QPen(Qt.black, 2, Qt.SolidLine))
                    qp.setBrush(Qt.black)
                    qp.drawEllipse(startVertical+j*width-pieceSize/2, startHorizental+i*width-pieceSize/2, pieceSize, pieceSize)

                if self.chessboard.board[i][j] == 2:
                    qp.setPen(QPen(Qt.white, 2, Qt.SolidLine))
                    qp.setBrush(Qt.white)
                    qp.drawEllipse(startVertical+j*width-pieceSize/2, startHorizental+i*width-pieceSize/2, pieceSize, pieceSize)

    def modifySide(self, player, bot):
        self.player_side = player
        self.bot_side = bot

    def mousePressEvent(self, event):

        i = int(round((event.y()-15)/25))
        j = int(round((event.x()-15)/25))

        player_piece = Piece(i, j, self.player_side)
        self.chessboard.go_a_step(player_piece)
        self.repaint()


        if self.chessboard.is_win(player_piece) is True:
            QMessageBox.information(self, "haha", "You Win")
            print('You Win!')

        mcts_tree = Tree(chessboard=self.chessboard, bot_side=self.bot_side)
        mcts_tree.back_propagation(mcts_tree.root)
        selected_node = mcts_tree.selection()
        bot_piece = selected_node.piece

        self.chessboard.go_a_step(bot_piece)

        if self.chessboard.is_win(bot_piece) is True:
            QMessageBox.information(self, "haha", "You Lose")
        self.repaint()




class ChessWindow(QWidget):
    def __init__(self, board):
        super().__init__()
        self.player_side = 0
        self.bot_side = 0
        self.board = board
        self.initUI()

    def initUI(self):

        self.startBtn = QPushButton("Start")
        self.radioBtn = QButtonGroup()
        self.radioBtnMe = QRadioButton("IFirst")
        self.radioBtnBot = QRadioButton("BotFirst")
        self.radioBtnBot.setChecked(True)
        self.radioBtn.addButton(self.radioBtnMe, 1)
        self.radioBtn.addButton(self.radioBtnBot, 2)


        self.startBtn.clicked.connect(self.on_click)


        self.canvas = ChessUI(board)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.radioBtnMe)
        self.hbox.addWidget(self.radioBtnBot)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.startBtn)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox)
        self.vbox.addWidget(self.canvas)

        self.setLayout(self.vbox)
        self.setWindowTitle("Go")

        self.resize(405, 440)
        self.center()
        self.show()

        # 窗口放在屏幕中间
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @pyqtSlot()
    def on_click(self):
        if self.radioBtnMe.isChecked():
            self.player_side = 1
            self.bot_side = 2
            self.canvas.modifySide(player=1, bot=2)
        else:
            self.player_side = 2
            self.bot_side = 1
            self.canvas.modifySide(player=2, bot=1)
            player_piece = Piece(7, 7, 1)
            self.board.go_a_step(player_piece)
            self.canvas.update()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    board = Chessboard()
    ex = ChessWindow(board)
    sys.exit(app.exec_())
