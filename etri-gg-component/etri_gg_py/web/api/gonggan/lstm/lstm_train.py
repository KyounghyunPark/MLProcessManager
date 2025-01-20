from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from fontTools.svgLib.path import PathBuilder
from sympy.strategies.core import switch

from etri_gg_py.web.api.gonggan.lstm.lstm import series_to_supervised, LSTMModel
import torch
from sklearn.preprocessing import MinMaxScaler
from torch import nn, optim
from torch.autograd import Variable


class LstmTrainParam:
    def __init__(
        self,
        input_full_path,
        output_full_path,
        model_full_path,
        ratio=0.2,
        optimizer_type='Adam',
        learning_rate=0.001,
        weight_decay=0.00001,
        epoch_num=200,
        time_steps=5,
        batch_size=256,
        cnn_hidden_layer=128,
        lstm_hidden_layer=256,
    ):
        self.input_full_path = input_full_path
        self.output_full_path = output_full_path
        self.model_full_path = model_full_path
        self.ratio = ratio
        self.optimizer_type = optimizer_type
        self.learning_rate = learning_rate
        self.weight_decay = weight_decay
        self.epoch_num = epoch_num
        self.time_steps = time_steps
        self.batch_size = batch_size
        self.cnn_hidden_layer = cnn_hidden_layer
        self.lstm_hidden_layer = lstm_hidden_layer


def lstm_train_data(param: LstmTrainParam):
    input_full_path: Path = param.input_full_path
    output_full_path: Path = param.output_full_path
    model_full_path: Path = param.model_full_path

    ratio = param.ratio
    optimizer_type = param.optimizer_type
    learning_rate = param.learning_rate
    weight_decay = param.weight_decay
    epoch_num = param.epoch_num
    time_steps = param.time_steps
    batch_size = param.batch_size
    cnn_hidden_layer = param.cnn_hidden_layer
    lstm_hidden_layer = param.lstm_hidden_layer


    input_df = pd.read_csv(input_full_path, header=0)
    input_df = input_df.drop(["date", "districtCode"], axis=1)
    dataset = input_df
    values = dataset.values
    values = values.astype("float32")
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(values)
    reframed = series_to_supervised(scaled, 1, 1)
    data = reframed.values

    feature_target_split = int(reframed.shape[1] / 2)

    train_test_split = int(ratio * len(data))
    train_X = Variable(torch.from_numpy(data[train_test_split:, :]), requires_grad=False)
    train_y = Variable(torch.from_numpy(data[train_test_split:, :]), requires_grad=False)
    test_X = Variable(torch.from_numpy(data[:train_test_split, :]), requires_grad=False)
    test_y = Variable(torch.from_numpy(data[:train_test_split, :]), requires_grad=False)
    model = LSTMModel()
    criterion = nn.MSELoss()

    if optimizer_type == 'Adam':
        optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    elif optimizer_type == 'SGD':
        optimizer = optim.SGD(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    elif optimizer_type == 'RMSprop':
        optimizer = optim.RMSprop(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    elif optimizer_type == 'Adagrad':
        optimizer = optim.Adagrad(model.parameters(), lr=learning_rate, weight_decay=weight_decay)
    else:
        optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=weight_decay)

    loss_list = []
    test_loss_list = []

    # begin to train
    for epoch in range(epoch_num):
        print("epoch : ", epoch)

        def closure():
            optimizer.zero_grad()
            out = model(train_X)
            loss = criterion(out, train_y)
            print("loss:", float(loss.data.numpy()))
            loss_list.append(float(loss.data.numpy()))
            loss.backward()
            return loss

        optimizer.step(closure)

        #   # begin to predict
        #     future = 1000
        #     pred = seq(test_X, future=future)
        pred = model(test_X)
        loss = criterion(pred, test_y)
        #     print('test loss:', loss.data_input.numpy()[0])
        test_loss_list.append(float(loss.data.numpy()))

        y = pred.data.numpy()

    torch.save(model.state_dict(), model_full_path)

    pred = model(test_X)

    pred_np = pred.detach().cpu().numpy()

    testxxx = data[:train_test_split, :-feature_target_split]
    testdata = scaler.inverse_transform(testxxx)

    testdata = np.around(testdata, decimals=4, out=None)

    output_df = pd.DataFrame(testdata)

    output_df = output_df.set_axis(["SO2", "CO", "O3", "NO2", "PM10"], axis=1)

    output_df.to_csv(output_full_path, index=False)

    return output_full_path.name
