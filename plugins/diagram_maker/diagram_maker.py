"""
Diagram Maker Plugin — create and edit Mermaid diagrams.

Skills:
    - create_diagram: Create a Mermaid diagram in the side panel
    - update_diagram: Update an existing diagram
"""

from __future__ import annotations

from tukuy.skill import Skill, skill

from cachibot.plugins.base import CachibotPlugin, PluginContext
from cachibot.plugins.sdk import artifact_update, mermaid_artifact


class DiagramMakerPlugin(CachibotPlugin):
    """Plugin for creating and editing Mermaid diagrams."""

    def __init__(self, ctx: PluginContext) -> None:
        super().__init__("diagram_maker", ctx)
        self._skills_map = self._build_skills()

    @property
    def skills(self) -> dict[str, Skill]:
        return self._skills_map

    def _build_skills(self) -> dict[str, Skill]:
        @skill(
            name="create_diagram",
            description=(
                "Create a Mermaid diagram in the side panel. Supports "
                "flowcharts, sequence diagrams, class diagrams, state "
                "diagrams, ER diagrams, Gantt charts, pie charts, and more. "
                "Use this when the user wants to visualize processes, "
                "architectures, relationships, or workflows."
            ),
            category="creative",
            tags=["diagram", "mermaid", "flowchart", "artifact"],
        )
        async def create_diagram(
            title: str,
            content: str,
        ) -> dict:
            """Create a new Mermaid diagram artifact.

            Args:
                title: Diagram title (e.g. "User Auth Flow", "DB Schema").
                content: Mermaid diagram syntax (e.g. "graph TD; A-->B;").
            """
            return mermaid_artifact(title=title, content=content)

        @skill(
            name="update_diagram",
            description=(
                "Update an existing Mermaid diagram in the side panel. "
                "Use when the user asks to modify, extend, or fix "
                "a diagram already displayed."
            ),
            category="creative",
            tags=["diagram", "mermaid", "artifact", "update"],
        )
        async def update_diagram(
            artifact_id: str,
            content: str,
            version: int = 2,
        ) -> dict:
            """Update an existing Mermaid diagram artifact.

            Args:
                artifact_id: ID of the artifact to update.
                content: The updated Mermaid diagram syntax.
                version: Version number (should increment).
            """
            return artifact_update(
                artifact_id=artifact_id,
                content=content,
                version=version,
            )

        return {
            "create_diagram": create_diagram.__skill__,
            "update_diagram": update_diagram.__skill__,
        }
