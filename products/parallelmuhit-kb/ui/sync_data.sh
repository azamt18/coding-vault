#!/bin/sh
# copy the pipeline's output next to the page (public/ is served as-is by vite)
set -e
cd "$(dirname "$0")"
mkdir -p public
cp ../extract/graph_grouped.json public/graph_grouped.json
echo "synced public/graph_grouped.json"
