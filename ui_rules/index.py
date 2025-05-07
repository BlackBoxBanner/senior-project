import base64
from typing import Tuple

from module.ColorModule import ColorModule
from module.UIComponentDetector import UIComponentDetector
from module.LayoutAnalyzer import LayoutAnalyzer, AxisEnum

# === Load and Convert Local Image to Base64 ===
def image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")
        
# === Example Usage ===
image_path = "sample/sample_4.png"
base64_str = image_to_base64(image_path)

# Run detection and analysis
ui_detector = UIComponentDetector(confidence_threshold=0, iou_threshold=0)
detected_ui = ui_detector.detect_from_base64(base64_str)

cm = ColorModule(base64_str, detections=detected_ui)
la = LayoutAnalyzer(detected_ui, tol_x=20, tol_y=20)

# Generate grid and collect skipped detections
image_grid, skipped_detections = la.generate_grid_with_skipped(
    tol_x=20, tol_y=20, allow_multi_assign=True, debug=False, allow_overlaps=True
)

row_count = len(image_grid)
col_count = len(image_grid[0]) if image_grid else 0

# Misalignment details (actual misalign + skipped)
row_misaligned, row_skipped = la.get_misaligned_and_skipped(AxisEnum.HORIZONTAL)
col_misaligned, col_skipped = la.get_misaligned_and_skipped(AxisEnum.VERTICAL)

h_score = la.calculate_misalignment_percentage(AxisEnum.HORIZONTAL)
v_score = la.calculate_misalignment_percentage(AxisEnum.VERTICAL)
col_spacing, row_spacing = la.get_spacing_statistics()


# Color analysis
color_content = cm.extract_dominant_colors()
color_content_percent = cm.calculate_percentages(color_content)
color_contrast = cm.contrast_ratio(
    color1=color_content[0][0],
    color2=color_content[1][0]
)

# === Report ===
print("=== UI Layout Analysis ===")
print(f"\nRow Count: {row_count}")
print(f"Misaligned Rows: {len(row_misaligned)} | Skipped: {len(row_skipped)}")

print(f"Column Count: {col_count}")
print(f"Misaligned Columns: {len(col_misaligned)} | Skipped: {len(col_skipped)}")
# Calculate misalignment percentages

print(f"\n📈 Alignment Scores:")
print(f"\tHorizontal Misalignment: {h_score}%")
print(f"\tVertical Misalignment: {v_score}%")

# Spacing statistics (average gaps)
print(f"\n📐 Average Spacing:")
print(f"\tColumns: {col_spacing:.2f}px")
print(f"\tRows: {row_spacing:.2f}px")

print("\n🎨 Dominant Colors:")
for rgb, percent in color_content_percent:
    r, g, b = rgb
    # ANSI escape: \033[48;2;<r>;<g>;<b>m for background color
    color_block = f"\033[48;2;{r};{g};{b}m     \033[0m"
    print(f"  {color_block} RGB: ({r}, {g}, {b}) - {percent}%")

print(f"Contrast Ratio: {color_contrast}/1")