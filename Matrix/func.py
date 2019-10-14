from Posit import posit, quire


def posit_dot_mul(mat1, mat2, row, col, use_quire=False):
    if use_quire:
        output = quire.QuireN8E1C14()
    else:
        output = posit.PositN8E1()

    for i in range(0, row):
        for j in range(0, col):
            tmp = mat1[i][j] * mat2[i][j]
            output += tmp

    return output

