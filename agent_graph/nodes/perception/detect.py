from pathlib import Path
from typing import List
from PIL import Image
from langchain_core.tools import tool
from ultralytics import YOLO

from agent_graph.state_schema import AgentState, ObjectBox
from common.config_loader import load_config

# 缓存模型（加载一次）
_yolo_model = None

def get_yolo_model() -> YOLO:
    global _yolo_model
    if _yolo_model is None:
        config = load_config()
        project_root = Path(__file__).resolve().parents[3]
        model_path = (project_root / config['yolo']['model_path']).resolve()
        if not model_path.exists():
            raise FileNotFoundError(f"未找到 YOLO 模型文件：{model_path}")
        _yolo_model = YOLO(str(model_path))
    return _yolo_model


@tool
def detect_objects(image_path: str) -> List[ObjectBox]:
    """
    使用YOLOv8模型检测图像中的物体，返回每个物体的标签、置信度和边界框。
    """
    model = get_yolo_model()
    # 加载图片
    image = Image.open(image_path)
    # 执行检测
    results = model(image)
    boxes = results[0].boxes
    cls_names = results[0].names
    seen_labels = set()
    detected_objects = []
    for i in range(len(boxes)):
        box = boxes[i]
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        confidence = box.conf[0].item()
        class_id = int(box.cls[0].item())
        label = cls_names[class_id]
        if label in seen_labels:
            continue
        seen_labels.add(label)
        detected_objects.append({
            "label": label,
            "confidence": confidence,
            "bbox": [x1, y1, x2, y2]
        })
    return detected_objects

# LangGraph 节点函数
def detect_node(state: AgentState) -> AgentState:
    if not state.get("image_path"):
        raise ValueError("image_path 未提供，无法执行检测")
    print("\n=============================[Perception Message]===============================\n")
    print(f"正在识别图像:{state.get('image_path')}")
    objects = detect_objects.invoke(state["image_path"])
    print("检查到如下物体：")
    for i, obj in enumerate(objects, 1):
        print(f"[{i}] 类别: {obj.get('label')} | 置信度: {obj.get('confidence'):.2f} | 位置: {obj.get('bbox')}")
    new_state = state.copy()
    new_state["objects"] = objects
    return new_state

if __name__ == '__main__':
    path = "D:\\User\\zhangruipeng\\PycharmProjects\\PBAgent\\data\\test1.jpg"
    res = detect_objects.invoke(path)
    print("检测到的物体列表:")
    for i, obj in enumerate(res, 1):
        print(f"[{i}] 类别: {obj.get('label')} | 置信度: {obj.get('confidence'):.2f} | 位置: {obj.get('bbox')}")