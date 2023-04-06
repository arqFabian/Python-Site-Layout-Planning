
import plotly.graph_objects as go
import numpy as np

def radar_plot (normalized_list, position_label):
    categories = ['processing cost', 'mechanical properties', 'chemical stability']
    fig = go.Figure()
    for i in range(5):
        fig.add_trace(go.Scatterpolar(
            r=normalized_list[i],
            theta=categories,
            fill='toself',
            name='Position' + str(position_label[i])
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

    print (name)

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

slp_plot = radar_plot(normalized_values, available_positions)