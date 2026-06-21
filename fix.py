import sys

with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "prompt = f'''Analiza el siguiente video de YouTube: {url}" in line:
        lines[i] = "        prompt = f'''Analiza el siguiente video de YouTube: {url}\nEres un experto evaluador. Evalúa el desempeño en el video basándote ESTRICTAMENTE en la siguiente rúbrica de calificación que el profesor ha proveído:\n\nIMPORTANTE: DEBES usar tus herramientas (como el skill youtube-content o scripts de Python con youtube-transcript-api) para extraer la transcripción del video. Extrae el texto primero, analiza el contenido y luego evalúalo. No digas que no puedes ver el video ni que YouTube te bloqueó.\n\n<RUBRICA>\n"
        # delete the next 4 lines
        del lines[i+1:i+6]
        break

with open('server.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
