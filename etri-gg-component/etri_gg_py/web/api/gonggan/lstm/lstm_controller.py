import os
from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from etri_gg_py.web.api.gonggan.lstm.lstm_predict import lstm_predict_data
from etri_gg_py.web.api.gonggan.lstm.lstm_train import lstm_train_data, LstmTrainParam
from etri_gg_py.web.lifespan import DATA_INPUT, DATA_MODEL, DATA_OUTPUT, global_var

lstm_router = APIRouter()


class AbstractRequest(BaseModel):
    id: str
    name: str
    value: str


class PredictParam(BaseModel):
    input: str
    output: str


class LstmPredictRequest(AbstractRequest):
    params: PredictParam


class TrainParam(BaseModel):
    input: str
    output: str
    modelFile: str
    ratio: float
    optimizerType: str
    learningRate: float
    weightDecay: float
    epochNum: int
    timeSteps: int
    batchSize: int
    cnnHiddenLayer: int
    lstmHiddenLayer: int


class LstmTrainRequest(AbstractRequest):
    params: TrainParam


@lstm_router.get("/list-model")
async def train() -> JSONResponse:
    data_model_path = Path(global_var[DATA_MODEL])

    lstm_model_path = data_model_path / "lstm"

    model_list = []
    for entry in os.scandir(lstm_model_path):
        if entry.is_file() and (entry.name.endswith(".pt") or entry.name.endswith(".pth")):
            model_list.append(entry.name)

    return JSONResponse(content={
        "content": model_list
    })


@lstm_router.post("/train")
async def train(request: LstmTrainRequest) -> str:
    data_input_path = Path(global_var[DATA_INPUT])
    data_output_path = Path(global_var[DATA_OUTPUT])
    data_model_path = Path(global_var[DATA_MODEL])

    request_params = request.params

    input_full_path = data_input_path / request_params.input
    output_full_path = data_output_path / request_params.output
    model_full_path = data_model_path / 'lstm' / request_params.modelFile

    param = LstmTrainParam(
        input_full_path=input_full_path,
        output_full_path=output_full_path,
        model_full_path=model_full_path,
        ratio=request_params.ratio,
        optimizer_type=request_params.optimizerType,
        learning_rate=request_params.learningRate,
        weight_decay=request_params.weightDecay,
        epoch_num=request_params.epochNum,
        time_steps=request_params.timeSteps,
        batch_size=request_params.batchSize,
        cnn_hidden_layer=request_params.cnnHiddenLayer,
        lstm_hidden_layer=request_params.lstmHiddenLayer,
    )

    output = lstm_train_data(param)

    return output


@lstm_router.post("/predict")
async def predict(request: LstmPredictRequest) -> str:
    data_input_path = Path(global_var[DATA_INPUT])
    data_output_path = Path(global_var[DATA_OUTPUT])
    data_model_path = Path(global_var[DATA_MODEL])

    print(request)

    input_full_path = data_input_path / request.params.input
    output_full_path = data_output_path / request.params.output
    model_full_path = data_model_path / "lstm" / "lstm_model.pt"

    output = lstm_predict_data(input_full_path, output_full_path, model_full_path)

    return output
