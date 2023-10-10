from flask import Flask, send_from_directory, request, redirect
from flask_cors import CORS, cross_origin
from drawWrapper import drawGraph, drawPlot
import os

# Switching backend to a non gui version fixes thread safety issues
import matplotlib.pyplot as plt
plt.switch_backend('agg')

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def index():
    return "backend server"

@app.route('/cache/<file>')
def sendFromCache(file):
    return send_from_directory('cache', file)

@app.route('/graph', methods = ['GET','POST'])
@cross_origin()
def graph():
    if request.method == 'POST':
        try:
            img = drawGraph(
                size = int(request.form.get('size')),
                percentage = float(request.form.get('percentage')),
                type = request.form.get('type'),
                coloredClusters = request.form.get('coloredClusters') == 'true'
            )
            return redirect(f'/{img}')
        except Exception as e:
            return f"an error occured\n {e}"
    if request.method == 'GET':
        try:   
            img = drawGraph(
                size = int(request.args.get('size')),
                percentage = float(request.args.get('percentage')),
                type = request.args.get('type'),
                coloredClusters = request.args.get('coloredClusters') == 'true'
            )
            return f'/{img}'
        except Exception as e:
            print(e)
            return f"an error occured\n {e}"
    
@app.route('/plot', methods = ['GET', 'POST'])
@cross_origin()
def plot():
    if request.method == 'GET':
        try:
            img = drawPlot(
                size = int(request.args.get('size')),
                type = request.args.get('type'),
                plotType = request.args.get('plotType')
            )
            
            return f'/{img}'
        except Exception as e:
            print(e)
            return f"an error occured\n {e}"
        





if __name__ == "__main__":
    app.run(debug=True)