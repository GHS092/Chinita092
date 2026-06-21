import sys

with open('server.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_json = """    "criteria": [
      {{ 
        "name": "Nombre del Criterio", 
        "score": [numero], 
        "max": [numero maximo], 
        "feedback": {{
           "justification": "[Párrafo detallado explicando el porqué de la nota, analizando el desempeño general en este criterio.]",
           "errors": ["Error específico 1 (ej: pronunció mal X, olvidó mencionar Y)", "Error 2"],
           "strengths": ["Fortaleza 1", "Fortaleza 2"]
        }}
      }}
    ]
}}
```
Asegúrate de que el JSON sea perfectamente parseable. Si un array como errors o strengths está vacío, envíalo como []."""

new_json = """    "criteria": [
      {{ 
        "name": "Nombre del Criterio", 
        "score": 3, 
        "max": 5, 
        "feedback": {{
           "justification": "[Párrafo detallado explicando el porqué de la nota, analizando el desempeño general en este criterio.]",
           "errors": ["Error específico 1", "Error 2"],
           "strengths": ["Fortaleza 1", "Fortaleza 2"]
        }}
      }}
    ]
}}
```
SOLO DEVUELVE EL JSON. NO añadas introducciones, ni saludos, ni notas finales. Si un array como errors o strengths está vacío, envíalo como []."""

if old_json in content:
    content = content.replace(old_json, new_json)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: server.py updated.")
else:
    print("WARNING: Could not find json block.")
