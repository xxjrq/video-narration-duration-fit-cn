#!/usr/bin/env python3
"""Validate measured narration against approved timing budgets."""
import json
import sys

MAX_SEGMENTS = 30

def ms(value, field, segment):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{segment}.{field} 必须是非负整数毫秒")
    return value

def main(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    version = data.get("version")
    if not isinstance(version, str) or not version.strip():
        raise ValueError("version 必填，用于标识已批准镜头版本")
    segments = data.get("segments")
    if not isinstance(segments, list) or not segments or len(segments) > MAX_SEGMENTS:
        raise ValueError("segments 必须为 1–30 个段落")
    rows, total_needed, total_available = [], 0, 0
    for i, s in enumerate(segments, 1):
        label = s.get("id", f"S{i}")
        if not isinstance(label, str) or not label:
            raise ValueError(f"第 {i} 段 id 必须为非空字符串")
        for field in ("narration_measured_ms", "approved_shot_ms", "start_offset_ms", "allowed_pause_after_ms"):
            if field not in s:
                raise ValueError(f"{label} 缺少 {field}；偏移或停顿缺失时无法确认合入")
        narration = ms(s["narration_measured_ms"], "narration_measured_ms", label)
        shot = ms(s["approved_shot_ms"], "approved_shot_ms", label)
        offset = ms(s["start_offset_ms"], "start_offset_ms", label)
        pause = ms(s["allowed_pause_after_ms"], "allowed_pause_after_ms", label)
        # A post-segment pause occupies the approved shot just like narration.
        # It is therefore required time, never extra narration capacity.
        available = shot - offset
        needed = narration + pause
        delta = needed - available
        status = "通过" if delta <= 0 else "超出"
        if delta <= 0:
            action = "无需改动"
        elif delta < narration:
            action = f"缩稿后重新实测，至少减少 {delta}ms；或申请延长已批准镜头至少 {delta}ms"
        elif offset + pause > shot:
            fixed_overrun = offset + pause - shot
            action = (f"申请延长已批准镜头至少 {delta}ms；起播偏移与停顿合计 {offset + pause}ms，"
                      f"即使删除全部旁白仍超出 {fixed_overrun}ms，仅缩稿无法满足；偏移和停顿如需调整须另行确认")
        else:
            action = (f"申请延长已批准镜头至少 {delta}ms；当前起播偏移与停顿已占满镜头，"
                      "缩稿需删除整段旁白，无法保留本段口播；如要删除或调整时间安排须另行确认")
        rows.append((label, available, needed, delta, status, action))
        total_needed += needed
        total_available += available
    print(f"版本：{version}")
    print("段落 | 可用ms | 所需ms | 超出ms | 结论 | 建议待办")
    print("---|---:|---:|---:|---|---")
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]}")
    total_delta = total_needed - total_available
    verdict = "通过" if total_delta <= 0 and all(r[4] == "通过" for r in rows) else "不通过"
    print(f"总计 | {total_available} | {total_needed} | {total_delta} | {verdict} | 仅按实测时间预算核对")
    return 0 if verdict == "通过" else 2

if __name__ == "__main__":
    try:
        if len(sys.argv) != 2:
            raise ValueError("用法：check_duration.py 输入.json")
        sys.exit(main(sys.argv[1]))
    except (OSError, ValueError, json.JSONDecodeError) as e:
        print(f"无法确认合入：{e}", file=sys.stderr)
        sys.exit(1)
