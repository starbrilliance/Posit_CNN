from Matrix import func, func_v2
from Posit import posit


def ConvBNReLU(input_data, conv_kernel, bn_weight, bn_bias, dsize, ksize, stride=1, ichannel=1, ochannel=1,
               threshold=posit.PositN8E1(6), posit_type="p8_1", use_fma=False, use_quire=False, one_group=True):
    pad_size = (ksize - 1) // 2
    if pad_size > 0:
        input_data = func.posit_pad(input_data, dsize, ichannel, pad_size, posit_type)
        dsize = dsize + pad_size * 2

    if one_group:
        conv_bn = func_v2.posit_conv2d_bn(input_data, conv_kernel, bn_weight, bn_bias, dsize, ksize, stride,
                                          ichannel, ochannel, posit_type, use_fma, use_quire)
    else:
        assert  ichannel == ochannel

        conv_bn = []

        for i in range(ochannel):
            conv_bn_tmp = func_v2.posit_conv2d_bn([input_data[i]], [conv_kernel[i]], [bn_weight[i]], [bn_bias[i]],
                                                  dsize, ksize, stride, 1, 1, posit_type, use_fma, use_quire)
            conv_bn.extend(conv_bn_tmp)

    output_data = func_v2.posit_relu6_active(conv_bn, ochannel, threshold)

    return output_data


def InvertedResidual(input_data, conv_kernel, bn_weight, bn_bias, dsize, stride=1, ichannel=1, ochannel=1,
                     expand_ratio=1, threshold=posit.PositN8E1(6), posit_type="p8_1", use_fma=False, use_quire=False):
    middle_oc = ichannel * expand_ratio
    osize = dsize // stride
    use_res_connect = stride == 1 and ichannel == ochannel

    if expand_ratio != 1:
        # pw
        pw_layers = ConvBNReLU(input_data, conv_kernel[0], bn_weight[0], bn_bias[0], dsize, 1, 1, ichannel,
                               middle_oc, threshold, posit_type, use_fma, use_quire)
        # dw
        dw_layers = ConvBNReLU(pw_layers, conv_kernel[1], bn_weight[1], bn_bias[1], dsize, 3, stride, middle_oc,
                               middle_oc, threshold, posit_type, use_fma, use_quire, False)
        # pw-linear
        pw_line_layers = func_v2.posit_conv2d_bn(dw_layers, conv_kernel[2], bn_weight[2], bn_bias[2], osize,
                                                 1, 1, middle_oc, ochannel, posit_type, use_fma, use_quire)
    else:
        # dw
        dw_layers = ConvBNReLU(input_data, conv_kernel[0], bn_weight[0], bn_bias[0], dsize, 3, stride, middle_oc,
                               middle_oc, threshold, posit_type, use_fma, use_quire, False)
        # pw-linear
        pw_line_layers = func_v2.posit_conv2d_bn(dw_layers, conv_kernel[1], bn_weight[1], bn_bias[1], osize,
                                                 1, 1, middle_oc, ochannel, posit_type, use_fma, use_quire)

    if use_res_connect:
        for oc in range(ochannel):
            for i in range(osize):
                for j in range(osize):
                    pw_line_layers[oc][i][j] += input_data[oc][i][j]

    return pw_line_layers


def read_param_for_convbnrelu(wfile, bfile, ichannel=1, ochannel=1, ksize=1, posit_type="p8_1"):
    bias = bfile.readline()
    conv_weight = []
    bn_bias = []
    bn_weight = []

    if posit_type == "p4_0":
        index_incre = 1
    else:
        index_incre = 2

    for oc in range(ochannel):
        if posit_type == "p4_0":
            tmp1 = posit.PositN4E0()
        elif posit_type == "p8_0":
            tmp1 = posit.PositN8E0()
        elif posit_type == "p8_2":
            tmp1 = posit.PositN8E2()
        else:
            tmp1 = posit.PositN8E1()

        index_base = index_incre * oc
        tmp1.set_from_bits(int(bias[index_base:index_base + index_incre], 16))
        bn_bias.append(tmp1)
        tmp2 = []

        for ic in range(ichannel):
            weight = wfile.readline()
            tmp3 = []

            for i in range(ksize):
                tmp4 = []
                row_base = i * index_incre * ksize

                for j in range(ksize):
                    col_base = index_incre * j

                    if posit_type == "p4_0":
                        tmp5 = posit.PositN4E0()
                    elif posit_type == "p8_0":
                        tmp5 = posit.PositN8E0()
                    elif posit_type == "p8_2":
                        tmp5 = posit.PositN8E2()
                    else:
                        tmp5 = posit.PositN8E1()

                    tmp5.set_from_bits(int(weight[row_base + col_base:row_base + col_base + index_incre], 16))
                    tmp4.append(tmp5)

                tmp3.append(tmp4)

            tmp2.append(tmp3)

        conv_weight.append(tmp2)

    weight = wfile.readline()
    for oc in range(ochannel):
        if posit_type == "p4_0":
            tmp6 = posit.PositN4E0()
        elif posit_type == "p8_0":
            tmp6 = posit.PositN8E0()
        elif posit_type == "p8_2":
            tmp6 = posit.PositN8E2()
        else:
            tmp6 = posit.PositN8E1()

        index_base = index_incre * oc
        tmp6.set_from_bits(int(weight[index_base:index_base + index_incre], 16))
        bn_weight.append(tmp6)

    return conv_weight, bn_weight, bn_bias


def read_param_for_ir(wfile, bfile, ichannel=1, ochannel=1, expand_ratio=1, posit_type="p8_1"):
    middle_layers = ichannel * expand_ratio
    bias = bfile.readline()
    conv_weight = []
    bn_bias = []
    bn_weight = []

    if posit_type == "p4_0":
        index_incre = 1
    else:
        index_incre = 2

    if expand_ratio != 1:


    for oc in range(ochannel):
        if posit_type == "p4_0":
            tmp1 = posit.PositN4E0()
        elif posit_type == "p8_0":
            tmp1 = posit.PositN8E0()
        elif posit_type == "p8_2":
            tmp1 = posit.PositN8E2()
        else:
            tmp1 = posit.PositN8E1()

        index_base = index_incre * oc
        tmp1.set_from_bits(int(bias[index_base:index_base + index_incre], 16))
        bn_bias.append(tmp1)
        tmp2 = []

        for ic in range(ichannel):
            weight = wfile.readline()
            tmp3 = []

            for i in range(ksize):
                tmp4 = []
                row_base = i * index_incre * ksize

                for j in range(ksize):
                    col_base = index_incre * j

                    if posit_type == "p4_0":
                        tmp5 = posit.PositN4E0()
                    elif posit_type == "p8_0":
                        tmp5 = posit.PositN8E0()
                    elif posit_type == "p8_2":
                        tmp5 = posit.PositN8E2()
                    else:
                        tmp5 = posit.PositN8E1()

                    tmp5.set_from_bits(int(weight[row_base + col_base:row_base + col_base + index_incre], 16))
                    tmp4.append(tmp5)

                tmp3.append(tmp4)

            tmp2.append(tmp3)

        conv_weight.append(tmp2)

    weight = wfile.readline()
    for oc in range(ochannel):
        if posit_type == "p4_0":
            tmp6 = posit.PositN4E0()
        elif posit_type == "p8_0":
            tmp6 = posit.PositN8E0()
        elif posit_type == "p8_2":
            tmp6 = posit.PositN8E2()
        else:
            tmp6 = posit.PositN8E1()

        index_base = index_incre * oc
        tmp6.set_from_bits(int(weight[index_base:index_base + index_incre], 16))
        bn_weight.append(tmp6)

    return conv_weight, bn_weight, bn_bias