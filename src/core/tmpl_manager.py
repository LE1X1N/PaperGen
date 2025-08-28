from pathlib import Path
import os
import random


class TemplateManager:
    def __init__(self):

        self.base_dir = Path(__file__).parent.parent.parent / "static"  
        
        self.tmpl_dirs = {
            0 : [self.base_dir / dir for dir in ["上中下布局", "侧边布局", "顶部-侧边布局"]], 
            1 : [self.base_dir / dir for dir in ["小程序"]]
        }
        
        self.tmpl_paths = {
            0 : [tmpl_dir / file for tmpl_dir in self.tmpl_dirs[0] for file in os.listdir(tmpl_dir) if file.endswith(".jsx")],
            1 : [tmpl_dir / file for tmpl_dir in self.tmpl_dirs[1] for file in os.listdir(tmpl_dir) if file.endswith(".jsx")]
        }

    def load_template(self, style: int=0):   
        # random choose one .jsx template based on style
        # style: 
        #      0: 网站
        #      1: 小程序     
        path = random.choice(self.tmpl_paths[style])  
              
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        return content
        