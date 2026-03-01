"""
Email Template Plugin — create and preview HTML email templates.

Skills:
    - create_email_template: Create an HTML email template with live preview
    - update_email_template: Update an existing email template
"""

from __future__ import annotations

from tukuy.skill import Skill, skill

from cachibot.plugins.base import CachibotPlugin, PluginContext
from cachibot.plugins.sdk import artifact_update, html_artifact


class EmailTemplatePlugin(CachibotPlugin):
    """Plugin for creating and previewing HTML email templates."""

    def __init__(self, ctx: PluginContext) -> None:
        super().__init__("email_template", ctx)
        self._skills_map = self._build_skills()

    @property
    def skills(self) -> dict[str, Skill]:
        return self._skills_map

    def _build_skills(self) -> dict[str, Skill]:
        @skill(
            name="create_email_template",
            description=(
                "Create an HTML email template with live preview in the side "
                "panel. Use this when the user wants to design newsletters, "
                "transactional emails, marketing emails, or notification "
                "templates. The HTML should use table-based layouts and "
                "inline styles for maximum email client compatibility."
            ),
            category="creative",
            tags=["email", "template", "html", "newsletter", "artifact"],
        )
        async def create_email_template(
            title: str,
            html_content: str,
        ) -> dict:
            """Create a new email template artifact.

            Args:
                title: Template title (e.g. "Welcome Email", "Weekly Newsletter").
                html_content: Complete HTML email content using table-based
                    layouts and inline CSS for email client compatibility.
            """
            return html_artifact(title=title, content=html_content)

        @skill(
            name="update_email_template",
            description=(
                "Update an existing email template in the side panel. "
                "Use when the user asks to modify content, adjust styling, "
                "or change the layout of an email template already displayed."
            ),
            category="creative",
            tags=["email", "template", "html", "artifact", "update"],
        )
        async def update_email_template(
            artifact_id: str,
            html_content: str,
            version: int = 2,
        ) -> dict:
            """Update an existing email template artifact.

            Args:
                artifact_id: ID of the artifact to update.
                html_content: The updated HTML email content.
                version: Version number (should increment).
            """
            return artifact_update(
                artifact_id=artifact_id,
                content=html_content,
                version=version,
            )

        return {
            "create_email_template": create_email_template.__skill__,
            "update_email_template": update_email_template.__skill__,
        }
