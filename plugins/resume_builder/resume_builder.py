"""
Resume Builder Plugin — create professional resumes and CVs.

Skills:
    - create_resume: Create a resume/CV in the side panel
    - update_resume: Update an existing resume
"""

from __future__ import annotations

from tukuy.skill import Skill, skill

from cachibot.plugins.base import CachibotPlugin, PluginContext
from cachibot.plugins.sdk import artifact_update, html_artifact


class ResumeBuilderPlugin(CachibotPlugin):
    """Plugin for creating professional resumes and CVs."""

    def __init__(self, ctx: PluginContext) -> None:
        super().__init__("resume_builder", ctx)
        self._skills_map = self._build_skills()

    @property
    def skills(self) -> dict[str, Skill]:
        return self._skills_map

    def _build_skills(self) -> dict[str, Skill]:
        @skill(
            name="create_resume",
            description=(
                "Create a professional resume or CV in the side panel. "
                "Renders as a beautifully styled HTML document ready for "
                "printing or PDF export. Use this when the user wants to "
                "build, design, or format a resume, CV, or professional "
                "profile. The HTML should include sections for contact info, "
                "summary, experience, education, and skills with clean, "
                "professional typography."
            ),
            category="creative",
            tags=["resume", "cv", "career", "professional", "artifact"],
        )
        async def create_resume(
            title: str,
            html_content: str,
        ) -> dict:
            """Create a new resume artifact.

            Args:
                title: Resume title (e.g. "John Doe - Resume", "Senior Dev CV").
                html_content: Complete HTML for the resume with professional
                    styling, A4/Letter dimensions, print-friendly CSS,
                    and organized sections (contact, summary, experience,
                    education, skills).
            """
            return html_artifact(title=title, content=html_content)

        @skill(
            name="update_resume",
            description=(
                "Update an existing resume in the side panel. "
                "Use when the user asks to add experience, change layout, "
                "update skills, or modify a resume already displayed."
            ),
            category="creative",
            tags=["resume", "cv", "artifact", "update"],
        )
        async def update_resume(
            artifact_id: str,
            html_content: str,
            version: int = 2,
        ) -> dict:
            """Update an existing resume artifact.

            Args:
                artifact_id: ID of the artifact to update.
                html_content: The updated HTML resume content.
                version: Version number (should increment).
            """
            return artifact_update(
                artifact_id=artifact_id,
                content=html_content,
                version=version,
            )

        return {
            "create_resume": create_resume.__skill__,
            "update_resume": update_resume.__skill__,
        }
