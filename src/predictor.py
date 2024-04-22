import flask

app = flask.Flask(__name__)

# /ping은 SageMaker Endpoint의 인스턴스 상태를 확인하는 데 사용된다.
@app.route("/ping", methods=["GET"])
def ping():
    response_body = "OK"
    status = 200

    return flask.Response(response=f"{response_body}\n",
                          status=status,
                          mimetype="application/json")


# /invocations는 SageMaker Endpoint를 통해 실제 추론을 행하는 API이다. sagemaker.predictor.predict()를 호출하면
# 내부적으로 /invocations가 호출된다.
@app.route("/invocations", methods=["POST"])
def transformation():
    # POST /invocations를 통해 전달된 Message Body는 아래와 같이 받을 수 있습니다.
    request_body = flask.request.data.decode("utf-8")
    print(request_body)

    # result = EmbeddingService.predict(data)
    return flask.jsonify([1.00121, -1.0023401])


if __name__ == '__main__':
    app.run('0.0.0.0', port=8080, debug=True)