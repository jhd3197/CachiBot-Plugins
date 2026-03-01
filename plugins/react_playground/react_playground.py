"""
React Playground Plugin — create and preview React/JSX components.

Skills:
    - create_react_component: Create a React component with live preview
    - update_react_component: Update an existing React component
"""

from __future__ import annotations

from tukuy.skill import Skill, skill

from cachibot.plugins.base import CachibotPlugin, PluginContext
from cachibot.plugins.sdk import artifact_update, react_artifact


class ReactPlaygroundPlugin(CachibotPlugin):
    """Plugin for creating and previewing React/JSX components."""

    def __init__(self, ctx: PluginContext) -> None:
        super().__init__("react_playground", ctx)
        self._skills_map = self._build_skills()

    @property
    def skills(self) -> dict[str, Skill]:
        return self._skills_map

    def _build_skills(self) -> dict[str, Skill]:
        @skill(
            name="create_react_component",
            description=(
                "Create a React/JSX component with live preview in the side "
                "panel. Use this when the user wants to prototype UI components, "
                "build interactive widgets, or experiment with React code. "
                "The component renders immediately with full interactivity."
            ),
            category="creative",
            tags=["react", "jsx", "component", "ui", "artifact"],
        )
        async def create_react_component(
            title: str,
            content: str,
        ) -> dict:
            """Create a new React component artifact.

            Args:
                title: Component title (e.g. "Todo App", "Dashboard Card").
                content: JSX code for the component. Should export a default
                    component or return JSX directly. Can use React hooks
                    and inline styles.
            """
            return react_artifact(title=title, content=content)

        @skill(
            name="update_react_component",
            description=(
                "Update an existing React component in the side panel. "
                "Use when the user asks to modify, restyle, or add "
                "features to a component already displayed."
            ),
            category="creative",
            tags=["react", "jsx", "component", "artifact", "update"],
        )
        async def update_react_component(
            artifact_id: str,
            content: str,
            version: int = 2,
        ) -> dict:
            """Update an existing React component artifact.

            Args:
                artifact_id: ID of the artifact to update.
                content: The updated JSX code.
                version: Version number (should increment).
            """
            return artifact_update(
                artifact_id=artifact_id,
                content=content,
                version=version,
            )

        return {
            "create_react_component": create_react_component.__skill__,
            "update_react_component": update_react_component.__skill__,
        }
