import yaml
from pathlib import Path

_config_cache = None

def load_config():
    global _config_cache
    if _config_cache is None:
        # 项目根目录
        project_root = Path(__file__).resolve().parents[1]
        config_path = project_root / 'config.yaml'
        if not config_path.exists():
            raise FileNotFoundError(f"配置文件未找到： {config_path}")
        with open(config_path, 'r', encoding="utf-8") as f:
            _config_cache = yaml.safe_load(f)
    return _config_cache


if __name__ == '__main__':
    print(load_config())