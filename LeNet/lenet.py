from Matrix import convert, func
from Posit import posit


def read_param(wfile, bfile, ksize, ichannel=1, ochannel=1, posit_type="p8_1"):
    bias = bfile.readline()
    posit_bias = []
    posit_weight = []

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
        posit_bias.append(tmp1)
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

        posit_weight.append(tmp2)

    return posit_weight, posit_bias


def read_param_from_txt(wfileName="", bfileName="", posit_type="p8_1"):
    wfile = open(wfileName)
    bfile = open(bfileName)

    weight = []
    bias = []

    """layer 1 param"""
    (weight1, bias1) = read_param(wfile, bfile, 5, 1, 6, posit_type)
    weight.append(weight1)
    bias.append(bias1)

    """layer 2 param"""
    (weight2, bias2) = read_param(wfile, bfile, 5, 6, 16, posit_type)
    weight.append(weight2)
    bias.append(bias2)

    """layer 3 param"""
    (weight3, bias3) = read_param(wfile, bfile, 5, 16, 120, posit_type)
    weight.append(weight3)
    bias.append(bias3)

    """layer 4 param"""
    (weight4, bias4) = read_param(wfile, bfile, 1, 120, 84, posit_type)
    weight.append(weight4)
    bias.append(bias4)

    """layer 5 param"""
    (weight5, bias5) = read_param(wfile, bfile, 1, 84, 10, posit_type)
    weight.append(weight5)
    bias.append(bias5)

    """file close"""
    wfile.close()
    bfile.close()

    return weight, bias


"""
def lenet_test(input_image, use_fma=False, use_quire=False):
    # assert isinstance(input_image[0][0])

    wfile = open('./p8_1_weight.txt')
    bfile = open('./p8_1_bias.txt')

    # input image pad
    posit_image = convert.float2posit(input_image, 28)
    posit_image_pad = func.posit_pad([posit_image], 28, 1, 2)

    # conv 1
    (weight1, bias1) = read_param(wfile, bfile, 5, 1, 6)
    conv1_res = func.posit_conv2d(posit_image_pad, weight1, bias1, 32, 5, 1, 1, 6, use_fma, use_quire)

    # pool1 & active
    pool1_res = func.posit_max_pool(conv1_res, 28, 6)
    act1_res = func.posit_relu_active(pool1_res, 6)

    # conv 2
    (weight2, bias2) = read_param(wfile, bfile, 5, 6, 16)
    conv2_res = func.posit_conv2d(act1_res, weight2, bias2, 14, 5, 1, 6, 16, use_fma, use_quire)

    # pool2 & active
    pool2_res = func.posit_max_pool(conv2_res, 10, 16)
    act2_res = func.posit_relu_active(pool2_res, 16)

    # fc 1
    (weight3, bias3) = read_param(wfile, bfile, 5, 16, 120)
    fc1_res = func.posit_conv2d(act2_res, weight3, bias3, 5, 5, 1, 16, 120, use_fma, use_quire)

    # active
    act3_res = func.posit_relu_active(fc1_res, 120)

    # fc 2
    (weight4, bias4) = read_param(wfile, bfile, 1, 120, 84)
    fc2_res = func.posit_conv2d(act3_res, weight4, bias4, 1, 1, 1, 120, 84, use_fma, use_quire)

    # active
    act4_res = func.posit_relu_active(fc2_res, 84)

    # fc 3
    (weight5, bias5) = read_param(wfile, bfile, 1, 84, 10)
    fc3_res = func.posit_conv2d(act4_res, weight5, bias5, 1, 1, 1, 84, 10, use_fma, use_quire)

    # file close
    wfile.close()
    bfile.close()

    # output label
    tmp = []

    for oc in range(10):
        tmp.append(fc3_res[oc][0][0])

    max_out = max(tmp)
    label = tmp.index(max_out)

    return label
"""


def lenet_test_without_read_param(input_image, weight, bias, posit_type="p8_1", use_fma=False, use_quire=False):
    """ ??? """
    """input image pad"""
    posit_image = convert.float2posit(input_image, 28, posit_type)
    posit_image_pad = func.posit_pad([posit_image], 28, 1, 2, posit_type)

    """conv 1"""
    # (weight1, bias1) = read_param(wfile, bfile, 5, 1, 6)
    conv1_res = func.posit_conv2d(posit_image_pad, weight[0], bias[0], 32, 5, 1, 1, 6, posit_type, use_fma, use_quire)

    """pool1 & active"""
    pool1_res = func.posit_max_pool(conv1_res, 28, 6)
    act1_res = func.posit_relu_active(pool1_res, 6)

    """conv 2"""
    # (weight2, bias2) = read_param(wfile, bfile, 5, 6, 16)
    conv2_res = func.posit_conv2d(act1_res, weight[1], bias[1], 14, 5, 1, 6, 16, posit_type, use_fma, use_quire)

    """pool2 & active"""
    pool2_res = func.posit_max_pool(conv2_res, 10, 16)
    act2_res = func.posit_relu_active(pool2_res, 16)

    """fc 1"""
    # (weight3, bias3) = read_param(wfile, bfile, 5, 16, 120)
    fc1_res = func.posit_conv2d(act2_res, weight[2], bias[2], 5, 5, 1, 16, 120, posit_type, use_fma, use_quire)

    """active"""
    act3_res = func.posit_relu_active(fc1_res, 120)

    """fc 2"""
    # (weight4, bias4) = read_param(wfile, bfile, 1, 120, 84)
    fc2_res = func.posit_conv2d(act3_res, weight[3], bias[3], 1, 1, 1, 120, 84, posit_type, use_fma, use_quire)

    """active"""
    act4_res = func.posit_relu_active(fc2_res, 84)

    """fc 3"""
    # (weight5, bias5) = read_param(wfile, bfile, 1, 84, 10)
    fc3_res = func.posit_conv2d(act4_res, weight[4], bias[4], 1, 1, 1, 84, 10, posit_type, use_fma, use_quire)

    """file close"""
    # wfile.close()
    # bfile.close()

    """output label"""
    tmp = []

    for oc in range(10):
        tmp.append(fc3_res[oc][0][0])

    max_out = max(tmp)
    label = tmp.index(max_out)

    return label
