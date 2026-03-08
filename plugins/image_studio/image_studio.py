"""
Image Studio Plugin — generate, refine, and remix AI images with workspace support.

Provides a canvas-based workflow for iterative image creation using Prompture's
async image generation drivers (DALL-E 3, Imagen 3, Stability AI, Grok Aurora).

Skills:
    - create_image: Generate an image from a text prompt (displayed in canvas)
    - refine_image: Tweak parameters and regenerate an existing image
    - remix_image: Reimagine the same subject with a new artistic direction
"""

from __future__ import annotations

import logging
from math import gcd
from typing import Any

from tukuy.skill import RiskLevel, Skill, skill

from cachibot.plugins.base import CachibotPlugin, PluginContext
from cachibot.plugins.sdk import image_artifact

logger = logging.getLogger(__name__)


def _resolve_model(ctx: PluginContext) -> str:
    """Get the image model from bot's model slots, falling back to DALL-E 3."""
    if ctx.bot_models:
        model = ctx.bot_models.get("image", "")
        if model:
            return model
    return "openai/dall-e-3"


def _build_driver_options(
    model: str,
    size: str,
    quality: str,
    style: str,
) -> dict[str, Any]:
    """Build provider-specific options dict for the image driver."""
    options: dict[str, Any] = {
        "size": size,
        "quality": quality,
        "style": style,
        "n": 1,
    }

    provider = model.split("/", 1)[0].lower() if "/" in model else ""
    if provider == "stability":
        parts = size.split("x")
        if len(parts) == 2:
            w, h = int(parts[0]), int(parts[1])
            d = gcd(w, h)
            options["aspect_ratio"] = f"{w // d}:{h // d}"
        options.pop("size", None)
        options.pop("quality", None)
        options.pop("style", None)

    return options


async def _generate(
    ctx: PluginContext,
    prompt: str,
    size: str,
    quality: str,
    style: str,
) -> dict[str, Any]:
    """Shared generation logic — calls Prompture driver and returns image artifact."""
    from prompture import get_async_img_gen_driver_for_model

    model = _resolve_model(ctx)
    options = _build_driver_options(model, size, quality, style)

    logger.info(
        "Image Studio: model=%s size=%s quality=%s style=%s",
        model, size, quality, style,
    )

    driver = get_async_img_gen_driver_for_model(model)
    result = await driver.generate_image(prompt, options)

    images = result.get("images", [])
    if not images:
        raise RuntimeError("No images returned from the provider.")

    image = images[0]
    media_type = getattr(image, "media_type", "image/png")
    image_data = getattr(image, "data", "")
    data_uri = f"data:{media_type};base64,{image_data}"

    meta = result.get("meta", {})
    metadata: dict[str, Any] = {
        "prompt": prompt,
        "model": meta.get("model_name", model),
        "size": size,
        "quality": quality,
        "style": style,
        "provider": model.split("/", 1)[0] if "/" in model else model,
    }
    if meta.get("revised_prompt"):
        metadata["revised_prompt"] = meta["revised_prompt"]
    if meta.get("cost"):
        metadata["cost"] = f"${meta['cost']:.4f}"

    return image_artifact(
        title=prompt[:80] + ("..." if len(prompt) > 80 else ""),
        content=data_uri,
        metadata=metadata,
    )


class ImageStudioPlugin(CachibotPlugin):
    """Workspace plugin for iterative AI image generation and refinement."""

    def __init__(self, ctx: PluginContext) -> None:
        super().__init__("image_studio", ctx)
        self._skills_map = self._build_skills()

    @property
    def skills(self) -> dict[str, Skill]:
        return self._skills_map

    def _build_skills(self) -> dict[str, Skill]:
        ctx = self.ctx

        def _cfg(key: str, fallback: str) -> str:
            return ctx.tool_configs.get("image_studio", {}).get(key, fallback)

        @skill(
            name="create_image",
            description=(
                "Generate an AI image from a text prompt and display it in the "
                "Image Studio canvas. Use this for any image creation request. "
                "Craft a detailed, descriptive prompt for best results."
            ),
            category="creative",
            tags=["image", "generation", "ai", "dall-e", "artifact"],
            side_effects=False,
            requires_network=True,
            display_name="Generate Image",
            icon="sparkles",
            risk_level=RiskLevel.MODERATE,
            input_schema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": (
                            "Detailed text description of the image to generate. "
                            "Be specific about subject, style, lighting, colors, "
                            "composition, and mood."
                        ),
                    },
                    "size": {
                        "type": "string",
                        "description": "Image dimensions.",
                        "enum": ["1024x1024", "1792x1024", "1024x1792"],
                        "default": "1024x1024",
                    },
                    "quality": {
                        "type": "string",
                        "description": "Image quality (OpenAI DALL-E only).",
                        "enum": ["standard", "hd"],
                        "default": "hd",
                    },
                    "style": {
                        "type": "string",
                        "description": "Image style (OpenAI DALL-E 3 only).",
                        "enum": ["vivid", "natural"],
                        "default": "vivid",
                    },
                },
                "required": ["prompt"],
                "additionalProperties": False,
            },
        )
        async def create_image(
            prompt: str,
            size: str = "",
            quality: str = "",
            style: str = "",
        ) -> dict:
            """Generate an AI image from a text prompt.

            Args:
                prompt: Detailed text description of the image to generate.
                size: Image dimensions (e.g., "1024x1024").
                quality: Image quality ("standard" or "hd", OpenAI only).
                style: Image style ("vivid" or "natural", DALL-E 3 only).
            """
            effective_size = size or _cfg("defaultSize", "1024x1024")
            effective_quality = quality or _cfg("defaultQuality", "hd")
            effective_style = style or _cfg("defaultStyle", "vivid")

            return await _generate(ctx, prompt, effective_size, effective_quality, effective_style)

        @skill(
            name="refine_image",
            description=(
                "Refine a previously generated image by adjusting the prompt, "
                "size, quality, or style and regenerating. Use when the user "
                "wants to tweak the current image — e.g., 'make it darker', "
                "'change the background to blue', 'try landscape format'."
            ),
            category="creative",
            tags=["image", "refine", "tweak", "adjust", "artifact"],
            side_effects=False,
            requires_network=True,
            display_name="Refine Image",
            icon="sliders-horizontal",
            risk_level=RiskLevel.MODERATE,
            input_schema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": (
                            "The refined prompt incorporating the user's requested "
                            "changes. Should be a complete prompt, not just the delta."
                        ),
                    },
                    "size": {
                        "type": "string",
                        "description": "Image dimensions (keep same or change).",
                        "enum": ["1024x1024", "1792x1024", "1024x1792"],
                    },
                    "quality": {
                        "type": "string",
                        "description": "Image quality.",
                        "enum": ["standard", "hd"],
                    },
                    "style": {
                        "type": "string",
                        "description": "Image style.",
                        "enum": ["vivid", "natural"],
                    },
                },
                "required": ["prompt"],
                "additionalProperties": False,
            },
        )
        async def refine_image(
            prompt: str,
            size: str = "",
            quality: str = "",
            style: str = "",
        ) -> dict:
            """Refine a previously generated image with adjusted parameters.

            Args:
                prompt: Complete refined prompt with the user's changes incorporated.
                size: Image dimensions.
                quality: Image quality.
                style: Image style.
            """
            effective_size = size or _cfg("defaultSize", "1024x1024")
            effective_quality = quality or _cfg("defaultQuality", "hd")
            effective_style = style or _cfg("defaultStyle", "vivid")

            return await _generate(ctx, prompt, effective_size, effective_quality, effective_style)

        @skill(
            name="remix_image",
            description=(
                "Reimagine the same subject with a completely different artistic "
                "direction. Rewrites the prompt to explore a new style, medium, "
                "or aesthetic while keeping the core concept. Use for 'try a "
                "different style', 'watercolor version', 'cyberpunk take', "
                "'make it minimalist', etc."
            ),
            category="creative",
            tags=["image", "remix", "style", "variation", "artifact"],
            side_effects=False,
            requires_network=True,
            display_name="Remix Image",
            icon="shuffle",
            risk_level=RiskLevel.MODERATE,
            input_schema={
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": (
                            "A completely rewritten prompt that reimagines the "
                            "subject in a new artistic style or direction. Should "
                            "be a full prompt, not a modifier."
                        ),
                    },
                    "size": {
                        "type": "string",
                        "description": "Image dimensions.",
                        "enum": ["1024x1024", "1792x1024", "1024x1792"],
                    },
                    "quality": {
                        "type": "string",
                        "description": "Image quality.",
                        "enum": ["standard", "hd"],
                    },
                    "style": {
                        "type": "string",
                        "description": "Image style.",
                        "enum": ["vivid", "natural"],
                    },
                },
                "required": ["prompt"],
                "additionalProperties": False,
            },
        )
        async def remix_image(
            prompt: str,
            size: str = "",
            quality: str = "",
            style: str = "",
        ) -> dict:
            """Reimagine a subject with a new artistic direction.

            Args:
                prompt: Completely rewritten prompt with new artistic style.
                size: Image dimensions.
                quality: Image quality.
                style: Image style.
            """
            effective_size = size or _cfg("defaultSize", "1024x1024")
            effective_quality = quality or _cfg("defaultQuality", "hd")
            effective_style = style or _cfg("defaultStyle", "vivid")

            return await _generate(ctx, prompt, effective_size, effective_quality, effective_style)

        return {
            "create_image": create_image.__skill__,
            "refine_image": refine_image.__skill__,
            "remix_image": remix_image.__skill__,
        }
