import matplotlib
import pandas as pd

matplotlib.use("Agg")

import torch
from torch import nn, optim
from torch.autograd import Variable


class LSTMModel(nn.Module):
    def __init__(self):
        super(LSTMModel, self).__init__()
        self.lstm1 = nn.LSTMCell(1, 51)
        self.lstm2 = nn.LSTMCell(51, 1)

    def forward(self, input, future=0):
        outputs = []
        h_t = Variable(torch.zeros(input.size(0), 51), requires_grad=False)
        c_t = Variable(torch.zeros(input.size(0), 51), requires_grad=False)
        h_t2 = Variable(torch.zeros(input.size(0), 1), requires_grad=False)
        c_t2 = Variable(torch.zeros(input.size(0), 1), requires_grad=False)

        for i, input_t in enumerate(input.chunk(input.size(1), dim=1)):
            h_t, c_t = self.lstm1(input_t, (h_t, c_t))
            h_t2, c_t2 = self.lstm2(c_t, (h_t2, c_t2))
            outputs += [c_t2]

        for i in range(future):  # if we should predict the future
            h_t, c_t = self.lstm1(c_t2, (h_t, c_t))
            h_t2, c_t2 = self.lstm2(c_t, (h_t2, c_t2))
            outputs += [c_t2]

        outputs = torch.stack(outputs, 1).squeeze(2)
        return outputs



# convert series to supervised learning
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()

    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [("input%d(t-%d)" % (j + 1, i)) for j in range(n_vars)]

    # forecast sequence (t, t+1, ... t+n)
    for i in range(n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [("forecast%d(t)" % (j + 1)) for j in range(n_vars)]
        else:
            names += [("forecast%d(t+%d)" % (j + 1, i)) for j in range(n_vars)]

    # put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names

    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg
