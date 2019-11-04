from __future__ import print_function
import numpy


def enter_S_row():
    print('')
    try:
        tmp = raw_input('Enter found sudoku elements row wise with 0 in empty spaces and \'-\' for each box\n').split('-')
        if len(tmp) == 3:
            for i in tmp:
                if len(i) != 3:
                    raise ValueError
        else:
            raise ValueError
    except Exception as e:
        print('Caught exception while reading elements', e)
        raise(e)
    else:
        tmp = list(''.join(tmp))
        return tmp


def generate_S():
    S = numpy.empty((9, 9), numpy.int8)
    try:
        for i in xrange(9):
            tmp = enter_S_row()
            for j in xrange(9):
                S[i][j] = int(tmp[j])
    except Exception as e:
        raise (e)
    else:
        print (S)

def validate_S(S):
    valid = 1
    for i in xrange(9):
        row_sum=0
        col_sum=0
        box_sum=0
        row_sum=S[i].sum()
        col_sum=S[:,i].sum()
        x = i/3
        y = i%3
        box_sum=S[3*x:3*x+3,3*y:3*y+3].sum()
        if row_sum != 45 or col_sum != 45 or box_sum !=45:
            valid = 0
            break
    if row_sum != 45: 
        print (S[i])
    if col_sum != 45:
        print (S[:,i])
    if box_sum !=45:
        print (S[3*x:3*x+3,3*y:3*y+3])
    return valid

if __name__ == "__main__":
    generate_S()
