import sys

with open('server.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_prompt_block = """        prompt = f'''Analiza el siguiente video de YouTube: {url}
Eres un experto evaluador. Evalúa el desempeño en el video basándote ESTRICTAMENTE en la siguiente rúbrica de calificación que el profesor ha proveído:

IMPORTANTE: DEBES usar tus herramientas (como el skill youtube-content o scripts de Python con youtube-transcript-api) para extraer la transcripción del video. Extrae el texto primero, analiza el contenido y luego evalúalo. No digas que no puedes ver el video ni que YouTube te bloqueó.

<RUBRICA>
</RUBRICA>

INSTRUCCIONES CRÍTICAS:
1. Extrae los criterios principales de la rúbrica provista.
2. Evalúa el video para cada criterio.
3. Debes devolver ÚNICAMENTE un objeto JSON válido. Usa EXACTAMENTE el bloque ```json ... ``` para tu respuesta:

```json
{{
    "criterio_1": {{ "name": "Nombre del Criterio", "score": [numero], "max": [numero maximo], "feedback": "[string breve]" }},
    "criterio_2": {{ "name": "Nombre del Criterio", "score": [numero], "max": [numero maximo], "feedback": "[string breve]" }}
}}
```
Asegúrate de que el JSON sea perfectamente parseable.
'''"""

new_prompt_block = """        prompt = f'''Analiza el siguiente video de YouTube: {url}
Eres un experto evaluador. Evalúa el desempeño en el video basándote ESTRICTAMENTE en la siguiente rúbrica de calificación que el profesor ha proveído:

IMPORTANTE: DEBES usar tus herramientas (como el skill youtube-content o scripts de Python con youtube-transcript-api) para extraer la transcripción del video. Extrae el texto primero, analiza el contenido y luego evalúalo. No digas que no puedes ver el video ni que YouTube te bloqueó.

<RUBRICA>
{rubric_text}
</RUBRICA>

INSTRUCCIONES CRÍTICAS:
1. Extrae los criterios principales de la rúbrica provista.
2. Escribe TODA tu respuesta, análisis y retroalimentación ÚNICAMENTE en Español.
3. Debes devolver ÚNICAMENTE un objeto JSON válido con la transcripción, el vocabulario y la evaluación.
Usa EXACTAMENTE este formato:

```json
{{
    "transcript": "[Texto completo de la transcripción de voz extraída]",
    "vocabulary_detected": ["palabra1", "palabra2"],
    "vocabulary_missing": ["palabra3", "palabra4"],
    "criteria": [
      {{ "name": "Nombre del Criterio", "score": [numero], "max": [numero maximo], "feedback": "[Retroalimentación detallada en Español]" }},
      {{ "name": "Nombre del Criterio", "score": [numero], "max": [numero maximo], "feedback": "[Retroalimentación detallada en Español]" }}
    ]
}}
```
Asegúrate de que el JSON sea perfectamente parseable y no contenga texto fuera del bloque.
'''"""

if old_prompt_block in content:
    content = content.replace(old_prompt_block, new_prompt_block)
else:
    print("WARNING: Could not find old prompt block. Trying partial replace...")
    # fallback partial replace for the <RUBRICA> section
    content = content.replace("<RUBRICA>\n</RUBRICA>", "<RUBRICA>\n{rubric_text}\n</RUBRICA>")

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(content)
