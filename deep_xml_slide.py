import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile("Miercoles de IA - Agent Framework - 10-06-2026.pptx", 'r') as z:
    for s_idx in [1, 2, 3]:
        print(f"\n{'='*30} SLIDE {s_idx} XML {'='*30}")
        xml_data = z.read(f"ppt/slides/slide{s_idx}.xml")
        root = ET.fromstring(xml_data)
        
        # Pretty print elements
        for elem in root.iter():
            tag = elem.tag.split('}')[-1]
            if tag in ['bg', 'tbl', 'tblPr', 'tcPr', 'ln', 'solidFill', 'srgbClr', 'schemeClr', 'rPr', 'pPr', 'tblStyleId']:
                attrs = ' '.join([f"{k.split('}')[-1]}='{v}'" for k, v in elem.attrib.items()])
                text = elem.text.strip() if elem.text and elem.text.strip() else ""
                print(f"  <{tag} {attrs}>{text}")
