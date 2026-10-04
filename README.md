# 实测旁白时长匹配表

![推广图](assets/promo-1600x900.png)

把已实测的旁白时长放进已批准的镜头时间预算，立即得到逐段超出毫秒和下一步待办。它帮助剪辑、导演与口播审核在成片前发现“声音短于镜头却仍因起播偏移超时”这类问题；不生成语音、不重排镜头，也不改口播。

## 输入与结果

输入最多 30 段，每段含实测旁白毫秒数、已批准镜头毫秒数、起播偏移、允许段后停顿，以及版本号。可用时长为镜头减起播偏移；段后停顿也占用该镜头预算，计入所需时长。结果是一张逐段“可用时长 / 所需时长 / 超出毫秒 / 结论 / 待办”表和总计核对。只有字数或估算语速时会请求实测时长；漏掉偏移或停顿时会明确拒绝报通过。

![图标](icon-512.png)

安装：`npx skills add xxjrq/video-narration-duration-fit-cn`

## 使用

```sh
python3 scripts/check_duration.py fixtures/within-budget-input.json
```

输入格式：

```json
{"version":"approved-cut-v7","segments":[{"id":"S1","narration_measured_ms":9500,"approved_shot_ms":10000,"start_offset_ms":1000,"allowed_pause_after_ms":0}]}
```

这里 S1 的可用时长是 9000ms，实测需要 9500ms，超出 500ms，结论应为不通过，而非因旁白小于十秒判通过。

## 可复制参考交付

- [成功输入](fixtures/within-budget-input.json) 与 [成功报告](fixtures/within-budget-report.md)
- [段后停顿超时输入](fixtures/success-input.json) 与 [对应报告](fixtures/success-report.md)
- [起播偏移超时输入](fixtures/over-budget-input.json)
- [缺少实测时长的失败输入](fixtures/missing-measured-duration.json) 与 [失败报告](fixtures/failure-report.md)


- [可缩稿的超时](fixtures/trim-feasible-input.json)、[停顿本身超预算](fixtures/fixed-pause-overrun-input.json)、[起播偏移本身超预算](fixtures/fixed-offset-overrun-input.json) → [实际离线核对报告](fixtures/action-boundary-report.md)

## 自检

在本目录独立运行：

```sh
sh scripts/self_test.sh
```

它执行成功、可缩稿超时、固定偏移/停顿超预算和缺失实测等真实输入分支，并检查根图标为 512×512 PNG。

## 范围与来源

本仓库原创实现，只进行实测时间预算核对。业务背景参考 [OpenAI Whisper](https://github.com/openai/whisper) 的公开项目与其 [工具实现](https://github.com/openai/whisper/blob/main/whisper/utils.py)，未复制其文字或源码；本 Skill 采用 MIT 许可证。
