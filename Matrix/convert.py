from Posit import posit


def float2posit(input_data, row, col):
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(input_data[0], list)
    output = [None] * row

    for i in range(0, row):
        tmp = [None] * col
        for j in range(0, col):
            p8 = posit.PositN8E1(input_data[i][j])
            tmp[j] = p8

        output[i] = tmp

    return output


def posit2float(input_data, row, col):
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(input_data[0], list)
    output = [None] * row

    for i in range(0, row):
        tmp = [None] * col
        for j in range(0, col):
            f32 = input_data[i][j].to_float()
            tmp[j] = f32

        output[i] = tmp

    return output
