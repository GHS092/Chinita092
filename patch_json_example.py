import sys

with open('server.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_json = """    "criteria": [
      { 
        "name": "Nombre del Criterio", 
        "score": 3, 
        "max": 5, 
        "feedback": {"""

new_json = """    "criteria": [
      { 
        "name": "[NOMBRE EXACTO DEL CRITERIO EN LA RÚBRICA]", 
        "score": [Tu puntaje asignado], 
        "max": [PUNTAJE MÁXIMO ESTRICTO DEL CRITERIO SEGÚN LA RÚBRICA], 
        "feedback": {"""

if old_json in content:
    content = content.replace(old_json, new_json)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: JSON example updated in server.py.")
else:
    print("WARNING: Could not find JSON example block.")
