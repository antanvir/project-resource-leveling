import os
import json
# import yaml
from flask_cors import CORS, cross_origin
from flask import Flask, render_template, request, jsonify

from cpm import *
from burgess_procedure import *
from estimated_resource_smoothing import *


app = Flask(__name__, template_folder='templates')
CORS(app, resources={ r"/postDataset/": {"origins": "*"} })

app.config['UPLOAD_FOLDER'] = "dataset"
app.static_folder = 'static'


@app.route('/postDataset/', methods=['POST', 'PUT'])
@cross_origin()
def post_dataset():
    if request.method == "POST":
        _file = request.files['file']
        if _file.filename != '':
            _file.save( os.path.join(app.config['UPLOAD_FOLDER'], _file.filename) )
        result = main( os.path.join(app.config['UPLOAD_FOLDER'], _file.filename) )
        response = { "estimated": result["estimated"], "burgess1": result["burgess1"], "burgess2": result["burgess2"] }
        # print(response["estimated"]["node_matrix"])
        # print(response["burgess1"]["node_matrix"])
        # print(response["burgess2"]["node_matrix"])
        # with open(r'dataset/resp.yaml', 'w') as file:
        #     documents = yaml.dump(response, file)
        return jsonify(response)



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
    print("EST --- \n")
    # ==== Estimated Method ===== #
    estimatedSmoothing = EstimatedResourceSmoothing(node_matrix)
    result["estimated"] = estimatedSmoothing.estimate_optimal_schedule()

    print("BUR 1 --- \n")
    # ==== Burgess Procedure ===== #
    burgessProcedure1 = BurgessProcedure(node_matrix)
    result["burgess1"] = burgessProcedure1.estimate_optimal_schedule_burgess1()
    

    print("BUR 2 --- \n")
    burgessProcedure2 = BurgessProcedure(node_matrix)
    result["burgess2"] = burgessProcedure2.estimate_optimal_schedule_burgess2()
    # print(result["estimated"]["node_matrix"])
    # print(result["burgess1"]["node_matrix"])
    # print(result["burgess2"]["node_matrix"])
    # print("\n\n")
    return result


if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
    
    # method = input()
    # main(method.strip())
    