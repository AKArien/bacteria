from flask import Flask, jsonify, request, render_template
import grpc

import bacteria_pb2
import bacteria_pb2_grpc


app = Flask(__name__)


channel = grpc.insecure_channel("localhost:50051")
stub = bacteria_pb2_grpc.BacteriaServiceStub(channel)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/info")
def get_info():
    response = stub.GetInfo(
        bacteria_pb2.BacteriaRequest()
    )

    return jsonify({
        "volume": response.volume,
        "state": bacteria_pb2.BacteriaInfo.State.Name(
            response.current_state
        ),
        "can_switch_to": [
            bacteria_pb2.BacteriaInfo.State.Name(s)
            for s in response.can_switch_to
        ]
    })


@app.route("/api/change_state", methods=["POST"])
def change_state():
    data = request.json

    state = bacteria_pb2.BacteriaInfo.State.Value(
        data["state"]
    )

    response = stub.ChangeState(
        bacteria_pb2.ChangeStateRequest(
            new_state=state
        )
    )

    return jsonify({
        "volume": response.volume,
        "state": bacteria_pb2.BacteriaInfo.State.Name(
            response.current_state
        )
    })


app.run(
    host="0.0.0.0",
    port=8080
)
