#!/bin/bash
# Batch download images from remaining arXiv papers

echo "🚀 Batch downloading images from remaining arXiv papers..."

# Remaining papers to download images from
papers=(
    "2409.19256"  # HybridFlow
    "2508.08221"  # Tricks or Traps
    "2510.11345"  # ROLL Flash
)

# Download images from each paper
for paper_id in "${papers[@]}"; do
    echo "📥 Downloading figures from https://arxiv.org/html/${paper_id}v1/"

    # Try to download figures 1-15 for each paper
    for i in {1..15}; do
        img_url="https://arxiv.org/html/${paper_id}v1/x${i}.png"
        output_file="./summaries/images/${paper_id}_figure_${i}.png"

        if wget -q "$img_url" -O "$output_file" 2>/dev/null; then
            echo "  ✅ Downloaded ${paper_id} figure ${i}"
        else
            # If figure doesn't exist, continue to next
            continue
        fi
    done

    echo "  📊 Completed downloading from ${paper_id}"
    echo ""
done

# Download images from blog posts
echo "🌐 Downloading images from blog posts..."

# slime blog
echo "📥 Downloading from slime blog..."
curl -s "https://lmsys.org/blog/2025-07-09-slime/" | \
  grep -o 'src="[^"]*\.png"' | \
  sed 's/src="//;s/"//' | \
  while read url; do
    if [[ $url == http* ]]; then
      filename="./summaries/images/slime_$(basename "$url")"
      wget -q "$url" -O "$filename" 2>/dev/null && echo "  ✅ Downloaded $(basename "$url")"
    fi
  done

# Miles blog
echo "📥 Downloading from Miles blog..."
curl -s "https://lmsys.org/blog/2025-11-19-miles/" | \
  grep -o 'src="[^"]*\.png"' | \
  sed 's/src="//;s/"//' | \
  while read url; do
    if [[ $url == http* ]]; then
      filename="./summaries/images/miles_$(basename "$url")"
      wget -q "$url" -O "$filename" 2>/dev/null && echo "  ✅ Downloaded $(basename "$url")"
    fi
  done

echo "🎉 Batch image download completed!"
echo "📁 Check ./summaries/images/ for downloaded files"