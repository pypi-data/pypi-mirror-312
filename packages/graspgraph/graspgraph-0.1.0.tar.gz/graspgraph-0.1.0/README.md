# graspgraph
Create easy-to-understand graphs

## Versions

|Version|Summary|
|:--|:--|
|0.1.0|Release statsgraph|

## Installation

`pip install graspgraph`

## Usage
![](./image/sample_usage.png)
```python
import graspgraph as gg

def test_statsgraph_usage():
  statsgraph = gg.Statsgraph(
    gg.StatsgraphAxis([1, 2, 3, 4, 5]),
    gg.StatsgraphAxis([11, 12, 13, 14, 15]),
    gg.FigureColors(line = "blue"))
  figure = statsgraph.to_figure_helper()
  figure.LayoutTitleText = "<b>[statsgraph]<br>Title</b>"
  figure.XTitleText = "X"
  figure.YTitleText = "Y"
  figure.write_image("./image/sample_usage.png")
```
