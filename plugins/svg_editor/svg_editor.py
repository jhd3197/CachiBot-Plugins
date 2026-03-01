"""
SVG Editor Plugin — create and edit SVG graphics.

Skills:
    - create_svg: Create an SVG graphic in the side panel
    - update_svg: Update an existing SVG graphic
"""

from __future__ import annotations

from tukuy.skill import Skill, skill

from cachibot.plugins.base import CachibotPlugin, PluginContext
from cachibot.plugins.sdk import artifact_update, svg_artifact


class SvgEditorPlugin(CachibotPlugin):
    """Plugin for creating and editing SVG graphics."""

    def __init__(self, ctx: PluginContext) -> None:
        super().__init__("svg_editor", ctx)
        self._skills_map = self._build_skills()

    @property
    def skills(self) -> dict[str, Skill]:
        return self._skills_map

    def _build_skills(self) -> dict[str, Skill]:
        @skill(
            name="create_svg",
            description=(
                "Create an SVG graphic in the side panel. Use this for "
                "illustrations, icons, logos, infographics, geometric "
                "art, or any vector graphic the user requests."
            ),
            category="creative",
            tags=["svg", "graphic", "illustration", "artifact"],
        )
        async def create_svg(
            title: str,
            content: str,
        ) -> dict:
            """Create a new SVG artifact.

            Args:
                title: Graphic title (e.g. "App Logo", "Architecture Diagram").
                content: Complete SVG markup starting with <svg>.
            """
            return svg_artifact(title=title, content=content)

        @skill(
            name="update_svg",
            description=(
                "Update an existing SVG graphic in the side panel. "
                "Use when the user asks to modify, adjust colors, "
                "resize, or change an SVG already displayed."
            ),
            category="creative",
            tags=["svg", "graphic", "artifact", "update"],
        )
        async def update_svg(
            artifact_id: str,
            content: str,
            version: int = 2,
        ) -> dict:
            """Update an existing SVG artifact.

            Args:
                artifact_id: ID of the artifact to update.
                content: The updated SVG markup.
                version: Version number (should increment).
            """
            return artifact_update(
                artifact_id=artifact_id,
                content=content,
                version=version,
            )

        return {
            "create_svg": create_svg.__skill__,
            "update_svg": update_svg.__skill__,
        }
