#!/usr/bin/env python3
"""Offline regression checks; only Python's standard library is required."""
from pathlib import Path
import json
import re
import struct
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
png = (root / 'icon-512.png').read_bytes()
assert png[:8] == b'\x89PNG\r\n\x1a\n' and struct.unpack('>II', png[16:24]) == (512, 512)

def run(file, status, snippets, forbidden=()):
    result = subprocess.run([sys.executable, str(root / 'scripts/check_duration.py'), str(root / 'fixtures' / file)], capture_output=True, text=True)
    assert result.returncode == status, (file, result.returncode, result.stdout, result.stderr)
    text = result.stdout + result.stderr
    for snippet in snippets:
        assert snippet in text, (file, snippet, text)
    for snippet in forbidden:
        assert snippet not in text, (file, snippet, text)
    return text

run('success-input.json', 2, ['S2 | 7000 | 7100 | 100 | 超出', '总计 | 16000 | 15600 | -400 | 不通过'])
run('within-budget-input.json', 0, ['S1 | 9000 | 8800 | -200 | 通过', '无需改动'])
run('over-budget-input.json', 2, ['S1 | 9000 | 9500 | 500 | 超出', '至少减少 500ms'])
run('missing-measured-duration.json', 1, ['narration_measured_ms'], ['| 通过'])
run('trim-feasible-input.json', 2, ['至少减少 200ms', '重新实测', '延长已批准镜头至少 200ms'])
run('fixed-pause-overrun-input.json', 2, ['1100 | 600 | 超出', '延长已批准镜头至少 600ms', '即使删除全部旁白仍超出 500ms', '仅缩稿无法满足'], ['缩稿至少', '至少减少'])
run('fixed-offset-overrun-input.json', 2, ['-500 | 100 | 600 | 超出', '即使删除全部旁白仍超出 500ms'], ['缩稿至少', '至少减少'])
run('fixed-budget-full-input.json', 2, ['删除整段旁白', '无法保留本段口播', '另行确认'], ['缩稿至少', '至少减少'])
run('zero-narration-overrun-input.json', 2, ['仍超出 100ms', '延长已批准镜头至少 100ms'], ['缩稿至少', '至少减少'])
agent = (root / 'agents/openai.yaml').read_text()
for key in ['display_name', 'short_description', 'default_prompt', 'icon_small', 'icon_large']:
    match = re.search(r'^  ' + key + r': (.+)$', agent, re.M)
    assert match and match[1].startswith('"') and match[1].endswith('"'), key
    value = json.loads(match[1])
    if key == 'short_description': assert 25 <= len(value) <= 64
    if key == 'default_prompt': assert '$video-narration-duration-fit-cn' in value
    if key.startswith('icon_'): assert value == './icon-512.png' and (root / value).is_file()
print('self-test: passed; 9 actual offline timing branches and formal metadata checked')
