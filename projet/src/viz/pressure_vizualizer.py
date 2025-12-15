import logging
import pandas as pd
import plotly.graph_objects as go

logger = logging.getLogger(__name__)


class PressureVizualizer:

    def plot(self, reports: pd.DataFrame) -> go.Figure:
        """
        Create an interactive line plot of pressure over time.

        Args:
            reports: DataFrame with 'date' (datetime) and 'pressure' (int) columns

        Returns:
            go.Figure: Plotly figure object with pressure timeline
        """
        # Créer la figure
        fig = go.Figure()

        # Ajouter la ligne de pression
        fig.add_trace(go.Scatter(
            x=reports['date'],
            y=reports['pressure'],
            mode='lines+markers',
            name='Pressure',
            line=dict(color='#2ca02c', width=2),
            marker=dict(size=6, color='#2ca02c')
        ))

        # Détecter les changements de jour et créer les annotations
        annotations = []
        for i in range(1, len(reports)):
            if reports['date'].dt.date.iloc[i] != reports['date'].dt.date.iloc[i - 1]:
                date_change = reports['date'].iloc[i]
                annotations.append(
                    dict(
                        x=date_change,
                        y=0,
                        yref="paper",
                        yshift=-50,
                        text=date_change.strftime('%d %B'),
                        showarrow=False,
                        font=dict(size=12, color='black'),
                        bgcolor='rgba(255, 255, 255, 0.7)',
                        borderpad=4,
                        xanchor='left'
                    )
                )

        # Configuration de la mise en page
        fig.update_layout(
            title=dict(
                text="Humidity Over Time",
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
                dtick=6 * 60 * 60 * 1000,
                tickmode='linear',
                gridcolor='rgba(128, 128, 128, 0.3)',
                showgrid=True,
                tickangle=45
            ),
            yaxis=dict(
                title="Humidity (%)",
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

        return fig
