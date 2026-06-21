import sys

file_path = "hermes-agent-main-original/hermes_cli/models.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add to OPENROUTER_MODELS
openrouter_marker = 'OPENROUTER_MODELS: list[tuple[str, str]] = [\n'
if '("anthropic/claude-fable-5",' not in content:
    content = content.replace(
        openrouter_marker,
        openrouter_marker + '    ("anthropic/claude-fable-5",               ""),\n'
    )

# 2. Add to nous provider
nous_marker = '"nous": [\n'
if '"anthropic/claude-fable-5",' not in content.split('"nous": [')[1][:200]:
    content = content.replace(
        nous_marker,
        nous_marker + '        "anthropic/claude-fable-5",\n'
    )

# 3. Also add normalization for claude-fable-5 if we want, but the patch doesn't strictly do that. Let's just follow the patch.

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Patched hermes_cli/models.py successfully.")
