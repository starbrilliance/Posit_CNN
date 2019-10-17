from Posit import posit, quire


def posit_conv2d(input_data, kernel, bias, dsize, ksize, stride=1, ichannel=1, ochannel=1, use_fma=False, use_quire=False):
    assert not use_fma & use_quire
    assert isinstance(input_data[0][0], list)
    assert isinstance(kernel[0][0][0], list)
    assert isinstance(bias[0], posit.PositN8E1)
    assert isinstance(input_data[0][0][0], posit.PositN8E1)
    assert isinstance(kernel[0][0][0][0], posit.PositN8E1)

    output_data = []

    osize = (dsize - ksize + 1) // stride

    if use_fma:
        for x in range(ochannel):
            acc = [[posit.PositN8E1(0) for _ in range(osize)] for _ in range(osize)]

            for y in range(ichannel):
                for i in range(osize):
                    d_base_row = i * stride

                    for j in range(osize):
                        d_base_col = j * stride

                        for m in range(ksize):
                            for n in range(ksize):
                                acc[i][j] = input_data[y][d_base_row + m][d_base_col + n].fma(kernel[x][y][m][n], acc[i][j])

            for i in range(osize):
                for j in range(osize):
                    acc[i][j] = acc[i][j].fma(posit.PositN8E1(1), bias[x])

            output_data.append(acc)
    else:
        if use_quire:
            for x in range(ochannel):
                acc = [[quire.QuireN8E1C14(0) for _ in range(osize)] for _ in range(osize)]

                for y in range(ichannel):
                    for i in range(osize):
                        d_base_row = i * stride

                        for j in range(osize):
                            d_base_col = j * stride

                            for m in range(ksize):
                                for n in range(ksize):
                                    acc[i][j] += input_data[y][d_base_row + m][d_base_col + n] * kernel[x][y][m][n]

                out_tmp = []
                for i in range(osize):
                    line_tmp = []

                    for j in range(osize):
                        acc[i][j] += bias[x]
                        line_tmp.append(acc[i][j].to_posit8_1())

                    out_tmp.append(line_tmp)

                output_data.append(out_tmp)
        else:
            for x in range(ochannel):
                acc = [[posit.PositN8E1(0) for _ in range(osize)] for _ in range(osize)]

                for y in range(ichannel):
                    for i in range(osize):
                        d_base_row = i * stride

                        for j in range(osize):
                            d_base_col = j * stride

                            for m in range(ksize):
                                for n in range(ksize):
                                    acc[i][j] += input_data[y][d_base_row + m][d_base_col + n] * kernel[x][y][m][n]

                for i in range(osize):
                    for j in range(osize):
                        acc[i][j] += bias[x]

                output_data.append(acc)

    return output_data


def posit_pad(input_data, dsize, ichannel=1, pad_size=1, pad_num=posit.PositN8E1(0)):
    assert isinstance(input_data[0][0], list)
    output_data = []

    for ic in range(ichannel):
        first_line = [pad_num for _ in range(dsize + 2 * pad_size)]
        pad_head = [first_line for _ in range(pad_size)]

        for i in range(dsize):
            line_head = [pad_num for _ in range(pad_size)]
            line_head.extend(input_data[ic][i])
            line_tail = [pad_num for _ in range(pad_size)]
            line_head.extend(line_tail)
            pad_head.append(line_head)

        last_line = [pad_num for _ in range(dsize + 2 * pad_size)]
        pad_tail = [last_line for _ in range(pad_size)]
        pad_head.extend(pad_tail)
        output_data.append(pad_head)

    return output_data


def posit_max_pool(input_data, dsize, ochannel=1, pool_size=2, stride=2):
    assert isinstance(input_data[0][0], list)

    output_data = []

    for oc in range(ochannel):
        out_tmp = []

        for i in range(0, dsize, stride):
            tmp1 = []

            for j in range(pool_size):
                tmp2 = []
                for k in range(0, dsize, stride):
                    tmp2.append(max(input_data[oc][i + j][k: k + pool_size]))

                tmp1.append(tmp2)

            for j in range(len(tmp1[0])):
                tmp3 = []

                for k in range(len(tmp1)):
                    tmp3.append(tmp1[k][j])

                tmp1[0][j] = max(tmp3)

            out_tmp.append(tmp1[0])

        output_data.append(out_tmp)

    return output_data


def posit_relu_active(input_data, ochannel=1):
    assert isinstance(input_data[0][0], list)

    dsize = len(input_data[0])

    for oc in range(ochannel):
        for i in range(dsize):
            for j in range(dsize):
                if input_data[oc][i][j].isneg():
                    input_data[oc][i][j].reset()

    return input_data
