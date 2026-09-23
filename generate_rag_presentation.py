"""
Compilador Equilibrado y Dinámico de la Presentación PPTX:
'RAG + Microsoft Agent Framework (Fase 04 - Transit: Misiones a Marte)'

Diseño: Alternancia de layouts (izq/der), placeholders de imágenes visuales claros,
fórmulas matemáticas en LaTeX de alta resolución y estética corporativa Credicorp/BCP.
Entorno: rag_demo_bcp (Python con python-pptx y matplotlib)
"""

import os
import sys
import zipfile
import pptx
from pptx.util import Pt, Emu
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.oxml import parse_xml
from pptx.enum.shapes import MSO_SHAPE
import matplotlib.pyplot as plt

# =============================================================================
# CONSTANTES Y CONFIGURACIÓN
# =============================================================================
ORIGINAL_PPTX = "Miercoles de IA - Agent Framework - 10-06-2026.pptx"
TEMPLATE_PPTX = "template_miercoles_ia.pptx"
OUTPUT_PPTX = "RAG_Microsoft_Agent_Framework_Transit.pptx"
ASSETS_DIR = "extracted_assets"
FORMULAS_DIR = "generated_formulas"

os.makedirs(FORMULAS_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

# Paleta Corporativa CREDICORP / BCP
COLOR_MAGENTA = RGBColor(0xC3, 0x33, 0x8E)   # Acento 1 (Magenta BCP)
COLOR_CYAN = RGBColor(0x2A, 0xD2, 0xC9)      # Acento 2 (Cian / Turquesa)
COLOR_DARK = RGBColor(0x33, 0x33, 0x33)      # Texto Principal Oscuro
COLOR_GRAY = RGBColor(0x55, 0x55, 0x55)      # Texto Secundario
COLOR_PLACEHOLDER_BG = RGBColor(0xF6, 0xF7, 0xFB) # Fondo Placeholder Suave
COLOR_BORDER = RGBColor(0xD1, 0xD5, 0xDB)    # Borde Suave
COLOR_WHITE = RGBColor(0xFF, 0xFF, 0xFF)     # Blanco

# Tipografías Corporativas
FONT_PRIMARY = "Inter Tight"
FONT_PRIMARY_BLACK = "Inter Tight Black"
FONT_PRIMARY_LIGHT = "Inter Tight Light"


# =============================================================================
# GENERADOR DE FÓRMULAS LATEX
# =============================================================================
def render_latex(formula_str, filename, fontsize=18, textcolor="#222222", dpi=300):
    """Renderiza una fórmula matemática LaTeX a imagen PNG de alta resolución con transparencia."""
    filepath = os.path.join(FORMULAS_DIR, filename)
    fig = plt.figure(figsize=(0.1, 0.1), dpi=dpi)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.patch.set_alpha(0.0)
    ax.text(0.5, 0.5, formula_str, fontsize=fontsize, color=textcolor,
            ha='center', va='center', usetex=False)
    fig.savefig(filepath, bbox_inches='tight', pad_inches=0.06, transparent=True, dpi=dpi)
    plt.close(fig)
    return filepath


# Pre-renderizar fórmulas requeridas
PATH_FORMULA_CLASSICAL = render_latex(r"$P(y \mid x) = \prod_{t=1}^{T} P(y_t \mid y_{<t}, x; \theta)$", "formula_classical.png", fontsize=17, textcolor="#333333")
PATH_FORMULA_RAG = render_latex(r"$P(y \mid x) = \sum_{d \in \mathcal{D}} P(d \mid x) \cdot P(y \mid x, d; \theta)$", "formula_rag.png", fontsize=19, textcolor="#C3338E")
PATH_FORMULA_RRF = render_latex(r"$\mathrm{RRF\_Score}(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$", "formula_rrf.png", fontsize=18, textcolor="#C3338E")


# =============================================================================
# HELPERS DE OPENXML Y FORMAS
# =============================================================================
def get_asset(filename):
    """Obtiene la ruta de un recurso o extrae si es necesario."""
    path = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(path):
        with zipfile.ZipFile(ORIGINAL_PPTX, 'r') as z:
            for fname in z.namelist():
                if fname.startswith('ppt/media/'):
                    tpath = os.path.join(ASSETS_DIR, os.path.basename(fname))
                    with open(tpath, 'wb') as f:
                        f.write(z.read(fname))
    return path


def set_slide_background_image(slide, image_path):
    """Inserta fondo de imagen nativo en <p:cSld>."""
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


def remove_placeholder(slide, idx):
    """Elimina placeholder específico."""
    for ph in list(slide.placeholders):
        if ph.placeholder_format.idx == idx:
            sp = ph._element
            sp.getparent().remove(sp)


def remove_all_placeholders(slide):
    """Elimina todos los placeholders."""
    for ph in list(slide.placeholders):
        sp = ph._element
        sp.getparent().remove(sp)


def set_title(slide, title_text):
    """Configura título superior en Magenta e Inter Tight Black."""
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
    """Agrega subtítulo en Magenta e Inter Tight Black."""
    tb = slide.shapes.add_textbox(Emu(359999), Emu(1281299), Emu(11324085), Emu(332399))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.space_before = Pt(0)
    p.space_after = Pt(0)
    r = p.add_run()
    r.text = subtitle_text
    r.font.name = FONT_PRIMARY_BLACK
    r.font.size = Pt(22)
    r.font.bold = True
    r.font.color.rgb = COLOR_MAGENTA
    return tb


def format_agenda_table(table_shape):
    """Aplica formato de tabla transparente con líneas horizontales divisorias finas (tx1)."""
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
            for f in tcPr.xpath('./a:solidFill | ./a:gradFill | ./a:pattFill'):
                tcPr.remove(f)
            if not tcPr.xpath('./a:noFill'):
                tcPr.append(parse_xml('<a:noFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>'))

            for border_tag in ['lnL', 'lnR', 'lnT', 'lnB']:
                for b in tcPr.xpath(f'./a:{border_tag}'):
                    tcPr.remove(b)

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


def add_image_placeholder(slide, left, top, width, height, title, prompt_description):
    """Crea una tarjeta de placeholder visual estilizada y con padding limpio."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_PLACEHOLDER_BG
    card.line.color.rgb = COLOR_BORDER
    card.line.width = Pt(1.2)

    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Emu(250000)
    tf.margin_right = Emu(250000)
    tf.margin_top = Emu(220000)
    tf.margin_bottom = Emu(220000)

    # Encabezado
    p0 = tf.paragraphs[0]
    p0.alignment = PP_ALIGN.CENTER
    p0.space_before = Pt(0)
    p0.space_after = Pt(4)
    r0 = p0.add_run()
    r0.text = "🖼️ [ RECURSO VISUAL SUGERIDO ]"
    r0.font.name = FONT_PRIMARY_BLACK
    r0.font.size = Pt(12.5)
    r0.font.bold = True
    r0.font.color.rgb = COLOR_MAGENTA

    # Título
    p1 = tf.add_paragraph()
    p1.alignment = PP_ALIGN.CENTER
    p1.space_before = Pt(2)
    p1.space_after = Pt(8)
    r1 = p1.add_run()
    r1.text = title
    r1.font.name = FONT_PRIMARY_BLACK
    r1.font.size = Pt(12)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_DARK

    # Prompt
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.LEFT
    p2.space_before = Pt(4)
    p2.space_after = Pt(0)
    r2 = p2.add_run()
    r2.text = prompt_description
    r2.font.name = FONT_PRIMARY
    r2.font.size = Pt(11)
    r2.font.color.rgb = COLOR_GRAY
    return card


def render_split_slide(slide, title, subtitle, content_blocks, placeholder_title, placeholder_desc, image_on_left=False):
    """Renderiza diapositiva con texto y placeholder de imagen alternando posición (izq/der)."""
    set_title(slide, title)
    remove_placeholder(slide, 2)
    add_section_subtitle(slide, subtitle)

    # Geometría según orientación
    if image_on_left:
        ph_left = Emu(359999)
        txt_left = Emu(6100000)
    else:
        txt_left = Emu(359999)
        ph_left = Emu(6100000)

    top_pos = Emu(1800000)
    col_w = Emu(5650000)
    col_h = Emu(4750000)

    # Columna de Texto
    tb_content = slide.shapes.add_textbox(txt_left, top_pos, col_w, col_h)
    tf = tb_content.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_top = 0

    is_first = True
    for header, body in content_blocks:
        if header:
            p_h = tf.paragraphs[0] if is_first else tf.add_paragraph()
            is_first = False
            p_h.space_before = Pt(8)
            p_h.space_after = Pt(2)
            r_h = p_h.add_run()
            r_h.text = header
            r_h.font.name = FONT_PRIMARY_BLACK
            r_h.font.size = Pt(15.5)
            r_h.font.bold = True
            r_h.font.color.rgb = COLOR_MAGENTA

        if body:
            p_b = tf.paragraphs[0] if is_first else tf.add_paragraph()
            is_first = False
            p_b.space_before = Pt(0)
            p_b.space_after = Pt(6)
            r_b = p_b.add_run()
            r_b.text = body
            r_b.font.name = FONT_PRIMARY
            r_b.font.size = Pt(13.5)
            r_b.font.color.rgb = COLOR_DARK

    # Placeholder de Imagen
    add_image_placeholder(
        slide,
        left=ph_left,
        top=top_pos,
        width=col_w,
        height=col_h,
        title=placeholder_title,
        prompt_description=placeholder_desc
    )


# =============================================================================
# CONSTRUCTORES DE DIAPOSITIVAS (1 a 14)
# =============================================================================

def build_slide_1(prs, layouts):
    """Slide 1: Carátula Principal."""
    slide = prs.slides.add_slide(layouts['CARATULA-01'])
    set_slide_background_image(slide, get_asset("image13.jpg"))

    # Título Principal
    tf_title = slide.placeholders[0].text_frame
    tf_title.clear()
    p_title = tf_title.paragraphs[0]
    p_title.space_before = Pt(0)
    p_title.space_after = Pt(0)
    r_title = p_title.add_run()
    r_title.text = "RAG + Agent Framework"
    r_title.font.name = FONT_PRIMARY_BLACK
    r_title.font.size = Pt(44)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_WHITE

    # Subtítulo
    tf_sub = slide.placeholders[1].text_frame
    tf_sub.clear()
    p_sub = tf_sub.paragraphs[0]
    r_sub = p_sub.add_run()
    r_sub.text = "Generación Aumentada por Recuperación con Azure AI y Microsoft Agent Framework"
    r_sub.font.name = FONT_PRIMARY
    r_sub.font.size = Pt(20)
    r_sub.font.color.rgb = COLOR_WHITE
    return slide


def build_slide_2(prs, layouts):
    """Slide 2: Agenda."""
    slide = prs.slides.add_slide(layouts['EN-BLANCO-01'])

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

    table_shape = slide.shapes.add_table(5, 2, Emu(1393348), Emu(2047937), Emu(9405305), Emu(4117660))
    table = table_shape.table
    table.columns[0].width = Emu(1800000)
    table.columns[1].width = Emu(7605305)
    for row in table.rows:
        row.height = Emu(823532)

    agenda_items = [
        ("01", "El Problema y la Solución: ¿Qué es y qué resuelve RAG?"),
        ("02", "Los Componentes Clave & Fundamento Matemático Bayesiano"),
        ("03", "Técnicas de Precisión: Búsqueda Híbrida y Semantic Reranker"),
        ("04", "RAG Agéntico: Integración con Microsoft Agent Framework en Azure"),
        ("05", "Demo en Vivo: Explorando el cráter Jezero con documentos de la NASA"),
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
        r_topic.font.size = Pt(22)
        r_topic.font.bold = False
        r_topic.font.color.rgb = COLOR_DARK

    format_agenda_table(table_shape)
    return slide


def build_slide_3(prs, layouts):
    """Slide 3: El Desafío de los LLMs (Texto a la Izquierda, Imagen a la Derecha)."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    blocks = [
        ("Corte de Conocimiento (Knowledge Cutoff):", "Los modelos solo saben lo que aprendieron durante su entrenamiento. No conocen tus datos de hoy."),
        ("Alucinaciones:", "Cuando un modelo no sabe la respuesta, tiende a inventar datos con absoluta seguridad sintáctica."),
        ("Falta de Trazabilidad:", "No pueden citar la página, el memorándum o el documento oficial de donde extrajeron el dato."),
        ("Costo y Lentitud de Reentrenar:", "Hacer fine-tuning o reentrenar continuamente es inviable técnica y económicamente para datos vivos."),
    ]
    desc = "Ilustración dividida en 2 paneles: en la izquierda, un robot LLM mirando un calendario vencido ('Entrenado en 2024') respondiendo con signos de interrogación y alucinaciones; a la derecha, una pila de documentos confidenciales y actualizados de 2026 a los cuales el LLM no tiene acceso por estar aislado."
    render_split_slide(slide, "El Desafío de los LLMs", "Límites de los Modelos de Lenguaje Aislados", blocks, "Robot LLM vs. Documentos Vivos 2026", desc, image_on_left=False)
    return slide


def build_slide_4(prs, layouts):
    """Slide 4: Fundamentos de RAG (Imagen a la Izquierda, Texto a la Derecha -> Variedad)."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    blocks = [
        ("La Analogía del Examen:", "Un examen tradicional de memoria vs. un examen a libro abierto con un índice perfecto."),
        ("¿Cómo funciona el flujo RAG?", "1. Retrieval: Recupera fragmentos relevantes de la base documental.\n2. Augmentation: Inyecta los fragmentos como contexto en el prompt.\n3. Generation: El LLM genera la respuesta citando fuentes."),
        ("Beneficios Inmediatos:", "Grounding garantizado, citas trazables, actualización instantánea de documentos y cero reentrenamiento."),
    ]
    desc = "Diagrama de flujo conceptual en 3 pasos: (1) Usuario pregunta -> (2) Base de datos documental filtra y extrae 3 fichas de texto relevantes -> (3) El LLM recibe la pregunta + las 3 fichas y entrega una respuesta fundamentada con etiquetas de citas numéricas [Doc1, Pág 4]."
    render_split_slide(slide, "Fundamentos de RAG", "Retrieval-Augmented Generation (Generación Aumentada por Recuperación)", blocks, "Flujo Conceptual RAG en 3 Pasos", desc, image_on_left=True)
    return slide


def build_slide_5(prs, layouts):
    """Slide 5: Componentes Clave de RAG (Texto a la Izquierda, Imagen a la Derecha)."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    blocks = [
        ("1. Chunking (Fragmentación):", "División de PDFs largos en fragmentos de 500-1000 tokens con solapamiento (overlap) para preservar el contexto."),
        ("2. Embeddings (Vectorización):", "Transformación de texto en vectores numéricos de 1536 dimensiones que capturan la semántica."),
        ("3. Vector Store & Search Index:", "Almacén especializado (Azure AI Search) con índices HNSW para búsqueda rápida por similitud coseno."),
        ("4. Grounded Prompting:", "Instrucciones estrictas al LLM para responder únicamente con base en la evidencia provista sin extrapolar."),
    ]
    desc = "Infografía horizontal: Documento PDF -> Cuchilla de corte (Chunking con overlap) -> Modelo de Embedding (convertidor texto a números) -> Espacio vectorial 3D de puntos -> Retriever -> Prompt final con contexto enriquecido."
    render_split_slide(slide, "Arquitectura del Pipeline", "De Documentos Crudos a Respuestas con Grounding", blocks, "Pipeline de Ingesta y Vectorización", desc, image_on_left=False)
    return slide


def build_slide_6(prs, layouts):
    """Slide 6: Deep Dive Bayesiano (Fórmulas LaTeX a la Izquierda + Imagen a la Derecha)."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    set_title(slide, "Fundamento Matemático")
    remove_placeholder(slide, 2)
    add_section_subtitle(slide, "RAG expresado formalmente como Inferencia Bayesiana")

    col_w = Emu(5650000)
    col_h = Emu(4750000)
    top_pos = Emu(1800000)

    # Columna Izquierda: Fórmulas LaTeX y Explicación
    tb_math = slide.shapes.add_textbox(Emu(359999), top_pos, col_w, col_h)
    tf = tb_math.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_top = 0

    p0 = tf.paragraphs[0]
    p0.space_before = Pt(0)
    p0.space_after = Pt(2)
    r0 = p0.add_run()
    r0.text = "Generación Clásica (Paramétrica):"
    r0.font.name = FONT_PRIMARY_BLACK
    r0.font.size = Pt(15.5)
    r0.font.bold = True
    r0.font.color.rgb = COLOR_MAGENTA

    # Fórmula 1
    slide.shapes.add_picture(PATH_FORMULA_CLASSICAL, Emu(360000), top_pos + Emu(380000), width=Emu(4600000))

    p1 = tf.add_paragraph()
    p1.space_before = Pt(45)
    p1.space_after = Pt(4)
    r1 = p1.add_run()
    r1.text = "El modelo depende únicamente de sus pesos fijos θ. Riesgo alto de alucinación si el dato no fue memorizado."
    r1.font.name = FONT_PRIMARY
    r1.font.size = Pt(12.5)
    r1.font.color.rgb = COLOR_DARK

    p2 = tf.add_paragraph()
    p2.space_before = Pt(12)
    p2.space_after = Pt(2)
    r2 = p2.add_run()
    r2.text = "Generación Aumentada (Inferencia No Paramétrica):"
    r2.font.name = FONT_PRIMARY_BLACK
    r2.font.size = Pt(15.5)
    r2.font.bold = True
    r2.font.color.rgb = COLOR_MAGENTA

    # Fórmula 2
    slide.shapes.add_picture(PATH_FORMULA_RAG, Emu(360000), top_pos + Emu(2350000), width=Emu(5200000))

    p3 = tf.add_paragraph()
    p3.space_before = Pt(50)
    p3.space_after = Pt(0)
    r3 = p3.add_run()
    r3.text = "• P(d | x): Prior de relevancia del documento d (Retriever)\n• P(y | x, d): Likelihood de la respuesta con evidencia (Generator)\n• La evidencia 'd' colapsa la entropía y enfoca la probabilidad en la verdad factual."
    r3.font.name = FONT_PRIMARY
    r3.font.size = Pt(12.5)
    r3.font.color.rgb = COLOR_DARK

    # Columna Derecha: Placeholder de Imagen
    desc = "Gráfico comparativo matemático: a la izquierda, una distribución de probabilidad difusa y dispersa (modelo estándar aislado); a la derecha, la distribución condicionada bayesiana que se estrecha y enfoca hacia la verdad cuando se incorpora la evidencia observable d, mostrando la reducción drástica de la entropía."
    add_image_placeholder(slide, Emu(6100000), top_pos, col_w, col_h, "Colapso de Incertidumbre y Distribución Condicionada", desc)
    return slide


def build_slide_7(prs, layouts):
    """Slide 7: Búsqueda Vectorial vs. Híbrida (Texto + Fórmula RRF + Imagen a la Derecha)."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    set_title(slide, "Estrategias de Recuperación")
    remove_placeholder(slide, 2)
    add_section_subtitle(slide, "¿Por qué los vectores puros no son suficientes?")

    col_w = Emu(5650000)
    col_h = Emu(4750000)
    top_pos = Emu(1800000)

    # Columna Izquierda: Texto y Fórmula
    tb = slide.shapes.add_textbox(Emu(359999), top_pos, col_w, col_h)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = 0
    tf.margin_top = 0

    p0 = tf.paragraphs[0]
    p0.space_before = Pt(0)
    p0.space_after = Pt(2)
    r0 = p0.add_run()
    r0.text = "Búsqueda Léxica (BM25):"
    r0.font.name = FONT_PRIMARY_BLACK
    r0.font.size = Pt(15.5)
    r0.font.bold = True
    r0.font.color.rgb = COLOR_MAGENTA

    p1 = tf.add_paragraph()
    p1.space_before = Pt(0)
    p1.space_after = Pt(6)
    r1 = p1.add_run()
    r1.text = "Excelente para códigos exactos, siglas, números de parte (ej. 'Curiosity RTG-04'). Falla en sinónimos."
    r1.font.name = FONT_PRIMARY
    r1.font.size = Pt(13)
    r1.font.color.rgb = COLOR_DARK

    p2 = tf.add_paragraph()
    p2.space_before = Pt(6)
    p2.space_after = Pt(2)
    r2 = p2.add_run()
    r2.text = "Búsqueda Vectorial (Semántica):"
    r2.font.name = FONT_PRIMARY_BLACK
    r2.font.size = Pt(15.5)
    r2.font.bold = True
    r2.font.color.rgb = COLOR_MAGENTA

    p3 = tf.add_paragraph()
    p3.space_before = Pt(0)
    p3.space_after = Pt(6)
    r3 = p3.add_run()
    r3.text = "Excelente para conceptos e intenciones (ej. 'buscar vida' -> 'biofirmas'). Falla en términos específicos o raros."
    r3.font.name = FONT_PRIMARY
    r3.font.size = Pt(13)
    r3.font.color.rgb = COLOR_DARK

    p4 = tf.add_paragraph()
    p4.space_before = Pt(6)
    p4.space_after = Pt(2)
    r4 = p4.add_run()
    r4.text = "Búsqueda Híbrida + RRF (Best of Both Worlds):"
    r4.font.name = FONT_PRIMARY_BLACK
    r4.font.size = Pt(15.5)
    r4.font.bold = True
    r4.font.color.rgb = COLOR_MAGENTA

    # Fórmula RRF
    slide.shapes.add_picture(PATH_FORMULA_RRF, Emu(360000), top_pos + Emu(3300000), width=Emu(4600000))

    p5 = tf.add_paragraph()
    p5.space_before = Pt(45)
    p5.space_after = Pt(0)
    r5 = p5.add_run()
    r5.text = "Ejecuta BM25 y Dense Vectors en paralelo combinando los rankings mediante Reciprocal Rank Fusion para una lista balanceada."
    r5.font.name = FONT_PRIMARY
    r5.font.size = Pt(12.5)
    r5.font.color.rgb = COLOR_DARK

    # Columna Derecha: Placeholder
    desc = "Diagrama con dos caminos convergentes: Camino Superior (BM25 Keyword Search) y Camino Inferior (Dense Vector Search) que procesan la misma consulta y convergen en un nodo central 'Reciprocal Rank Fusion' que entrega una lista unificada y balanceada de candidatos."
    add_image_placeholder(slide, Emu(6100000), top_pos, col_w, col_h, "Convergencia Híbrida BM25 + Vectores (RRF)", desc)
    return slide


def build_slide_8(prs, layouts):
    """Slide 8: Semantic Reranker (Imagen a la Izquierda, Texto a la Derecha -> Variedad)."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    blocks = [
        ("El Dilema: Velocidad vs. Precisión:", "Los Bi-Encoders (vectores) filtran 1,000,000 de docs a 50 en milisegundos, pero comparan textos de forma independiente."),
        ("Cross-Encoder / Semantic Reranker:", "Evalúa la pregunta y el fragmento juntos mediante Cross-Attention profunda, entendiendo negaciones y matices contextuales."),
        ("Impacto en Producción:", "Evita que fragmentos irrelevantes contaminen el contexto del LLM y garantiza que el Top 3 contenga la respuesta exacta."),
    ]
    desc = "Diagrama de embudo en dos fases: Fase 1 (Primer nivel rápido): De 100,000 documentos a Top 50 usando Búsqueda Híbrida -> Fase 2 (Semantic Reranker / Cross-Encoder): Reordena los 50 y coloca exactamente en el Top 3 los documentos con mayor relevancia semántica real hacia el LLM."
    render_split_slide(slide, "La Pieza Crítica: Semantic Reranker", "Transformando candidatos crudos en evidencia de alta calidad", blocks, "Embudo de Relevancia: Top 50 a Top 3", desc, image_on_left=True)
    return slide


def build_slide_9(prs, layouts):
    """Slide 9: RAG Agéntico (Texto a la Izquierda, Imagen a la Derecha)."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    blocks = [
        ("RAG Tradicional (Pipeline Rígido):", "Siempre consulta la base vectorial obligatoriamente, incluso ante saludos o preguntas generales, gastando cómputo innecesario."),
        ("RAG con Agente (Tool Calling & Razonamiento):", "El agente utiliza la búsqueda como una herramienta (Search Tool):\n• Conversación general -> Responde de inmediato.\n• Pregunta técnica -> Invoca Azure AI Search.\n• Resultado insuficiente -> Reformula la consulta automáticamente."),
    ]
    desc = "Ilustración de la arquitectura de Microsoft Agent Framework: Agente con LLM en el centro conectado a un catálogo de herramientas (Tool: Azure AI Search, Tool: Calculadora, Tool: CRM). El agente evalúa la intención del usuario y decide si activa o no la herramienta de recuperación de documentos."
    render_split_slide(slide, "RAG Agéntico", "Integración con Microsoft Agent Framework (MAF)", blocks, "Orquestación de Agente y Catálogo de Tools", desc, image_on_left=False)
    return slide


def build_slide_10(prs, layouts):
    """Slide 10: Optimizaciones para RAG Empresarial (Imagen a la Izquierda, Texto a la Derecha -> Variedad)."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    blocks = [
        ("Filtrado por Metadatos:", "Etiquetado de chunks (misión, fecha, categoría) para segmentar búsquedas antes del cálculo de similitud."),
        ("Control de Alucinaciones (Fallback):", "Umbrales de confianza estrictos: si la evidencia es insuficiente, el agente declara honestamente que no dispone del dato."),
        ("Streaming de Respuestas (SSE):", "Transmisión de tokens en tiempo real mejorando la latencia percibida por el usuario final."),
        ("Trazabilidad & Citas Interactivas:", "Cada respuesta incluye enlaces directos al documento PDF, número de página y score de confianza."),
    ]
    desc = "Cuadrícula de 4 iconos modernos con tarjetas visuales: (1) Filtro de Metadatos [Misión: Mars2020], (2) Escudo de Seguridad / Fallback contra alucinaciones, (3) Transmisión de texto en tiempo real (Streaming SSE), (4) Tarjeta de Citas con badge de confianza (Score 98%)."
    render_split_slide(slide, "Mejores Prácticas de Ingeniería", "Estrategias aplicadas en la Fase 04 - Transit", blocks, "Los 4 Pilares de un RAG Empresarial", desc, image_on_left=True)
    return slide


def build_slide_11(prs, layouts):
    """Slide 11: Arquitectura del Proyecto (Texto a la Izquierda, Imagen a la Derecha)."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    blocks = [
        ("Almacenamiento e Ingesta:", "PDFs oficiales de la NASA en Azure Blob Storage procesados mediante Azure AI Search Indexer."),
        ("Motor de Búsqueda:", "Azure AI Search con índice híbrido HNSW vectorial + BM25 + Semantic Reranker activo."),
        ("Cerebro y Orquestación:", "Microsoft Agent Framework en backend FastAPI conectando Azure OpenAI (GPT-4o y Text-Embedding-3)."),
        ("Experiencia de Usuario:", "Frontend en Next.js con explorador de chunks, comparador de rerank y chat conversacional."),
    ]
    desc = "Diagrama de arquitectura cloud de extremo a extremo: Azure Blob Storage -> Indexer & Skills de Azure AI Search -> Índice Híbrido -> Backend FastAPI (Microsoft Agent Framework) -> Frontend Next.js con panel de control de documentos y chat."
    render_split_slide(slide, "Arquitectura del Proyecto", "Ecosistema Cloud: Azure AI Foundry + Search + FastAPI + Next.js", blocks, "Arquitectura End-to-End Cloud y On-Premise", desc, image_on_left=False)
    return slide


def build_slide_12(prs, layouts):
    """Slide 12: Transición a la Demo."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    set_title(slide, "Laboratorio Práctico")
    
    ph_body = slide.placeholders[2]
    tf = ph_body.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "Con estos conceptos claros, veamos a RAG y a nuestro agente en acción sobre las misiones a Marte."
    r.font.name = FONT_PRIMARY
    r.font.size = Pt(48)
    r.font.color.rgb = COLOR_DARK
    return slide


def build_slide_13(prs, layouts):
    """Slide 13: Casos de Prueba en la Demo (Texto a la Izquierda, Imagen a la Derecha)."""
    slide = prs.slides.add_slide(layouts['DIAPOSITIVA-02'])
    blocks = [
        ("Caso 1: Búsqueda Semántica Conceptual:", "Pregunta sin palabras exactas ('¿Qué experimentos buscan biofirmas fósiles?') -> Encuentra Perseverance y Mars 2020."),
        ("Caso 2: El Poder del Semantic Reranker (Cráter Jezero):", "• Sin Rerank: Se mezclan fragmentos de Phoenix/Curiosity y el agente reporta falta de evidencia.\n• Con Rerank: Los fragmentos de Mars 2020 suben al #1 y la respuesta es 100% precisa."),
        ("Caso 3: Pregunta Fuera de Dominio (Out of Corpus):", "Pregunta ajena ('¿Cuál es el menú del comedor de la NASA?') -> El agente reconoce límites sin alucinar."),
    ]
    desc = "Captura de pantalla dividida de la aplicación web: Panel izquierdo mostrando la comparativa de chunks con vs sin Rerank; Panel derecho mostrando la respuesta final del agente con citas interactivas y badges de confianza."
    render_split_slide(slide, "Casos de Prueba en la Demo", "Lo que demostraremos en vivo", blocks, "Interfaz de la Demo (Next.js + FastAPI)", desc, image_on_left=False)
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


def generate_balanced_presentation(output_path=OUTPUT_PPTX, template_path=TEMPLATE_PPTX):
    """Compila la presentación equilibrada con variedad y placeholders de imágenes."""
    print("=" * 70)
    print("Iniciando compilación equilibrada 'RAG + MAF'...")
    print("=" * 70)

    prs = pptx.Presentation(template_path)
    layouts = {l.name: l for l in prs.slide_layouts}

    print("Construyendo Slide 1: Carátula...")
    build_slide_1(prs, layouts)

    print("Construyendo Slide 2: Agenda...")
    build_slide_2(prs, layouts)

    print("Construyendo Slide 3: El Desafío de los LLMs (Texto Izq / Imagen Der)...")
    build_slide_3(prs, layouts)

    print("Construyendo Slide 4: Fundamentos de RAG (Imagen Izq / Texto Der)...")
    build_slide_4(prs, layouts)

    print("Construyendo Slide 5: Arquitectura del Pipeline (Texto Izq / Imagen Der)...")
    build_slide_5(prs, layouts)

    print("Construyendo Slide 6: Deep Dive: Inferencia Bayesiana con Fórmulas LaTeX...")
    build_slide_6(prs, layouts)

    print("Construyendo Slide 7: Búsqueda Vectorial vs. Híbrida (Con Fórmula RRF)...")
    build_slide_7(prs, layouts)

    print("Construyendo Slide 8: Semantic Reranker (Imagen Izq / Texto Der)...")
    build_slide_8(prs, layouts)

    print("Construyendo Slide 9: RAG Agéntico (Texto Izq / Imagen Der)...")
    build_slide_9(prs, layouts)

    print("Construyendo Slide 10: Mejores Prácticas de Ingeniería (Imagen Izq / Texto Der)...")
    build_slide_10(prs, layouts)

    print("Construyendo Slide 11: Arquitectura del Proyecto (Texto Izq / Imagen Der)...")
    build_slide_11(prs, layouts)

    print("Construyendo Slide 12: Transición a la Demo...")
    build_slide_12(prs, layouts)

    print("Construyendo Slide 13: Casos de Prueba en la Demo (Texto Izq / Imagen Der)...")
    build_slide_13(prs, layouts)

    print("Construyendo Slide 14: Cierre / Feedback...")
    build_slide_14(prs, layouts)

    prs.save(output_path)
    print("=" * 70)
    print(f"[ÉXITO] Presentación generada exitosamente en: '{output_path}'")
    print(f"Total de diapositivas generadas: {len(prs.slides)}")
    print("=" * 70)


if __name__ == "__main__":
    generate_balanced_presentation()
