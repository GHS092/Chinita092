import sys

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_js = """              if(res.ok && data.result) {
                  this.hermesState.result = data.result;
              } else {
                  this.hermesState.error = data.error || 'Failed to evaluate video';
              }"""

new_js = """              if(res.ok && data.result) {
                  this.hermesState.result = data.result;
              } else {
                  this.hermesState.error = data.error || 'Failed to evaluate video';
                  if (data.raw) {
                      this.hermesState.error += '\\n\\nRAW OUTPUT FROM LLM:\\n' + data.raw;
                  }
              }"""

if old_js in content:
    content = content.replace(old_js, new_js)
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: evaluateVideo updated with data.raw.")
else:
    print("WARNING: Could not find js block.")
