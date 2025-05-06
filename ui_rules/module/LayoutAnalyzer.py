import json
import statistics
from typing import List, Tuple, Optional, Union
from dataclasses import dataclass
from functools import cached_property

@dataclass
class Detection:
    x: float
    y: float
    width: float
    height: float
    confidence: float
    class_label: str
    class_id: int
    detection_id: str

    @property
    def center(self) -> Tuple[float, float]:
        return (self.x + self.width / 2, self.y + self.height / 2)

    def __repr__(self) -> str:
        return f"Detection({self.class_label}, id={self.detection_id[:6]}, conf={self.confidence:.2f})"

    def iou(self, other: 'Detection') -> float:
        x1, y1 = max(self.x, other.x), max(self.y, other.y)
        x2, y2 = min(self.x + self.width, other.x + other.width), min(self.y + self.height, other.y + other.height)
        inter_area = max(0, x2 - x1) * max(0, y2 - y1)
        area1 = self.width * self.height
        area2 = other.width * other.height
        return inter_area / (area1 + area2 - inter_area + 1e-6)


class LayoutAnalyzer:
    def __init__(self, predictions_json: str):
        data = json.loads(predictions_json)
        self.detections: List[Detection] = [
            Detection(
                x=p['x'], y=p['y'], width=p['width'], height=p['height'],
                confidence=p['confidence'], class_label=p['class'],
                class_id=p['class_id'], detection_id=p['detection_id']
            ) for p in data.get("predictions", [])
        ]
        self.centers = [det.center for det in self.detections]

    def _cluster_1d(self, values: List[float], tol: float, min_cluster_size: int = 2) -> List[float]:
        if not values:
            return []
        sorted_vals = sorted(values)
        clusters = [[sorted_vals[0]]]
        for v in sorted_vals[1:]:
            if abs(v - clusters[-1][-1]) <= tol:
                clusters[-1].append(v)
            else:
                clusters.append([v])
        return [statistics.mean(cluster) for cluster in clusters if len(cluster) >= min_cluster_size]

    @cached_property
    def row_positions(self) -> List[float]:
        return self._cluster_1d([c[1] for c in self.centers], tol=10.0)

    @cached_property
    def column_positions(self) -> List[float]:
        return self._cluster_1d([c[0] for c in self.centers], tol=10.0)

    def get_row_positions(self, tol: float = 10.0) -> List[float]:
        return self._cluster_1d([c[1] for c in self.centers], tol, min_cluster_size=2)

    def get_column_positions(self, tol: float = 10.0) -> List[float]:
        return self._cluster_1d([c[0] for c in self.centers], tol, min_cluster_size=2)

    def generate_grid(
        self, tol_x: float = 10.0, tol_y: float = 10.0, debug: bool = False,
        allow_multi_assign: bool = False, allow_overlaps: bool = True
    ) -> List[List[List[Detection]]]:
        row_pos = self.get_row_positions(tol_y)
        col_pos = self.get_column_positions(tol_x)
        grid: List[List[List[Detection]]] = [[[] for _ in col_pos] for _ in row_pos]

        for det in self.detections:
            cx, cy = det.center
            matched_rows = [i for i, y in enumerate(row_pos) if abs(cy - y) <= tol_y]
            matched_cols = [j for j, x in enumerate(col_pos) if abs(cx - x) <= tol_x]

            if not matched_rows or not matched_cols:
                if debug:
                    print(f"Skipping {det} (center=({cx:.1f},{cy:.1f})) - no grid match within tolerance")
                continue

            targets = [(i, j) for i in matched_rows for j in matched_cols]
            if allow_multi_assign:
                for i, j in targets:
                    if allow_overlaps or not any(det.iou(existing) > 0.5 for existing in grid[i][j]):
                        grid[i][j].append(det)
                        if debug:
                            print(f"Assigning {det} to grid[{i}][{j}] (multi-assign)")
            else:
                i, j = targets[0]
                if allow_overlaps or not any(det.iou(existing) > 0.5 for existing in grid[i][j]):
                    grid[i][j].append(det)
                    if debug:
                        print(f"Assigning {det} to grid[{i}][{j}] (single-assign)")

        return grid

    def check_alignment(self, axis: str = "horizontal", tol: float = 5.0, min_cluster_size: int = 2) -> bool:
        if axis == "horizontal":
            row_pos = self._cluster_1d([c[1] for c in self.centers], tol, min_cluster_size)
            aligned = [
                det for det in self.detections
                if any(abs(det.center[1] - rp) <= tol for rp in row_pos)
            ]
            return len(aligned) > 0 and all(min(abs(det.center[1] - rp) for rp in row_pos) <= tol for det in aligned)

        elif axis == "vertical":
            col_pos = self._cluster_1d([c[0] for c in self.centers], tol, min_cluster_size)
            aligned = [
                det for det in self.detections
                if any(abs(det.center[0] - cp) <= tol for cp in col_pos)
            ]
            return len(aligned) > 0 and all(min(abs(det.center[0] - cp) for cp in col_pos) <= tol for det in aligned)

        else:
            raise ValueError("Axis must be 'horizontal' or 'vertical'")

    def _spacing_stats(self, positions: List[float]) -> float:
        return statistics.mean([j - i for i, j in zip(positions, positions[1:])]) if len(positions) > 1 else 0.0

    def get_spacing_statistics(self) -> Tuple[float, float]:
        return (
            self._spacing_stats(self.get_column_positions()),
            self._spacing_stats(self.get_row_positions())
        )

def report_grid_alignment(analyzer: LayoutAnalyzer, tol_x: float = 10.0, tol_y: float = 10.0) -> None:
    row_pos = analyzer.get_row_positions(tol_y)
    col_pos = analyzer.get_column_positions(tol_x)

    print("\n🧭 Grid Line Positions:")
    print(f"  Horizontal Rows (Y): {['%.1f' % y for y in row_pos]}")
    print(f"  Vertical Columns (X): {['%.1f' % x for x in col_pos]}")

    print("\n📏 Row Alignment Details:")
    for i, y in enumerate(row_pos):
        row_dets = [det for det in analyzer.detections if abs(det.center[1] - y) <= tol_y]
        aligned = all(abs(det.center[1] - y) <= tol_y for det in row_dets)
        print(f"  Row {i} (Y={y:.1f}) - {len(row_dets)} item(s) - {'Aligned' if aligned else '⚠️ Misaligned'}")
        if row_dets:
            print("    " + ", ".join(f"{det.class_label}#{det.detection_id[:6]}" for det in row_dets))

    print("\n🖐️ Column Alignment Details:")
    for j, x in enumerate(col_pos):
        col_dets = [det for det in analyzer.detections if abs(det.center[0] - x) <= tol_x]
        aligned = all(abs(det.center[0] - x) <= tol_x for det in col_dets)
        print(f"  Col {j} (X={x:.1f}) - {len(col_dets)} item(s) - {'Aligned' if aligned else '⚠️ Misaligned'}")
        if col_dets:
            print("    " + ", ".join(f"{det.class_label}#{det.detection_id[:6]}" for det in col_dets))


if __name__ == "__main__":
    with open("./sample/layout_analyzer_sample.json", "r") as f:
        sample_json = f.read()

    print("\n== Version: Single Assignment ==")
    analyzer_single = LayoutAnalyzer(sample_json)
    grid_single = analyzer_single.generate_grid(tol_x=20, tol_y=20, debug=True, allow_multi_assign=False, allow_overlaps=False)
    print(f"\nGrid: {len(grid_single)} rows x {len(grid_single[0]) if grid_single else 0} cols")
    print("Horizontally aligned:", analyzer_single.check_alignment("horizontal", tol=10))
    print("Vertically aligned:", analyzer_single.check_alignment("vertical", tol=10))
    print("Spacing (h, v):", analyzer_single.get_spacing_statistics())
    report_grid_alignment(analyzer_single, tol_x=20, tol_y=20)

    print("\n== Version: Multi Assignment with Overlap ==")
    analyzer_multi = LayoutAnalyzer(sample_json)
    grid_multi = analyzer_multi.generate_grid(tol_x=20, tol_y=20, debug=True, allow_multi_assign=True, allow_overlaps=True)
    print(f"\nGrid: {len(grid_multi)} rows x {len(grid_multi[0]) if grid_multi else 0} cols")
    print("Horizontally aligned:", analyzer_multi.check_alignment("horizontal", tol=10))
    print("Vertically aligned:", analyzer_multi.check_alignment("vertical", tol=10))
    print("Spacing (h, v):", analyzer_multi.get_spacing_statistics())
    report_grid_alignment(analyzer_multi, tol_x=20, tol_y=20)
