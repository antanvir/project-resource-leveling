import os
import json
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request, jsonify

from cpm import *
from burgess_procedure import *
from estimated_resource_smoothing import *


app = Flask(__name__, template_folder='templates')
CORS(app, resources={ r"/postDataset/": {"origins": "*"} })

app.config['UPLOAD_FOLDER'] = "dataset"
app.static_folder = 'static'


@app.route('/postDataset/', methods=['POST'])
@cross_origin()
def post_dataset():
    if request.method == "POST":
        _file = request.files['file']
        if _file.filename != '':
            _file.save( os.path.join(app.config['UPLOAD_FOLDER'], _file.filename) )
        result = main( os.path.join(app.config['UPLOAD_FOLDER'], _file.filename) )

        response = { "estimated": result["estimated"], "burgess1": result["burgess1"], "burgess2": result["burgess2"] }
        # print(response)
        return json.dumps(response)



@app.route('/')
def index():
    return render_template('index.html')



def main(filepath):
    # input_file = 'input1.csv'
    input_file = filepath
    cpm = None
    node_matrix = None
    result = {"estimated": None, "burgess1": None, "burgess2": None}

    cpm = CPM()
    cpm.find_all_activity_informations(input_file)
    node_matrix = cpm.get_node_matrix()
    # print(node_matrix)
    
    # ==== Estimated Method ===== #
    estimatedSmoothing = EstimatedResourceSmoothing(node_matrix)
    result["estimated"] = estimatedSmoothing.estimate_optimal_schedule()

    # ==== Burgess Procedure ===== #
    burgessProcedure1 = BurgessProcedure(node_matrix)
    result["burgess1"] = burgessProcedure1.estimate_optimal_schedule_burgess1()
    
    burgessProcedure2 = BurgessProcedure(node_matrix)
    result["burgess2"] = burgessProcedure2.estimate_optimal_schedule_burgess2()
    return result


if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
    
    # method = input()
    # main(method.strip())
    