import torch
from torchvision import datasets, transforms


def read_data(data_path="", batch_size=1):
    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST(data_path, train=True, download=True,
                       transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ])),
        batch_size, shuffle=True, num_workers=1)

    test_loader = torch.utils.data.DataLoader(
        datasets.MNIST(data_path, train=False, transform=transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])),
        batch_size, shuffle=True, num_workers=1)

    return train_loader, test_loader
