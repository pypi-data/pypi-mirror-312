import plotly

#this method prints a random graph using plotly
def printGraph():
    plotly.offline.plot({
    "data": [{"x": [1, 2, 3, 4], "y": [4, 3, 2, 1]}],
    "layout": {"title": "Random Graph"}
    })