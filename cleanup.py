import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the "+ X more" caption for library
content = re.sub(r'            if len\(library\) > 24:\n\s+st\.caption\(f"\+ \{len\(library\)-24\} more"\)', '', content)

# 2. Remove the "+ X more" caption for candidates
content = re.sub(r'                    if len\(candidates\) > 24:\n\s+st\.caption\(f"\+ \{len\(candidates\)-24\} more"\)', '', content)

# 3. Remove Researcher tools expander
expander_pattern = re.compile(r'\s+with st\.expander\("Researcher tools", expanded=False\):.*?st\.markdown\(f"\*\*LLM Latency:\*\* \{st\.session_state\.get\(\'last_latency\', 0\)\} ms"\)', re.DOTALL)
content = re.sub(expander_pattern, '', content)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Cleanup complete.")
