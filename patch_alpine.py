import sys

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the x-show with x-if for the results container
old_container = """          <!-- Results Side-by-Side Layout -->
          <div class="eval-layout" x-show="hermesState.result && !hermesState.loading">"""

new_container = """          <!-- Results Side-by-Side Layout -->
          <template x-if="hermesState.result && !hermesState.loading">
          <div class="eval-layout">"""

# Close the template at the end of the eval-layout block. It ends right before <!-- Chat Tab -->
# Let's use string replacement for the exact end block.
old_end_block = """            </div>
          </div>
        </div>
        
        <!-- Chat Tab"""

new_end_block = """            </div>
          </div>
          </template>
        </div>
        
        <!-- Chat Tab"""

if old_container in content and old_end_block in content:
    content = content.replace(old_container, new_container)
    content = content.replace(old_end_block, new_end_block)
    print("SUCCESS: x-if wrapped the results.")
else:
    print("WARNING: Could not wrap results with x-if. Trying a different strategy...")

# Also fix the 422 error. A 422 error means "Unprocessable Entity" in FastAPI, which means the JSON payload sent in POST /setup/api/hermes/evaluate was invalid or missing required fields.
# Let's check server.py:
# class EvaluateRequest(BaseModel):
#     url: str
#     rubric_text: str
#
# If rubric_text is empty, does it fail? It shouldn't, as long as it's a string.
# Wait, let's look at the JS in index.html for `evaluateVideo`:
#             body: JSON.stringify({ url: this.hermesState.url, rubric_text: this.hermesState.rubricText })
#

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
