import sys

with open('server.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_inst = """INSTRUCCIONES CRÍTICAS:
1. Analiza el video contra CADA criterio de la rúbrica.
2. Escribe TODA tu respuesta ÚNICAMENTE en Español.
3. Para cada criterio, debes justificar tu puntuación, listar errores específicos cometidos por el alumno (si los hay), y destacar sus fortalezas. Si omitió algo, indícalo.
4. Debes devolver ÚNICAMENTE un objeto JSON válido."""

new_inst = """INSTRUCCIONES CRÍTICAS, ESTRICTAS Y OBLIGATORIAS:
1. Tienes PROHIBIDO inventar criterios. Debes extraer EXACTAMENTE el nombre de cada criterio y su PUNTAJE MÁXIMO literal de la sección <RUBRICA>. 
2. Si la rúbrica dice "1. Elaboration of contents", tu JSON debe decir "name": "1. Elaboration of contents". Si su puntaje máximo es 4 pts, tu JSON debe decir "max": 4.
3. Escribe TODA tu respuesta (la retroalimentación, errores y fortalezas) ÚNICAMENTE en Español.
4. Para cada criterio, justifica tu puntuación, lista errores específicos (citas exactas del estudiante) y destaca sus fortalezas.
5. Debes devolver ÚNICAMENTE un objeto JSON válido sin texto extra."""

if old_inst in content:
    content = content.replace(old_inst, new_inst)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: server.py updated.")
else:
    print("WARNING: Could not find INSTRUCCIONES CRÍTICAS block.")
