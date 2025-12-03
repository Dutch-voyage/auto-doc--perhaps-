#!/usr/bin/env python3
"""
Automated script to enhance remaining RL materials with images and bracketed tags
"""

import os
import re
import subprocess
from pathlib import Path

def download_arxiv_images(arxiv_id, max_figures=15):
    """Download all images from HTML arXiv paper"""
    base_url = f"https://arxiv.org/html/{arxiv_id}v1"
    output_dir = Path("./summaries/images")

    for i in range(1, max_figures + 1):
        img_url = f"{base_url}/x{i}.png"
        output_file = output_dir / f"{arxiv_id}_figure_{i}.png"

        try:
            subprocess.run([
                "wget", "-q", img_url, "-O", str(output_file)
            ], check=True, capture_output=True)
            print(f"✅ Downloaded {arxiv_id} figure {i}")
            return True
        except subprocess.CalledProcessError:
            # Continue trying other figures
            continue
    return False

def extract_blog_images(blog_url, prefix):
    """Extract images from blog posts"""
    output_dir = Path("./summaries/images")

    try:
        result = subprocess.run([
            "curl", "-s", blog_url
        ], capture_output=True, text=True, check=True)

        # Extract image URLs
        img_pattern = r'src="([^"]*\.png)"'
        images = re.findall(img_pattern, result.stdout)

        for i, img_url in enumerate(images):
            if not img_url.startswith('http'):
                img_url = blog_url + img_url if not blog_url.endswith('/') else blog_url + img_url[1:]

            output_file = output_dir / f"{prefix}_image_{i+1}.png"

            try:
                subprocess.run([
                    "wget", "-q", img_url, "-O", str(output_file)
                ], check=True, capture_output=True)
                print(f"✅ Downloaded {prefix} image {i+1}")
            except subprocess.CalledProcessError:
                continue

        return len(images) > 0
    except subprocess.CalledProcessError:
        return False

def enhance_summary_template(content, material_name):
    """Add bracketed tags and image placeholders to summary"""

    # External links mapping
    external_links = {
        "HybridFlow": {
            "hardware": "[PyTorch FSDP](https://pytorch.org/tutorials/beginner/dist_overview.html)",
            "training": "[PPO Algorithm](https://arxiv.org/abs/1707.06347)",
            "system": "[3D-Parallelism](https://pytorch.org/tutorials/intermediate/model_parallel_tutorial.html)"
        },
        "slime": {
            "inference": "[SGLang](https://docs.sglang.ai/)",
            "framework": "[SGLang-Native RL](https://lmsys.org/blog/2025-07-09-slime/)",
            "system": "[Ray Documentation](https://docs.ray.io/)"
        },
        "Miles": {
            "training": "[MoE Training](https://arxiv.org/abs/2409.06234)",
            "enterprise": "[LMSYS Blog](https://lmsys.org/blog/2025-11-19-miles/)",
            "scaling": "[Large-Scale Training](https://arxiv.org/abs/2405.19216)"
        },
        "Tricks or Traps": {
            "training": "[PPO Optimization](https://arxiv.org/abs/2005.12729)",
            "algorithm": "[GRPO Paper](https://arxiv.org/abs/2402.03300)",
            "comparison": "[RLHF Survey](https://arxiv.org/abs/2203.02155)"
        },
        "ROLL Flash": {
            "agentic": "[Agentic RL](https://arxiv.org/abs/2310.01797)",
            "scaling": "[Large-Scale RL](https://arxiv.org/abs/2310.12940)",
            "async": "[Async Training](https://arxiv.org/abs/2505.24298)"
        }
    }

    # Add external resources section if not present
    if "**External Resources:**" not in content:
        if material_name in external_links:
            links = external_links[material_name]
            resources = "\n\n**External Resources:**\n"
            for category, link in links.items():
                resources += f"- [{category.title()}]: {link}\n"
            content += resources

    return content

def main():
    """Main enhancement process"""

    remaining_materials = [
        {
            "name": "HybridFlow",
            "arxiv": "2409.19256",
            "file": "5_hybridflow_flexible_efficient_rlhf.md",
            "tags": "#Hardware_Topics #GPU-side #System_/_Runtime\n#RL_Training_phases #Training #Weight_Synchrony\n#Scenarios #Alignment",
            "type": "paper"
        },
        {
            "name": "slime",
            "blog": "https://lmsys.org/blog/2025-07-09-slime/",
            "file": "6_slime_sglang_native_rl_framework.md",
            "tags": "#Hardware_Topics #GPU-side #System_/_Runtime\n#RL_Training_phases #Inference #Training\n#Scenarios #Math_/_Coding #Multi-agents",
            "type": "blog"
        },
        {
            "name": "Miles",
            "blog": "https://lmsys.org/blog/2025-11-19-miles/",
            "file": "7_miles_enterprise_rl_moe_framework.md",
            "tags": "#Hardware_Topics #GPU-side #System_/_Runtime\n#RL_Training_phases #Training #Inference\n#Scenarios #Multi-agents",
            "type": "blog"
        },
        {
            "name": "Tricks or Traps",
            "arxiv": "2508.08221",
            "file": "9_tricks_or_traps_rl_reasoning.md",
            "tags": "#Hardware_Topics #System_/_Runtime\n#RL_Training_phases #Training\n#Scenarios #Math_/_Coding",
            "type": "paper"
        },
        {
            "name": "ROLL Flash",
            "arxiv": "2510.11345",
            "file": "10_roll_flash_async_rl_agentic.md",
            "tags": "#Hardware_Topics #GPU-side #System_/_Runtime\n#RL_Training_phases #Inference #Training #Experience_Buffer_/_Replay\n#Scenarios #Math_/_Coding #Multi-agents",
            "type": "paper"
        }
    ]

    for material in remaining_materials:
        print(f"\n🚀 Processing {material['name']}...")

        # Download images
        if material.get('arxiv'):
            download_arxiv_images(material['arxiv'])
        elif material.get('blog'):
            extract_blog_images(material['blog'], material['name'].lower().replace(' ', '_'))

        # Enhance summary file
        summary_file = Path(f"./summaries/{material['file']}")
        if summary_file.exists():
            with open(summary_file, 'r') as f:
                content = f.read()

            # Update tags
            content = re.sub(r'#.*\n', material['tags'] + '\n', content, count=1)

            # Add external links and enhance content
            content = enhance_summary_template(content, material['name'])

            with open(summary_file, 'w') as f:
                f.write(content)

            print(f"✅ Enhanced {material['name']} summary")
        else:
            print(f"⚠️  {material['file']} not found")

if __name__ == "__main__":
    main()