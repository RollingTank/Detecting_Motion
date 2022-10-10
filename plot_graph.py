from turtle import width
from motion_detection import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

df["Start"]=df["StartTime"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End"]=df["EndTime"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds = ColumnDataSource(df)

f = figure(x_axis_type="datetime", height=100, width=500, sizing_mode='scale_width', title="Times Object Was Detected")
q = f.quad(left="Start", right="End", bottom=0, top=1,color="blue", source=cds)
f.yaxis.minor_tick_line_color=None
f.yaxis.ticker.desired_num_ticks = 1

hover = HoverTool(tooltips=[("Starting Time","@Start"), ("Ending Time","@End")])
f.add_tools(hover)
output_file("time_graph.html")
show(f)


