import sqlite3
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime

conn = sqlite3.connect('kurume-dx.db')
cursor = conn.cursor()
cursor.execute('SELECT time, temp FROM temperature')
rows = cursor.fetchall()

times = [row[0] for row in rows]
temps = [row[1] for row in rows]

conn.close()

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=times, y=temps, mode='lines', name='Temperature'))
fig1.update_layout(title='Temperature Data', xaxis_title='Time', yaxis_title='Temperature [degree C]')

pio.write_html(fig1, file='temperature_plot.html', auto_open=True)

fig2 = go.Figure()
fig2.add_trace(go.Histogram(x=temps))
fig2.update_layout(title='Temperature Histogram', xaxis_title='Temperature [degree C]', yaxis_title='Count', bargap=0.1)

pio.write_html(fig2, file='temperature_hist.html', auto_open=True)