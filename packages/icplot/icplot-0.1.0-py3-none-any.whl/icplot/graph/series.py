import typing

from pydantic import BaseModel

from icplot.color import Color


class PlotSeries(BaseModel):
    """
    A data series in a plot, such as a single line in a line-plot
    """

    label: str
    color: Color = Color()
    series_type: str = ""
    highlight: bool = False


class ImageSeries(PlotSeries):
    """
    A plot data series where the elements are images
    """

    data: typing.Any
    transform: typing.Any
    series_type: str = "image"


class LinePlotSeries(PlotSeries):
    """
    A plot series for line plots
    """

    x: list
    y: list
    marker: str = "o"
    series_type: str = "line"


class ScatterPlotSeries(PlotSeries):

    data: typing.Any
    series_type: str = "scatter"
