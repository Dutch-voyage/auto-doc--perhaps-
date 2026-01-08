# ROLL PR List

**Repository**: [alibaba/ROLL](https://github.com/alibaba/ROLL)
**Analysis Period**: 2024-07-01 to 2026-01-08 (6 months)
**Analysis Date**: 2026-01-08
**Total Merged PRs**: 100+

---

## PR Summary by Priority

### High Priority (Roadmap-Aligned, Major Features)
- **#111** - Refactor agentic RL design, async training, add distill/DPO/LoRA
- **#283** - Sync to v0.1.3 (major release sync)
- **#136** - Agentic RL stepwise learning GiGPO, multi-modal distill
- **#266** - Ascend NPU support for vLLM
- **#139** - AMD GPU dockerfile and pre-built images
- **#137** - AMD GPU support (0.5B, 7B, 30B models)
- **#99** - Device abstraction and Ascend NPU support
- **#89** - Multi-images RL-VL support
- **#67** - VL agentic pipeline and thread env

### Medium Priority (Feature Additions, Enhancements)
- **#295** - Add validation for distill pipeline
- **#292** - Add timer for mgr
- **#278** - Fix LLM proxy mode rollout pipeline
- **#266** - Ascend support for vLLM
- **#255** - Per-token loss calculation
- **#251** - Add sokoban sandbox env example for ROCK
- **#231** - Fix position_ids issue for Qwen VL with Megatron
- **#218** - Add merge LoRA scripts and update Reward-FL docs
- **#202** - Publish ROLL Flash
- **#172** - Sync to GitHub 0924
- **#170** - Fix log information metrics for qwen2.5-vl-7B-rlvr
- **#135** - Validate rollout_batch_size for trainer data parallelism
- **#126** - Multi-dim numpy array support
- **#122** - Set max_env_num_per_worker to 1 in webshop
- **#121** - Webshop refactor
- **#119** - Add custom reward worker docs
- **#111** - Refactor agentic RL design (see above)
- **#97** - Add RLVR pipeline docs
- **#81** - Add webshop env, env global limiter

### Low Priority (Bug Fixes, Documentation, Typos)
- **#311** - Update readme with Let It Flow paper
- **#304** - Fix get_pad_mask for eos/pad token
- **#297** - Fix template name resolution
- **#277** - Fix typos
- **#271** - Rollback daily stats workflow
- **#270** - Debug scheduler daily stats workflow
- **#269** - Remove redundant tensors_meta assignment
- **#268** - Fix stats chart line stack
- **#267** - Add workflow to collect GitHub stats
- **#265** - Add redirect to Overview when page not found
- **#262** - Add quick start guide for Alibaba Cloud DevPod
- **#260** - Adjust user-guide folder order
- **#259** - Fix error metrics link
- **#258** - Refactor documentation structure
- **#257** - Add gtag collect
- **#249** - Move logo png to CDN
- **#248** - Move image link to CDN and add X to home
- **#247** - Add deterministic coverage for collator utilities
- **#246** - Add zh-Hans to docs home
- **#244** - Add language dropdown to docs
- **#239** - Fix TS model
- **#237** - Update readme
- **#228** - Update readme for ROCK
- **#227** - Add deepwiki link and wechat modal
- **#221** - Fix gitignore *.png in docs
- **#220** - Add new docs home and searchBar
- **#216** - Fix patch version and MCP client
- **#211** - Remove nebula_patch
- **#209** - Update readme
- **#208** - Delete wandb key
- **#206** - Update docs
- **#198** - Add readme paper
- **#194** - Update readme
- **#192** - Update readme
- **#191** - Update readme
- **#188** - Skip _align_special_tokens during training
- **#179** - Update ascend doc
- **#176** - Fix tool register
- **#174** - Fix GRPO definition
- **#166** - Fix GSPO config in doc
- **#163** - Update demo yaml configs
- **#162** - Fix DataProto.concat error with inconsistent metrics keys
- **#156** - Auto generate userGuide in start
- **#155** - Sync codes to GitHub
- **#152** - Update readme 0825
- **#151** - Update ROLL PPT
- **#149** - Update README and fix typo in GRPO
- **#148** - Add docs in README and fix prompt generation guide
- **#142** - Enhance roll_docs & update local code test
- **#141** - Fix vLLM v1 engine on vLLM 0.10.0
- **#138** - Add home page to docs
- **#130** - Fix AI chat styles
- **#129** - Add AI chat to docs
- **#128** - Add ROLL PPT
- **#117** - Refine README
- **#116** - Refine README
- **#96** - Trigger GitHub Pages rebuild
- **#95** - Trigger GitHub Pages rebuild
- **#88** - Add pipeline docs
- **#77** - Add prompt intro doc
- **#74** - Add customer env doc English version
- **#73** - Fix deploy
- **#72** - Add customer env doc
- **#70** - Revert comment translation
- **#68** - Translate comment to English and add copyright
- **#66** - Fix ref for config_guide.md
- **#65** - Add experiment data tracking section
- **#64** - Add multi nodes quick start docs
- **#62** - Fix sampling_params comparison
- **#61** - Fix format for single_node_quick_start_cn.md
- **#60** - Fix ref for docs
- **#59** - Refine format for image_address.md
- **#57** - Simplify quick start doc and add demo config
- **#54** - Fix reward post process return

---

## PRs Organized by Keyword Category

### Training Infrastructure

#### training-backend
- **#99** - Device abstraction and Ascend NPU support
- **#266** - Ascend support for vLLM
- **#137** - AMD GPU model support (0.5B, 7B, 30B)
- **#139** - AMD GPU dockerfile and images
- **#218** - Add merge LoRA scripts

#### parallel-strategies
- **#135** - Validate rollout_batch_size for trainer data parallelism
- **#126** - Multi-dim numpy array support

#### rollout-inference
- **#278** - Fix LLM proxy mode rollout pipeline
- **#141** - Fix vLLM v1 engine on vLLM 0.10.0
- **#266** - Ascend support for vLLM

### RL Algorithms

#### rl-algorithms
- **#136** - Agentic RL stepwise learning GiGPO
- **#111** - Refactor agentic RL design
- **#174** - Fix GRPO definition
- **#166** - Fix GSPO config in doc
- **#255** - Per-token loss calculation

#### alignment
- **#111** - Add distill/DPO pipeline features
- **#295** - Add validation for distill pipeline
- **#218** - Update Reward-FL docs

#### verifier-guidance
- **#119** - Add custom reward worker docs
- **#54** - Fix reward post process return
- **#122** - Set max_env_num_per_worker in webshop

### Model Architecture

#### model-architecture
- **#231** - Fix position_ids for Qwen VL with Megatron
- **#170** - Fix log metrics for qwen2.5-vl-7B-rlvr
- **#89** - Multi-images RL-VL support

#### multimodal
- **#136** - Multi-modal distill support
- **#89** - Multi-images RL-VL support
- **#67** - VL agentic pipeline

#### quantization
- (No specific PRs in timeframe)

### Performance & Optimization

#### performance-optimization
- **#292** - Add timer for mgr (performance monitoring)
- **#126** - Multi-dim numpy array support
- **#255** - Per-token loss calculation

#### memory-optimization
- **#218** - Add merge LoRA scripts (memory-efficient training)

#### communication-optimization
- **#111** - Async training support
- **#67** - Thread env for env scaling

### Data Pipeline

#### data-pipeline
- **#162** - Fix DataProto.concat error with inconsistent metrics keys
- **#135** - Validate rollout_batch_size

### Evaluation & Testing

#### monitoring
- **#65** - Add experiment data tracking section
- **#292** - Add timer for mgr

### Agent & Tool Use

#### agent-framework
- **#111** - Refactor agentic RL design
- **#136** - Agentic RL stepwise learning GiGPO
- **#67** - VL agentic pipeline and thread env
- **#251** - Add sokoban sandbox env for ROCK
- **#121** - Webshop refactor
- **#81** - Add webshop env, env global limiter
- **#122** - Set max_env_num_per_worker in webshop

#### tool-integration
- **#176** - Fix tool register
- **#74, #77** - Custom environment documentation

### Deployment & Production

#### deployment
- **#139** - AMD GPU dockerfile and images
- **#262** - Quick start for Alibaba Cloud DevPod
- **#64** - Multi nodes quick start docs
- **#73** - Fix deploy

#### scalability
- **#99** - Device abstraction for NPU
- **#67** - Thread env for scaling
- **#81** - Env global limiter

---

## Release-Aligned PRs

### v0.1.3 (2025-12-08) - PR #283
Major sync PR containing:
- Math rule reward worker updates
- vLLM beam search support
- Qwen-3-next AMD GPU support
- Agentic RL enhancements
- Sequence packing for SFT/Distill
- Various bug fixes

### Major Features
- **#111** - Agentic RL refactor (async training, distill, DPO, LoRA)
- **#136** - GiGPO stepwise learning
- **#99** - Ascend NPU support
- **#139** - AMD GPU docker support

---

## Documentation PRs (Excluded from Technical Analysis)

Major documentation efforts:
- **#220** - New docs home and search
- **#258** - Documentation structure refactor
- **#262** - Alibaba Cloud DevPod quick start
- **#97** - RLVR pipeline docs
- **#88** - Pipeline docs
- **#156** - Auto generate userGuide

---

**Analysis Complete**: 2026-01-08
**Next Review**: 2026-02-08
