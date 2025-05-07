import uuid
import json
import base64
import io
from typing import List, Dict, Any
from PIL import Image
import numpy as np
from ultralytics import YOLO


class UIComponentDetector:
    def __init__(self, model_path: str='module/model/ui_component_models_weights.pt'):
        self.model = YOLO(model_path)
        self.class_names = self.model.names

    def _load_image_from_base64(self, base64_str: str) -> np.ndarray:
        image_data = base64.b64decode(base64_str)
        image = Image.open(io.BytesIO(image_data)).convert("RGB")
        return np.array(image)

    def detect_from_base64(self, base64_str: str) -> Dict[str, List[Dict[str, Any]]]:
        image = self._load_image_from_base64(base64_str)
        results = self.model(image)[0]

        predictions = []
        for box in results.boxes:
            cls_id = int(box.cls[0].item())
            class_name = self.class_names[cls_id]
            confidence = float(box.conf[0].item())
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            x_center = round((x1 + x2) / 2, 1)
            y_center = round((y1 + y2) / 2, 1)
            width = int(round(x2 - x1))
            height = int(round(y2 - y1))

            predictions.append({
                "x": x_center,
                "y": y_center,
                "width": width,
                "height": height,
                "confidence": round(confidence, 3),
                "class": class_name,
                "class_id": cls_id,
                "detection_id": str(uuid.uuid4())
            })

        return {"predictions": predictions}

    def detect_base64_as_json(self, base64_str: str) -> str:
        result = self.detect_from_base64(base64_str)
        return json.dumps(result, indent=2)


# Example usage:
if __name__ == "__main__":
    with open("sample/sample_2.png", "rb") as img_file:
        base64_str = base64.b64encode(img_file.read()).decode("utf-8")
    detector = UIComponentDetector()
    print(detector.detect_base64_as_json(base64_str))