
import plotly.graph_objects as go
import numpy as np

def radar_plot (normalized_list, position_label, n_solutions):
    list = normalized_list
    list_id = position_label
    n = n_solutions
    categories = ['f1 Earthwork values', 'f2 earthwork costs', 'f3 deforestation values']
    fig = go.Figure()
    for i in range(n):
        fig.add_trace(go.Scatterpolar(
            r=list[i],
            theta=categories,
            fill='toself',
            name='Position' + str(list_id[i])
        ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1]
            )),
        showlegend=False
    )

    fig.show()

    print ('Plot Successful')

"""categories = ['processing cost', 'mechanical properties', 'chemical stability',
              'thermal stability', 'device integration']

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=[1, 5, 2, 2, 3],
    theta=categories,
    fill='toself',
    name='Product A'
))
fig.add_trace(go.Scatterpolar(
    r=[4, 3, 2.5, 1, 2],
    theta=categories,
    fill='toself',
    name='Product B'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 5]
        )),
    showlegend=False
)

fig.show()"""

normalized_values = np.load('/Users/arqfa/OneDrive/Desktop/Research/normalized_values.npy')
print("normalized values successfully loaded")
available_positions = np.load('/Users/arqfa/OneDrive/Desktop/Research/available_positions.npy')
print("available positions successfully loaded")
scores_positions = np.load('/Users/arqfa/OneDrive/Desktop/Research/scores_positions.npy')
print("available positions successfully loaded")

number_solutions = 5


slp_plot = radar_plot(normalized_values, available_positions, number_solutions)