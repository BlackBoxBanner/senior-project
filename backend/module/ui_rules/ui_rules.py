from .color import ColorModule


class UIRulesModule:
    def __init__(self, image_path: str):
        """
        Initialize the UIRulesModule with the image path and color module.
        :param image_path: Path to the image file.
        """
        self.color_module = ColorModule(image_path)

    def check_60_30_10_rule(self):
        """
        Check if the extracted dominant colors follow the 60-30-10 UI rule.

        Returns:
            result (dict): Dictionary with rule validation and detailed breakdown.
        """
        dominant_colors = self.color_module.extract_dominant_colors()

        # Sort colors by percentage (descending)
        dominant_colors = sorted(
            dominant_colors, key=lambda x: x["percentage"], reverse=True
        )

        # Assign roles: Primary (60%), Secondary (30%), Accent (10%)
        primary = dominant_colors[0]
        secondary = (
            dominant_colors[1]
            if len(dominant_colors) > 1
            else {"color": None, "percentage": 0}
        )
        accent = (
            dominant_colors[2]
            if len(dominant_colors) > 2
            else {"color": None, "percentage": 0}
        )

        # Check if the percentages roughly follow the 60-30-10 rule
        primary_ok = 50 <= primary["percentage"] <= 70
        secondary_ok = 20 <= secondary["percentage"] <= 40
        accent_ok = 5 <= accent["percentage"] <= 15

        return {
            "primary_color": primary,
            "secondary_color": secondary,
            "accent_color": accent,
            "rule_followed": primary_ok and secondary_ok and accent_ok,
            "details": {
                "primary_ok": primary_ok,
                "secondary_ok": secondary_ok,
                "accent_ok": accent_ok,
            },
        }
