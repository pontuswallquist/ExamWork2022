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

hej = [1,2,3]

if hej:
    print('hej')

hejdå = []

if not hejdå:
    print('hejdå')