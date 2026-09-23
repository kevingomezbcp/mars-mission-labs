import zipfile
import xml.etree.ElementTree as ET

with zipfile.ZipFile("Miercoles de IA - Agent Framework - 10-06-2026.pptx", 'r') as z:
    for i in range(1, 15):
        slide_xml_name = f"ppt/slides/slide{i}.xml"
        if slide_xml_name in z.namelist():
            xml_data = z.read(slide_xml_name)
            print(f"=== SLIDE {i} XML LENGTH: {len(xml_data)} ===")
            root = ET.fromstring(xml_data)
            
            # Check bg
            bg = root.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}bg')
            if bg is not None:
                print(f"  Slide {i} has explicit <p:bg>!")
                print(ET.tostring(bg, encoding='unicode')[:300])
            else:
                print(f"  Slide {i} has NO explicit <p:bg> (inherits from layout/master)")
                
            # Check rels
            rels_name = f"ppt/slides/_rels/slide{i}.xml.rels"
            if rels_name in z.namelist():
                rels_xml = z.read(rels_name)
                print(f"  Rels for slide {i}:")
                r_root = ET.fromstring(rels_xml)
                for r in r_root:
                    print(f"    rId={r.get('Id')} type={r.get('Type').split('/')[-1]} target={r.get('Target')}")
