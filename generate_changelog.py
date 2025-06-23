# -*- coding: UTF-8 -*-

# Description: This script generates a changelog based on Git tags and commit messages. 

# Author: Edilberto Fonseca
# Email: <edilberto.fonseca@outlook.com>
# Copyright (C) 2022-2025 Edilberto Fonseca
# This file is covered by the GNU General Public License.
# See the file COPYING for more details or visit https://www.gnu.org/licenses/gpl-2.0.html.

# Date of creation: 23/06/2025

import subprocess
import re
from collections import defaultdict

TYPES = {
    "feat": "✨ New Features",
    "fix": "🐛 Bug Fixes",
    "docs": "📝 Documentation",
    "style": "🎨 Style and Formatting",
    "refactor": "♻️ Refactoring",
    "perf": "⚡ Performance Improvements",
    "test": "✅ Tests",
    "chore": "🔧 Other Tasks",
    "build": "🏗️ Build Changes",
    "ci": "🔁 Continuous Integration"
}

def run_command(cmd):
    result = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
    return result.decode("utf-8").strip()

def get_tags():
    tags = run_command(["git", "tag", "--sort=-creatordate"]).split("\n")
    return tags

def get_tag_date(tag):
    date = run_command(["git", "log", "-1", "--format=%ad", "--date=short", tag])
    return date

def get_commits_between_tags(current_tag, previous_tag=None):
    if previous_tag:
        range_ = f"{previous_tag}..{current_tag}"
    else:
        range_ = current_tag
    log = run_command([
        "git", "log", range_,
        "--pretty=format:%H|%s|%an|%ad",
        "--date=short"
    ])
    commits = []
    for line in log.split("\n"):
        parts = line.split("|")
        if len(parts) == 4:
            hash_, msg, author, date = parts
            commits.append((hash_, msg.strip(), author.strip(), date.strip()))
    return commits

def group_by_type(commits):
    grouped = defaultdict(list)
    for hash_, msg, author, date in commits:
        type_match = re.match(r"(\w+)(\(.+\))?:\s", msg)
        type_ = type_match.group(1) if type_match else "others"
        entry = f"* {msg} — `{author}` on {date}"
        grouped[type_].append(entry)
    return grouped

def generate_changelog(file_name="CHANGELOG.md"):
    tags = get_tags()
    if not tags:
        print("⚠️ No Git tags found. Add one with `git tag v1.0.0`.")
        return

    with open(file_name, "w", encoding="utf-8") as f:
        f.write("# 📋 Changelog\n\n")

        for i, tag in enumerate(tags):
            tag_date = get_tag_date(tag)
            previous_tag = tags[i + 1] if i + 1 < len(tags) else None
            commits = get_commits_between_tags(tag, previous_tag)

            if not commits:
                continue

            f.write(f"## {tag} — {tag_date}\n\n")
            grouped = group_by_type(commits)

            for type_, entries in grouped.items():
                title = TYPES.get(type_, f"🔸 {type_.capitalize()}")
                f.write(f"### {title}\n\n")
                for entry in entries:
                    f.write(f"{entry}\n")
                f.write("\n")

    print(f"✅ Changelog by tags generated in '{file_name}'.")
