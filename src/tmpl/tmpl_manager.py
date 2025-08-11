from pathlib import Path

class TemplateManager:
    def __init__(self):
        
        self.tmpl_dir = Path(__file__).parent / "static"
        self.style_map = {
            0: "小程序模板.jsx",
            1: "网页模板-管理系统（上下）.jsx",
            2: "网页模板-管理系统（左右）.jsx"
        }
        self._cache = {}

    def load_template(self, style: int=0):
        # read cache
        if style in self._cache:
            return self._cache[style]
        
        path = self.tmpl_dir / self.style_map.get(style)
        if not path:
            raise ValueError(f"未知模板：{style}")
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        self._cache[style] = content  
        return content
        