import sys

with open('server.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_block = """INSTRUCCIONES CRÍTICAS, ESTRICTAS Y OBLIGATORIAS:
1. Tienes PROHIBIDO inventar criterios. Debes extraer EXACTAMENTE el nombre de cada criterio y su PUNTAJE MÁXIMO literal de la sección <RUBRICA>. 
2. Si la rúbrica dice "1. Elaboration of contents", tu JSON debe decir "name": "1. Elaboration of contents". Si su puntaje máximo es 4 pts, tu JSON debe decir "max": 4.
3. Escribe TODA tu respuesta (la retroalimentación, errores y fortalezas) ÚNICAMENTE en Español.
4. Para cada criterio, justifica tu puntuación, lista errores específicos (citas exactas del estudiante) y destaca sus fortalezas.
5. Debes devolver ÚNICAMENTE un objeto JSON válido sin texto extra.
Usa EXACTAMENTE este formato:

```json
{{
    "transcript": "[Texto completo de la transcripción de voz extraída]",
    "vocabulary_detected": ["palabra1", "palabra2"],
    "vocabulary_missing": ["palabra3", "palabra4"],
    "criteria": [
      {{ 
        "name": "Nombre Exacto del Primer Criterio extraído de la Rúbrica", 
        "score": 3.5, 
        "max": 5.0, 
        "feedback": {{
           "justification": "[Párrafo detallado explicando el porqué de la nota, analizando el desempeño general en este criterio.]",
           "errors": ["Error específico 1", "Error 2"],
           "strengths": ["Fortaleza 1", "Fortaleza 2"]
        }}
      }},
      {{ 
        "name": "Nombre Exacto del Segundo Criterio extraído de la Rúbrica", 
        "score": 2.0, 
        "max": 4.0, 
        "feedback": {{
           "justification": "[...]",
           "errors": [],
           "strengths": []
        }}
      }},
      {{ 
        "name": "... Repite este bloque para CADA UNO de los criterios de la Rúbrica ...", 
        "score": 0, 
        "max": 0, 
        "feedback": {{
           "justification": "...",
           "errors": [],
           "strengths": []
        }}
      }}
    ]
}}
```"""

new_block = """INSTRUCCIONES CRÍTICAS, ESTRICTAS Y OBLIGATORIAS:
1. COPIA TEXTUALMENTE los nombres de los criterios de la sección <RUBRICA>. NO INVENTES NOMBRES. NO RESUMAS.
2. Extrae el PUNTAJE MÁXIMO literal de cada criterio. Si la rúbrica dice "4 pts", el JSON debe decir "max": 4. NO PONGAS 5.0 EN TODOS.
3. Genera EXACTAMENTE un bloque en el arreglo "criteria" por cada criterio que exista en la rúbrica proporcionada.
4. Escribe TODA tu respuesta (la retroalimentación, errores y fortalezas) ÚNICAMENTE en Español.
5. Debes devolver ÚNICAMENTE un objeto JSON válido.
Usa EXACTAMENTE este formato:

```json
{{
    "transcript": "[Texto completo de la transcripción de voz extraída]",
    "vocabulary_detected": ["palabra1", "palabra2"],
    "vocabulary_missing": ["palabra3", "palabra4"],
    "criteria": [
      {{ 
        "name": "[Copia aquí el nombre exacto del Criterio 1, ej: '1. Elaboration of contents']", 
        "score": [Tu calificación, ej: 3], 
        "max": [Puntaje máximo exacto según rúbrica, ej: 4], 
        "feedback": {{
           "justification": "[Párrafo detallado explicando el porqué de la nota, analizando el desempeño general en este criterio.]",
           "errors": ["Error específico 1", "Error 2"],
           "strengths": ["Fortaleza 1", "Fortaleza 2"]
        }}
      }},
      {{ 
        "name": "[Copia aquí el nombre exacto del Criterio 2, ej: '2. Use of grammar']", 
        "score": [Tu calificación, ej: 2.5], 
        "max": [Puntaje máximo exacto según rúbrica, ej: 3.5], 
        "feedback": {{
           "justification": "[...]",
           "errors": [],
           "strengths": []
        }}
      }},
      {{ 
        "name": "[... Y ASÍ SUCESIVAMENTE PARA TODOS LOS CRITERIOS DE LA RÚBRICA ...]", 
        "score": 0, 
        "max": 0, 
        "feedback": {{
           "justification": "...",
           "errors": [],
           "strengths": []
        }}
      }}
    ]
}}
```"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: server.py updated with strictly explicit JSON format.")
else:
    print("WARNING: Could not find block in server.py.")
