"""
Spreadsheet Plugin — create data tables and spreadsheets with canvas preview.

Skills:
    - create_spreadsheet: Create an interactive spreadsheet in the side panel
    - update_spreadsheet: Update an existing spreadsheet
"""

from __future__ import annotations

from tukuy.skill import Skill, skill

from cachibot.plugins.base import CachibotPlugin, PluginContext
from cachibot.plugins.sdk import artifact_update, html_artifact


class SpreadsheetPlugin(CachibotPlugin):
    """Plugin for creating data tables and spreadsheets rendered as HTML."""

    def __init__(self, ctx: PluginContext) -> None:
        super().__init__("spreadsheet", ctx)
        self._skills_map = self._build_skills()

    @property
    def skills(self) -> dict[str, Skill]:
        return self._skills_map

    def _build_skills(self) -> dict[str, Skill]:
        @skill(
            name="create_spreadsheet",
            description=(
                "Create a spreadsheet or data table in the side panel. "
                "Renders as a styled HTML table similar to Excel or Google "
                "Sheets. Use this when the user wants to display tabular data, "
                "create a data summary, show statistics, build a comparison "
                "table, or organize information in rows and columns. The HTML "
                "should include a styled table with headers, alternating row "
                "colors, and optional formulas or totals."
            ),
            category="creative",
            tags=["spreadsheet", "table", "data", "excel", "artifact"],
        )
        async def create_spreadsheet(
            title: str,
            html_content: str,
        ) -> dict:
            """Create a new spreadsheet artifact.

            Args:
                title: Spreadsheet title (e.g. "Q4 Sales Report", "Budget").
                html_content: Complete HTML with styled table. Should include
                    CSS for Excel-like appearance (borders, header styling,
                    alternating rows, number formatting).
            """
            return html_artifact(title=title, content=html_content)

        @skill(
            name="update_spreadsheet",
            description=(
                "Update an existing spreadsheet in the side panel. "
                "Use when the user asks to add rows, change data, "
                "add columns, or modify a spreadsheet already displayed."
            ),
            category="creative",
            tags=["spreadsheet", "table", "data", "artifact", "update"],
        )
        async def update_spreadsheet(
            artifact_id: str,
            html_content: str,
            version: int = 2,
        ) -> dict:
            """Update an existing spreadsheet artifact.

            Args:
                artifact_id: ID of the artifact to update.
                html_content: The updated HTML table content.
                version: Version number (should increment).
            """
            return artifact_update(
                artifact_id=artifact_id,
                content=html_content,
                version=version,
            )

        return {
            "create_spreadsheet": create_spreadsheet.__skill__,
            "update_spreadsheet": update_spreadsheet.__skill__,
        }
