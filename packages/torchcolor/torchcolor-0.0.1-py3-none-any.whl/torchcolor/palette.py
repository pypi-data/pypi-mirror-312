from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, ClassVar, Dict, Union

from .color import Color, reset_color, hex_to_rgb

@dataclass
class Palette:
    """Palette dataclass that stores a palette name and a list of colors"""
    _registry: ClassVar[Dict[str, "Palette"]] = {}

    name: str
    colors: List[Color]
    disable_registry: bool = field(default=False, repr=False)

    def __post_init__(self):
        """Automatically register the new palette."""
        if not self.disable_registry:
            if self.name in Palette._registry:
                raise ValueError(f"A palette named '{self.name}' is already registered.")
            Palette._registry[self.name] = self

    @classmethod
    def get_palette(cls, name: str) -> "Palette":
        """Retrieve a palette by name."""
        return cls._registry.get(name)

    @classmethod
    def get(cls, name: str) -> "Palette":
        """Retrieve a palette by name."""
        if name in cls._registry:
            return cls._registry.get(name)
        raise NameError(f"Palette '{name}' does not exist")

    def __getitem__(self, index: int) -> Color:
        """Get a color by index, cycling through the palette."""
        return self.colors[index % len(self.colors)]

    def generate_gradient(self, n: int) -> List[Color]:
        """Generate a gradient of `n` colors, ensuring the first and last colors are from the palette."""
        gradient_colors = []
        total_palette_colors = len(self.colors)

        # If n is smaller than the number of colors in the palette, just return the existing colors
        if n <= total_palette_colors:
            return [self.colors[i % total_palette_colors] for i in range(n)]

        # Number of interpolated colors between two anchor colors
        steps = n // (total_palette_colors - 1)

        # Interpolate between consecutive colors in the palette
        # Gradient not working for non RGB or HEX color
        for i in range(total_palette_colors - 1):
            color1_rgb = hex_to_rgb(self.colors[i].value) if isinstance(self.colors[i].value, str) else self.colors[i].value
            color2_rgb = hex_to_rgb(self.colors[i + 1].value) if isinstance(self.colors[i + 1].value, str) else self.colors[i + 1].value

            for step in range(steps):
                r = int(color1_rgb[0] + (color2_rgb[0] - color1_rgb[0]) * step / steps)
                g = int(color1_rgb[1] + (color2_rgb[1] - color1_rgb[1]) * step / steps)
                b = int(color1_rgb[2] + (color2_rgb[2] - color1_rgb[2]) * step / steps)
                gradient_colors.append(Color((r, g, b)))

        # Add the last color in the palette if there are any remaining colors needed
        gradient_colors.append(self.colors[-1])

        return gradient_colors


# List of preset palettes

palette_warm_sunset = Palette(
    "warm_sunset", [
        Color("#FF4500"),  # Orange Red
        Color("#FF6347"),  # Tomato
        Color("#FF7F50"),  # Coral
        Color("#FFD700"),  # Gold
        Color("#FF1493")   # Deep Pink
    ]
)
palette_ocean_breeze = Palette(
    "ocean_breeze", [
        Color("#00CED1"),  # Dark Turquoise
        Color("#20B2AA"),  # Light Sea Green
        Color("#48D1CC"),  # Medium Turquoise
        Color("#40E0D0"),  # Turquoise
        Color("#7FFFD4")   # Aquamarine
    ]
)
palette_forest_greens = Palette(
    "forest_greens", [
        Color("#228B22"),  # Forest Green
        Color("#006400"),  # Dark Green
        Color("#2E8B57"),  # Sea Green
        Color("#8FBC8F"),  # Dark Sea Green
        Color("#98FB98")   # Pale Green
    ]
)
palette_lavender_dreams = Palette(
    "lavender_dreams", [
        Color("#E6E6FA"),  # Lavender
        Color("#D8BFD8"),  # Thistle
        Color("#C71585"),  # Medium Violet Red
        Color("#9932CC"),  # Dark Orchid
        Color("#8A2BE2")   # Blue Violet
    ]
)
palette_autumn_foliage = Palette(
    "autumn_foliage", [
        Color("#FF4500"),  # Orange Red
        Color("#8B4513"),  # Saddle Brown
        Color("#A52A2A"),  # Brown
        Color("#D2691E"),  # Chocolate
        Color("#FFD700")   # Gold
    ]
)
palette_pastel = Palette(
    "pastel", [
        Color("#FFB6C1"),  # Light Pink
        Color("#B0E0E6"),  # Powder Blue
        Color("#98FB98"),  # Pale Green
        Color("#FFFACD"),  # Lemon Chiffon
        Color("#F0E68C")   # Khaki
    ]
)
palette_retro_neon = Palette(
    "retro_neon", [
        Color("#FF00FF"),  # Magenta
        Color("#00FF00"),  # Lime
        Color("#FFFF00"),  # Yellow
        Color("#000000"),  # Black
        Color("#00FFFF"),  # Cyan
        Color("#FF0000")   # Red
    ]
)
palette_monochrome = Palette(
    "monochrome", [
        Color("#000000"),  # Black
        Color("#404040"),  # Dark Gray
        Color("#808080"),  # Gray
        Color("#B0B0B0"),  # Light Gray
        Color("#FFFFFF")   # White
    ]
)
palette_rainbow = Palette(
    "rainbow", [
        Color("#FF0000"),  # Red
        Color("#FF7F00"),  # Orange
        Color("#FFFF00"),  # Yellow
        Color("#00FF00"),  # Green
        Color("#0000FF"),  # Blue
        Color("#A50052"),  # Indigo
        Color("#9400D3")   # Violet
    ]
)