# Requirements - DAG-Based Training Systems

I will provide materials related to **DAG-Based Training Systems** for multi-modal agentic reasoning and reinforcement learning. Their links are listed in `outlines.md`.

Please:

1. Retrieve the necessary information
2. Summarize the content
3. Create tags for each summary
4. **✨ Enhance summaries with tag-relevant highlighting and image integration**

---

## Retrieval

The contents of the materials include: technology blogs, GitHub repositories (markdowns), research papers, and more. Since only links are provided, use the following tools to extract actual content:

### 1. Web Reader
- Use `web_reader` to get content directly from URLs
- **Extract important images** - DAG architecture diagrams, workflow visualizations, performance charts
- Images are critical for quickly understanding complex DAG-based concepts

### 2. Web Search
- Use `web-search-prime` to find supplementary/additional content when needed
- Search for key terms like "DAG-based RL", "multi-modal agent training", "asynchronous rollout"


#### Multi-level Links
For materials with multi-level links (e.g., GitHub repos with docs/ directories):
1. Determine if linked content is informative
2. Read only necessary links and conclude in structured directories
3. Pick most relevant docs (5 at most) to summarize
4. Paste links to less relevant docs in the main summary

---

## Image Integration Guidelines

For DAG-related visual materials (architecture diagrams, workflow figures, node structures):

### 1. Download Images
```bash
# Create image directory
mkdir -p ./summaries/images/

# Download from arXiv HTML (95% success rate)
wget -O ./summaries/images/{paper_id}_figure_{i}.png \
     https://arxiv.org/html/{paper_id}v1/x{i}.png

# Download from blog posts
wget -O ./summaries/images/dag_architecture.png [image_url]
```

### 2. Local Image Storage
Store downloaded images in `./summaries/images/` directory

### 3. Integrate in Summaries
Use proper markdown syntax:
```markdown
![DAG Architecture](./images/dag_architecture.png)

**Figure 1**: DAG-based training system showing node-level batching and asynchronous execution
```

### 4. Image Relevance
Only include images that:
- Illustrate DAG topology and graph structures
- Show node dependencies and execution flow
- Demonstrate training architecture (chunking, batching, parallelism)
- Visualize performance comparisons and benchmarks

### 5. Image Attribution
Include figure numbers and descriptive captions explaining the technical content

---

## Summary

After retrieving content, create separate markdown files in `./summaries/` (e.g., `01_distflow.md`, `02_asyncflow.md`).

Keep summaries **concise**. Suggested structure:

```markdown
# Title
[ST][DAG][Async] | [TP][Rollout][Train] | [APP][Reasoning][MultiModal]

## Summary
[Brief 2-3 sentence overview]

## Key Technical Innovations

### 1. Innovation Name [DAG][Async]

![DAG Architecture](./images/file.png)

**Figure X**: Technical explanation

- **Core breakthrough**: Tag-relevant emphasis
- **Technical detail**: Specific mechanism
- **Performance impact**: Quantitative results

## Performance Results
- **X times speedup**: Concrete measurement
- **GPU utilization**: Efficiency metrics

## External Resources
- [Framework Docs](https://...)
- [Paper Repository](https://...)
```

### Multi-level Links Handling
For material with external reference:
- choose the top relavant links and create an independency .md to summarize it if necessary.
- Paste links to less relevant docs with brief summary.

### Content Consistency
Revise summary content to ensure consistency with tags. Highlight content relevant to each tag.

### Duplicate Filtering
Filter out overlapping/repetitive sources

---

## Tagging

See `Tags.md` for the complete tag taxonomy. Use bracketed format: `[TagName]`

### Three Categories

| Category | Symbol | Quick Reference |
|----------|--------|-----------------|
| **System Topics** | [ST] | DAG, Async, Batch, Shard, Runtime, Network, GPU |
| **Training Phases** | [TP] | SFT, RL, Rollout, Train, Chunk, Reward, Oracle, Sync |
| **Application** | [APP] | Reasoning, MultiModal, Agent, Verifier, MultiAgent, Alignment, Coding, Math |

### Tag Format Example
```markdown
# Title
[ST][DAG][Async] | [TP][Rollout][Train] | [APP][Reasoning]

## Section Title [DAG][Async]
Content with tag-relevant emphasis
```

### Tagging Workflow
1. Review `Tags.md` for available tags
2. Select relevant tags from each category
3. Add tags to section headers using `[TagName]`
4. Add new tags to `Tags.md` if needed (follow guidelines in Tags.md)

---

## Checkbox

Remember to check off completed items in `outlines.md`.

---

## DAG-Specific Considerations

When summarizing DAG-based training materials, pay special attention to:

1. **Graph Topology**: How DAGs are defined, structured and executed
2. **Workload Shift**: How different parts(tool-use)/modality(image/video/table) affect workloads in traing/inference
3. **Parallelization**: How independent branches are executed
4. **Chunk/Node-level Scheduling**: How training/inference are scheduled in finer granularity
5. **Asynchrony Design**: How asynchrony is ensured for (train/infer, infer/tool-call, multi-agent cooperation e.t.c)
6. **Reward Attribution**: How rewards flow through the graph
7. **SFT/RL Balance**: How supervised learning and RL are combined
8. **Tool Integration**: How external tools are called and integrated

## Quality
Please refer to [example](summaries/01_distflow.md) to control the quality of the summaries. And refine the content to be more related the **DAG-specific** contents. 