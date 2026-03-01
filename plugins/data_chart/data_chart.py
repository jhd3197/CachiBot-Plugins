"""
Data Chart Plugin — create data visualizations with SVG.

Skills:
    - create_chart: Create an SVG chart in the side panel
    - update_chart: Update an existing chart
"""

from __future__ import annotations

from tukuy.skill import Skill, skill

from cachibot.plugins.base import CachibotPlugin, PluginContext
from cachibot.plugins.sdk import artifact_update, svg_artifact


class DataChartPlugin(CachibotPlugin):
    """Plugin for creating data visualizations with SVG charts."""

    def __init__(self, ctx: PluginContext) -> None:
        super().__init__("data_chart", ctx)
        self._skills_map = self._build_skills()

    @property
    def skills(self) -> dict[str, Skill]:
        return self._skills_map

    def _build_skills(self) -> dict[str, Skill]:
        @skill(
            name="create_chart",
            description=(
                "Create a data visualization chart in the side panel using "
                "SVG. Supports bar charts, line charts, pie charts, scatter "
                "plots, area charts, and other data visualizations. Use this "
                "when the user wants to visualize data, statistics, metrics, "
                "or any numerical information."
            ),
            category="creative",
            tags=["chart", "data", "visualization", "svg", "artifact"],
        )
        async def create_chart(
            title: str,
            content: str,
        ) -> dict:
            """Create a new chart artifact.

            Args:
                title: Chart title (e.g. "Monthly Revenue", "User Growth").
                content: Complete SVG markup for the chart including axes,
                    labels, data points, legends, and styling.
            """
            return svg_artifact(title=title, content=content)

        @skill(
            name="update_chart",
            description=(
                "Update an existing chart in the side panel. "
                "Use when the user asks to change data, add series, "
                "adjust styling, or modify a chart already displayed."
            ),
            category="creative",
            tags=["chart", "data", "visualization", "artifact", "update"],
        )
        async def update_chart(
            artifact_id: str,
            content: str,
            version: int = 2,
        ) -> dict:
            """Update an existing chart artifact.

            Args:
                artifact_id: ID of the artifact to update.
                content: The updated SVG chart markup.
                version: Version number (should increment).
            """
            return artifact_update(
                artifact_id=artifact_id,
                content=content,
                version=version,
            )

        return {
            "create_chart": create_chart.__skill__,
            "update_chart": update_chart.__skill__,
        }
