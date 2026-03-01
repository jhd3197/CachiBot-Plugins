"""
Blog Writer Plugin — create and edit blog articles with canvas.

Skills:
    - create_blog_post: Create a blog article in the side panel
    - update_blog_post: Update an existing blog article
"""

from __future__ import annotations

from tukuy.skill import Skill, skill

from cachibot.plugins.base import CachibotPlugin, PluginContext
from cachibot.plugins.sdk import artifact_update, markdown_artifact


class BlogWriterPlugin(CachibotPlugin):
    """Plugin for creating and editing blog articles in a canvas panel."""

    def __init__(self, ctx: PluginContext) -> None:
        super().__init__("blog_writer", ctx)
        self._skills_map = self._build_skills()

    @property
    def skills(self) -> dict[str, Skill]:
        return self._skills_map

    def _build_skills(self) -> dict[str, Skill]:
        @skill(
            name="create_blog_post",
            description=(
                "Create a blog article in the side panel with rich markdown "
                "rendering. Use this when the user wants to write, draft, or "
                "generate a blog post, article, or essay. The content should "
                "be well-structured with headings, paragraphs, and formatting."
            ),
            category="creative",
            tags=["blog", "article", "writing", "markdown", "artifact"],
        )
        async def create_blog_post(
            title: str,
            content: str,
        ) -> dict:
            """Create a new blog article artifact.

            Args:
                title: Blog post title (e.g. "Getting Started with Python").
                content: Full markdown content of the blog article including
                    headings, paragraphs, code blocks, lists, and images.
            """
            return markdown_artifact(title=title, content=content)

        @skill(
            name="update_blog_post",
            description=(
                "Update an existing blog article in the side panel. "
                "Use when the user asks to revise, edit, expand, or "
                "rewrite a blog post already displayed."
            ),
            category="creative",
            tags=["blog", "article", "writing", "artifact", "update"],
        )
        async def update_blog_post(
            artifact_id: str,
            content: str,
            version: int = 2,
        ) -> dict:
            """Update an existing blog article artifact.

            Args:
                artifact_id: ID of the artifact to update.
                content: The updated markdown content.
                version: Version number (should increment).
            """
            return artifact_update(
                artifact_id=artifact_id,
                content=content,
                version=version,
            )

        return {
            "create_blog_post": create_blog_post.__skill__,
            "update_blog_post": update_blog_post.__skill__,
        }
