from pyecharts.charts import Page, Bar, Line, Map, Gauge, Grid
from pyecharts.options import VisualMapOpts
from pyecharts import options as opts
bar = Bar()
page = Page()
line = Line()
gauge = Gauge()
grid = Grid(init_opts=opts.InitOpts(width="1200px", height="720px"))
# 折线图
line.add_xaxis(["day 1", "day 2", "day 3"])
line.add_yaxis("私人区域", [58, 98, 65])
line.add_yaxis("公共区域", [55, 65, 99])
# 柱形图
bar.add_xaxis(["私人区域", "公共区域"])
bar.add_yaxis("室内人数", [62, 89])
bar.reversal_axis()
# 地图
map = Map()
# 添加对象
data = [
    ("南岗区", -23),
    ("平房区", -23),
    ("松北区", -22),
    ("道里区", -23),
    ("道外区", -23),
    ("呼兰区", -24),
    ("香坊区", -23),
    ("双城区", -21),
    ("阿城区", -22),
    ("五常市", -18),
    ("巴彦县", -27),
    ("宾县", -20),
    ("尚志市", -18),
    ("木兰县", -25),
    ("延寿县", -21),
    ("通河县", -26),
    ("方正县", -24),
    ("依兰县", -25)

]
map.add("test map", data, "哈尔滨")

# 设置全局选项
map.set_global_opts(
    visualmap_opts=VisualMapOpts(
        is_show=True,
        is_piecewise=True,
        pieces=[
            {"min": -30, "max": -25, "label": "-30--25", "color": "#00868B"},
            {"min": -25, "max": -20, "label": "-25--20", "color": "#00F5FF"},
            {"min": -20, "max": -15, "label": "-20--15", "color": "#BBFFFF"},
            {"min": -15, "max": -10, "label": "-15--10", "color": "#FAEBD7"},
            {"min": -10, "max": -5, "label": "-10--5", "color": "#FFDAB9"},
        ]

    )
)
# 仪表盘
gauge.add("", data_pair=[("室内温度", "25.6")])
# 布局
grid.add(bar, grid_opts=opts.GridOpts(pos_bottom="60", pos_left="60"))
grid.add(line, grid_opts=opts.GridOpts(pos_bottom="60", pos_right="60"))
grid.add(map, grid_opts=opts.GridOpts(pos_top="60", pos_left="60"))
grid.add(gauge, grid_opts=opts.GridOpts(pos_top="60", pos_right="60"))
grid.render()