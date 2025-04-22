## C. Update Issues
- Change to complete 1 technique at a time.
- Create specialize Image Processing (Image Segmentation) for task.
- Create simple website to help gather information and notate image before train ml model.

### Problem and Solution
- Problem: Overfitting in the ML model.
  - Solution: Fine-tune the K-Means algorithm and use ML image segmentation to improve color accuracy.

#### Workflow
1. Using k-means to pick dominant color and percentage.
  - Not accurate on some images.
  - Using hex color codes.
2. Implement custom RGB to HEX function.
  - Not accurate.
3. Try different ways to extract color from image.
  - Using images from PIL and removing background using OpenCV.
4. Train ML to select colors.
  - Not the best approach.
  - Task too simple.
  - Overfitting.
5. Change back to K-Means but do some fine-tuning.
6. Use ML image segmentation to select regions within the image and remove those sections. This ensures that when using the K-Means function, colors from the image do not interfere with the dominant colors.

### List of Features
- Image upload and preview.
- Color picker for primary, secondary, and accent colors.
- Save and export color data.
- Display color percentages.
- Image segmentation to improve color accuracy (Not complete).
- Fine-tuned K-Means algorithm for better color extraction.
- User-friendly interface for selecting and annotating images.
- Integration with backend for storing and retrieving color data.

### List of Deliverable
- Start creating project structure: Frontend, Backend, Train ML.
  - Frontend: Mimic final project data pipeline, test, and data visualizer.
  - Backend: UI Rules algorithm and ML Model.

### Project Plan and Workload
- No changes.