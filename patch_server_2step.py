import sys
import re

with open('server.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_evaluate = """async def api_hermes_evaluate(request: Request):
    try:
        body = await request.json()
        url = body.get("url")
        rubric_text = body.get("rubric", "")
        
        if not url: return JSONResponse({"error": "No URL provided"}, status_code=400)
        if not rubric_text or not isinstance(rubric_text, str): 
            return JSONResponse({"error": "No rubric provided or invalid format"}, status_code=400)
        
        prompt = f'''Analiza el siguiente video de YouTube: {url}
Eres un profesor universitario experto, sumamente analítico y riguroso. Evalúa el desempeño en el video basándote ESTRICTAMENTE en la siguiente rúbrica de calificación:

IMPORTANTE: DEBES usar tus herramientas para extraer la transcripción del video. Extrae el texto primero, analiza el contenido y luego evalúalo. No digas que no puedes ver el video.

<RUBRICA>
{rubric_text}
</RUBRICA>"""

new_evaluate = """import asyncio
async def api_hermes_evaluate(request: Request):
    try:
        body = await request.json()
        url = body.get("url")
        rubric_text = body.get("rubric", "")
        
        if not url: return JSONResponse({"error": "No URL provided"}, status_code=400)
        if not rubric_text or not isinstance(rubric_text, str): 
            return JSONResponse({"error": "No rubric provided or invalid format"}, status_code=400)
            
        # STEP 1: Extraer transcripción primero para evitar alucinaciones del modelo
        fetch_prompt = f"Extrae TODA la transcripción de este video y devuélvela como texto plano: {url}"
        process1 = await asyncio.create_subprocess_exec(
            "hermes", "-s", "youtube-content", "-z", fetch_prompt,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout1, stderr1 = await process1.communicate()
        transcript_text = stdout1.decode('utf-8').strip()
        
        if "bloque" in transcript_text.lower() or "blocked" in transcript_text.lower() or "limitacion" in transcript_text.lower():
             return JSONResponse({"error": "YouTube bloqueó la extracción o el video no tiene subtítulos. (Intenta en el Chat o usa otro video)."}, status_code=422)
             
        if not transcript_text or len(transcript_text) < 10:
             return JSONResponse({"error": "No se pudo obtener la transcripción del video."}, status_code=422)

        # STEP 2: Inyectar texto en el prompt evaluador
        prompt = f'''Analiza el siguiente texto que es la transcripción de un video de YouTube:

<TRANSCRIPCION>
{transcript_text}
</TRANSCRIPCION>

Eres un profesor universitario experto, sumamente analítico y riguroso. Evalúa el desempeño en la transcripción basándote ESTRICTAMENTE en la siguiente rúbrica de calificación:

<RUBRICA>
{rubric_text}
</RUBRICA>"""

if old_evaluate in content:
    content = content.replace(old_evaluate, new_evaluate)
    
    # We also need to remove the prompt part that says DEBES usar tus herramientas...
    # Oh wait, my old_evaluate replacement already replaces that! Yes!
    
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: server.py updated to 2-step process.")
else:
    print("WARNING: Could not find block in server.py.")
