from module.color import ColorModule

cm = ColorModule()
img = cm.load_image("ui_rules/image/sample_2.png")
img_resized = cm.resize_image(img, (300, 300))
img_no_bg = cm.remove_background(img_resized)

dominant = cm.extract_dominant_colors(img_no_bg, color_number=3)
dominant_percent = cm.check_percent(dominant)

contrast = cm.contrast_ratio(dominant_percent[0][0], dominant_percent[1][0])

print(dominant_percent)
print(f'Contrast ratio: {contrast:.2f}/1')
# cm.plot_colors(dominant_percent)
# cm.save_colors(dominant_percent, "ui_rules/dominant_colors.txt")
