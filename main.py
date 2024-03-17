import random

board = "000000000"
Games = []
INITIAL_BEADS_NO = 15
NUM_OF_ROUNDS = 10000
gameEnded = False


class Bot:

  def __init__(self, type):
    self.boxes = {}
    self.movesMade = []
    self.type = type

  def makeMove(self, boardId):
    state = ternary_to_decimal(int(boardId))
    if self.boxes.get(state) is not None:
      box = self.boxes[state]
    else:
      self.boxes.update({(state, Box(boardId))})
      box = self.boxes[state]
    sumOfBeads = sum(box.getBeads())
    boxBeads = box.getBeads()
    indexer = random.randint(1, sumOfBeads)
    move = 0
    counter = 0
    for num in boxBeads:
      indexer -= num
      if indexer <= 0:
        move = counter
        break
      counter += 1
    board_list = list(boardId)
    board_list[move] = self.type
    self.movesMade.append([state, move])
    return ''.join(board_list)

  def botLost(self):
    for move in self.movesMade:
      box = self.boxes[move[0]]
      box.removeMove(move[1])
    Games.append(showBoard(board))


class Box:

  def __init__(self, board):
    self.id = ternary_to_decimal(board)
    self.beads = []
    self.board = board
    for i in range(9):
      if self.board[i] == "0":
        self.beads.append(INITIAL_BEADS_NO)
      else:
        self.beads.append(0)

  def removeMove(self, move):
    if self.beads[move] != 1:
      self.beads[move] -= 1

  def getBeads(self):
    return self.beads


def ternary_to_decimal(ternary_number):
  decimal_number = 0
  power = 0

  # Iterate through the ternary digits in reverse order
  for digit in reversed(str(ternary_number)):
    # Convert the digit to an integer and add it to the decimal number
    decimal_number += int(digit) * (3**power)
    power += 1

  return decimal_number


def showBoard(board_id):
  i = 0
  visual_board = ""
  for integer in board_id:
    if integer == "0":
      visual_board += "_"
    if integer == "1":
      visual_board += "X"
    if integer == "2":
      visual_board += "O"
    if i == 2:
      visual_board += '\n'
    if i == 5:
      visual_board += '\n'
    i += 1
  return visual_board


def boardCheck(board_id):
  b = list(board_id)
  if b[0] == "1" and b[1] == "1" and b[2] == "1":
    return 1
  elif b[3] == "1" and b[4] == "1" and b[5] == "1":
    return 1
  elif b[6] == "1" and b[7] == "1" and b[8] == "1":
    return 1
  elif b[0] == "1" and b[3] == "1" and b[6] == "1":
    return 1
  elif b[1] == "1" and b[4] == "1" and b[7] == "1":
    return 1
  elif b[2] == "1" and b[5] == "1" and b[8] == "1":
    return 1
  elif b[0] == "1" and b[4] == "1" and b[8] == "1":
    return 1
  elif b[2] == "1" and b[4] == "1" and b[6] == "1":
    return 1
  elif b[0] == "2" and b[1] == "2" and b[2] == "2":
    return 2
  elif b[3] == "2" and b[4] == "2" and b[5] == "2":
    return 2
  elif b[6] == "2" and b[7] == "2" and b[8] == "2":
    return 2
  elif b[0] == "2" and b[3] == "2" and b[6] == "2":
    return 2
  elif b[1] == "2" and b[4] == "2" and b[7] == "2":
    return 2
  elif b[2] == "2" and b[5] == "2" and b[8] == "2":
    return 2
  elif b[0] == "2" and b[4] == "2" and b[8] == "2":
    return 2
  elif b[2] == "2" and b[4] == "2" and b[6] == "2":
    return 2
  elif "0" not in board:
    return 3
  else:
    return 0


if __name__ == "__main__":
  botX = Bot("1")
  botO = Bot("2")
  for i in range(NUM_OF_ROUNDS):
    gameEnded = False
    board = "000000000"
    while not gameEnded:
      board = botX.makeMove(board)
      if boardCheck(board) == 2:
        botX.botLost()
        botX.movesMade = []
        botO.movesMade = []
        gameEnded = True
        break
      elif boardCheck(board) == 1:
        botO.botLost()
        gameEnded = True
        botX.movesMade = []
        botO.movesMade = []
        break
      elif boardCheck(board) == 3:
        gameEnded = True
        botX.movesMade = []
        botO.movesMade = []
        break
      board = botO.makeMove(board)
      if boardCheck(board) == 2:
        botX.botLost()
        gameEnded = True
        botX.movesMade = []
        botO.movesMade = []
        break
      elif boardCheck(board) == 1:
        botO.botLost()
        gameEnded = True
        botX.movesMade = []
        botO.movesMade = []
        break
      elif boardCheck(board) == 3:
        gameEnded = True
        botX.movesMade = []
        botO.movesMade = []
        break
