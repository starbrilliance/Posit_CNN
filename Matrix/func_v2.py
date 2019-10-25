from Posit import posit, quire


def posit_conv2d_bn(input_data, conv_kernel, bn_weight, bn_bias, dsize, ksize, stride=1, ichannel=1, ochannel=1,
                    posit_type="p8_1", use_fma=False, use_quire=False):
    assert not use_fma & use_quire
    assert isinstance(input_data[0][0], list)
    assert isinstance(conv_kernel[0][0][0], list)
    # assert isinstance(bn_bias[0], posit.PositN8E1)
    # assert isinstance(input_data[0][0][0], posit.PositN8E1)
    # assert isinstance(conv_kernel[0][0][0][0], posit.PositN8E1)

    output_data = []

    osize = (dsize - ksize + 1) // stride

    if use_fma:
        for x in range(ochannel):
            if posit_type == "p4_0":
                acc = [[posit.PositN4E0() for _ in range(osize)] for _ in range(osize)]
            elif posit_type == "p8_0":
                acc = [[posit.PositN8E0() for _ in range(osize)] for _ in range(osize)]
            elif posit_type == "p8_2":
                acc = [[posit.PositN8E2() for _ in range(osize)] for _ in range(osize)]
            else:
                acc = [[posit.PositN8E1() for _ in range(osize)] for _ in range(osize)]

            for y in range(ichannel):
                for i in range(osize):
                    d_base_row = i * stride

                    for j in range(osize):
                        d_base_col = j * stride

                        for m in range(ksize):
                            for n in range(ksize):
                                acc[i][j] = input_data[y][d_base_row + m][d_base_col + n].fma(conv_kernel[x][y][m][n],
                                                                                              acc[i][j])

            for i in range(osize):
                for j in range(osize):
                    acc[i][j] = acc[i][j].fma(bn_weight[x], bn_bias[x])

            output_data.append(acc)
    else:
        if use_quire:
            for x in range(ochannel):
                if posit_type == "p4_0":
                    acc = [[quire.QuireN4E0C6() for _ in range(osize)] for _ in range(osize)]
                elif posit_type == "p8_0":
                    acc = [[quire.QuireN8E0C6() for _ in range(osize)] for _ in range(osize)]
                elif posit_type == "p8_2":
                    acc = [[quire.QuireN8E2C30() for _ in range(osize)] for _ in range(osize)]
                else:
                    acc = [[quire.QuireN8E1C14() for _ in range(osize)] for _ in range(osize)]

                for y in range(ichannel):
                    for i in range(osize):
                        d_base_row = i * stride

                        for j in range(osize):
                            d_base_col = j * stride

                            for m in range(ksize):
                                for n in range(ksize):
                                    acc[i][j] += input_data[y][d_base_row + m][d_base_col + n] * conv_kernel[x][y][m][n]

                out_tmp = []

                if posit_type == "p4_0":
                    for i in range(osize):
                        line_tmp = []

                        for j in range(osize):
                            p_tmp = acc[i][j].to_posit4_0()
                            p_tmp = p_tmp.fma(bn_weight[x], bn_bias[x])
                            line_tmp.append(p_tmp)

                        out_tmp.append(line_tmp)

                    output_data.append(out_tmp)

                elif posit_type == "p8_0":
                    for i in range(osize):
                        line_tmp = []

                        for j in range(osize):
                            p_tmp = acc[i][j].to_posit8_0()
                            p_tmp = p_tmp.fma(bn_weight[x], bn_bias[x])
                            line_tmp.append(p_tmp)

                        out_tmp.append(line_tmp)

                    output_data.append(out_tmp)

                elif posit_type == "p8_2":
                    for i in range(osize):
                        line_tmp = []

                        for j in range(osize):
                            p_tmp = acc[i][j].to_posit8_2()
                            p_tmp = p_tmp.fma(bn_weight[x], bn_bias[x])
                            line_tmp.append(p_tmp)

                        out_tmp.append(line_tmp)

                    output_data.append(out_tmp)

                else:
                    for i in range(osize):
                        line_tmp = []

                        for j in range(osize):
                            p_tmp = acc[i][j].to_posit8_1()
                            p_tmp = p_tmp.fma(bn_weight[x], bn_bias[x])
                            line_tmp.append(p_tmp)

                        out_tmp.append(line_tmp)

                    output_data.append(out_tmp)
        else:
            for x in range(ochannel):
                if posit_type == "p4_0":
                    acc = [[posit.PositN4E0() for _ in range(osize)] for _ in range(osize)]
                elif posit_type == "p8_0":
                    acc = [[posit.PositN8E0() for _ in range(osize)] for _ in range(osize)]
                elif posit_type == "p8_2":
                    acc = [[posit.PositN8E2() for _ in range(osize)] for _ in range(osize)]
                else:
                    acc = [[posit.PositN8E1() for _ in range(osize)] for _ in range(osize)]

                for y in range(ichannel):
                    for i in range(osize):
                        d_base_row = i * stride

                        for j in range(osize):
                            d_base_col = j * stride

                            for m in range(ksize):
                                for n in range(ksize):
                                    acc[i][j] += input_data[y][d_base_row + m][d_base_col + n] * conv_kernel[x][y][m][n]

                for i in range(osize):
                    for j in range(osize):
                        acc[i][j] = acc[i][j] * bn_weight[x] + bn_bias[x]

                output_data.append(acc)

    return output_data


def posit_avg_pool(input_data, dsize, ochannel=1, posit_type="p8_1", use_quire=False):
    assert isinstance(input_data[0][0], list)

    output_data = []
    divisor = dsize * dsize

    if posit_type == "p4_0":
        div = posit.PositN4E0(divisor)
        if use_quire:
            acc = quire.QuireN4E0C6()
        else:
            acc = posit.PositN4E0()
    elif posit_type == "p8_0":
        div = posit.PositN8E0(divisor)
        if use_quire:
            acc = quire.QuireN8E0C6()
        else:
            acc = posit.PositN8E0()
    elif posit_type == "p8_2":
        div = posit.PositN8E2(divisor)
        if use_quire:
            acc = quire.QuireN8E2C30()
        else:
            acc = posit.PositN8E2()
    else:
        div = posit.PositN8E1(divisor)
        if use_quire:
            acc = quire.QuireN8E1C14()
        else:
            acc = posit.PositN8E1()

        for oc in range(ochannel):

            for i in range(dsize):
                for j in range(dsize):
                    acc += input_data[oc][i][j]

            if use_quire:
                if posit_type == "p4_0":
                    tmp1 = acc.to_posit4_0()
                elif posit_type == "p8_0":
                    tmp1 = acc.to_posit8_0()
                elif posit_type == "p8_2":
                    tmp1 = acc.to_posit8_2()
                else:
                    tmp1 = acc.to_posit8_1()
            else:
                tmp1 = acc

            tmp2 = [[tmp1 / div]]
            acc.reset()

            output_data.append(tmp2)

    return output_data


def posit_relu6_active(input_data, ochannel=1, threshold=posit.PositN8E1(6)):
    assert isinstance(input_data[0][0], list)

    dsize = len(input_data[0])

    for oc in range(ochannel):
        for i in range(dsize):
            for j in range(dsize):
                if input_data[oc][i][j].isneg():
                    input_data[oc][i][j].reset()
                elif input_data[oc][i][j] > threshold:
                    input_data[oc][i][j].assign(6)

    return input_data
