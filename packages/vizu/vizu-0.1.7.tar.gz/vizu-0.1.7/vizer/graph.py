from pandas import DataFrame
import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype
from plotly import graph_objs as go
import numpy as np


def _create_scatter(x, y, name):
    return go.Scattergl(
        x=x, y=y, name=name,
        mode='markers', opacity=0.7,
        marker={'line': {'width': 0.5, 'color': 'white'}}
    )


AGGREGATIONS = {
    "count": lambda x: x.count(),
    "mean": lambda x: x.mean(),
    "max": lambda x: x.max(),
    "min": lambda x: x.min(),
    "std": lambda x: x.std(),
    "var": lambda x: x.var(),
    "sum": lambda x: x.sum()
}


class PlotBase:

    def __init__(self, graph_idx=None):
        self.graph_idx = graph_idx

    def _create_fig(self, x, y, z, name, idx_col=None):
        raise NotImplementedError()

    def _create_annotation(self, x, y, z):
        pass

    def generate_figure(self, df: DataFrame, query=None, x=None, y=None, z=None, group_by=None, groups=None,
                        aggregation=None, prefix='', idx_col=None, x_grp=None, y_grp=None, z_grp=None):
        df = df.copy()

        if query:
            df = df.query(query)

        if idx_col is None:
            idx_col = df.columns[0]

        chart_data = pd.concat([
            df[idx_col] if idx_col not in [x, y, x, group_by] else None,
            df[x] if x else None,
            df[y] if y else None,
            df[z] if z else None,
            df[group_by] if group_by else None,
        ], axis=1)

        # Remove duplicate columns
        chart_data = chart_data.loc[:, ~chart_data.columns.duplicated()]

        def as_string(col, value):
            if col in chart_data.select_dtypes('object').columns:
                return f"'{value}'"
            else:
                return f'{value}'

        if group_by:

            if groups:
                query = " or ".join([f"(`{group_by}` == {as_string(group_by, x)})" for x in groups])
                chart_data = chart_data.query(query)

            elif any(_k is not None for _k in [x_grp, y_grp, z_grp]):
                _x = f'{x}_{x_grp}' if x is not None else x
                _y = f'{y}_{y_grp}' if y is not None else y
                _z = f'{z}_{z_grp}' if z is not None else z

                _sub_chart = chart_data.query(f"`{group_by}` == {as_string(group_by, x_grp)}")[idx_col].to_frame()

                if x is not None:
                    _df = chart_data.query(f"`{group_by}` == {as_string(group_by, x_grp)}")[[idx_col, x]].rename(columns={x: _x})
                    _sub_chart = _sub_chart.merge(_df, how='outer', left_on=idx_col, right_on=idx_col)

                if y is not None:
                    _df = chart_data.query(f"`{group_by}` == {as_string(group_by, y_grp)}")[[idx_col, y]].rename(columns={y: _y})
                    _sub_chart = _sub_chart.merge(_df, how='outer', left_on=idx_col, right_on=idx_col)

                if z is not None:
                    _df = chart_data.query(f"`{group_by}` == {as_string(group_by, z_grp)}")[[idx_col, z]].rename(columns={z: _z})
                    _sub_chart = _sub_chart.merge(_df, how='outer', left_on=idx_col, right_on=idx_col)

                x = _x
                y = _y
                z = _z

                chart_data = _sub_chart.dropna()

        if idx_col:
            chart_data.sort_values([idx_col])

        # if aggregation:
        #     to_grp = [x]
        #     if group_by:
        #         to_grp += [group_by]
        #     chart_data = chart_data.groupby(to_grp)[[y]]
        #     chart_data = AGGREGATIONS[aggregation](chart_data).reset_index()

        chart_data = chart_data.dropna()
        if x:
            chart_data = chart_data.sort_values(by=x)

        if group_by is not None and groups:
            data = []
            annotations = []
            for grp in groups:
                sub = chart_data.query(f"`{group_by}` == {as_string(group_by, grp)}")
                data.append(self._create_fig(sub[x], sub[y], sub[z] if z else None, f"{prefix}_" + str(grp), sub[idx_col]))
                annotations.append(self._create_annotation(sub[x], sub[y], sub[z] if z else None))
        else:
            data = [self._create_fig(chart_data[x], chart_data[y], chart_data[z] if z else None, prefix,
                                     chart_data[idx_col])]
            annotations = [self._create_annotation(chart_data[x], chart_data[y], chart_data[z] if z else None)]
        return data, annotations


def r_squared(obs, exp):

    if not (is_numeric_dtype(obs) and is_numeric_dtype(exp)):
        return np.nan
    y_mean = np.mean(obs)
    ss_tot = sum((obs - y_mean)**2)
    ss_res = sum((obs - exp)**2)
    if ss_tot == 0.0:
        return np.nan

    return 1.0 - ss_res / ss_tot


def rmse(data, exp):
    if not (is_numeric_dtype(data) and is_numeric_dtype(exp)):
        return np.nan
    return np.sqrt(np.mean((data - exp)**2.0))


class Line(PlotBase):
    def _create_fig(self, x, y, z, name, idx_col=None):
        return go.Scattergl(
            x=x, y=y, name=name, hovertext=idx_col,
            mode='lines', opacity=0.7
        )

    def _create_annotation(self, x, y, z):
        r2 = r_squared(x, y)
        _rmse = rmse(x, y)
        if np.isnan(r2):
            return []
        return [f"r2={r2:0.3f}", f"rmse={_rmse:0.3f}"]


class Scatter(PlotBase):
    def _create_fig(self, x, y, z, name, idx_col=None):
        return go.Scattergl(
            x=x, y=y, name=name, hovertext=idx_col,
            mode='markers', opacity=0.7,
            marker={'line': {'width': 0.5, 'color': 'white'}}
        )

    def _create_annotation(self, x, y, z):
        r2 = r_squared(x, y)
        _rmse = rmse(x, y)
        if np.isnan(r2):
            return []
        return [f"r2={r2:0.3f}", f"rmse={_rmse:0.3f}"]


class Hist(PlotBase):

    def _create_fig(self, x, y, z, name, idx_col=None):
        fig = go.Histogram(x=y, name=name, nbinsx=100)
        return fig

    def _create_annotation(self, x, y, z):
        return [f"mean={np.mean(y):0.3f}", f"std={np.std(y):0.3f}"]


class Hist2D(PlotBase):

    def _create_fig(self, x, y, z, name, idx_col=None):
        fig = go.Histogram2d(x=x, y=y, name=name, nbinsx=100, nbinsy=100, coloraxis='coloraxis')
        return fig

    def _create_annotation(self, x, y, z):
        return [f"mean_x={np.mean(x):0.3f}", f"std_x={np.std(x):0.3f}", f"mean_y={np.mean(y):0.3f}", f"std_y={np.std(y):0.3f}"]


class HistCum(PlotBase):

    def _create_fig(self, x, y, z, name, idx_col=None):
        fig = go.Histogram(x=y, name=name, cumulative_enabled=True)
        return fig

    def _create_annotation(self, x, y, z):
        return [f"mean={np.mean(y):0.3f}", f"std={np.std(y):0.3f}"]


class Table(PlotBase):

    def _create_fig(self, x, y, z, name, idx_col=None):

        header = []
        cells = []
        for col in [idx_col, x, y, z]:
            if col is not None:
                header.append(col.name)
                cells.append(col)

        return go.Table(
           header=dict(
               values=header
           ),
           cells=dict(
               values=cells
           )
        )


class Heatmap(PlotBase):

    def _create_fig(self, x, y, z, name, idx_col=None):
        return go.Scatter(x=x, y=y, name=name, mode='markers', marker=dict(
            size=16,
            color=z,
            colorscale='Viridis',
            showscale=True,
            line={'width': 0.5, 'color': 'white'},
            coloraxis='coloraxis'
        ))


class Map(PlotBase):

    def _create_fig(self, x, y, z, name, idx_col=None):

        if idx_col is not None and z is not None:
            hover_text = [f"{_x}={_z}" for _x, _z in zip(idx_col, z)]
        elif z is not None:
            hover_text = [f"{_z}" for _z in z]
        else:
            hover_text = None

        return go.Scattermapbox(
            lat=x, lon=y, hovertext=hover_text, name=name,
            marker=dict(
                size=16,
                color=z,
                colorscale='Viridis',
                showscale=True,
                coloraxis='coloraxis'
            )
        )
