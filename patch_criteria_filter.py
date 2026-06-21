import sys

with open('server.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_block = """INSTRUCCIONES CRÍTICAS, ESTRICTAS Y OBLIGATORIAS:
1. COPIA TEXTUALMENTE los nombres de los criterios de la sección <RUBRICA>. NO INVENTES NOMBRES. NO RESUMAS.
2. Extrae el PUNTAJE MÁXIMO literal de cada criterio. Si la rúbrica dice "4 pts", el JSON debe decir "max": 4. NO PONGAS 5.0 EN TODOS.
3. Genera EXACTAMENTE un bloque en el arreglo "criteria" por cada criterio que exista en la rúbrica proporcionada.
4. Escribe TODA tu respuesta (la retroalimentación, errores y fortalezas) ÚNICAMENTE en Español.
5. Debes devolver ÚNICAMENTE un objeto JSON válido.
Usa EXACTAMENTE este formato:"""

new_block = """INSTRUCCIONES CRÍTICAS, ESTRICTAS Y OBLIGATORIAS PARA EXTRAER CRITERIOS:
1. La sección <RUBRICA> contiene mucho texto de contexto (instrucciones, Learning Outcomes, longitud del video, etc.). DEBES IGNORAR ESE TEXTO.
2. LOS CRITERIOS REALES A CALIFICAR son ÚNICAMENTE aquellos que tienen explícitamente una ESCALA DE PUNTAJES (ej. "4 pts, 3 pts, 2 pts", "3.5 pts, 2.5 pts", etc.).
3. Busca CADA bloque que tenga una escala de puntos. El título justo encima de esa escala es el NOMBRE EXACTO DEL CRITERIO (ej. "1. Elaboration of contents", "2. Use of grammar").
4. COPIA TEXTUALMENTE esos nombres. NO inventes nombres ni extraigas "Learning Outcome" o "Length of video" si no son los criterios calificados con escala de puntos.
5. El valor "max" en tu JSON debe ser el NÚMERO MÁS ALTO de la escala de ese criterio (Si la escala empieza en 3.5 pts, el max es 3.5. Si empieza en 4 pts, el max es 4).
6. Genera EXACTAMENTE un bloque en "criteria" por CADA criterio real encontrado que tenga escala de puntajes.
7. Escribe TODA tu respuesta ÚNICAMENTE en Español.
8. Debes devolver ÚNICAMENTE un objeto JSON válido.

Usa EXACTAMENTE este formato:"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: server.py updated with syllabus filtering instructions.")
else:
    print("WARNING: Could not find block in server.py.")
