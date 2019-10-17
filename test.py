from Matrix import convert, func
from Posit import posit, quire
from LeNet import lenet, dataloader
import torch

"""
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

"""
dataiter = iter(train_loader)
images, labels = dataiter.next()

test_res = lenet.lenet_test(images[0][0])

#print(images.size())
print(labels)
print(test_res)
"""
"""
total = 0
equal = 0
(weight, bias) = lenet.read_param_from_txt('./LeNet/p8_1_weight.txt', './LeNet/p8_1_bias.txt')
(train_data, test_data) = dataloader.read_data("./LeNet/data")

for i, (images, labels) in enumerate(test_data):
    if total == 1:
        break

    total += 1
    test_res = lenet.lenet_test_without_read_param(images[0][0], weight, bias)

    if (labels[0].item() == test_res):
        equal += 1

print("total = " + str(total))
print("equal = " + str(equal))
"""
print("posit<8,2>")
a = posit.PositN8E2(1)
b = posit.PositN8E2(2)
c = [a+b, a-b, a*b, a/b]
q = quire.QuireN8E2C30()
for i in range(len(c)):
    print("op(a,b) = " + c[i].format_bits_string())
    q += c[i]
    print("quire = " + str(q.to_float()))

print("posit<8,0>")
a = posit.PositN8E0(1)
b = posit.PositN8E0(2)
c = [a+b, a-b, a*b, a/b]
q = quire.QuireN8E0C6()
for i in range(len(c)):
    print("op(a,b) = " + c[i].format_bits_string())
    q += c[i]
    print("quire = " + str(q.to_float()))

print("posit<4,0>")
a = posit.PositN4E0(1)
b = posit.PositN4E0(2)
c = [a+b, a-b, a*b, a/b]
q = quire.QuireN4E0C6()
for i in range(len(c)):
    print("op(a,b) = " + c[i].format_bits_string())
    q += c[i]
    print("quire = " + str(q.to_float()))