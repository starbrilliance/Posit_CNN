from Posit import posit
import torch


def float2posit(input_data, dsize, posit_type="p8_1"):
    assert isinstance(dsize, int)

    output = []

    if posit_type == "p4_0":
        for i in range(dsize):
            line_tmp = []
            for j in range(dsize):
                p4 = posit.PositN4E0(input_data[i][j].item())
                line_tmp.append(p4)

            output.append(line_tmp)

    elif posit_type == "p8_0":
        for i in range(dsize):
            line_tmp = []
            for j in range(dsize):
                p8 = posit.PositN8E0(input_data[i][j].item())
                line_tmp.append(p8)

            output.append(line_tmp)

    elif posit_type == "p8_2":
        for i in range(dsize):
            line_tmp = []
            for j in range(dsize):
                p8 = posit.PositN8E2(input_data[i][j].item())
                line_tmp.append(p8)

            output.append(line_tmp)

    else:
        for i in range(dsize):
            line_tmp = []
            for j in range(dsize):
                p8 = posit.PositN8E1(input_data[i][j].item())
                line_tmp.append(p8)

            output.append(line_tmp)

    return output


"""
def posit2float(input_data, row, col):
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(input_data[0], list)
    output = []

    for i in range(0, row):
        tmp = []
        for j in range(0, col):
            f32 = input_data[i][j].to_float()
            tmp.append(f32)

        output.append(tmp)

    return output
"""
