from main import df
import pandas
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource

#df = pandas.read_csv("sample.csv")
df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

cds = ColumnDataSource(df)
p = figure(x_axis_type = 'datetime', height = 100, width = 500, sizing_mode = "scale_both", title = "Motion Graph")
p.yaxis.minor_tick_line_color = None
p.yaxis[0].ticker.desired_num_ticks = 1


hover = HoverTool(tooltips = [("Start", "@Start"), ("End", "@End")])
p.add_tools(hover)

q = p.quad(left = "Start", right = "End", top = 1, bottom = 0, color = "green", source = cds)
output_file("MotionDetector.html")
show(p)