# Requirements (Enhanced)
I will provide some materials which belong to the topic of **Efficient RL post-training**. Their link are listed in "outlines.md".
Please
1. Retrieve the necessary information;
2. Summarize the content;
3. Create tags for each summary.
4. **✨ NEW: Enhance summaries with tag-relevant highlighting and image integration**

## Retrieval
The contents of the materials are part of the following: technology blog, github repo (markdowns), papers and etc. I have provided the link only, meaning you need to call the following tools to extract the actual contents:
1.  **web_reader**: get the content directly. **You may extract some images. It's important for others to understand an idea quickly.**
2.  **web-search-prime**: search for key word to get supplementary/additional content when needed.
3.  (\*optional) For links to pdf, you may need to do the following (you should probably avoid using pdf extraction for arxiv paper, extract paper in html first):
    1.  `wget -O "./raw_docs/{name_of_the_links_to_pdf}.pdf" {links_to_pdf}` (e.g. `wget -O ./raw_docs/2410.1234.md https://arxiv.org/pdf/2410.1234`)
    2.  Then run `python pdf_parse.py ./raw_docs/{name_of_the_links_to_pdf}.pdf ./parsed_docs/{name_of_the_parsed_file}.md`
    3.  Then analyze the parsed file, treat it like an ordinary markdown file. **Note that the paper might be very long, so you may need to search for key words or read them chapter by chapter.**

**For the material with multi-level links, please 1. determine if their contents to other links are informative; 2. Read only the necessary links and conclude them in the structured directories.**

### (suppplement) Image Integration Guidelines (See Image_Download_Guidance.md)
For visual materials (diagrams, architecture figures, performance charts):

1. **Download images** from papers and blog posts:
   ```bash
   # Create image directory
   mkdir -p ./summaries/images/

   # Download important figures from web sources
   wget -O ./summaries/images/system_architecture.png [image_url]
   ```

2. **Local image storage**: Store downloaded images in `./summaries/images/` directory

3. **Integrate in summaries**: Use proper markdown syntax to reference local images:
   ```markdown
   ![System Architecture](./images/system_architecture.png)

   **Figure 1**: Asynchronous RL architecture showing decoupled rollout and training phases
   ```

4. **Image relevance**: Only include images that:
   - Illustrate key architectural concepts
   - Show performance comparisons/benchmarks
   - Demonstrate algorithmic innovations
   - Help understand system workflows

5. **Image attribution**: Include figure numbers and descriptive captions explaining the visual content


## Summary
After you get the content, you need to create separate markdown files with summary and tags (like "./summaries/1.md" or "./summaries/{proper title}.md").

Please make the summary as concise as possible. 
The stucture of the summary might look like

```markdown
# Title
#tag1 #tag2 #tag3
## Introduction
## key points
### key point1 [tag1]
content(with figures)
### key point2 [tag2][tag3]
### key point3 [tag1][tag3]
## external links
[description/name of the link/tag].(link).
```

If their are multi-level links, you can optionally add the link directly to the summary, instead of fetching them and summarize as additoinal docs. For example, sowm github repos have a independent diretory called "docs", only some of the content is related to the tags in the next parts, you may pick the most relevant doc.md (five at most as a suggestion) to summary it and paste the links to less relevant docs.md in the summary of the main material.

When complete the tagging afterwards, you can revise the summary content to ensure the consistency with the tags, to highlight the relevant content to each tag.

**Note that the content you've retrieved may have overlapped source, you may filter out the repetitive ones**

## Taggging

Please label the data from the following aspects:
1. **hardware topics**: GPU-side, CPU-side and networking.
2. **RL training phases**: inference (rollouts), training (backward), weight synchrony, environments computation (batching/scheduling/vectorization) and etc.
3. **scenarios**: math/coding (with verifier), alignment (with contrast examples), multi-agents, GUI-agent, etc.
You should first determine which aspects (none or all three are allowed) belongs to **hardware topics**, **RL training phases** and **scenarios**. Then you decide the labels for each aspect.

**Note that you may need to 1. remove/add/edit tags to better organize the topics; 2.record all used tags during labeling, and make the labels as coherent as possible (you should use Tags.md to record are used tags/labels)**

Here is an example of multi-level tagging that you may consider as a start:

Tags.md

You can also go beyond the three main topics to do taxonomy. For example, the mainstream inference engines including verl/slime/Areal have their derivative products/design notes/optimizations. Tagging them by the main-brance project is worth considering.

When you decide your set of labels for a material (make sure they contain at least one of the three "hardware topics, RL training phases, scenarios"), you only need to create tag/label by adding "#" under the first title. Note that you need to connect phrases by "_".
e.g.
```mardown
# RL traing techniques
#RL_training_phases #Training #policy_optimization
*links to the material*
```

also see 1.md as an example

## Checkbox

Remember to check in the checkboxed in the outlines.md.