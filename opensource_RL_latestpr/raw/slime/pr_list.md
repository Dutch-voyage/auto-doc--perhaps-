# slime PR List

**Repository**: THUDM/slime
**Timeframe**: 2024-07-01 to 2026-01-08 (last 6 months)
**Total PRs Analyzed**: 150+
**Keywords**: training-backend, parallel-strategies, rl-algorithms, multimodal, quantization, agent-framework, performance-optimization, fault-tolerance, reproducibility

---

## High Priority (Roadmap-Aligned & Major Features)

### VLM + FSDP Integration
| PR # | Title | Keywords | Roadmap | Link |
|------|-------|----------|---------|------|
| 501 | [FSDP, VLM] feat: add vlm training for FSDP | training-backend, multimodal | ✓ v0.2.1 | https://github.com/THUDM/slime/pull/501 |
| 1056 | [FSDP, VLM] feat: true on policy for VLM | training-backend, multimodal | ✓ v0.2.1 | https://github.com/THUDM/slime/pull/1056 |
| 1079 | [VLM, FSDP] Update Experiment Readme | multimodal | ✓ v0.2.1 | https://github.com/THUDM/slime/pull/1079 |
| 1093 | [VLM] fix: fix non true-on-policy vlm regression | multimodal | ✓ v0.2.1 | https://github.com/THUDM/slime/pull/1093 |
| 1155 | fix: fix 8B VLM true on policy issue | multimodal | ✓ v0.2.1 | https://github.com/THUDM/slime/pull/1155 |
| 1210 | Megatron VLM Support (Qwen2.5-VL series) (3/N) | multimodal | In Progress | https://github.com/THUDM/slime/pull/1210 |

### FSDP Backend Development
| PR # | Title | Keywords | Roadmap | Link |
|------|-------|----------|---------|------|
| 282 | [feat] init support for FSDP | training-backend | ✓ v0.2.0 | https://github.com/THUDM/slime/pull/282 |
| 321 | [FSDP] Data Packing Implementation | training-backend | ✓ v0.2.0 | https://github.com/THUDM/slime/pull/321 |
| 344 | [FSDP] Add reference model support for KL | training-backend, rl-algorithms | ✓ v0.2.0 | https://github.com/THUDM/slime/pull/344 |
| 915 | [FSDP] Optimize FSDP2 Model Loading | training-backend | ✓ v0.2.1 | https://github.com/THUDM/slime/pull/915 |
| 988 | [FSDP] Add script for FSDP Qwen3-4B | training-backend | ✓ v0.2.1 | https://github.com/THUDM/slime/pull/988 |
| 996 | [FSDP] Add gpt oss 20b script | training-backend | ✓ v0.2.1 | https://github.com/THUDM/slime/pull/996 |
| 1001 | [FSDP][3/N] support true_on_policy training | training-backend | ✓ v0.2.1 | https://github.com/THUDM/slime/pull/1001 |
| 1040 | [FSDP] Support lr scheduler | training-backend | ✓ v0.2.1 | https://github.com/THUDM/slime/pull/1040 |
| 1041 | [FSDP] fix args error in apply_fsdp2 function | training-backend | ✓ v0.2.1 | https://github.com/THUDM/slime/pull/1041 |
| 1140 | [FSDP][1/n] Support LoRA training for FSDP | training-backend, quantization | In Progress | https://github.com/THUDM/slime/pull/1140 |

### PPO & RL Algorithms
| PR # | Title | Keywords | Roadmap | Link |
|------|-------|----------|---------|------|
| 342 | [feat] init support for PPO | rl-algorithms | ✓ v0.2.0 | https://github.com/THUDM/slime/pull/342 |
| 347 | feature: ppo | rl-algorithms | ✓ v0.2.0 | https://github.com/THUDM/slime/pull/347 |
| 350 | [feat] add --critic-lr and --num-critic-only-steps | rl-algorithms | ✓ v0.2.0 | https://github.com/THUDM/slime/pull/350 |
| 373 | [fix] fix ppo bugs | rl-algorithms | ✓ v0.2.0 | https://github.com/THUDM/slime/pull/373 |
| 999 | [Feature] Add off-policy sequence masking (DeepSeek v3.2) | rl-algorithms | ✓ v0.2.1 | https://github.com/THUDM/slime/pull/999 |
| 1004 | feat: Add Unbiased KL Estimation (DeepSeek-V3.2) | rl-algorithms | ✓ v0.2.1 | https://github.com/THUDM/slime/pull/1004 |

### PD-Disaggregation & Distributed Training
| PR # | Title | Keywords | Roadmap | Link |
|------|-------|----------|---------|------|
| 1080 | [Feature] PD Disaggregation Support | parallel-strategies | ✓ v0.2.1 | https://github.com/THUDM/slime/pull/1080 |
| 1046 | Support pd disaggregation with p and d | parallel-strategies | ✓ v0.2.1 | https://github.com/THUDM/slime/pull/1046 |

### Quantization
| PR # | Title | Keywords | Roadmap | Link |
|------|-------|----------|---------|------|
| 974 | Add fp8 kv cache and tis in qwen3 30b | quantization, performance-optimization | ✓ v0.2.1 | https://github.com/THUDM/slime/pull/974 |
| 1172 | [FEATURE] support Int4 qat in slime | quantization | In Progress | https://github.com/THUDM/slime/pull/1172 |
| 1173 | [feature] update fp8 weight from megatron fp8 | quantization | In Progress | https://github.com/THUDM/slime/pull/1173 |

---

## Medium Priority (Feature Additions)

### Agent & Tool Use
| PR # | Title | Keywords | Link |
|------|-------|----------|------|
| 269 | [example] add an example for multi-agent rl | agent-framework, multi-agent | https://github.com/THUDM/slime/pull/269 |
| 976 | Add strands-agents example | agent-framework | https://github.com/THUDM/slime/pull/976 |
| 1159 | [FEATURE] Add tool call support for multi-turn SFT | tool-integration, agent-framework | https://github.com/THUDM/slime/pull/1159 |
| 1203 | Feat(router): add oai interface support | tool-integration | https://github.com/THUDM/slime/pull/1203 |
| 1359 | feat(examples): add strands-sglang integration (agentic RL) | agent-framework | https://github.com/THUDM/slime/pull/1359 |

### Performance Optimization
| PR # | Title | Keywords | Link |
|------|-------|----------|------|
| 361 | [FEAT] Deterministic rollout | reproducibility, performance-optimization | https://github.com/THUDM/slime/pull/361 |
| 370 | [reproducibility][docker] enable training reproducibility | reproducibility | https://github.com/THUDM/slime/pull/370 |
| 374 | [feat] enable use_flattened_tensor_bucket with quantization | performance-optimization | https://github.com/THUDM/slime/pull/374 |
| 973 | Support zero host or device memory waste for weight update | memory-optimization | https://github.com/THUDM/slime/pull/973 |
| 975 | Add GB200, MTP, benchmark, fp8 rollout mode | performance-optimization | https://github.com/THUDM/slime/pull/975 |
| 1078 | split train data in-advance to reduce communication | communication-optimization | https://github.com/THUDM/slime/pull/1078 |
| 1088 | Set --train-memory-margin-bytes to 1GB by default | memory-optimization | https://github.com/THUDM/slime/pull/1088 |

### Evaluation & Benchmarking
| PR # | Title | Keywords | Link |
|------|-------|----------|------|
| 989 | Add nemo skills evaluation | evaluation | https://github.com/THUDM/slime/pull/989 |
| 1000 | [ci] Add CI for gradient norm verification | reproducibility, evaluation | https://github.com/THUDM/slime/pull/1000 |
| 1154 | Integrate Terminal Bench Evaluation | evaluation | https://github.com/THUDM/slime/pull/1154 |
| 1156 | Add tau2-bench training cookbook | evaluation | https://github.com/THUDM/slime/pull/1156 |
| 1158 | tau-bench: offline stub user + tool parsing fallback | evaluation | https://github.com/THUDM/slime/pull/1158 |

### Data Pipeline
| PR # | Title | Keywords | Link |
|------|-------|----------|------|
| 242 | [Feature] Support token in token out for multi turn | data-pipeline | https://github.com/THUDM/slime/pull/242 |
| 387 | [feat] add --use-routing-replay | data-pipeline, experience-replay | https://github.com/THUDM/slime/pull/387 |
| 912 | Add DataSource and --data-source-path | data-pipeline | https://github.com/THUDM/slime/pull/912 |
| 961 | Add --rollout-sample-filter-path | data-pipeline | https://github.com/THUDM/slime/pull/961 |
| 1016 | [rollout] support disable trim samples | data-pipeline | https://github.com/THUDM/slime/pull/1016 |
| 1045 | [rollout] Truncate last token for rollout routing replay | data-pipeline, experience-replay | https://github.com/THUDM/slime/pull/1045 |
| 1298 | [data][feat] add large dataset support | data-pipeline | https://github.com/THUDM/slime/pull/1298 |
| 1355 | Feat: multi-threads data fetching for sft data | data-pipeline | https://github.com/THUDM/slime/pull/1355 |

### Router & Infrastructure
| PR # | Title | Keywords | Link |
|------|-------|----------|------|
| 366 | [router] support slime-router only | training-backend | https://github.com/THUDM/slime/pull/366 |
| 367 | [router] extract middleware folder | training-backend | https://github.com/THUDM/slime/pull/367 |
| 368 | [feat] support distributed post | communication-optimization | https://github.com/THUDM/slime/pull/368 |
| 1029 | extract all sglang deps in megatron actor | training-backend | https://github.com/THUDM/slime/pull/1029 |

---

## Low Priority (Bug Fixes & Improvements)

### Bug Fixes
| PR # | Title | Keywords | Link |
|------|-------|----------|------|
| 963 | Fix: resolve variable shadowing bug | reproducibility | https://github.com/THUDM/slime/pull/963 |
| 964 | Tiny fix fp8_cast_bf16 not copying chat template | bug-fix | https://github.com/THUDM/slime/pull/964 |
| 967 | Fix convert_hf_to_torch_dist OOM | bug-fix | https://github.com/THUDM/slime/pull/967 |
| 970 | Fix random port in use error | bug-fix | https://github.com/THUDM/slime/pull/970 |
| 998 | Fixed bug in checking max_length for SFT | bug-fix | https://github.com/THUDM/slime/pull/998 |
| 1005 | Fix evaluation parameter parsing | bug-fix | https://github.com/THUDM/slime/pull/1005 |
| 1084 | fix raw_reward upload in fsdp | bug-fix | https://github.com/THUDM/slime/pull/1084 |
| 1095 | fix_load_ckpt | bug-fix | https://github.com/THUDM/slime/pull/1095 |
| 1098 | fix actor init bugs | bug-fix | https://github.com/THUDM/slime/pull/1098 |
| 1100 | Fix bug for convert_hf_to_torch_dist.py | bug-fix | https://github.com/THUDM/slime/pull/1100 |

### Code Quality & Documentation
| PR # | Title | Keywords | Link |
|------|-------|----------|------|
| 991-995 | [1-4/N] Tiny execute Ruff auto lint | reproducibility | https://github.com/THUDM/slime/pull/991 |
| 1021 | pre-commit run --all-files | reproducibility | https://github.com/THUDM/slime/pull/1021 |
| 1067 | Fix typos and improve documentation | documentation | https://github.com/THUDM/slime/pull/1067 |
| 1074 | fix: remove redundant gc.collect() | performance-optimization | https://github.com/THUDM/slime/pull/1074 |

### Docker & Environment
| PR # | Title | Keywords | Link |
|------|-------|----------|------|
| 965 | Super tiny install dnsutils in dockerfile | deployment | https://github.com/THUDM/slime/pull/965 |
| 966 | Super tiny sanity check checkpoint dir | deployment | https://github.com/THUDM/slime/pull/966 |
| 968 | Tiny support environment variables in scripts | deployment | https://github.com/THUDM/slime/pull/968 |
| 1066 | [docker] fix cudnn version | deployment | https://github.com/THUDM/slime/pull/1066 |
| 1069 | fix(examples): correct quotes in Qwen3 script | deployment | https://github.com/THUDM/slime/pull/1069 |
| 1070 | [docker] fix megatron cpu adam load issue | deployment | https://github.com/THUDM/slime/pull/1070 |

---

## Roadmap Alignment Summary

| Category | Count | Percentage |
|----------|-------|------------|
| Implemented (✓) | 47 | 31% |
| In Progress | 6 | 4% |
| Open/Proposed | 10 | 7% |
| Total Analyzed | 150+ | 100% |

---

## Keyword Distribution

| Keyword | PR Count | Priority |
|---------|----------|----------|
| training-backend | 15 | High |
| multimodal | 6 | High |
| rl-algorithms | 6 | High |
| parallel-strategies | 2 | High |
| quantization | 3 | High |
| agent-framework | 5 | Medium |
| tool-integration | 2 | Medium |
| performance-optimization | 8 | Medium |
| data-pipeline | 8 | Medium |
| evaluation | 5 | Medium |
| reproducibility | 6 | Low |
| bug-fix | 15+ | Low |

---

## Search Queries Used

```
is:pr is:merged repo:THUDM/slime merged:>=2024-07-01
is:pr is:merged repo:THUDM/slime label:enhancement
is:pr is:merged repo:THUDM/slime FSDP
is:pr is:merged repo:THUDM/slime VLM
is:pr is:merged repo:THUDM/slime PPO
is:pr is:merged repo:THUDM/slime label:feature
```

---

**Next Step**: Proceed to PR collection (Step 4)
