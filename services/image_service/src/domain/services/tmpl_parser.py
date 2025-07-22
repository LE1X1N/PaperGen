import random
from pathlib import Path


class TemplateParser:
    def __init__(self):

        self.base_dir = Path(__file__).parent.parent.parent.parent / "templates"  
        
        self.style_map = {
            0 : self.base_dir / "web", 
            1 : self.base_dir / "app",
            2 : self.base_dir / "wechat"
        }
        
        self.tmpl_paths = {
            0 : list(self.style_map[0].rglob("*.jsx")),
            1 : list(self.style_map[1].rglob("*.jsx")),
            2 : list(self.style_map[2].rglob("*.jsx"))
        }

    def load_template(self, style: int=0):   
        # random choose one .jsx template based on style
        # style: 
        #      0: web     网站类
        #      1: app     手机应用类
        #      2: wechat  微信小程序类
        path = random.choice(self.tmpl_paths[style])  
              
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        return content
        