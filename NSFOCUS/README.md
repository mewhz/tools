## 简介

把该脚本放在绿盟 html 漏扫报告的根目录，即和 index.html 同一层

```bash
pip install lxml
pip install openpyxl
```

安装依赖后运行

```python
python main.py
```

运行结束后会生成 Excel 文件，会把报告里面的中高危漏洞，包含漏洞名称、漏洞详情、修复方案写入到 Excel 中。方便整理报告