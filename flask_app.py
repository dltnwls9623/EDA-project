from flask import Flask, jsonify, request, render_template
from plot_graph import *

app = Flask(__name__)


@app.route('/')
def eda():
    map_graphJSON  = draw_mapplot()
    corr_graphJSON = draw_corr()
    box_graphJSON = draw_boxplot()
    scatter_graphJSON = draw_scatter()
    return render_template('eda.html', plot={'mapgraph': map_graphJSON, 'corrgraph':corr_graphJSON, 'boxgraph':box_graphJSON, 'scatter' :scatter_graphJSON})    


if __name__ == '__main__':
    app.run(debug=True)
