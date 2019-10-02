import numpy as np
from board_utils import *


target_array = np.array([[1,2,3],[8,0,4],[7,6,5]]) #From Problem Set, also use for test case 1.


#target_array = np.array([[1,2,3],[4,5,6],[7,8,0]]) #test target_array (test case 2) - from https://algorithmsinsight.wordpress.com/graph-theory-2/a-star-in-general/implementing-a-star-to-solve-n-puzzle/
target = Board(target_array, 0, target_array)

#board_array = np.array([[3,5,1],[8,2,6],[0,7,4]]) #Problem Set Config
#board_array = np.array([[1,2,3],[8,4,7],[0,6,5]]) #Simple case test 1 - solves in 12 moves.
#board_array = np.array([[1,2,3],[0,4,6],[7,5,8]]) #Simple case test 2 - shown here to solve in three: https://algorithmsinsight.wordpress.com/graph-theory-2/a-star-in-general/implementing-a-star-to-solve-n-puzzle/

board = gen_board(3,3, target) #generate random board.

#board = Board(board_array, 0, target_array)


state = {}

openList = []
closedList = {}
# Add the start node:
# put the startNode on the openList (leave it's f at zero)
openList.append(board)
state[board] = 'open'

deepest = 0

# Loop until you find the end
while len(openList) > 0:
    # Get the current node
    # let the currentNode equal the node with the least f value
    # remove the currentNode from the openList
    openList.sort(key=lambda x: x.f)
    currNode = openList.pop(0)

    most_deep = max(deepest, currNode.g)
    if most_deep != deepest:
        print(f'explored to depth {most_deep}')
        print(f'{len(state.keys())} nodes explored of a possible {fact(9)}')
        deepest = most_deep


    # add the currentNode to the closedList
    state[board] = 'closed'
    # Found the goal
    # if currentNode is the goal

    if currNode.is_target():
        # Congrats! You've found the end! Break, then backtrack to get path
        break

    #To monitor progress:
    #print(currNode.g)

    # Generate children
    children = pathgen(currNode, target)
    for child in children:

        child.parent = currNode

        key = str(child.board)
        if not state.get(key):
            state[key] = 'new'

        if child.g >= 20:
            state[key] = 'closed'

        # Child is on the closedList
        if state[key] == 'closed':
            continue
        # Create the f, g, and h values - DONE BY BOARD OBJECT
        # child.g = currentNode.g + distance between child and current
        # child.h = distance from child to end
        # child.f = child.g + child.h

        # Child is already in openList
        if state[key] == 'open':
            if child.g > currNode.g:
                continue
        # Add the child to the openList
        openList.append(child)
        state[key] = 'open'


#Traceback:
moves = []
tb = currNode
moves.append(tb)

while tb.g != 0:
    tb = tb.parent
    moves.append(tb)
moves = moves[::-1]

print('Start Board:')
print(moves[0])

for idx, m in enumerate(moves[1:]):
    print(f'Move #{idx+1}')
    print(m)
    print('')
print(f'Solved in {len(moves)-1} moves.')