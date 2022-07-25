import digraphs

def validMoves(gameBoard):
    moves = []
    indexList = [str(x) for x in range(len(gameBoard))]
    for i in indexList:
        if gameBoard[int(i):int(i)+3] in ['XXo']:
            moves += [(int(i),'R')]
        elif gameBoard[int(i):int(i)+3] in ['oXX']:
            moves += [(int(i)+2,'L')]
    if (moves != []):
        return moves

def makeMove(gameBoard, move):
    newBoard = list(gameBoard)
    if (move[1]=='R'): 
        newBoard[move[0]:move[0]+3] = 'ooX' 
    elif (move[1]=='L'): 
        newBoard[move[0]-2:move[0]+1] = 'Xoo'
    return ''.join(newBoard)

def moveMade(originalGameBoard, subsequentGameBoard):
    return [move for move in validMoves(originalGameBoard) if (makeMove(originalGameBoard, move) == subsequentGameBoard)][0]

def createAdjacencyList(gameBoard, adjacencyList):
    moves = validMoves(gameBoard)
    if moves != None:
        childGameBoards = [makeMove(gameBoard, i) for i in moves]
        adjacencyList.update({gameBoard : childGameBoards})
        for childGameBoard in childGameBoards:
            createAdjacencyList(childGameBoard, adjacencyList)


def adjacencyListToDirectedGraph ( adjacencyList ):
    #modified from CAB203 tutorial solutions Week 7
    keys = list(adjacencyList.keys())
    values = [item for sublist in list(adjacencyList.values()) for item in sublist]
    V = set( keys + values )
    E = { (u, v) for u, Nu in adjacencyList . items () for v in Nu}
    return V, E


def pegsSolution(gameBoard):
   if gameBoard.count("X") == 1:
        return []
   elif 'ooXoo' in gameBoard: #unsolvable sub-string
       return None
   adjacencyList = {}
   createAdjacencyList(gameBoard, adjacencyList)
   solutionGraph = adjacencyListToDirectedGraph(adjacencyList)
   solutionGameBoard = [item for tuple in solutionGraph[1] for item in tuple if item.count('X')==1]
   if solutionGameBoard != []:
       solutionPath = digraphs.findPath(solutionGraph[0], solutionGraph[1], gameBoard, solutionGameBoard[0])
       solutionMoves = [moveMade(solutionPath[index], solutionPath[index+1]) for index in [x for x in range(len(solutionPath)-1)]]
       return solutionMoves