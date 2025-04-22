from .color import ColorModule


class UIRulesModule:
    def __init__(self, image_byte: bytes):
        """
        Initialize the UIRulesModule with the image path and color module.
        :param image_path: Path to the image file.
        """
        self.color_module = ColorModule(image_byte)

    def check_60_30_10_rule(self, acceptable_range=5):
        """
        Check if the extracted dominant colors follow the 60-30-10 UI rule.

        Returns:
            result (dict): Dictionary with rule validation and detailed breakdown.
        """
        dominant_colors = self.color_module.extract_dominant_colors()

        # Convert the list of colors to a list of dictionaries with percentages
        total_pixels = sum([color[1] for color in dominant_colors])
        dominant_colors = [
            {"color": color[0], "percentage": color[1] / total_pixels * 100}
            for color in dominant_colors
        ]

        dominant_colors = sorted(
            dominant_colors, key=lambda x: x["percentage"], reverse=True
        )

        primary = dominant_colors[0]["color"]
        secondary = dominant_colors[1]["color"]
        accent = dominant_colors[2]["color"]

        primary_ok = (
            60 - acceptable_range
            <= dominant_colors[0]["percentage"]
            <= 60 + acceptable_range
        )
        secondary_ok = (
            30 - acceptable_range
            <= dominant_colors[1]["percentage"]
            <= 30 + acceptable_range
        )
        accent_ok = (
            10 - acceptable_range
            <= dominant_colors[2]["percentage"]
            <= 10 + acceptable_range
        )

        return {
            "primary_color": {
                "color": primary,
                "percentage": dominant_colors[0]["percentage"],
            },
            "secondary_color": {
                "color": secondary,
                "percentage": dominant_colors[1]["percentage"],
            },
            "accent_color": {
                "color": accent,
                "percentage": dominant_colors[2]["percentage"],
            },
            "rule_followed": bool(primary_ok and secondary_ok and accent_ok),
            "details": {
                "primary_ok": bool(primary_ok),
                "secondary_ok": bool(secondary_ok),
                "accent_ok": bool(accent_ok),
            },
        }
