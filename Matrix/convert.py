from Posit import posit
import torch


def float2posit(input_data, dsize):
    assert isinstance(dsize, int)

    output = []

    if isinstance(input_data, torch.Tensor):
        for i in range(dsize):
            tmp = []
            for j in range(dsize):
                p8 = posit.PositN8E1(input_data[i][j].item())
                tmp.append(p8)

            output.append(tmp)
    else:
        for i in range(dsize):
            tmp = []
            for j in range(dsize):
                p8 = posit.PositN8E1(input_data[i][j])
                tmp.append(p8)

            output.append(tmp)

    return output


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
