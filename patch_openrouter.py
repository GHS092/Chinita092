import sys

file_path = "hermes-agent-main-original/plugins/model-providers/openrouter/__init__.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add _ANTHROPIC_REASONING_OPTIONAL_SUBSTRINGS and _anthropic_reasoning_is_mandatory
mandatory_logic = """
_ANTHROPIC_REASONING_OPTIONAL_SUBSTRINGS = (
    "claude-3",          # 3, 3.5, 3.7
    "claude-opus-4-0", "claude-opus-4.0", "claude-opus-4-1", "claude-opus-4.1",
    "claude-sonnet-4-0", "claude-sonnet-4.0",
    "claude-opus-4-2025", "claude-sonnet-4-2025",  # date-stamped 4.0 IDs
    "claude-opus-4-5", "claude-opus-4.5",
    "claude-sonnet-4-5", "claude-sonnet-4.5",
    "claude-haiku-4-5", "claude-haiku-4.5",
)

def _anthropic_reasoning_is_mandatory(model: str | None) -> bool:
    m = (model or "").lower()
    if not m.startswith(("anthropic/", "claude")) and "claude" not in m:
        return False
    return not any(sub in m for sub in _ANTHROPIC_REASONING_OPTIONAL_SUBSTRINGS)

class OpenRouterProfile"""

if "_anthropic_reasoning_is_mandatory" not in content:
    content = content.replace("class OpenRouterProfile", mandatory_logic)

# 2. Update build_api_kwargs_extras
orig_reasoning_logic = """        if supports_reasoning:
            if reasoning_config is not None:
                extra_body["reasoning"] = dict(reasoning_config)
            else:
                extra_body["reasoning"] = {"enabled": True, "effort": "medium"}"""

new_reasoning_logic = """        if supports_reasoning:
            if _anthropic_reasoning_is_mandatory(model):
                pass
            elif reasoning_config is not None:
                extra_body["reasoning"] = dict(reasoning_config)
            else:
                extra_body["reasoning"] = {"enabled": True, "effort": "medium"}"""

if "_anthropic_reasoning_is_mandatory(model):" not in content:
    content = content.replace(orig_reasoning_logic, new_reasoning_logic)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Patched openrouter/__init__.py successfully.")
