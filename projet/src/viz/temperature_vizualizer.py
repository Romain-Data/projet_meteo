import logging
import pandas as pd
import plotly.graph_objects as go

logger = logging.getLogger(__name__)


class TemperatureVizualizer:

    def plot(self, reports: pd.DataFrame) -> go.Figure:
        """
        Create an interactive line plot of temperature over time.

        Args:
            reports: DataFrame with 'date' (datetime) and 'temperature' (float) columns

        Returns:
            go.Figure: Plotly figure object with temperature timeline
        """
        if reports.empty:
            logger.warning("Cannot create chart: empty DataFrame")
            return go.Figure()

        logger.info(f"Creating combined chart for {len(reports)} records")

        try:
            fig = go.Figure()

            # Add temperature line
            fig.add_trace(go.Scatter(
                x=reports['date'],
                y=reports['temperature'],
                mode='lines+markers',
                name='Temperature',
                line=dict(color='#FB8500', width=2),
                marker=dict(size=6, color='#FB8500')
            ))

            # Detect changes in the day and create annotations
            annotations = []
            for i in range(1, len(reports)):
                if reports['date'].dt.date.iloc[i] != reports['date'].dt.date.iloc[i - 1]:
                    date_change = reports['date'].iloc[i]
                    annotations.append(
                        dict(
                            x=date_change,
                            y=0,  # Relative position
                            yref="paper",
                            yshift=-60,  # Downward pixel offset
                            text=date_change.strftime('%d %B'),
                            showarrow=False,
                            font=dict(size=12, color='black'),
                            bgcolor='rgba(255, 255, 255, 0.7)',
                            borderpad=4,
                            xanchor='left'
                        )
                    )

            # Page layout configuration
            fig.update_layout(
                title=dict(
                    text="Temperature Over Time",
                    x=0.5,
                    xanchor='center',
                    font=dict(size=16)
                ),
                xaxis=dict(
                    title=dict(
                        text="Hour",
                        standoff=25
                    ),
                    tickformat='%Hh',
                    dtick=6 * 60 * 60 * 1000,  # 6-hour interval
                    tickmode='linear',
                    gridcolor='rgba(128, 128, 128, 0.3)',
                    showgrid=True,
                    tickangle=45
                ),
                yaxis=dict(
                    title="Temperature (°C)",
                    gridcolor='rgba(128, 128, 128, 0.3)',
                    showgrid=True
                ),
                annotations=annotations,
                hovermode='x unified',
                plot_bgcolor='white',
                width=1200,
                height=600,
                margin=dict(b=100, t=80, l=60, r=40)
            )

            logger.info("Chart created successfully")
            return fig

        except Exception as e:
            logger.error(f"Chart creation failed: {type(e).__name__} - {str(e)}")
            return go.Figure()
