import flask
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
from transformers import AutoConfig, PretrainedConfig, PreTrainedModel
from transformers import AutoModel, AutoTokenizer, logging

# The flask app for serving predictions
app = flask.Flask(__name__)
EMBEDDING_MODEL_NAME = 'daekeun-ml/KoSimCSE-supervised-roberta-large'

class SimCSEConfig(PretrainedConfig):
    def __init__(self, version=1.0, **kwargs):
        self.version = version
        super().__init__(**kwargs)

class SimCSEModel(PreTrainedModel):
    config_class = SimCSEConfig

    def __init__(self, config):
        super().__init__(config)
        self.backbone = AutoModel.from_pretrained(config.base_model)
        self.hidden_size: int = self.backbone.config.hidden_size
        self.dense = nn.Linear(self.hidden_size, self.hidden_size)
        self.activation = nn.Tanh()

    def forward(
        self,
        input_ids: Tensor,
        attention_mask: Tensor = None,
        # RoBERTa variants don't have token_type_ids, so this argument is optional
        token_type_ids: Tensor = None,
    ) -> Tensor:
        # shape of input_ids: (batch_size, seq_len)
        # shape of attention_mask: (batch_size, seq_len)
        outputs: BaseModelOutputWithPoolingAndCrossAttentions = self.backbone(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids,
        )

        emb = outputs.last_hidden_state[:, 0]

        if self.training:
            emb = self.dense(emb)
            emb = self.activation(emb)

        return emb


@app.route("/ping", methods=["GET"])
def ping():
    response_body = "OK"
    status = 200

    return flask.Response(response=f"{response_body}\n", status=status, mimetype="application/json")


@app.route("/invocations", methods=["POST"])
def transformation():
    # The Message Body passed through POST /invocations can be received as follows:
    request_body = flask.request.data.decode("utf-8")
    print(">>>>>>>>>>>>", request_body)

    model = SimCSEModel.from_pretrained(EMBEDDING_MODEL_NAME).to("cuda:0")
    tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL_NAME)
    inputs = tokenizer(request_body, padding=True, truncation=True, return_tensors="pt").to("cuda:0")
    embedding_result = model(**inputs)

    json_response = {
        "status": 200,
        "vectors": embedding_result.tolist(),
    }
    print(">>>>>>>>>>>>", request_body, json_response)
    return flask.jsonify(json_response)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
