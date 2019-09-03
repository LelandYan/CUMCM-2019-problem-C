import torch
from torch import nn
from torch.nn import functional as F


class Lenet5(nn.Module):
    """
    for cifar10 dataset.
    """

    def __init__(self):
        super(Lenet5, self).__init__()
        self.conv_unit = nn.Sequential(
            # x:[b,3,32,32] => [b,6,]
            nn.Conv2d(3, 6, kernel_size=5, stride=1, padding=0),
            nn.AvgPool2d(kernel_size=2, stride=2, padding=0),
            nn.Conv2d(6, 16, kernel_size=5, stride=1, padding=0),
            nn.AvgPool2d(kernel_size=2, stride=2, padding=0),
        )
        # flatten
        self.fc_unit = nn.Sequential(
            nn.Linear(16 * 5 * 5, 120),
            nn.ReLU(),
            nn.Linear(120, 84),
            nn.ReLU(),
            nn.Linear(84, 10)
        )

        # temp = torch.randn(2, 3, 32, 32)
        # out = self.conv_unit(temp)
        # print("conv_out:", out.shape)

        #
        # self.criteon = nn.CrossEntropyLoss()

    def forward(self, x):
        batchsz = x.size(0)
        x = self.conv_unit(x)
        x = x.view(batchsz, -1)
        logits = self.fc_unit(x)

        # loss = self.criteon(logits, y)
        return logits


def main():
    net = Lenet5()
    temp = torch.randn(2, 3, 32, 32)
    out = net(temp)
    print("lenet_out:", out.shape)


if __name__ == '__main__':
    main()
