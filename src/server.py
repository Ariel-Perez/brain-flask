import flask
import subprocess
import tempfile
from protobrain.proto import experiment_pb2
from protobrain.util import proto_io


app = flask.Flask(__name__)
exp = experiment_pb2.Experiment()


@app.route('/')
def index():
    return 'Hello'


@app.route("/experiment", methods=['POST'])
def experiment():
    exp.ParseFromString(flask.request.data)
    with tempfile.NamedTemporaryFile('wb') as input_file:
        with tempfile.NamedTemporaryFile('rb') as output_file:
            input_file.write(exp.SerializeToString())
            input_file.seek(0)

            subprocess.run(
                ['python', 'protobrain-experiment', input_file.name, output_file.name]
            )

            output_file.seek(0)
            reader = proto_io.ProtoReader(output_file, snapshot_pb2.Snapshot)
            return [str(proto) for proto in reader]

    return '[]'


@app.route('/ping')
def ping():
    return ''


if __name__ == '__main__':
    app.run()
