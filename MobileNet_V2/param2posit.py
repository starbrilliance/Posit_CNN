import torch
import os
import math
from Posit import posit


def param2posit(input_data, dsize, posit_type="p8_1", is_matrix=True):
    output_str = ""

    if posit_type == "p4_0":
        tmp = posit.PositN4E0()
    elif posit_type == "p8_0":
        tmp = posit.PositN8E0()
    elif posit_type == "p8_2":
        tmp = posit.PositN8E2()
    else:
        tmp = posit.PositN8E1()

    if is_matrix:
        for i in range(dsize):
            for j in range(dsize):
                tmp.assign(input_data[i][j].item())
                tmp_str = tmp.raw_hex_string()
                output_str += tmp_str
    else:
        for i in range(dsize):
            tmp.assign(input_data[i])
            tmp_str = tmp.raw_hex_string()
            output_str += tmp_str

    return output_str


def posit_param_file(fileName="", weightFile="", biasFile="", posit_type="p8_1"):
    assert os.path.exists(fileName)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    collection = torch.load(fileName, map_location=device)

    wfile = open(weightFile, "w")
    bfile = open(biasFile, 'w')

    global weight_tmp
    global bias_tmp
    global mean_tmp
    global var_tmp

    for param_tensor in collection:
        size = collection[param_tensor].size()

        if 'weight' in param_tensor:
            if len(size) == 4:
                for oc in range(size[0]):
                    for ic in range(size[1]):
                        param_str = param2posit(collection[param_tensor][oc][ic], size[2], posit_type)
                        wfile.write(param_str)
                        wfile.write('\n')
            elif len(size) == 2:
                for oc in range(size[0]):
                    for ic in range(size[1]):
                        param_str = param2posit([collection[param_tensor][oc][ic].item()], 1, posit_type, False)
                        wfile.write(param_str)
                        wfile.write('\n')
            else:
                weight_tmp = collection[param_tensor]

        elif 'bias' in param_tensor:
            if 'classifier' in param_tensor:
                classifier_bias = []

                for i in range(size[0]):
                    classifier_bias.append(collection[param_tensor][i].item())

                bias_str = param2posit(classifier_bias, size[0], posit_type, False)
                bfile.write(bias_str)
                bfile.write('\n')
            else:
                bias_tmp = collection[param_tensor]
        elif 'mean' in param_tensor:
            mean_tmp = collection[param_tensor]
        elif 'var' in param_tensor:
            comb_weight = []
            comb_bias = []

            for i in range(size[0]):
                coeff1 = 1 / math.sqrt(collection[param_tensor][i].item())
                weight1 = coeff1 * weight_tmp[i].item()
                comb_weight.append(weight1)
                bias1 = bias_tmp[i].item() - weight1 * mean_tmp[i].item()
                comb_bias.append(bias1)

            weight_str = param2posit(comb_weight, size[0], posit_type, False)
            bias_str = param2posit(comb_bias, size[0], posit_type, False)

            wfile.write(weight_str)
            wfile.write('\n')
            bfile.write(bias_str)
            bfile.write('\n')

    bfile.close()
    wfile.close()

