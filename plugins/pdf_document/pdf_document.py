"""
PDF Document Plugin — create print-ready documents with canvas preview.

Skills:
    - create_pdf: Create a PDF-style document in the side panel
    - update_pdf: Update an existing PDF-style document
"""

from __future__ import annotations

from tukuy.skill import Skill, skill

from cachibot.plugins.base import CachibotPlugin, PluginContext
from cachibot.plugins.sdk import artifact_update, html_artifact


class PdfDocumentPlugin(CachibotPlugin):
    """Plugin for creating print-ready PDF-style documents."""

    def __init__(self, ctx: PluginContext) -> None:
        super().__init__("pdf_document", ctx)
        self._skills_map = self._build_skills()

    @property
    def skills(self) -> dict[str, Skill]:
        return self._skills_map

    def _build_skills(self) -> dict[str, Skill]:
        @skill(
            name="create_pdf",
            description=(
                "Create a professional, print-ready document in the side "
                "panel styled like a PDF. Use this when the user wants to "
                "create formal documents such as reports, invoices, letters, "
                "contracts, certificates, or any document meant for printing "
                "or PDF export. The HTML should use A4/Letter page dimensions, "
                "proper margins, print-friendly fonts, headers, footers, and "
                "page breaks."
            ),
            category="creative",
            tags=["pdf", "document", "print", "report", "artifact"],
        )
        async def create_pdf(
            title: str,
            html_content: str,
        ) -> dict:
            """Create a new PDF-style document artifact.

            Args:
                title: Document title (e.g. "Invoice #1234", "Annual Report").
                html_content: Complete HTML styled as a print-ready document.
                    Should include CSS with @page rules, A4 dimensions
                    (210mm x 297mm), margins, page breaks, and print-friendly
                    typography. The user can print or save as PDF from the
                    browser preview.
            """
            return html_artifact(title=title, content=html_content)

        @skill(
            name="update_pdf",
            description=(
                "Update an existing PDF-style document in the side panel. "
                "Use when the user asks to change content, adjust layout, "
                "or modify a document already displayed."
            ),
            category="creative",
            tags=["pdf", "document", "print", "artifact", "update"],
        )
        async def update_pdf(
            artifact_id: str,
            html_content: str,
            version: int = 2,
        ) -> dict:
            """Update an existing PDF-style document artifact.

            Args:
                artifact_id: ID of the artifact to update.
                html_content: The updated HTML document content.
                version: Version number (should increment).
            """
            return artifact_update(
                artifact_id=artifact_id,
                content=html_content,
                version=version,
            )

        return {
            "create_pdf": create_pdf.__skill__,
            "update_pdf": update_pdf.__skill__,
        }
