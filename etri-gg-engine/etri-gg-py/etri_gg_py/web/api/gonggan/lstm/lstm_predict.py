from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

from etri_gg_py.web.api.gonggan.lstm.lstm import series_to_supervised, LSTMModel

matplotlib.use("Agg")


import torch
from sklearn.preprocessing import MinMaxScaler
from torch import nn, optim
from torch.autograd import Variable






def lstm_predict_data(input_path, output_path: Path, model_path):
    input_df = pd.read_csv(input_path, header=0)
    input_df = input_df.drop(["date", "districtCode"], axis=1)
    dataset = input_df
    values = dataset.values
    values = values.astype("float32")
    # normalize features
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled = scaler.fit_transform(values)
    reframed = series_to_supervised(scaled, 1, 1)
    data = reframed.values

    feature_target_split = int(reframed.shape[1] / 2)

    train_test_split = int(0.2 * len(data))
    print(train_test_split)


    train_X = Variable(
        torch.from_numpy(data[train_test_split:, :]), requires_grad=False,
    )
    train_y = Variable(
        torch.from_numpy(data[train_test_split:, :]), requires_grad=False,
    )

    test_X = Variable(torch.from_numpy(data[:train_test_split, :]), requires_grad=False)
    test_y = Variable(torch.from_numpy(data[:train_test_split, :]), requires_grad=False)

    model = LSTMModel()
    model.load_state_dict(torch.load(str(model_path)))
    model.eval()

    pred = model(test_X)
    pred_np = pred.detach().cpu().numpy()

    testxxx = pred_np[:train_test_split, :-feature_target_split]
    testdata = scaler.inverse_transform(testxxx)

    testdata = np.around(testdata, decimals=4, out=None)

    output_df = pd.DataFrame(testdata)
    output_df = output_df.set_axis(["SO2", "CO", "O3", "NO2", "PM10"], axis=1)

    output_df.to_csv(str(output_path), index=False)

    return str(output_path.name)
