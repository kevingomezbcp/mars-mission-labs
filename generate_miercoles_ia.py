"""
Generador e Ingeniería Inversa de la Presentación:
'Miércoles de IA - Agent Framework'

Entorno: rag_demo_bcp (Python con python-pptx)
Genera: Miercoles_de_IA_Agent_Framework_Reverse_Engineered.pptx
"""

import os
import sys
import zipfile
import pptx
from pptx.util import Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.oxml import parse_xml

# Constantes de rutas
ORIGINAL_PPTX = "Miercoles de IA - Agent Framework - 10-06-2026.pptx"
TEMPLATE_PPTX = "template_miercoles_ia.pptx"
OUTPUT_PPTX = "Miercoles_de_IA_Agent_Framework_Reverse_Engineered.pptx"
ASSETS_DIR = "extracted_assets"

# Paleta de Colores Corporativa (Tema CREDICORP)
COLOR_MAGENTA = RGBColor(0xC3, 0x33, 0x8E)   # Acento Principal (Magenta BCP)
COLOR_CYAN = RGBColor(0x2A, 0xD2, 0xC9)      # Acento Secundario (Turquesa/Cian)
COLOR_DARK = RGBColor(0x33, 0x33, 0x33)      # Texto Oscuro Principal
COLOR_GRAY = RGBColor(0x55, 0x55, 0x55)      # Texto Secundario (Gris)
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)     # Blanco

# Tipografías Corporativas
FONT_PRIMARY = "Inter Tight"
FONT_PRIMARY_BLACK = "Inter Tight Black"
FONT_PRIMARY_LIGHT = "Inter Tight Light"


def extract_assets(pptx_path=ORIGINAL_PPTX, output_dir=ASSETS_DIR):
    """Extrae automáticamente todos los recursos multimedia (imágenes, gráficos) del archivo PPTX."""
    os.makedirs(output_dir, exist_ok=True)
    with zipfile.ZipFile(pptx_path, 'r') as z:
        for filename in z.namelist():
            if filename.startswith('ppt/media/'):
                target_path = os.path.join(output_dir, os.path.basename(filename))
                with open(target_path, 'wb') as f:
                    f.write(z.read(filename))
    print(f"[OK] Recursos extraídos en '{output_dir}'")


def create_clean_template(src_pptx=ORIGINAL_PPTX, template_pptx=TEMPLATE_PPTX):
    """Crea una plantilla base limpia eliminando las diapositivas pero conservando temas y layouts."""
    prs = pptx.Presentation(src_pptx)
    sldIdLst = prs.slides._sldIdLst
    for sldId in list(sldIdLst):
        rId = sldId.rId
        prs.part.drop_rel(rId)
        sldIdLst.remove(sldId)
    prs.save(template_pptx)
    print(f"[OK] Plantilla limpia generada en '{template_pptx}'")


def get_asset(filename):
    """Retorna la ruta absoluta del asset solicitado."""
    path = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(path):
        extract_assets()
    return path


def set_slide_background_image(slide, image_path):
    """Establece una imagen como fondo nativo de la diapositiva usando OpenXML blipFill dentro de <p:cSld>."""
    image_part, rId = slide.part.get_or_add_image_part(image_path)
    p_bg = parse_xml(f'''
        <p:bg xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
              xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
              xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
            <p:bgPr>
                <a:blipFill dpi="0" rotWithShape="1">
                    <a:blip r:embed="{rId}">
                        <a:lum/>
                    </a:blip>
                    <a:srcRect/>
                    <a:stretch>
                        <a:fillRect/>
                    </a:stretch>
                </a:blipFill>
                <a:effectLst/>
            </p:bgPr>
        </p:bg>
    ''')
    cSld = slide._element.xpath('./p:cSld')[0]
    for old_bg in cSld.xpath('./p:bg'):
        cSld.remove(old_bg)
    cSld.insert(0, p_bg)


def remove_placeholder(slide, placeholder_idx):
    """Elimina un placeholder específico de la diapositiva si no se requiere."""
    for ph in list(slide.placeholders):
        if ph.placeholder_format.idx == placeholder_idx:
            sp = ph._element
            sp.getparent().remove(sp)


def remove_all_placeholders(slide):
    """Elimina todos los placeholders de una diapositiva."""
    for ph in list(slide.placeholders):
        sp = ph._element
        sp.getparent().remove(sp)


def set_title(slide, title_text):
    """Configura el título de la diapositiva con la tipografía y color magenta corporativo."""
    title_ph = slide.placeholders[0]
    tf = title_ph.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.space_before = Pt(0)
    p.space_after = Pt(0)
    r = p.add_run()
    r.text = title_text
    r.font.name = FONT_PRIMARY_BLACK
    r.font.size = Pt(28)
    r.font.bold = True
    r.font.color.rgb = COLOR_MAGENTA


def add_section_subtitle(slide, subtitle_text):
    """Agrega el subtítulo de la sección en color magenta corporativo."""
    tb = slide.shapes.add_textbox(Emu(359999), Emu(1281299), Emu(11324085), Emu(332399))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.space_before = Pt(0)
    p.space_after = Pt(0)
    r = p.add_run()
    r.text = subtitle_text
    r.font.name = FONT_PRIMARY_BLACK
    r.font.size = Pt(24)
    r.font.bold = True
    r.font.color.rgb = COLOR_MAGENTA
    return tb


def format_agenda_table(table_shape):
    """Aplica el estilo limpio sin rellenos con líneas horizontales divisorias finas (tx1)."""
    tblPr = table_shape._element.xpath('.//a:tblPr')[0]
    tblPr.set('bandRow', '1')
    if 'firstRow' in tblPr.attrib:
        del tblPr.attrib['firstRow']
        
    if not tblPr.xpath('./a:noFill'):
        tblPr.insert(0, parse_xml('<a:noFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'))

    table = table_shape.table
    num_rows = len(table.rows)

    for r_i, row in enumerate(table.rows):
        for c_i, cell in enumerate(row.cells):
            tcPr = cell._tc.get_or_add_tcPr()
            # Eliminar rellenos existentes
            for f in tcPr.xpath('./a:solidFill | ./a:gradFill | ./a:pattFill'):
                tcPr.remove(f)
            if not tcPr.xpath('./a:noFill'):
                tcPr.append(parse_xml('<a:noFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'))

            # Limpiar bordes previos
            for border_tag in ['lnL', 'lnR', 'lnT', 'lnB']:
                for b in tcPr.xpath(f'./a:{border_tag}'):
                    tcPr.remove(b)

            # Bordes: laterales transparentes, superior e inferior finos tx1
            tcPr.append(parse_xml('<a:lnL xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" w="12700"><a:noFill/></a:lnL>'))
            tcPr.append(parse_xml('<a:lnR xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" w="12700"><a:noFill/></a:lnR>'))

            if r_i == 0:
                tcPr.append(parse_xml('<a:lnT xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" w="6350"><a:noFill/></a:lnT>'))
            else:
                tcPr.append(parse_xml('<a:lnT xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" w="6350"><a:solidFill><a:schemeClr val="tx1"/></a:solidFill></a:lnT>'))

            if r_i == num_rows - 1:
                tcPr.append(parse_xml('<a:lnB xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" w="6350"><a:noFill/></a:lnB>'))
            else:
                tcPr.append(parse_xml('<a:lnB xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" w="6350"><a:solidFill><a:schemeClr val="tx1"/></a:solidFill></a:lnB>'))


# =============================================================================
# CONSTRUCTORES DE DIAPOSITIVAS
# =============================================================================

def build_slide_1(prs, layouts):
    """Slide 1: Carátula Principal con imagen de fondo completa."""
    slide = prs.slides.add_slide(layouts['CARATULA-01'])
    
    # Fondo con foto de personas (image13.jpg)
    set_slide_background_image(slide, get_asset("image13.jpg"))
    
    # Título Principal (Blanco)
    tf_title = slide.placeholders[0].text_frame
    tf_title.clear()
    p_title = tf_title.paragraphs[0]
    p_title.space_before = Pt(0)
    p_title.space_after = Pt(0)
    r_title = p_title.add_run()
    r_title.text = "Python + Agents"
    r_title.font.name = FONT_PRIMARY_BLACK
    r_title.font.size = Pt(44)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_WHITE

    # Subtítulo (Blanco)
    tf_sub = slide.placeholders[1].text_frame
    tf_sub.clear()
    p_sub = tf_sub.paragraphs[0]
    r_sub = p_sub.add_run()
    r_sub.text = "Domina el Microsoft Agent Framework 1.0 desde cero"
    r_sub.font.name = FONT_PRIMARY
    r_sub.font.size = Pt(20)
    r_sub.font.color.rgb = COLOR_WHITE
    return slide


def build_slide_2(prs, layouts):
    """Slide 2: Agenda con tabla limpia sin cabecera de color."""
    slide = prs.slides.add_slide(layouts['EN-BLANCO-01'])
    
    # Título Agenda en Magenta
    t_shape = slide.shapes.add_textbox(Emu(360000), Emu(414431), Emu(10515600), Emu(1325563))
    tf_title = t_shape.text_frame
    tf_title.word_wrap = True
    p = tf_title.paragraphs[0]
    p.space_before = Pt(0)
    p.space_after = Pt(0)
    r = p.add_run()
    r.text = "Agenda"
    r.font.name = FONT_PRIMARY_BLACK
    r.font.size = Pt(48)
    r.font.bold = True
    r.font.color.rgb = COLOR_MAGENTA

    # Tabla de 5 filas x 2 columnas
    table_shape = slide.shapes.add_table(5, 2, Emu(1393348), Emu(2047937), Emu(9405305), Emu(4117660))
    table = table_shape.table
    table.columns[0].width = Emu(2463545)
    table.columns[1].width = Emu(6941760)
    for row in table.rows:
        row.height = Emu(823532)

    agenda_items = [
        ("01", "Fundamentos de IA"),
        ("02", "Diferencias entre LLM y Agentes"),
        ("03", "Introducción a Microsoft Agent Framework"),
        ("04", "Componentes clave de MAF"),
        ("05", "Demo: Construcción de un agente"),
    ]

    for row_idx, (num, topic) in enumerate(agenda_items):
        cell_num = table.cell(row_idx, 0)
        cell_num.margin_left = Emu(141446)
        cell_num.margin_right = Emu(141446)
        cell_num.margin_top = Emu(141446)
        cell_num.margin_bottom = Emu(141446)
        tf_num = cell_num.text_frame
        tf_num.clear()
        p_num = tf_num.paragraphs[0]
        r_num = p_num.add_run()
        r_num.text = num
        r_num.font.name = FONT_PRIMARY
        r_num.font.size = Pt(33)
        r_num.font.bold = True
        r_num.font.color.rgb = COLOR_MAGENTA

        cell_topic = table.cell(row_idx, 1)
        cell_topic.margin_left = Emu(141446)
        cell_topic.margin_right = Emu(141446)
        cell_topic.margin_top = Emu(141446)
        cell_topic.margin_bottom = Emu(141446)
        tf_topic = cell_topic.text_frame
        tf_topic.clear()
        p_topic = tf_topic.paragraphs[0]
        p_topic.alignment = PP_ALIGN.LEFT
        r_topic = p_topic.add_run()
        r_topic.text = topic
        r_topic.font.name = FONT_PRIMARY
        r_topic.font.size = Pt(24)
        r_topic.font.bold = False
        r_topic.font.color.rgb = COLOR_DARK

    format_agenda_table(table_shape)
    return slide


def build_slide_3(prs, layouts):
    """Slide 3: Conceptos Clave - Modelo."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    set_title(slide, "Conceptos Clave")
    remove_placeholder(slide, 2)
    add_section_subtitle(slide, "Modelo")

    # Contenido
    tb_content = slide.shapes.add_textbox(Emu(359999), Emu(1870200), Emu(5199973), Emu(2797689))
    tf = tb_content.text_frame
    tf.word_wrap = True

    lines = [
        ("Es el componente central de un sistema de IA.", False, Pt(18), COLOR_DARK, Pt(0), Pt(4)),
        ("Ha sido entrenado con datos para identificar patrones y generar resultados.", False, Pt(18), COLOR_DARK, Pt(0), Pt(14)),
        ("¿Para qué sirve?", True, Pt(20), COLOR_MAGENTA, Pt(0), Pt(4)),
        ("Convierte una entrada (texto, imagen o datos) en una salida útil basada en su entrenamiento.", False, Pt(18), COLOR_DARK, Pt(0), Pt(14)),
        ("Ejemplo:", True, Pt(20), COLOR_MAGENTA, Pt(0), Pt(4)),
        ("Generar una imagen modificada (por ejemplo, agregar un objeto a una foto).", False, Pt(18), COLOR_DARK, Pt(0), Pt(0)),
    ]
    for idx, (text, is_bold, sz, col, sb, sa) in enumerate(lines):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.space_before = sb
        p.space_after = sa
        r = p.add_run()
        r.text = text
        r.font.name = FONT_PRIMARY
        r.font.size = sz
        r.font.bold = is_bold
        r.font.color.rgb = col

    # Imagen / Diagrama
    slide.shapes.add_picture(get_asset("image14.png"), Emu(5820346), Emu(1613698), Emu(5863738), Emu(3147145))
    return slide


def build_slide_4(prs, layouts):
    """Slide 4: Conceptos Clave - LLM."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    set_title(slide, "Conceptos Clave")
    remove_placeholder(slide, 2)
    add_section_subtitle(slide, "LLM (Large Language Model / Modelo de Lenguaje Grande)")

    tb_content = slide.shapes.add_textbox(Emu(360000), Emu(1870200), Emu(5736000), Emu(3628686))
    tf = tb_content.text_frame
    tf.word_wrap = True

    lines = [
        ("Modelo especializado en lenguaje natural, entrenado con grandes volúmenes de texto.", False, Pt(18), COLOR_DARK, Pt(0), Pt(14)),
        ("¿Para qué sirve?", True, Pt(20), COLOR_MAGENTA, Pt(0), Pt(4)),
        ("Comprender, generar y transformar lenguaje humano.", False, Pt(18), COLOR_DARK, Pt(0), Pt(14)),
        ("Casos de uso:", True, Pt(20), COLOR_MAGENTA, Pt(0), Pt(4)),
        ("- Redacción de textos", False, Pt(18), COLOR_DARK, Pt(0), Pt(2)),
        ("- Traducción", False, Pt(18), COLOR_DARK, Pt(0), Pt(2)),
        ("- Resumen de información", False, Pt(18), COLOR_DARK, Pt(0), Pt(2)),
        ("- Chat conversacional", False, Pt(18), COLOR_DARK, Pt(0), Pt(14)),
        ("Ejemplo:", True, Pt(20), COLOR_MAGENTA, Pt(0), Pt(4)),
        ("Generar un correo formal automáticamente.", False, Pt(18), COLOR_DARK, Pt(0), Pt(0)),
    ]
    for idx, (text, is_bold, sz, col, sb, sa) in enumerate(lines):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.space_before = sb
        p.space_after = sa
        r = p.add_run()
        r.text = text
        r.font.name = FONT_PRIMARY
        r.font.size = sz
        r.font.bold = is_bold
        r.font.color.rgb = col

    slide.shapes.add_picture(get_asset("image15.png"), Emu(6022041), Emu(1940838), Emu(5784809), Emu(3502645))
    return slide


def build_slide_5(prs, layouts):
    """Slide 5: Conceptos Clave - Agente."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    set_title(slide, "Conceptos Clave")
    remove_placeholder(slide, 2)
    add_section_subtitle(slide, "Agente")

    tb_content = slide.shapes.add_textbox(Emu(360000), Emu(1870200), Emu(10980548), Emu(3074688))
    tf = tb_content.text_frame
    tf.word_wrap = True

    lines = [
        ("Sistema que utiliza un LLM como “cerebro” y puede tomar decisiones para cumplir un objetivo.", False, Pt(18), COLOR_DARK, Pt(0), Pt(14)),
        ("Características clave:", True, Pt(20), COLOR_MAGENTA, Pt(0), Pt(4)),
        ("- Autonomía", False, Pt(18), COLOR_DARK, Pt(0), Pt(2)),
        ("- Uso de herramientas", False, Pt(18), COLOR_DARK, Pt(0), Pt(2)),
        ("- Ejecución de acciones", False, Pt(18), COLOR_DARK, Pt(0), Pt(14)),
        ("¿Para qué sirve?", True, Pt(20), COLOR_MAGENTA, Pt(0), Pt(4)),
        ("Automatizar procesos completos sin intervención constante.", False, Pt(18), COLOR_DARK, Pt(0), Pt(14)),
        ("Ejemplo:", True, Pt(20), COLOR_MAGENTA, Pt(0), Pt(4)),
        ("Gestionar automáticamente la planificación de vacaciones.", False, Pt(18), COLOR_DARK, Pt(0), Pt(0)),
    ]
    for idx, (text, is_bold, sz, col, sb, sa) in enumerate(lines):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.space_before = sb
        p.space_after = sa
        r = p.add_run()
        r.text = text
        r.font.name = FONT_PRIMARY
        r.font.size = sz
        r.font.bold = is_bold
        r.font.color.rgb = col

    return slide


def build_slide_6(prs, layouts):
    """Slide 6: Conceptos Clave - Agente (Diagrama)."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    set_title(slide, "Conceptos Clave")
    remove_placeholder(slide, 2)
    add_section_subtitle(slide, "Agente")

    slide.shapes.add_picture(get_asset("image16.png"), Emu(359999), Emu(1723028), Emu(10449000), Emu(4543032))
    return slide


def build_slide_7(prs, layouts):
    """Slide 7: Conceptos Clave - Sistema multiagente."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    set_title(slide, "Conceptos Clave")
    remove_placeholder(slide, 2)
    add_section_subtitle(slide, "Sistema multiagente")

    tb_content = slide.shapes.add_textbox(Emu(359999), Emu(1870200), Emu(11324085), Emu(2243691))
    tf = tb_content.text_frame
    tf.word_wrap = True

    lines = [
        ("Conjunto de agentes especializados que colaboran para resolver problemas complejos.", False, Pt(18), COLOR_DARK, Pt(0), Pt(14)),
        ("¿Para qué sirve?", True, Pt(20), COLOR_MAGENTA, Pt(0), Pt(4)),
        ("Dividir un problema en tareas más pequeñas y coordinadas.", False, Pt(18), COLOR_DARK, Pt(0), Pt(14)),
        ("Ejemplo:", True, Pt(20), COLOR_MAGENTA, Pt(0), Pt(4)),
        ("- Agente 1 (Atención): interactúa con el cliente", False, Pt(18), COLOR_DARK, Pt(0), Pt(2)),
        ("- Agente 2 (Riesgo): analiza historial crediticio", False, Pt(18), COLOR_DARK, Pt(0), Pt(2)),
        ("- Agente 3 (Decisión): aprueba o rechaza el crédito", False, Pt(18), COLOR_DARK, Pt(0), Pt(0)),
    ]
    for idx, (text, is_bold, sz, col, sb, sa) in enumerate(lines):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.space_before = sb
        p.space_after = sa
        r = p.add_run()
        r.text = text
        r.font.name = FONT_PRIMARY
        r.font.size = sz
        r.font.bold = is_bold
        r.font.color.rgb = col

    return slide


def build_slide_8(prs, layouts):
    """Slide 8: Conceptos Clave - Sistema multiagente (Diagrama)."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    set_title(slide, "Conceptos Clave")
    remove_placeholder(slide, 2)
    add_section_subtitle(slide, "Sistema multiagente")

    slide.shapes.add_picture(get_asset("image17.png"), Emu(359999), Emu(1898374), Emu(10449000), Emu(3438939))
    return slide


def build_slide_9(prs, layouts):
    """Slide 9: LLM vs Agente - Comparativa."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    set_title(slide, "LLM vs Agente")
    remove_placeholder(slide, 2)
    add_section_subtitle(slide, "Cuando usar uno y no el otro")

    # Encabezado 1
    tb_h1 = slide.shapes.add_textbox(Emu(359996), Emu(1849486), Emu(11324085), Emu(332399))
    r_h1 = tb_h1.text_frame.paragraphs[0].add_run()
    r_h1.text = "Usar un LLM si :"
    r_h1.font.name = FONT_PRIMARY
    r_h1.font.size = Pt(20)
    r_h1.font.bold = True
    r_h1.font.color.rgb = COLOR_MAGENTA

    # Lista 1
    tb_c1 = slide.shapes.add_textbox(Emu(359997), Emu(2417673), Emu(11324085), Emu(830997))
    tf1 = tb_c1.text_frame
    tf1.word_wrap = True
    lines1 = [
        "- La tarea es simple y puntual (una sola interacción)",
        "- Necesitas respuestas rápidas y de bajo costo",
        "- Siempre hay validación humana",
    ]
    for idx, text in enumerate(lines1):
        p = tf1.paragraphs[0] if idx == 0 else tf1.add_paragraph()
        p.space_before = Pt(2)
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = text
        r.font.name = FONT_PRIMARY
        r.font.size = Pt(18)
        r.font.color.rgb = COLOR_DARK

    # Encabezado 2
    tb_h2 = slide.shapes.add_textbox(Emu(359995), Emu(3484458), Emu(11324085), Emu(332399))
    r_h2 = tb_h2.text_frame.paragraphs[0].add_run()
    r_h2.text = "Usar un agente si :"
    r_h2.font.name = FONT_PRIMARY
    r_h2.font.size = Pt(20)
    r_h2.font.bold = True
    r_h2.font.color.rgb = COLOR_MAGENTA

    # Lista 2
    tb_c2 = slide.shapes.add_textbox(Emu(359997), Emu(4052645), Emu(11324085), Emu(1107996))
    tf2 = tb_c2.text_frame
    tf2.word_wrap = True
    lines2 = [
        "- La tarea requiere múltiples pasos",
        "- Se deben tomar decisiones dinámicas",
        "- Hay interacción con sistemas externos (APIs, BD, correo, etc.)",
        "- Se necesita auto-validación (razonamiento iterativo)",
    ]
    for idx, text in enumerate(lines2):
        p = tf2.paragraphs[0] if idx == 0 else tf2.add_paragraph()
        p.space_before = Pt(2)
        p.space_after = Pt(2)
        r = p.add_run()
        r.text = text
        r.font.name = FONT_PRIMARY
        r.font.size = Pt(18)
        r.font.color.rgb = COLOR_DARK

    return slide


def build_slide_10(prs, layouts):
    """Slide 10: LLM vs Agente (Diagrama)."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    set_title(slide, "LLM vs Agente")
    remove_placeholder(slide, 2)
    slide.shapes.add_picture(get_asset("image18.png"), Emu(360000), Emu(1093303), Emu(10287000), Emu(5685183))
    return slide


def build_slide_11(prs, layouts):
    """Slide 11: Microsoft Agent Framework."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    set_title(slide, "Microsoft Agent Framework")
    remove_placeholder(slide, 2)

    tb_content = slide.shapes.add_textbox(Emu(359999), Emu(1302834), Emu(11324085), Emu(3323987))
    tf = tb_content.text_frame
    tf.word_wrap = True

    lines = [
        ("¿Qué es?", True, Pt(20), COLOR_MAGENTA, Pt(0), Pt(4)),
        ("Framework unificado para construir, desplegar y gestionar agentes inteligentes.", False, Pt(18), COLOR_DARK, Pt(0), Pt(14)),
        ("¿Por qué usarlo?", True, Pt(20), COLOR_MAGENTA, Pt(0), Pt(4)),
        ("- Seguridad empresarial (ecosistema Microsoft)", False, Pt(18), COLOR_DARK, Pt(0), Pt(2)),
        ("- Flexibilidad (soporta múltiples modelos)", False, Pt(18), COLOR_DARK, Pt(0), Pt(2)),
        ("- Integración nativa con Azure", False, Pt(18), COLOR_DARK, Pt(0), Pt(14)),
        ("¿Dónde aplicarlo?", True, Pt(20), COLOR_MAGENTA, Pt(0), Pt(4)),
        ("- Automatización de procesos", False, Pt(18), COLOR_DARK, Pt(0), Pt(2)),
        ("- Asistentes conversacionales", False, Pt(18), COLOR_DARK, Pt(0), Pt(2)),
        ("- Análisis y generación de reportes", False, Pt(18), COLOR_DARK, Pt(0), Pt(0)),
    ]
    for idx, (text, is_bold, sz, col, sb, sa) in enumerate(lines):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.space_before = sb
        p.space_after = sa
        r = p.add_run()
        r.text = text
        r.font.name = FONT_PRIMARY
        r.font.size = sz
        r.font.bold = is_bold
        r.font.color.rgb = col

    return slide


def build_slide_12(prs, layouts):
    """Slide 12: Conceptos básicos de Microsoft Agent Framework."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    set_title(slide, "Conceptos básicos de Microsoft Agent Framework")
    remove_placeholder(slide, 2)

    tb_content = slide.shapes.add_textbox(Emu(359999), Emu(1286221), Emu(11324085), Emu(2215991))
    tf = tb_content.text_frame
    tf.word_wrap = True

    lines = [
        ("Sesión", True, Pt(20), COLOR_MAGENTA, Pt(0), Pt(4)),
        ("Historial de conversación que permite mantener contexto.", False, Pt(18), COLOR_DARK, Pt(0), Pt(14)),
        ("Tools", True, Pt(20), COLOR_MAGENTA, Pt(0), Pt(4)),
        ("Funciones externas que el agente puede ejecutar (APIs, lógica de negocio).", False, Pt(18), COLOR_DARK, Pt(0), Pt(14)),
        ("Memoria", True, Pt(20), COLOR_MAGENTA, Pt(0), Pt(4)),
        ("Capacidad de almacenar información a largo plazo (preferencias, historial).", False, Pt(18), COLOR_DARK, Pt(0), Pt(0)),
    ]
    for idx, (text, is_bold, sz, col, sb, sa) in enumerate(lines):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.space_before = sb
        p.space_after = sa
        r = p.add_run()
        r.text = text
        r.font.name = FONT_PRIMARY
        r.font.size = sz
        r.font.bold = is_bold
        r.font.color.rgb = col

    return slide


def build_slide_13(prs, layouts):
    """Slide 13: Creando nuestro primer agente."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    set_title(slide, "Creando nuestro primer agente")

    # Mensaje central en placeholder 2
    ph_body = slide.placeholders[2]
    tf = ph_body.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "Con estos conceptos, estamos listos para crear nuestro primer agente utilizando Microsoft Agent Framework."
    r.font.name = FONT_PRIMARY
    r.font.size = Pt(48)
    r.font.color.rgb = COLOR_DARK
    return slide


def build_slide_14(prs, layouts):
    """Slide 14: Cierre / Feedback."""
    slide = prs.slides.add_slide(layouts['Diapositiva de título'])
    remove_all_placeholders(slide)

    # 1. Fondo completo de cierre
    slide.shapes.add_picture(get_asset("image19.png"), Emu(1), Emu(4049), Emu(12192000), Emu(6853951))

    # 2. Hashtag superior
    tb_hash = slide.shapes.add_textbox(Emu(185316), Emu(121555), Emu(6084807), Emu(558604))
    r_hash = tb_hash.text_frame.paragraphs[0].add_run()
    r_hash.text = "#ComunidadIA"
    r_hash.font.name = FONT_PRIMARY_LIGHT
    r_hash.font.size = Pt(30)
    r_hash.font.italic = True
    r_hash.font.color.rgb = COLOR_WHITE

    # 3. Logo superior derecho
    slide.shapes.add_picture(get_asset("image20.png"), Emu(9481369), Emu(299946), Emu(2159555), Emu(261236))

    # 4. Título Principal
    tb_main = slide.shapes.add_textbox(Emu(507877), Emu(861733), Emu(11133047), Emu(1328046))
    tf_main = tb_main.text_frame
    
    p1 = tf_main.paragraphs[0]
    p1.alignment = PP_ALIGN.CENTER
    r1 = p1.add_run()
    r1.text = "¡Ayúdanos a potenciar los"
    r1.font.name = FONT_PRIMARY_BLACK
    r1.font.size = Pt(40)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_WHITE

    p2 = tf_main.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    r2 = p2.add_run()
    r2.text = "MIÉRCOLES DE IA!"
    r2.font.name = FONT_PRIMARY_BLACK
    r2.font.size = Pt(40)
    r2.font.bold = True
    r2.font.color.rgb = COLOR_CYAN

    # 5. Mascota
    slide.shapes.add_picture(get_asset("image22.png"), Emu(4626432), Emu(1907601), Emu(3292900), Emu(4939351))

    # 6. QR Code
    slide.shapes.add_picture(get_asset("image21.png"), Emu(7791227), Emu(2524765), Emu(3292900), Emu(3471502))

    # 7. Subtítulo
    tb_sub = slide.shapes.add_textbox(Emu(507877), Emu(3590142), Emu(4344103), Emu(1574267))
    tf_sub = tb_sub.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.alignment = PP_ALIGN.RIGHT
    r_sub = p_sub.add_run()
    r_sub.text = "Tu opinión es clave para seguir aprendiendo juntos.🚀"
    r_sub.font.name = FONT_PRIMARY
    r_sub.font.size = Pt(32)
    r_sub.font.color.rgb = COLOR_WHITE

    # 8. Slogan Inferior
    tb_foot = slide.shapes.add_textbox(Emu(1240206), Emu(6293450), Emu(10936591), Emu(230832))
    p_foot = tb_foot.text_frame.paragraphs[0]
    p_foot.alignment = PP_ALIGN.CENTER

    parts = [
        ("PONLE ", FONT_PRIMARY_LIGHT),
        ("IA ", FONT_PRIMARY_BLACK),
        ("A TU D", FONT_PRIMARY_LIGHT),
        ("IA", FONT_PRIMARY_BLACK),
    ]
    for text, font_name in parts:
        r = p_foot.add_run()
        r.text = text
        r.font.name = font_name
        r.font.size = Pt(15)
        r.font.color.rgb = COLOR_WHITE

    return slide


def generate_presentation(output_path=OUTPUT_PPTX, template_path=TEMPLATE_PPTX):
    """Ejecuta el pipeline completo de generación de la presentación."""
    print("=" * 60)
    print("Iniciando generación de presentación inversa 'Miércoles de IA'...")
    print("=" * 60)

    # 1. Asegurar assets y plantilla base
    if not os.path.exists(ASSETS_DIR) or len(os.listdir(ASSETS_DIR)) == 0:
        extract_assets()

    if not os.path.exists(template_path):
        create_clean_template(ORIGINAL_PPTX, template_path)

    # 2. Cargar plantilla limpia
    prs = pptx.Presentation(template_path)
    layouts = {l.name: l for l in prs.slide_layouts}

    # 3. Construir diapositivas secuencialmente
    print("Construyendo Slide 1: Carátula (Fondo foto + texto blanco)...")
    build_slide_1(prs, layouts)

    print("Construyendo Slide 2: Agenda (Título magenta + tabla limpia con separadores)...")
    build_slide_2(prs, layouts)

    print("Construyendo Slide 3: Conceptos Clave - Modelo (Título y subtítulo magenta)...")
    build_slide_3(prs, layouts)

    print("Construyendo Slide 4: Conceptos Clave - LLM...")
    build_slide_4(prs, layouts)

    print("Construyendo Slide 5: Conceptos Clave - Agente...")
    build_slide_5(prs, layouts)

    print("Construyendo Slide 6: Conceptos Clave - Agente (Diagrama)...")
    build_slide_6(prs, layouts)

    print("Construyendo Slide 7: Conceptos Clave - Sistema multiagente...")
    build_slide_7(prs, layouts)

    print("Construyendo Slide 8: Conceptos Clave - Sistema multiagente (Diagrama)...")
    build_slide_8(prs, layouts)

    print("Construyendo Slide 9: LLM vs Agente (Comparativa)...")
    build_slide_9(prs, layouts)

    print("Construyendo Slide 10: LLM vs Agente (Diagrama)...")
    build_slide_10(prs, layouts)

    print("Construyendo Slide 11: Microsoft Agent Framework...")
    build_slide_11(prs, layouts)

    print("Construyendo Slide 12: Conceptos básicos de MAF...")
    build_slide_12(prs, layouts)

    print("Construyendo Slide 13: Creando nuestro primer agente...")
    build_slide_13(prs, layouts)

    print("Construyendo Slide 14: Cierre / Feedback...")
    build_slide_14(prs, layouts)

    # 4. Guardar archivo final
    prs.save(output_path)
    print("=" * 60)
    print(f"[ÉXITO] Presentación generada exitosamente en: '{output_path}'")
    print(f"Total de diapositivas generadas: {len(prs.slides)}")
    print("=" * 60)


if __name__ == "__main__":
    generate_presentation()
