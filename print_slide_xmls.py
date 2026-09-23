import zipfile

with zipfile.ZipFile("Miercoles de IA - Agent Framework - 10-06-2026.pptx", 'r') as z:
    s1_xml = z.read("ppt/slides/slide1.xml").decode('utf-8')
    s2_xml = z.read("ppt/slides/slide2.xml").decode('utf-8')
    s3_xml = z.read("ppt/slides/slide3.xml").decode('utf-8')

print("=== SLIDE 1 FULL XML ===")
print(s1_xml)

print("\n=== SLIDE 2 TABLE XML ===")
# Extract tbl element from slide 2
start = s2_xml.find('<a:tbl>')
end = s2_xml.find('</a:tbl>') + len('</a:tbl>')
if start != -1 and end != -1:
    print(s2_xml[start:end])
else:
    print(s2_xml)
