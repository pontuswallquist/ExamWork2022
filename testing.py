from crypt import Crypt

actionspace = [
    [0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
]

def ActiontoIndex(place, servant, value):
    servantIndex = servant - 1
    valueIndex = value - 1
    rowIndex = place
    columnIndex = servantIndex * 6 + valueIndex
    return rowIndex, columnIndex


def testActionSpace():
    for place in range(1, 4):
        for servant in range(1, 4):
            for value in range(1,7):
                rowIndex, columnIndex = ActiontoIndex(place, servant, value)
                print(str(place) + '-' + str(servant) + '-' + str(value))
                actionspace[rowIndex][columnIndex] = 1




