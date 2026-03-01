"""
Slide Deck Plugin — create presentation slides with canvas preview.

Skills:
    - create_slides: Create a slide deck in the side panel
    - update_slides: Update an existing slide deck
"""

from __future__ import annotations

from tukuy.skill import Skill, skill

from cachibot.plugins.base import CachibotPlugin, PluginContext
from cachibot.plugins.sdk import artifact_update, html_artifact


class SlideDeckPlugin(CachibotPlugin):
    """Plugin for creating presentation slides rendered as HTML."""

    def __init__(self, ctx: PluginContext) -> None:
        super().__init__("slide_deck", ctx)
        self._skills_map = self._build_skills()

    @property
    def skills(self) -> dict[str, Skill]:
        return self._skills_map

    def _build_skills(self) -> dict[str, Skill]:
        @skill(
            name="create_slides",
            description=(
                "Create a presentation slide deck in the side panel. "
                "Renders as styled HTML slides similar to PowerPoint or "
                "Google Slides. Use this when the user wants to create a "
                "presentation, pitch deck, lecture slides, or any content "
                "organized as sequential slides. The HTML should use CSS "
                "to create distinct slide pages with titles, bullet points, "
                "images, and navigation between slides."
            ),
            category="creative",
            tags=["slides", "presentation", "powerpoint", "deck", "artifact"],
        )
        async def create_slides(
            title: str,
            html_content: str,
        ) -> dict:
            """Create a new slide deck artifact.

            Args:
                title: Presentation title (e.g. "Product Launch", "Q4 Review").
                html_content: Complete HTML for the slide deck. Should include
                    CSS for slide-like appearance (16:9 aspect ratio, large
                    headings, bullet points) and JavaScript for slide
                    navigation (arrow keys, click to advance).
            """
            return html_artifact(title=title, content=html_content)

        @skill(
            name="update_slides",
            description=(
                "Update an existing slide deck in the side panel. "
                "Use when the user asks to add slides, change content, "
                "adjust styling, or modify a presentation already displayed."
            ),
            category="creative",
            tags=["slides", "presentation", "artifact", "update"],
        )
        async def update_slides(
            artifact_id: str,
            html_content: str,
            version: int = 2,
        ) -> dict:
            """Update an existing slide deck artifact.

            Args:
                artifact_id: ID of the artifact to update.
                html_content: The updated HTML slide deck content.
                version: Version number (should increment).
            """
            return artifact_update(
                artifact_id=artifact_id,
                content=html_content,
                version=version,
            )

        return {
            "create_slides": create_slides.__skill__,
            "update_slides": update_slides.__skill__,
        }
