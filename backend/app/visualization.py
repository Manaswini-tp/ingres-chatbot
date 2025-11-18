import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import List, Dict, Any

class VisualizationEngine:
    def __init__(self):
        self.chart_templates = {
            'groundwater_level': self.create_groundwater_chart,
            'trends': self.create_trend_chart,
            'comparison': self.create_comparison_chart,
            'water_quality': self.create_quality_chart
        }
    
    def create_groundwater_chart(self, data: List[Dict], entities: Dict) -> Dict[str, Any]:
        """Create groundwater level chart"""
        df = pd.DataFrame(data)
        
        if 'district' in entities and entities['district']:
            # District-level data
            fig = px.bar(df, x='month', y='groundwater_level', 
                        title=f"Groundwater Level in {entities['district']}, {entities['state']} ({entities['year']})",
                        color='groundwater_level',
                        color_continuous_scale='Blues_r')
        else:
            # State-level data
            fig = px.line(df, x='district', y='groundwater_level',
                         title=f"Groundwater Level Across Districts in {entities['state']} ({entities['year']})")
        
        fig.update_layout(
            xaxis_title="Location",
            yaxis_title="Groundwater Level (meters)",
            template="plotly_white"
        )
        
        return fig.to_dict()
    
    def create_trend_chart(self, data: List[Dict], entities: Dict) -> Dict[str, Any]:
        """Create trend analysis chart"""
        df = pd.DataFrame(data)
        
        fig = px.line(df, x='year', y='groundwater_level', color='district',
                     title=f"Groundwater Trends in {entities['state']} ({entities.get('time_period', 5)} years)")
        
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Groundwater Level (meters)",
            template="plotly_white"
        )
        
        return fig.to_dict()
    
    def create_comparison_chart(self, data: List[Dict], entities: Dict) -> Dict[str, Any]:
        """Create comparison chart between entities"""
        df = pd.DataFrame(data)
        
        fig = px.bar(df, x='district', y='groundwater_level', color='state',
                    title="Groundwater Level Comparison",
                    barmode='group')
        
        fig.update_layout(
            xaxis_title="District",
            yaxis_title="Groundwater Level (meters)",
            template="plotly_white"
        )
        
        return fig.to_dict()
    
    def create_quality_chart(self, data: List[Dict], entities: Dict) -> Dict[str, Any]:
        """Create water quality chart"""
        df = pd.DataFrame(data)
        quality_counts = df['water_quality'].value_counts().reset_index()
        quality_counts.columns = ['quality', 'count']
        
        fig = px.pie(quality_counts, values='count', names='quality',
                    title=f"Water Quality Distribution in {entities['state']}")
        
        return fig.to_dict()
    
    def generate_chart(self, data: List[Dict], intent: str, entities: Dict) -> Dict[str, Any]:
        """Generate appropriate chart based on intent"""
        chart_func = self.chart_templates.get(intent, self.create_groundwater_chart)
        return chart_func(data, entities)