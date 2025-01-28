from module.ui_rules import UIRulesModule
import os


def print_color_box(color, text):
    """
    Print a color box next to the text in the terminal.
    :param color: Tuple (R, G, B) representing the color.
    :param text: Text to display next to the color box.
    """
    r, g, b = color
    print(f"\033[48;2;{r};{g};{b}m  \033[0m {text}")


def main():

    # Path to your image
    # image_path = os.path.join("image", "Screenshot 2568-01-03 at 18.30.33.png")
    # image_path = os.path.join("image", "40-40-20-blank.png")
    image_path = os.path.join("image", "Screenshot 2568-01-04 at 20.26.38.png")

    ui_rules_module = UIRulesModule(image_path)
    rule_result = ui_rules_module.check_60_30_10_rule()

    print("UI Color Rule Validation:")
    print_color_box(
        rule_result["primary_color"]["color"],
        f"Primary Color: {rule_result['primary_color']}",
    )
    print_color_box(
        rule_result["secondary_color"]["color"],
        f"Secondary Color: {rule_result['secondary_color']}",
    )
    print_color_box(
        rule_result["accent_color"]["color"],
        f"Accent Color: {rule_result['accent_color']}",
    )
    print(f"Follows 60-30-10 Rule: {rule_result['rule_followed']}")
    print(f"Details: {rule_result['details']}")


if __name__ == "__main__":
    main()
