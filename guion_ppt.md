Viewed README.md:1-188

# 🚀 Guión de Presentación: "RAG con Microsoft Agent Framework & Azure AI"
### *Fase 04 - Transit: Misiones a Marte*
**Serie:** Miércoles de IA (Comunidad IA / BCP - Credicorp)  
**Público objetivo:** Público general e ingenieros de negocio, con secciones de profundidad matemática/técnica explicadas de manera intuitiva.

---

## 📋 Resumen de la Estructura de Diapositivas

| # | Diapositiva | Layout Base | Objetivo Clave |
|---|---|---|---|
| **01** | **Carátula**: RAG + Microsoft Agent Framework | `CARATULA-01` | Impacto inicial y presentación del tema. |
| **02** | **Agenda** | `EN-BLANCO-01` | Estructura en 5 bloques del evento. |
| **03** | **¿Por qué fallan los LLMs solos? El problema de la memoria cerrada** | `DIAPOSITIVA-02` | Motivar la necesidad de RAG (alucinación y desactualización). |
| **04** | **¿Qué es RAG? La analogía del "Examen a libro abierto"** | `DIAPOSITIVA-02` | Definición intuitiva de Retrieval-Augmented Generation. |
| **05** | **Componentes Fundamentales de un Sistema RAG** | `DIAPOSITIVA-02` | Explicar Ingesta, Chunking, Embeddings y Retrieval. |
| **06** | **Deep Dive Técnico: RAG como Probabilidad Bayesiana** 🧠 | `DIAPOSITIVA-02` | Sección "sorpresa" con fundamento matemático claro. |
| **07** | **Búsqueda Vectorial vs. Búsqueda Híbrida** | `DIAPOSITIVA-02` | Por qué combinar palabras clave (BM25) con vectores. |
| **08** | **Reranking: El secreto de la precisión en Azure AI Search** | `DIAPOSITIVA-02` | Bi-Encoder vs. Cross-Encoder (Semantic Reranker). |
| **09** | **Evolución Arquitectural: De RAG Estático a RAG con Agentes (MAF)** | `DIAPOSITIVA-02` | El LLM como agente que decide cuándo y cómo buscar (*Tool Calling*). |
| **10** | **Optimizaciones Clave para RAG Empresarial** | `DIAPOSITIVA-02` | Metadatos, Grounded Prompting y control de alucinaciones. |
| **11** | **Arquitectura de la Solución: Azure AI Search + Foundry + MAF** | `DIAPOSITIVA-02` | Vista integral del pipeline del proyecto `04-transit`. |
| **12** | **Transición a la Demo** | `DIAPOSITIVA-02` | Puente hacia la parte práctica en vivo. |
| **13** | **DEMO EN VIVO: Corpus NASA & Misión Marte (Crater Jezero)** | `DIAPOSITIVA-02` | Casos: Búsqueda semántica, impacto del Reranker y pregunta fuera de dominio. |
| **14** | **Cierre & Feedback** | `Diapositiva de título` | Llamado a la acción, comunidad y feedback con QR. |

---

## 📑 Guión Detallado Diapositiva por Diapositiva

---

### Diapositiva 1: Carátula Principal
- **Layout:** `CARATULA-01`
- **Fondo:** Fotografía corporativa completa de personas / equipo (`image13.jpg`).
- **Elementos en pantalla:**
  - **Título (Blanco, 44pt, Inter Tight Black):** `RAG + Agent Framework`
  - **Subtítulo (Blanco, 20pt, Inter Tight):** `Generación Aumentada por Recuperación con Azure AI y Microsoft Agent Framework`
  - **Pie de página:** Logo Credicorp en vector blanco.

> 🎙️ **Guión del Expositor:**  
> *"¡Buenas tardes a todos y bienvenidos a una nueva edición de los Miércoles de IA! Hoy vamos a hablar de una de las tecnologías más demandadas y transformadoras en la inteligencia artificial generativa moderna: **RAG (Retrieval-Augmented Generation)**. Vamos a descubrir no solo qué es y cómo resuelve las limitaciones de los modelos de lenguaje, sino cómo integrarlo con el nuevo **Microsoft Agent Framework** y **Azure AI Search** a través de una demo real con documentos de misiones a Marte de la NASA. ¡Comencemos!"*

---

### Diapositiva 2: Agenda
- **Layout:** `EN-BLANCO-01`
- **Elementos en pantalla:**
  - **Título (Magenta `#C3338E`, 48pt, Inter Tight Black):** `Agenda`
  - **Tabla limpia sin fondo (5 filas x 2 columnas):**
    - `01` | **El Problema y la Solución:** ¿Qué es y qué resuelve RAG?
    - `02` | **Los Componentes Clave & Fundamento Matemático:** De vectores a probabilidad bayesiana
    - `03` | **Técnicas de Precisión:** Búsqueda Híbrida y Semantic Reranker
    - `04` | **RAG Agéntico:** Integración con Microsoft Agent Framework en Azure
    - `05` | **Demo en Vivo:** Explorando el cráter Jezero con documentos de la NASA

> 🎙️ **Guión del Expositor:**  
> *"Nuestra sesión de hoy está dividida en 5 momentos clave. Primero entenderemos el dolor real de negocio que resuelve RAG. Luego desglosaremos su anatomía y veremos una perspectiva matemática elegante pero muy accesible. Después aprenderemos las técnicas avanzadas como la búsqueda híbrida y el reordenamiento semántico. En el cuarto bloque veremos cómo un agente autónomo toma el control de las búsquedas, y cerraremos con una demostración interactiva en tiempo real."*

---

### Diapositiva 3: El Problema
- **Layout:** `DIAPOSITIVA-02`
- **Elementos en pantalla:**
  - **Título:** `El Desafío de los LLMs`
  - **Subtítulo (Magenta):** `Límites de los Modelos de Lenguaje Aislados`
  - **Cuerpo de texto:**
    - **Corte de conocimiento (Knowledge Cutoff):**  
      Los modelos solo saben lo que aprendieron durante su entrenamiento. No conocen tus datos de hoy.
    - **Alucinaciones:**  
      Cuando un modelo no sabe la respuesta, tiende a inventar datos con absoluta seguridad sintáctica.
    - **Falta de Trazabilidad:**  
      No pueden citar la página, el memorándum o el documento oficial de donde extrajeron el dato.
    - **Costo y lentitud de reentrenar:**  
      Hacer *fine-tuning* o reentrenar cada semana es inviable técnica y económicamente.

- 🖼️ **Descripción de la Imagen sugerida (Lado derecho):**  
  *Ilustración dividida en 2 paneles: en la izquierda, un robot LLM mirando un calendario vencido ("Entrenado en 2024") respondiendo con signos de interrogación y alucinaciones; a la derecha, una pila de documentos confidenciales y actualizados de 2026 a los cuales el LLM no tiene acceso por estar aislado.*

> 🎙️ **Guión del Expositor:**  
> *"Imaginemos que contratamos al profesional más inteligente del mundo, pero lo encerramos en una habitación sin conexión a internet y con libros de hace dos años. Si le preguntamos sobre la política crediticia aprobada ayer o un manual técnico interno, tiene dos opciones: admitir que no sabe, o peor aún, **alucinar** inventando una respuesta convincente. Reentrenar el modelo cada vez que subimos un PDF al banco costaría miles de dólares y semanas de cómputo. Aquí es donde surge la necesidad de conectar el cerebro del modelo con nuestras fuentes de datos."*

---

### Diapositiva 4: ¿Qué es RAG?
- **Layout:** `DIAPOSITIVA-02`
- **Elementos en pantalla:**
  - **Título:** `Fundamentos de RAG`
  - **Subtítulo (Magenta):** `Retrieval-Augmented Generation (Generación Aumentada por Recuperación)`
  - **Cuerpo de texto:**
    - **La Analogía:**  
      Un examen de memoria vs. un **examen a libro abierto**.
    - **¿Cómo funciona?**  
      1. El usuario hace una pregunta.  
      2. El sistema **recupera (Retrieve)** fragmentos relevantes de nuestra base documental.  
      3. Se **inyectan (Augment)** estos fragmentos en el prompt como contexto.  
      4. El modelo **genera (Generate)** la respuesta final citando las fuentes.
    - **Beneficios inmediatos:**  
      Grounding garantizado, citas trazables, actualización instantánea de documentos y cero reentrenamiento.

- 🖼️ **Descripción de la Imagen sugerida (Lado derecho):**  
  *Diagrama de flujo conceptual en 3 pasos: (1) Usuario pregunta -> (2) Base de datos documental filtra y extrae 3 fichas de texto relevantes -> (3) El LLM recibe la pregunta + las 3 fichas y entrega una respuesta con etiquetas de citas numéricas [Doc1, Pág 4].*

> 🎙️ **Guión del Expositor:**  
> *"RAG no entrena al modelo; le da material de consulta en tiempo real. Es exactamente la diferencia entre pedirle a un estudiante que memorice una enciclopedia de 10,000 páginas para un examen, o permitirle entrar al examen con el libro en la mano y un índice perfecto para buscar la página exacta antes de responder. RAG es ese índice inteligente que le entrega al LLM solo la evidencia necesaria para construir una respuesta certera y verificable."*

---

### Diapositiva 5: Componentes Clave de RAG
- **Layout:** `DIAPOSITIVA-02`
- **Elementos en pantalla:**
  - **Título:** `Arquitectura del Pipeline`
  - **Subtítulo (Magenta):** `De Documentos Crudos a Respuestas con Grounding`
  - **Cuerpo de texto:**
    - **1. Chunking (Fragmentación):**  
      División de PDFs largos en fragmentos de 500-1000 tokens con solapamiento (*overlap*) para no perder contexto entre bordes.
    - **2. Embeddings (Vectorización):**  
      Transformación de cada fragmento de texto en vectores numéricos de alta dimensión (ej. 1536 dimensiones) que capturan el significado semántico.
    - **3. Vector Store / Search Index:**  
      Almacén especializado (Azure AI Search) con índices HNSW para búsqueda por proximidad angular/coseno.
    - **4. Grounded Prompting:**  
      Instrucciones estrictas al LLM: *"Responde únicamente utilizando la evidencia provista. Si no está en el texto, declara que no tienes información."*

- 🖼️ **Descripción de la Imagen sugerida (Lado derecho):**  
  *Infografía horizontal: Documento PDF -> Cuchilla de corte (Chunking con overlap) -> Modelo de Embedding (convertidor texto a números) -> Espacio vectorial 3D de puntos -> Retriever -> Prompt final con contexto.*

> 🎙️ **Guión del Expositor:**  
> *"Para que esto funcione con millones de páginas, necesitamos un pipeline muy estructurado. No podemos pasarle un PDF de 400 páginas entero al modelo. Primero lo dividimos en fragmentos manejables llamados 'chunks', cuidando un solapamiento para no cortar ideas por la mitad. Luego convertimos esos textos en representaciones matemáticas llamadas 'embeddings', que colocan las ideas similares cerca unas de otras en un espacio multidimensional. Cuando el usuario pregunta, encontramos los fragmentos más cercanos y se los entregamos al LLM con una regla de oro: responder únicamente con base en esa evidencia."*

---

### Diapositiva 6: Deep Dive Técnico (RAG como Probabilidad Bayesiana) 🧠
- **Layout:** `DIAPOSITIVA-02`
- **Elementos en pantalla:**
  - **Título:** `Fundamento Matemático`
  - **Subtítulo (Magenta):** `RAG expresado como Inferencia Bayesiana`
  - **Cuerpo de texto:**
    - **Generación Clásica (Paramétrica):**  
      $$P(y \mid x) = \prod_{t=1}^{T} P(y_t \mid y_{<t}, x; \theta)$$  
      *El modelo depende exclusivamente de sus pesos internos $\theta$. Si el dato no está en $\theta$, hay riesgo de alucinación.*
    - **Generación Aumentada (No Paramétrica):**  
      $$P(y \mid x) = \sum_{d \in D} \underbrace{P(d \mid x)}_{\text{Retriever (Prior)}} \cdot \underbrace{P(y \mid x, d; \theta)}_{\text{Generator (Likelihood)}}$$
    - **La Intuición:**  
      Tratamos el documento recuperado $d$ como una **variable latente**. El Retriever calcula la probabilidad de que el documento $d$ sea relevante para la pregunta $x$, y el LLM condiciona su generación a esa evidencia observable.

- 🖼️ **Descripción de la Imagen sugerida (Lado derecho):**  
  *Gráfico comparativo elegante: a la izquierda, una distribución de probabilidad difusa (modelo estándar); a la derecha, la distribución condicionada bayesiana que se estrecha y enfoca hacia la verdad cuando se incorpora la evidencia $d$, mostrando la reducción drástica de la entropía/incertidumbre.*

> 🎙️ **Guión del Expositor:**  
> *"Para los que disfrutan del rigor técnico: ¿qué es RAG matemáticamente? En un LLM tradicional, la probabilidad de generar una respuesta depende únicamente de los pesos estáticos del modelo. En cambio, en RAG introducimos una formulación bayesiana marginalizada sobre los documentos: el buscador calcula la probabilidad de que un fragmento $d$ contenga la evidencia dada la pregunta $x$, y luego el modelo generativo evalúa la probabilidad de la respuesta condicionada a dicho fragmento. Al introducir evidencia real, reducimos la entropía y la incertidumbre, colapsando el espacio de posibles alucinaciones."*

---

### Diapositiva 7: Búsqueda Vectorial vs. Búsqueda Híbrida
- **Layout:** `DIAPOSITIVA-02`
- **Elementos en pantalla:**
  - **Título:** `Estrategias de Recuperación`
  - **Subtítulo (Magenta):** `¿Por qué los vectores puros no son suficientes?`
  - **Cuerpo de texto:**
    - **Búsqueda por Palabras Clave (Léxica / BM25):**  
      Excelente para códigos exactos, siglas, números de parte (ej. *"Curiosity Rover RTG-04"*). Falla en sinónimos.
    - **Búsqueda Vectorial (Semántica):**  
      Excelente para conceptos e intenciones (ej. *"misiones que buscan vida"* encuentra *"estudios de biofirmas"*). Falla en términos raros o códigos específicos.
    - **Búsqueda Híbrida (Best of Both Worlds):**  
      Ejecuta BM25 y similitud vectorial en paralelo y combina los rankings usando **RRF (Reciprocal Rank Fusion)**:
      $$RRF\_Score(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

- 🖼️ **Descripción de la Imagen sugerida (Lado derecho):**  
  *Diagrama con dos caminos convergentes: Camino Superior (BM25 Keyword Search) y Camino Inferior (Dense Vector Search) que procesan la misma consulta y convergen en un nodo central "Reciprocal Rank Fusion" que entrega una lista unificada y balanceada de candidatos.*

> 🎙️ **Guión del Expositor:**  
> *"Existe el mito de que 'con vectores se resuelve todo'. Pero si buscas un número de contrato como 'B-4029-X', la búsqueda vectorial puede confundirse porque los embeddings no fueron entrenados para recordar números de serie específicos. Por otro lado, la búsqueda tradicional por palabras clave no entiende sinónimos. En Azure AI Search usamos **Búsqueda Híbrida**: disparamos ambos motores al mismo tiempo y fusionamos sus listas con el algoritmo RRF, garantizando que encontremos tanto la coincidencia conceptual como la palabra técnica exacta."*

---

### Diapositiva 8: Reranking en RAG
- **Layout:** `DIAPOSITIVA-02`
- **Elementos en pantalla:**
  - **Título:** `La Pieza Crítica: Semantic Reranker`
  - **Subtítulo (Magenta):** `Transformando candidatos crudos en evidencia de alta calidad`
  - **Cuerpo de texto:**
    - **El dilema de la velocidad vs. precisión:**  
      Los *Bi-Encoders* (vectores) son ultrarrápidos para filtrar 1,000,000 de documentos a los 50 mejores, pero comparan textos de forma independiente.
    - **Cross-Encoder / Semantic Reranker:**  
      Evalúa la pregunta y el fragmento **juntos** mediante atención cruzada (*Cross-Attention*), entendiendo matices, negaciones y contexto profundo.
    - **El Impacto en Negocio:**  
      Evita que fragmentos irrelevantes desplacen al dato correcto en el top 3, reduciendo la contaminación del contexto del LLM.

- 🖼️ **Descripción de la Imagen sugerida (Lado derecho):**  
  *Diagrama de embudo en dos fases: Fase 1 (Primer nivel rápido): De 100,000 documentos a Top 50 usando Búsqueda Híbrida -> Fase 2 (Semantic Reranker / Cross-Encoder): Reordena los 50 y coloca exactamente en el Top 3 los documentos con mayor relevancia semántica real hacia el LLM.*

> 🎙️ **Guión del Expositor:**  
> *"Imaginemos que la búsqueda híbrida nos devuelve 50 candidatos en milisegundos. Si le enviamos los 50 al LLM, saturamos su ventana de contexto y aumentamos el costo. Aquí entra el **Semantic Reranker**: un modelo de atención cruzada que analiza los mejores candidatos uno a uno con la pregunta. Detecta matices que los vectores pasaron por alto y reordena la lista para asegurar que los 3 fragmentos que llegan al modelo contengan exactamente la respuesta correcta."*

---

### Diapositiva 9: De RAG Tradicional a RAG con Agentes (MAF)
- **Layout:** `DIAPOSITIVA-02`
- **Elementos en pantalla:**
  - **Título:** `RAG Agéntico`
  - **Subtítulo (Magenta):** `Integración con Microsoft Agent Framework (MAF)`
  - **Cuerpo de texto:**
    - **RAG Tradicional (Pipeline Rígido):**  
      Siempre busca en la base de datos, incluso si la pregunta es un saludo (*"Hola"* -> busca en la BD -> gasta recursos).
    - **RAG con Agente (Orquestación Dinámica):**  
      El agente utiliza la búsqueda como una **Herramienta (Tool Calling)**.  
      - Si le preguntas algo general, responde directamente.  
      - Si requiere evidencia técnica, invoca la herramienta de búsqueda en Azure AI Search.  
      - Si la primera búsqueda no es suficiente, puede reformular la consulta (*Query Reformulation*).

- 🖼️ **Descripción de la Imagen sugerida (Lado derecho):**  
  *Ilustración de la arquitectura de Microsoft Agent Framework: Agente con LLM en el centro conectado a un catálogo de herramientas (Tool: Azure AI Search, Tool: Calculadora, Tool: CRM). El agente evalúa la intención del usuario y decide si activa o no la herramienta de recuperación de documentos.*

> 🎙️ **Guión del Expositor:**  
> *"Hasta hace poco, los sistemas RAG eran tuberías rígidas: entraba una pregunta y obligatoriamente se consultaba la base vectorial. Con el nuevo **Microsoft Agent Framework**, convertimos la recuperación en una **herramienta** que el agente decide cuándo y cómo usar. Si el usuario dice 'Hola, ¿cómo estás?', el agente no busca en los manuales; pero si pregunta por especificaciones de la nave Perseverance, invoca la herramienta de Azure AI Search, analiza los resultados y razona antes de responder."*

---

### Diapositiva 10: Optimizaciones para RAG Empresarial
- **Layout:** `DIAPOSITIVA-02`
- **Elementos en pantalla:**
  - **Título:** `Mejores Prácticas de Ingeniería`
  - **Subtítulo (Magenta):** `Estrategias aplicadas en la Fase 04 - Transit`
  - **Cuerpo de texto:**
    - **Filtrado por Metadatos:**  
      Etiquetar cada chunk con misión, fecha, autor y confidencialidad para segmentar búsquedas antes del cálculo vectorial.
    - **Control Estricto de Alucinaciones (*Out-of-Corpus Fallback*):**  
      Si los scores de relevancia no superan el umbral de confianza, el agente responde con honestidad que la información no está disponible.
    - **Streaming de Respuestas (SSE):**  
      Envío progresivo de tokens a la interfaz con citas enriquecidas en tiempo real.
    - **Trazabilidad & Citas:**  
      Cada respuesta entrega enlaces directos al archivo original, número de página y score de confianza.

- 🖼️ **Descripción de la Imagen sugerida (Lado derecho):**  
  *Cuadrícula de 4 iconos modernos con tarjetas visuales: (1) Filtro de Metadatos [Misión: Mars2020], (2) Escudo de Seguridad / Fallback contra alucinaciones, (3) Transmisión de texto en tiempo real (Streaming SSE), (4) Tarjeta de Citas con badge de confianza (Score 98%).*

> 🎙️ **Guión del Expositor:**  
> *"Llevar un RAG a producción corporativa requiere ingeniería sólida. En el proyecto implementamos filtros por metadatos para buscar solo en la misión o categoría relevante; umbrales de confianza para que el modelo reconozca cuando una pregunta está fuera del corpus; streaming para una experiencia de usuario instantánea; y trazabilidad total donde cada afirmación está respaldada por su página y documento fuente."*

---

### Diapositiva 11: Arquitectura de la Solución
- **Layout:** `DIAPOSITIVA-02`
- **Elementos en pantalla:**
  - **Título:** `Arquitectura del Proyecto`
  - **Subtítulo (Magenta):** `Ecosistema Cloud: Azure AI Foundry + Search + FastAPI + Next.js`
  - **Cuerpo de texto:**
    - **Almacenamiento e Ingesta:**  
      PDFs oficiales de la NASA en Azure Blob Storage procesados con Azure AI Search Indexer.
    - **Motor de Búsqueda:**  
      Azure AI Search con índice HNSW vectorial + BM25 + Semantic Reranker habilitado.
    - **Cerebro y Agente:**  
      Microsoft Agent Framework en backend FastAPI conectando Azure OpenAI (GPT-4o / Text-Embedding-3).
    - **Experiencia de Usuario:**  
      Frontend interactivo en Next.js con explorador de chunks, comparador de rerank y chat conversacional.

- 🖼️ **Descripción de la Imagen sugerida (Lado derecho):**  
  *Diagrama de arquitectura cloud de extremo a extremo: Azure Blob Storage -> Indexer & Skills de Azure AI Search -> Índice Híbrido -> Backend FastAPI (Microsoft Agent Framework) -> Frontend Next.js con panel de control de documentos y chat.*

> 🎙️ **Guión del Expositor:**  
> *"Veamos la arquitectura completa de nuestra solución. Todo nace en Azure Blob Storage con los documentos técnicos de la NASA. El Indexer de Azure AI Search extrae el texto, genera los chunks y calcula los embeddings. Cuando un usuario interactúa en la aplicación web en Next.js, la petición llega a nuestro backend en FastAPI con Microsoft Agent Framework, que orquesta la búsqueda híbrida con Semantic Reranking y alimenta a Azure OpenAI para generar la respuesta final."*

---

### Diapositiva 12: Transición a la Demo
- **Layout:** `DIAPOSITIVA-02`
- **Elementos en pantalla:**
  - **Título (Magenta, 28pt):** `Laboratorio Práctico`
  - **Mensaje central (Texto grande, 48pt, Centrado, Inter Tight):**  
    `Con estos conceptos claros, veamos a RAG y a nuestro agente en acción sobre las misiones a Marte.`

> 🎙️ **Guión del Expositor:**  
> *"La teoría cobra sentido cuando la vemos en vivo. Pasemos a nuestro laboratorio interactivo para comprobar cómo la búsqueda híbrida y el reordenamiento semántico transforman una consulta compleja en una respuesta exacta y citada."*

---

### Diapositiva 13: Demo en Vivo (Casos de Prueba Clave)
- **Layout:** `DIAPOSITIVA-02`
- **Elementos en pantalla:**
  - **Título:** `Casos de Prueba en la Demo`
  - **Subtítulo (Magenta):** `Lo que demostraremos en vivo`
  - **Cuerpo de texto:**
    - **Caso 1: Búsqueda Semántica Conceptual:**  
      Pregunta sin palabras exactas (*"¿Qué experimentos buscan biofirmas fósiles?"*) -> Encuentra Perseverance y Mars 2020.
    - **Caso 2: El Poder del Semantic Reranker (Cráter Jezero):**  
      *Sin Rerank:* Los fragmentos de Phoenix y Curiosity se mezclan y el grounding estricto reconoce falta de evidencia.  
      *Con Rerank:* Los fragmentos de Mars 2020 suben a la primera posición y la respuesta es 100% precisa.
    - **Caso 3: Pregunta Fuera de Dominio (Out of Corpus):**  
      Pregunta ajena (*"¿Cuál es el menú del comedor de la NASA?"*) -> El agente responde honestamente sin alucinar.

- 🖼️ **Descripción de la Imagen sugerida (Lado derecho):**  
  *Captura de pantalla dividida de la aplicación web: Panel izquierdo mostrando la comparativa de chunks con vs sin Rerank; Panel derecho mostrando la respuesta final del agente con citas interactivas y badges de confianza.*

> 🎙️ **Guión del Expositor:**  
> *(Durante la ejecución de la demo en pantalla):*  
> *"Observemos estos tres momentos clave en la demo:*  
> *1. Primero hacemos una pregunta conceptual sin usar nombres propios: el modelo entiende la intención semántica y localiza los documentos de Perseverance.*  
> *2. Ahora miren el Caso 2 con el Cráter Jezero: cuando desactivamos el Semantic Reranker, la búsqueda vectorial tradicional trae fragmentos de otras misiones como Curiosity y Phoenix. Al activar el Semantic Reranker, inmediatamente los fragmentos relevantes de Mars 2020 saltan al primer lugar del ranking y la respuesta se vuelve impecable.*  
> *3. Finalmente, si preguntamos por algo que no existe en los documentos, el agente reconoce sus límites y evita inventar información. Esto es lo que garantiza seguridad en entornos bancarios y empresariales."*

---

### Diapositiva 14: Cierre & Feedback
- **Layout:** `Diapositiva de título`
- **Fondo:** Gráfico institucional completo de cierre (`image19.png`).
- **Elementos en pantalla:**
  - **Hashtag superior izquierdo:** `#ComunidadIA` (Blanco, Italic, 30pt)
  - **Logo superior derecho:** Logo Credicorp (`image20.png`)
  - **Título central:**  
    `¡Ayúdanos a potenciar los` *(Blanco, 40pt, Bold)*  
    `MIÉRCOLES DE IA!` *(Turquesa/Cian `#2AD2C9`, 40pt, Bold)*
  - **Mascota corporativa:** Ilustración de personaje BCP (`image22.png`)
  - **Código QR:** Recuadro con QR interactivo de encuesta (`image21.png`)
  - **Subtítulo:** `Tu opinión es clave para seguir aprendiendo juntos. 🚀` *(Blanco, 32pt)*
  - **Slogan inferior:** `PONLE IA A TU DIA`

> 🎙️ **Guión del Expositor:**  
> *"RAG combinado con agentes no es solo una arquitectura técnica, es el puente definitivo entre el conocimiento estático de los LLMs y la información viva de nuestra organización. Muchas gracias a todos por acompañarnos hoy en este Miércoles de IA. Por favor, escaneen el código QR en pantalla para dejarnos su feedback y sugerencias de temas para las próximas sesiones. ¡Abrimos el espacio para preguntas!"*

---

### 💡 Tips para el Presentador durante la Sesión
1. **Ritmo:** Mantén los primeros 8-10 minutos en conceptos visuales e intuitivos antes de mostrar la formulación matemática de la Diapositiva 6.
2. **Énfasis en el Reranker:** Dedícale un momento especial a la Diapositiva 8 y al Caso 2 de la Demo, ya que el *Semantic Reranker* es el diferenciador que más sorprende a los equipos técnicos.
3. **Seguridad y Confianza:** Resalta que el objetivo de RAG en la organización no es solo responder rápido, sino **eliminar el riesgo operacional** mediante citas y trazabilidad documental.