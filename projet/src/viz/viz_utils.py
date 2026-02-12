"""
Utility module for visualization components.
Contains shared logic for creating Plotly traces, annotations, and layouts.
"""

import logging
from datetime import datetime, timedelta
import pandas as pd
import plotly.graph_objects as go


logger = logging.getLogger(__name__)


def filter_last_7_days(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter a DataFrame to keep only records from the last 7 days.
    
    Args:
        df: DataFrame containing a 'date' column with datetime objects.
        
    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    if df.empty or 'date' not in df.columns:
        return df

    # Ensure date column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        df = df.copy()
        df['date'] = pd.to_datetime(df['date'])

    # Time zone management
    if df['date'].dt.tz is not None:
        cutoff_date = pd.Timestamp.now(tz='UTC') - pd.Timedelta(days=7)
    else:
        cutoff_date = datetime.now() - timedelta(days=7)

    return df[df['date'] >= cutoff_date]


def create_line_trace(
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    name: str,
    color: str
) -> go.Scatter:
    """
    Create a standardized line trace for Plotly.

    Args:
        df: DataFrame containing the data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        name: Name of the trace
        color: Hex color code for the line and markers

    Returns:
        go.Scatter: Configured scatter trace
    """
    return go.Scatter(
        x=df[x_col],
        y=df[y_col],
        mode='lines+markers',
        name=name,
        line={'color': color, 'width': 2},
        marker={'size': 6, 'color': color}
    )


def create_date_change_annotations(reports: pd.DataFrame) -> list[dict]:
    """
    Create annotations for date changes on the x-axis.

    Args:
        reports: DataFrame containing 'date' column with datetime objects

    Returns:
        list[dict]: List of annotation dictionaries for Plotly layout
    """
    annotations = []
    # Ensure date column is accessed safely
    dates = reports['date']

    for i in range(1, len(reports)):
        current_date = dates.iloc[i]
        prev_date = dates.iloc[i - 1]

        # Check if day has changed
        if current_date.date() != prev_date.date():
            annotations.append(
                {
                    'x': current_date,
                    'y': 0,
                    'yref': "paper",
                    'yshift': -53,
                    'text': current_date.strftime('%d %B'),
                    'showarrow': False,
                    'font': {'size': 12, 'color': 'black'},
                    'bgcolor': 'rgba(255, 255, 255, 0.7)',
                    'borderpad': 4,
                    'xanchor': 'left'
                }
            )
    return annotations


def update_layout(
    fig: go.Figure,
    title: str,
    y_title: str,
    annotations: list[dict]
) -> None:
    """
    Apply standard layout configuration to a Plotly figure.

    Args:
        fig: The figure to update
        title: Chart title
        y_title: Y-axis title
        annotations: List of annotations to add
    """
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16}
        },
        xaxis={
            'title': {
                'text': "Hour",
                'standoff': 25
            },
            'tickformat': '%Hh',
            'dtick': 6 * 60 * 60 * 1000,  # 6 hours in milliseconds
            'tickmode': 'linear',
            'gridcolor': 'rgba(128, 128, 128, 0.3)',
            'showgrid': True,
            'tickangle': 45
        },
        yaxis={
            'title': y_title,
            'gridcolor': 'rgba(128, 128, 128, 0.3)',
            'showgrid': True
        },
        annotations=annotations,
        hovermode='x unified',
        plot_bgcolor='white',
        width=1200,
        height=600,
        margin={'b': 100, 't': 80, 'l': 60, 'r': 40}
    )


def create_time_series_chart(
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    df: pd.DataFrame,
    y_col: str,
    title: str,
    y_title: str,
    color: str,
    x_col: str = 'date'
) -> go.Figure:
    """
    Creates a complete time series chart with standard styling and error handling.

    Args:
        df: DataFrame containing the data
        y_col: Column name for y-axis data
        title: Chart title
        y_title: Y-axis title
        color: Hex color code for the line
        x_col: Column name for x-axis data (default: 'date')

    Returns:
        go.Figure: The generated Plotly figure
    """
    if df.empty:
        logger.warning("Cannot create chart: empty DataFrame")
        return go.Figure()

    try:
        fig = go.Figure()

        # Add Trace
        fig.add_trace(create_line_trace(
            df=df,
            x_col=x_col,
            y_col=y_col,
            name=y_title,
            color=color
        ))

        # Add Annotations
        annotations = create_date_change_annotations(df)

        # Update Layout
        update_layout(
            fig=fig,
            title=title,
            y_title=y_title,
            annotations=annotations
        )

        return fig

    except Exception as e:  # pylint: disable=broad-exception-caught
        logger.error("Chart creation failed: %s - %s", type(e).__name__, str(e))
        return go.Figure()
