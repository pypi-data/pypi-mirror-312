from pathlib import Path
import logging
from typing import cast

logging.getLogger("matplotlib").setLevel(logging.WARNING)
import matplotlib as mpl  # NOQA

default_backend = mpl.get_backend()
mpl.use("Agg")
import matplotlib.pyplot as plt  # NOQA

from icplot.color import ColorMap  # NOQA
from .series import PlotSeries, LinePlotSeries, ScatterPlotSeries, ImageSeries  # NOQA
from .plot import Plot, GridPlot, apply_colors  # NOQA


class MatplotlibColorMap(ColorMap):
    """
    A matplotlib based colormap
    """

    def __init__(self, label: str):
        super().__init__(label, mpl.colormaps[label])


def _set_decorations(ax, plot: Plot):
    ax.legend(loc="upper left")
    if plot.x_axis.label:
        ax.set_xlabel(plot.x_axis.label)
    if plot.y_axis.label:
        ax.set_ylabel(plot.y_axis.label)
    if plot.x_axis.ticks:
        ax.set_xticks(plot.x_axis.resolved_ticks)
    if plot.y_axis.ticks:
        ax.set_yticks(plot.y_axis.resolved_ticks)
    if plot.title:
        ax.set_title(plot.title)


def _plot_line(ax, series: LinePlotSeries):
    ax.plot(
        series.x,
        series.y,
        label=series.label,
        color=series.color.as_list(),
        marker=series.marker,
    )


def _plot_scatter(ax, series: ScatterPlotSeries):
    ax.scatter(series.data, label=series.label, color=series.color.as_list())


def _plot_image(ax, series: ImageSeries):
    ax.imshow(series.data)
    ax.axis("off")


def _plot_series(ax, series: PlotSeries):
    if series.series_type == "line":
        _plot_line(ax, cast(LinePlotSeries, series))
    elif series.series_type == "scatter":
        _plot_scatter(ax, cast(ScatterPlotSeries, series))
    elif series.series_type == "image":
        _plot_image(ax, cast(ImageSeries, series))


def _render(fig, path: Path | None = None):
    if path:
        fig.savefig(path)
    else:
        plt.switch_backend(default_backend)
        fig.show()
        plt.switch_backend("Agg")


def render(
    plot: Plot, path: Path | None = None, cmap=MatplotlibColorMap("gist_rainbow")
):

    apply_colors(cmap, plot)

    fig, ax = plt.subplots()

    for series in plot.series:
        _plot_series(ax, series)

    _set_decorations(ax, plot)

    _render(fig, path)


def render_grid(
    plot: GridPlot,
    path: Path | None = None,
    num_samples: int = 0,
):
    rows, cols, series = plot.get_subplots(num_samples)
    fig, axs = plt.subplots(rows, cols)

    for ax, series_item in zip(axs, series):
        _plot_series(ax, series_item)

    _render(fig, path)
