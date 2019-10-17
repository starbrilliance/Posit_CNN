import torch
from torchvision import datasets, transforms
from LeNet import lenet

train_loader = torch.utils.data.DataLoader(
    datasets.MNIST('./data', train=True, download=True,
                    transform=transforms.Compose([
                    transforms.ToTensor(),
                    transforms.Normalize((0.1307,), (0.3081,))
                 ])),
    batch_size=1, shuffle=True, num_workers=1)

test_loader = torch.utils.data.DataLoader(
    datasets.MNIST('./data', train=False, transform=transforms.Compose([
                    transforms.ToTensor(),
                    transforms.Normalize((0.1307,), (0.3081,))
                 ])),
    batch_size=1, shuffle=True, num_workers=1)
    
    
"""
dataiter = iter(train_loader)
images, labels = dataiter.next()

test_res = lenet.lenet_test(images[0][0])

#print(images.size())
print(labels)
print(test_res)
"""

total = 0
equal = 0
(weight, bias) = lenet.read_param_from_txt('./p8_1_weight.txt', './p8_1_bias.txt')

for i,(images, labels) in enumerate(test_loader):
    if total == 1:
        break

    total += 1
    test_res = lenet.lenet_test_without_read_param(images[0][0], weight, bias)

    if(labels[0].item() == test_res):
        equal += 1

print("total = " + str(total))
print("equal = " + str(equal))


