#!/usr/bin/env python3
"""
Generate examples.json manifest from example files.

This script scans all example .py files, extracts metadata from their docstrings,
and generates a manifest file that can be consumed by the documentation website.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional


def extract_metadata(content: str) -> Optional[Dict]:
    """Extract metadata from example docstring."""
    # Find the docstring
    docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
    if not docstring_match:
        return None

    docstring = docstring_match.group(1)

    # Extract title (first line starting with #)
    title_match = re.search(r'^#\s+(.+)$', docstring, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else None

    # Extract description (first paragraph after title)
    desc_match = re.search(r'^#.*?\n\n(.+?)(?:\n\n|##)', docstring, re.DOTALL | re.MULTILINE)
    description = desc_match.group(1).strip() if desc_match else None

    # Extract metadata section
    metadata = {}
    metadata_section = re.search(r'## Metadata\n(.*?)(?:\n##|$)', docstring, re.DOTALL)
    if metadata_section:
        for line in metadata_section.group(1).strip().split('\n'):
            if match := re.match(r'-\s+\*\*(.+?)\*\*:\s+(.+)', line):
                key = match.group(1).lower().replace(' ', '_')
                value = match.group(2).strip()
                metadata[key] = value

    return {
        'title': title,
        'description': description,
        **metadata
    }


def generate_manifest(repo_path: Path) -> List[Dict]:
    """Generate manifest from all example files."""
    examples = []

    # Iterate through all directories
    for category_dir in sorted(repo_path.iterdir()):
        if not category_dir.is_dir() or category_dir.name.startswith('.'):
            continue

        # Extract category info
        category_num, category_name = category_dir.name.split('_', 1)
        category_id = category_name.replace('_', '-')

        # Find all Python files in category
        for example_file in sorted(category_dir.glob('*.py')):
            if example_file.name.startswith('_'):
                continue

            # Read and parse example
            content = example_file.read_text()
            metadata = extract_metadata(content)

            if not metadata or not metadata.get('title'):
                print(f"Warning: Skipping {example_file} - no valid metadata found")
                continue

            # Build example entry
            example = {
                'id': example_file.stem,
                'title': metadata['title'],
                'description': metadata['description'],
                'category': category_name.replace('_', ' ').title(),
                'difficulty': metadata.get('difficulty', 'Intermediate'),
                'time': metadata.get('time', '15 min'),
                'tags': [tag.strip() for tag in metadata.get('tags', '').split(',')],
                'product': metadata.get('product', 'Blazing Core').lower().replace(' ', '-'),
                'file_path': f"{category_dir.name}/{example_file.name}",
                'github_url': f"https://github.com/Blazing-work/blazing-examples/blob/main/{category_dir.name}/{example_file.name}",
                'href': f"/docs/{example_file.stem}",
            }

            examples.append(example)

    return examples


def main():
    """Main entry point."""
    repo_path = Path(__file__).parent

    print("Scanning for examples...")
    examples = generate_manifest(repo_path)

    print(f"Found {len(examples)} examples")

    # Write manifest
    manifest_path = repo_path / 'examples.json'
    with open(manifest_path, 'w') as f:
        json.dump(examples, f, indent=2)

    print(f"Manifest written to {manifest_path}")

    # Print summary
    print("\nExamples by category:")
    from collections import Counter
    categories = Counter(ex['category'] for ex in examples)
    for category, count in sorted(categories.items()):
        print(f"  {category}: {count}")

    print("\nExamples by product:")
    products = Counter(ex['product'] for ex in examples)
    for product, count in sorted(products.items()):
        print(f"  {product}: {count}")


if __name__ == "__main__":
    main()
