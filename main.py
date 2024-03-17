import random

board = "000000000"
Games = []
INITIAL_BEADS_NO = 15
NUM_OF_ROUNDS = 1000000
gameEnded = False
botXWins = 0
botOWins = 0
ties = 0
botXBoxes = open("BotXBoxes.txt", "r+")
botOBoxes = open("BotOBoxes.txt", "r+")


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
      self.boxes.update({(state, Box(boardId, 0))})
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
      box.removePoint(move[1])

  def botWon(self):
    for move in self.movesMade:
      box = self.boxes[move[0]]
      box.addPointWon(move[1])

  def botTied(self):
    for move in self.movesMade:
      box = self.boxes[move[0]]
      box.addPointTie(move[1])


class Box:

  def __init__(self, board, beads):
    self.id = ternary_to_decimal(board)
    self.board = board
    if beads == 0:
      self.beads = []
      for i in range(9):
        if self.board[i] == "0":
          self.beads.append(INITIAL_BEADS_NO)
        else:
          self.beads.append(0)
    else:
      self.beads = beads

  def removePoint(self, move):
    if self.beads[move] != 0 and sum(self.beads) != 1:
      self.beads[move] -= 1

  def addPointWon(self, move):
    self.beads[move] += 2

  def addPointTie(self, move):
    self.beads[move] += 1

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


botX = Bot("1")
botO = Bot("2")


def writeBoxes(bot):
  if bot == "X":
    boxes = botX.boxes
  else:
    boxes = botO.boxes
  boxesKeys = list(boxes.keys())
  boxesValues = list(boxes.values())
  result = ""
  for i in range(len(boxesKeys)):
    beadsShow = str(boxesValues[i].beads)
    beadsShow = beadsShow.replace(',', '')
    beadsShow = beadsShow.replace(']', '')
    beadsShow = beadsShow.replace('[', '')
    result += str(boxesKeys[i]) + " " + str(
        boxesValues[i].board) + " " + beadsShow
    result += "\n"
  return result


def readBoxes(input):
  boxes = {}
  for line in input:
    word = ""
    box = []
    boxClass = ""
    numOfWords = 0
    beads = []
    for letter in line:
      if letter != " " and letter != "\n":
        word += letter
      elif letter == "\n":
        beads.append(int(word))
      else:
        if numOfWords == 1:
          box.append(word)
        elif numOfWords == 2:
          boxClass = word
        else:
          beads.append(int(word))
          word = ""
        numOfWords += 1
    boxes.update({int(word): Box(boxClass, beads)})
  return boxes


if __name__ == "__main__":
  command = input("Decide What You Want To Do: ")
  if command == "train":
    print("It Will Take Approximately 8 Minutes")
    botXBoxes.truncate(0)
    botOBoxes.truncate(0)
    for i in range(NUM_OF_ROUNDS):
      gameEnded = False
      board = "000000000"
      while not gameEnded:
        board = botX.makeMove(board)
        if boardCheck(board) == 2:
          botOWins += 1
          botX.botLost()
          botO.botWon()
          botX.movesMade = []
          botO.movesMade = []
          Games.append(showBoard(board))
          gameEnded = True
          break
        elif boardCheck(board) == 1:
          botXWins += 1
          botO.botLost()
          botX.botWon()
          Games.append(showBoard(board))
          gameEnded = True
          botX.movesMade = []
          botO.movesMade = []
          break
        elif boardCheck(board) == 3:
          gameEnded = True
          botX.botTied()
          botO.botTied()
          Games.append(showBoard(board))
          botX.movesMade = []
          botO.movesMade = []
          ties += 1
          break
        board = botO.makeMove(board)
        if boardCheck(board) == 2:
          botOWins += 1
          botX.botLost()
          botO.botWon()
          Games.append(showBoard(board))
          gameEnded = True
          botX.movesMade = []
          botO.movesMade = []
          break
        elif boardCheck(board) == 1:
          botXWins += 1
          botO.botLost()
          botX.botWon()
          Games.append(showBoard(board))
          gameEnded = True
          botX.movesMade = []
          botO.movesMade = []
          break
        elif boardCheck(board) == 3:
          gameEnded = True
          botX.botTied()
          botO.botTied()
          Games.append(showBoard(board))
          botX.movesMade = []
          botO.movesMade = []
          ties += 1
          break
    botXBoxes.write(writeBoxes("X"))
    botOBoxes.write(writeBoxes("O"))
  elif command == "reuseX":
    botX.boxes = readBoxes(botXBoxes)
    for i in range(10):
      gameEnded = False
      board = "000000000"
      while not gameEnded:
        board = botX.makeMove(board)
        if boardCheck(board) == 2:
          botOWins += 1
          botX.movesMade = []
          botO.movesMade = []
          Games.append(showBoard(board))
          gameEnded = True
          break
        elif boardCheck(board) == 1:
          botXWins += 1
          Games.append(showBoard(board))
          gameEnded = True
          botX.movesMade = []
          botO.movesMade = []
          break
        elif boardCheck(board) == 3:
          gameEnded = True
          Games.append(showBoard(board))
          botX.movesMade = []
          botO.movesMade = []
          ties += 1
          break
        board = botO.makeMove(board)
        if boardCheck(board) == 2:
          botOWins += 1
          Games.append(showBoard(board))
          gameEnded = True
          botX.movesMade = []
          botO.movesMade = []
          break
        elif boardCheck(board) == 1:
          botXWins += 1
          Games.append(showBoard(board))
          gameEnded = True
          botX.movesMade = []
          botO.movesMade = []
          break
        elif boardCheck(board) == 3:
          gameEnded = True
          Games.append(showBoard(board))
          botX.movesMade = []
          botO.movesMade = []
          ties += 1
          break
  elif command == "reuseO":
    botO.boxes = readBoxes(botOBoxes)
    for i in range(10):
      gameEnded = False
      board = "000000000"
      while not gameEnded:
        board = botX.makeMove(board)
        if boardCheck(board) == 2:
          botOWins += 1
          botX.movesMade = []
          botO.movesMade = []
          Games.append(showBoard(board))
          gameEnded = True
          break
        elif boardCheck(board) == 1:
          botXWins += 1
          Games.append(showBoard(board))
          gameEnded = True
          botX.movesMade = []
          botO.movesMade = []
          break
        elif boardCheck(board) == 3:
          gameEnded = True
          Games.append(showBoard(board))
          botX.movesMade = []
          botO.movesMade = []
          ties += 1
          break
        board = botO.makeMove(board)
        if boardCheck(board) == 2:
          botOWins += 1
          Games.append(showBoard(board))
          gameEnded = True
          botX.movesMade = []
          botO.movesMade = []
          break
        elif boardCheck(board) == 1:
          botXWins += 1
          Games.append(showBoard(board))
          gameEnded = True
          botX.movesMade = []
          botO.movesMade = []
          break
        elif boardCheck(board) == 3:
          gameEnded = True
          Games.append(showBoard(board))
          botX.movesMade = []
          botO.movesMade = []
          ties += 1
          break

print(botXWins)
print(botOWins)
print(ties)
for game in Games:
  print(game)
  print("\n")
