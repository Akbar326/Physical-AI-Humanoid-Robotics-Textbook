#!/usr/bin/env python3
"""
Chapter Validation Script for Physical AI & Humanoid Robotics Textbook

This script validates chapter files against the textbook's quality standards,
checking for required elements, proper structure, and constitutional compliance.
"""

import os
import sys
import re
import yaml
import argparse
from pathlib import Path
from typing import List, Dict, Any, Tuple
import requests
from urllib.parse import urlparse
import readability  # type: ignore


def check_front_matter_completeness(content: str) -> Tuple[bool, List[str]]:
    """Check if front-matter has all required fields."""
    errors = []

    # Extract front matter (content between ---)
    front_matter_match = re.match(r'---\n(.*?)\n---', content, re.DOTALL)
    if not front_matter_match:
        errors.append("No front matter found (missing --- delimiters)")
        return False, errors

    try:
        front_matter = yaml.safe_load(front_matter_match.group(1))
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML in front matter: {e}")
        return False, errors

    required_fields = ['title', 'sidebar_position', 'description', 'difficulty', 'time_hours', 'module']
    for field in required_fields:
        if field not in front_matter or not front_matter[field]:
            errors.append(f"Missing required field: {field}")

    # Validate specific field values
    if 'difficulty' in front_matter:
        valid_difficulties = ['Beginner', 'Beginner-Intermediate', 'Intermediate', 'Intermediate-Advanced', 'Advanced']
        if front_matter['difficulty'] not in valid_difficulties:
            errors.append(f"Invalid difficulty level: {front_matter['difficulty']}. Must be one of {valid_difficulties}")

    if 'time_hours' in front_matter:
        try:
            time = float(front_matter['time_hours'])
            if time < 0.5 or time > 12.0:
                errors.append(f"Time hours should be between 0.5 and 12.0, got: {time}")
        except (ValueError, TypeError):
            errors.append(f"Time hours must be a number, got: {front_matter['time_hours']}")

    if 'module' in front_matter:
        try:
            module = int(front_matter['module'])
            if module < 1 or module > 4:
                errors.append(f"Module should be 1-4, got: {module}")
        except (ValueError, TypeError):
            errors.append(f"Module must be an integer, got: {front_matter['module']}")

    return len(errors) == 0, errors


def verify_heading_hierarchy(content: str) -> Tuple[bool, List[str]]:
    """Verify heading hierarchy (no skipping levels)."""
    errors = []

    # Extract all headings
    headings = re.findall(r'^(#+)\s+(.*)', content, re.MULTILINE)

    for i, (level, title) in enumerate(headings):
        current_level = len(level)

        # Check if next heading skips a level
        if i < len(headings) - 1:
            next_level = len(headings[i + 1][0])
            if next_level > current_level + 1:
                errors.append(f"Heading level skipped from {current_level} to {next_level}: {title}")

    return len(errors) == 0, errors


def count_exercises(content: str) -> Tuple[bool, List[str]]:
    """Count exercises (should be ≥2)."""
    errors = []

    # Look for exercise headers (case insensitive)
    exercise_pattern = r'##\s*Hands?-?On\s+Exercise|##\s*Exercise|##\s*Practical\s+Exercise'
    exercises = re.findall(exercise_pattern, content, re.IGNORECASE)

    if len(exercises) < 2:
        errors.append(f"Found {len(exercises)} exercises, minimum 2 required")

    return len(exercises) >= 2, errors


def count_diagrams(content: str) -> Tuple[bool, List[str]]:
    """Count diagrams (should be ≥1)."""
    errors = []

    # Look for image markdown patterns
    image_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    images = re.findall(image_pattern, content)

    # Filter for diagrams (not just decorative images)
    diagrams = [img for img in images if img[0].lower() != 'logo' and img[0].lower() != 'favicon']

    if len(diagrams) < 1:
        errors.append(f"Found {len(diagrams)} diagrams, minimum 1 required")

    # Check for alt text
    for alt_text, img_path in images:
        if not alt_text or len(alt_text.strip()) < 10:
            errors.append(f"Image {img_path} has insufficient alt text: '{alt_text}'")

    return len(diagrams) >= 1, errors


def count_code_examples(content: str) -> Tuple[bool, List[str]]:
    """Count code examples (should be ≥3)."""
    errors = []

    # Look for code blocks
    code_blocks = re.findall(r'```.*?\n.*?\n```', content, re.DOTALL)

    # Filter for actual code (not empty blocks)
    code_examples = [block for block in code_blocks if len(block.strip()) > 10]

    if len(code_examples) < 3:
        errors.append(f"Found {len(code_examples)} code examples, minimum 3 required")

    return len(code_examples) >= 3, errors


def validate_links(content: str, file_path: str) -> Tuple[bool, List[str]]:
    """Validate internal and external links."""
    errors = []

    # Extract all markdown links
    links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)

    for link_text, url in links:
        if url.startswith(('http://', 'https://')):
            # External link - try to validate
            try:
                response = requests.head(url, timeout=5, allow_redirects=True)
                if response.status_code >= 400:
                    errors.append(f"External link broken: {url} (status {response.status_code})")
            except requests.RequestException:
                # Could be a temporary issue, but report it
                errors.append(f"Could not validate external link: {url}")
        elif url.startswith(('#', '/')) or url.endswith(('.md', '.png', '.jpg', '.svg', '.gif')):
            # Internal link - check if file exists relative to current file
            if url.startswith('/'):
                # Absolute path from docs root
                target_path = Path('docs') / url[1:]
            elif url.startswith('#'):
                # Anchor link - skip validation
                continue
            else:
                # Relative path
                base_dir = Path(file_path).parent
                target_path = base_dir / url

            # If it's a .md file, check if it exists
            if url.endswith('.md') and not target_path.exists():
                errors.append(f"Internal link broken: {url} (file does not exist)")

    return len(errors) == 0, errors


def estimate_reading_level(content: str) -> Tuple[bool, List[str]]:
    """Estimate reading level using readability metrics."""
    errors = []

    # Extract just the text content (remove markdown formatting)
    text_content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)  # Remove code blocks
    text_content = re.sub(r'!\[.*?\]\(.*?\)', '', text_content)  # Remove image references
    text_content = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text_content)  # Replace links with text
    text_content = re.sub(r'#+\s*', '', text_content)  # Remove headings
    text_content = re.sub(r'\*{1,2}(.*?)\*{1,2}', r'\1', text_content)  # Remove emphasis
    text_content = re.sub(r'_+(.*?)_+', r'\1', text_content)  # Remove underlines

    # Calculate Flesch Reading Ease score
    try:
        from textstat import flesch_reading_ease
        score = flesch_reading_ease(text_content)

        # Flesch score: 90-100 is 5th grade, 60-70 is 8th-9th grade, 0-30 is college graduate
        # For Grade 8-12, we want roughly 45-70
        if score < 45 or score > 80:
            errors.append(f"Reading level may be inappropriate (Flesch score: {score:.1f}). Should target Grade 8-12 level.")
    except ImportError:
        # If textstat is not available, skip this check
        pass

    return True, errors  # Always return True since this is an estimate


def validate_chapter(file_path: str) -> Tuple[bool, List[str]]:
    """Validate a single chapter file."""
    errors = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False, [f"Could not read file {file_path}: {e}"]

    # Run all validation checks
    checks = [
        ("Front matter completeness", check_front_matter_completeness),
        ("Heading hierarchy", verify_heading_hierarchy),
        ("Exercise count (≥2)", count_exercises),
        ("Diagram count (≥1)", count_diagrams),
        ("Code example count (≥3)", count_code_examples),
        ("Link validation", lambda c: validate_links(c, file_path)),
        ("Reading level estimation", estimate_reading_level),
    ]

    for check_name, check_func in checks:
        try:
            is_valid, check_errors = check_func(content)
            if not is_valid:
                errors.extend([f"{check_name}: {err}" for err in check_errors])
        except Exception as e:
            errors.append(f"{check_name}: Validation failed with error: {e}")

    return len(errors) == 0, errors


def main():
    parser = argparse.ArgumentParser(description='Validate textbook chapter files')
    parser.add_argument('files', nargs='+', help='Chapter files to validate')
    parser.add_argument('--report', action='store_true', help='Generate detailed validation report')

    args = parser.parse_args()

    all_valid = True
    total_errors = 0

    for file_path in args.files:
        print(f"Validating: {file_path}")

        is_valid, errors = validate_chapter(file_path)

        if is_valid:
            print(f"✅ {file_path} - PASSED")
        else:
            print(f"❌ {file_path} - FAILED")
            for error in errors:
                print(f"   - {error}")
            all_valid = False
            total_errors += len(errors)

        print()

    if args.report:
        print("=" * 50)
        print("VALIDATION REPORT")
        print("=" * 50)
        print(f"Files processed: {len(args.files)}")
        print(f"Total errors: {total_errors}")
        print(f"Overall status: {'PASS' if all_valid else 'FAIL'}")

    return 0 if all_valid else 1


if __name__ == "__main__":
    sys.exit(main())