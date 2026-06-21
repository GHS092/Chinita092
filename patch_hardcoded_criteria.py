import sys

with open('server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Buscamos la definición del prompt antiguo
start_idx = content.find("        prompt = f'''Analiza el siguiente texto que es la transcripción de un video de YouTube:")
if start_idx == -1:
    print("WARNING: Could not find prompt start in server.py.")
    sys.exit(1)

end_idx = content.find("        process = await asyncio.create_subprocess_exec(")
if end_idx == -1:
    print("WARNING: Could not find prompt end in server.py.")
    sys.exit(1)

old_prompt_block = content[start_idx:end_idx]

new_prompt_block = """        prompt = f'''Analiza el siguiente texto que es la transcripción de un video de YouTube:

<TRANSCRIPCION>
{transcript_text}
</TRANSCRIPCION>

Eres un profesor universitario experto, sumamente analítico y riguroso. Tu objetivo es CALIFICAR al estudiante basándote en los 6 criterios estáticos de la universidad.
Debes rellenar los puntajes y la retroalimentación para cada uno de los 6 criterios que se te entregan en el formato JSON.

INSTRUCCIONES CRÍTICAS, ESTRICTAS Y OBLIGATORIAS:
1. TIENES PROHIBIDO INVENTAR CRITERIOS O CAMBIAR LOS NOMBRES. Los 6 criterios son ESTÁTICOS e INAMOVIBLES.
2. Escribe TODA tu respuesta ÚNICAMENTE en Español.
3. Para cada criterio, elige UNA de las notas permitidas, justifica tu puntuación, lista errores específicos (citas exactas del estudiante) y destaca fortalezas.
4. Debes devolver ÚNICAMENTE un objeto JSON válido, copiando EXACTAMENTE la estructura de abajo y rellenando los campos indicados con corchetes [ ].

Usa EXACTAMENTE este formato:

```json
{{
    "transcript": "[Texto completo de la transcripción de voz extraída]",
    "vocabulary_detected": ["palabra1", "palabra2"],
    "vocabulary_missing": ["palabra3", "palabra4"],
    "criteria": [
      {{ 
        "name": "1. Elaboration of contents", 
        "score": [ELIGE UNO: 4, 3, 2, 1, 0], 
        "max": 4, 
        "feedback": {{
           "justification": "[Párrafo detallado explicando por qué el contenido responde o no a las indicaciones de la actividad.]",
           "errors": ["Error específico 1", "Error 2"],
           "strengths": ["Fortaleza 1", "Fortaleza 2"]
        }}
      }},
      {{ 
        "name": "2. Use of grammar", 
        "score": [ELIGE UNO: 3.5, 2.5, 1.5, 0.5, 0], 
        "max": 3.5, 
        "feedback": {{
           "justification": "[Párrafo detallado sobre el uso de gramática sin errores.]",
           "errors": [],
           "strengths": []
        }}
      }},
      {{ 
        "name": "3. Use of vocabulary", 
        "score": [ELIGE UNO: 3.5, 2.5, 1.5, 0.5, 0], 
        "max": 3.5, 
        "feedback": {{
           "justification": "[Párrafo detallado sobre el uso del vocabulario de la unidad.]",
           "errors": [],
           "strengths": []
        }}
      }},
      {{ 
        "name": "4. Use of pronunciation and intonation", 
        "score": [ELIGE UNO: 5, 3.5, 2, 0.5, 0], 
        "max": 5, 
        "feedback": {{
           "justification": "[Párrafo detallado sobre pronunciación, entonación y si el mensaje se entiende a pesar de errores.]",
           "errors": [],
           "strengths": []
        }}
      }},
      {{ 
        "name": "5. Oral presentation", 
        "score": [ELIGE UNO: 2, 1.5, 1, 0.5, 0], 
        "max": 2, 
        "feedback": {{
           "justification": "[Párrafo detallado sobre si mira a la cámara y no depende de sus notas.]",
           "errors": [],
           "strengths": []
        }}
      }},
      {{ 
        "name": "6. Delivery of speech/dialogue", 
        "score": [ELIGE UNO: 2, 1.5, 1, 0.5, 0], 
        "max": 2, 
        "feedback": {{
           "justification": "[Párrafo detallado sobre si vocaliza con un volumen de voz audible.]",
           "errors": [],
           "strengths": []
        }}
      }}
    ]
}}
```
'''
"""

content = content.replace(old_prompt_block, new_prompt_block)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("SUCCESS: server.py updated with hardcoded static criteria.")
