import sys

with open('server.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_block = """        out = stdout.decode('utf-8')
        
        import json
        import re
        
        try:
            match = re.search(r'```json\\s*(.*?)\\s*```', out, re.DOTALL)"""

new_block = """        out = stdout.decode('utf-8')
        err = stderr.decode('utf-8')
        print(f"HERMES OUT: {out}", flush=True)
        print(f"HERMES ERR: {err}", flush=True)
        
        import json
        import re
        
        try:
            match = re.search(r'```json\\s*(.*?)\\s*```', out, re.DOTALL)
            if not match:
                # Fallback: maybe it just outputted the JSON directly without the markdown wrapper
                match_fallback = re.search(r'\\{.*\\}', out, re.DOTALL)
                if match_fallback:
                    out = match_fallback.group(0)
                    # We create a fake match object so the next block works
                    class FakeMatch:
                        def group(self, idx): return out
                    match = FakeMatch()"""

content = content.replace(old_block, new_block)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(content)
