import flask
from protobrain import scientist
from protobrain.proto import experiment_pb2


app = flask.Flask(__name__)
exp = experiment_pb2.Experiment()
sc = scientist.Scientist()


@app.route("/")
def index():
    return "Hello"

@app.route("/experiment", methods=['POST'])
def experiment():
    exp.ParseFromString(flask.request.data)
    hist = sc.run(exp)
    return hist.SerializeToString()

@app.route("/ping")
def ping():
    return ""

if __name__ == "__main__":
    app.run()
