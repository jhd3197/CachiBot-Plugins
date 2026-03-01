"""
Social Post Plugin — preview social media posts.

Skills:
    - create_social_post: Create a social media post preview in the side panel
    - update_social_post: Update an existing social post preview
"""

from __future__ import annotations

from tukuy.skill import Skill, skill

from cachibot.plugins.base import CachibotPlugin, PluginContext
from cachibot.plugins.sdk import artifact_update, html_artifact


class SocialPostPlugin(CachibotPlugin):
    """Plugin for previewing social media posts."""

    def __init__(self, ctx: PluginContext) -> None:
        super().__init__("social_post", ctx)
        self._skills_map = self._build_skills()

    @property
    def skills(self) -> dict[str, Skill]:
        return self._skills_map

    def _build_skills(self) -> dict[str, Skill]:
        @skill(
            name="create_social_post",
            description=(
                "Create a social media post preview in the side panel. "
                "Renders as a realistic mockup of a post on platforms like "
                "Twitter/X, LinkedIn, Instagram, or Facebook. Use this when "
                "the user wants to draft, preview, or design social media "
                "content. The HTML should mimic the platform's card style "
                "with avatar, username, post body, engagement metrics, and "
                "platform-specific styling."
            ),
            category="creative",
            tags=["social", "twitter", "linkedin", "post", "artifact"],
        )
        async def create_social_post(
            title: str,
            html_content: str,
        ) -> dict:
            """Create a new social post preview artifact.

            Args:
                title: Post title (e.g. "Twitter Thread Preview", "LinkedIn Post").
                html_content: Complete HTML mimicking a social media post card
                    with platform-specific styling, user avatar area, post
                    content, and engagement button mockups.
            """
            return html_artifact(title=title, content=html_content)

        @skill(
            name="update_social_post",
            description=(
                "Update an existing social media post preview. "
                "Use when the user asks to change the text, switch "
                "platforms, or modify a post preview already displayed."
            ),
            category="creative",
            tags=["social", "post", "artifact", "update"],
        )
        async def update_social_post(
            artifact_id: str,
            html_content: str,
            version: int = 2,
        ) -> dict:
            """Update an existing social post preview artifact.

            Args:
                artifact_id: ID of the artifact to update.
                html_content: The updated HTML post preview content.
                version: Version number (should increment).
            """
            return artifact_update(
                artifact_id=artifact_id,
                content=html_content,
                version=version,
            )

        return {
            "create_social_post": create_social_post.__skill__,
            "update_social_post": update_social_post.__skill__,
        }
