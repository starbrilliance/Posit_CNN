from Matrix import convert, func
from Posit import posit, quire
from LeNet import weight2posit
import torch


a = [
        [posit.PositN8E1(1), posit.PositN8E1(2), posit.PositN8E1(3)],
        [posit.PositN8E1(1), posit.PositN8E1(1.5), posit.PositN8E1(1)],
        [posit.PositN8E1(4), posit.PositN8E1(8), posit.PositN8E1(3)]
    ]

b = [
        [posit.PositN8E1(1), posit.PositN8E1(1)],
        [posit.PositN8E1(1), posit.PositN8E1(1)]
    ]

c = [posit.PositN8E1(1)]

x = func.posit_conv2d([a],[[b]],c,3,2,use_fma=True)

for i in range(len(x[0])):
    for j in range(len(x[0][0])):
        print(x[0][i][j].to_float(),end="\t")
    print("\n")


x = func.posit_conv2d([a],[[b]],c,3,2,use_quire=True)

for i in range(len(x[0])):
    for j in range(len(x[0][0])):
        print(x[0][i][j].to_float(),end="\t")
    print("\n")

x = func.posit_conv2d([a],[[b]],c,3,2)

for i in range(len(x[0])):
    for j in range(len(x[0][0])):
        print(x[0][i][j].to_float(),end="\t")
    print("\n")

"""
ifile = r"./LeNet/mnist_cnn.pt"
#wfile = "a.txt"
#bfile = "b.txt"
#weight2posit.posit_weight_file(ifile, wfile, bfile)

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
collection = torch.load(ifile, map_location=device)
print(collection['conv1.weight'])

p8 = posit.PositN8E1(collection['conv1.weight'][0][0][4][4].item())
print(p8.raw_hex_string())
"""