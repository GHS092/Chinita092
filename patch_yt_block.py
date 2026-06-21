import sys

with open('server.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_code = """            data = json.loads(json_str)
            return JSONResponse({"result": data})
        except json.JSONDecodeError:"""

new_code = """            data = json.loads(json_str)
            # Detectar si la IA indicó que YouTube bloqueó el acceso
            if "bloque" in str(data.get("transcript", "")).lower() or "blocked" in str(data.get("transcript", "")).lower() or "captcha" in str(data.get("transcript", "")).lower():
                return JSONResponse({"error": "YouTube ha bloqueado temporalmente el acceso desde el servidor (CAPTCHA/IP Block). Inténtalo más tarde con este video o usa otro.", "raw": out}, status_code=422)
            
            return JSONResponse({"result": data})
        except json.JSONDecodeError:"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('server.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: server.py updated to catch YouTube block.")
else:
    print("WARNING: Could not find code block in server.py.")
