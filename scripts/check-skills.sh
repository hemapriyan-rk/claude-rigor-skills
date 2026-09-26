#!/usr/bin/env bash
# check-skills.sh — keep the docs in sync with the skills/ directory.
#
# Fails if:
#   - a skill folder has no SKILL.md, or its frontmatter `name` differs from the folder name
#   - a skill is missing from README.md or SKILLS.md
#   - README.md, SKILLS.md, or INSTALL.md link to a skill folder that doesn't exist
#   - a skill count stated in those files ("30 skills", "all 30", the badge) is wrong
#
# Usage: scripts/check-skills.sh   (run from anywhere inside the repo)

set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

docs=(README.md SKILLS.md INSTALL.md)
errors=0
fail() { echo "✗ $1"; errors=$((errors + 1)); }

count=0
for dir in skills/*/; do
  name=$(basename "$dir")
  count=$((count + 1))

  if [ ! -f "$dir/SKILL.md" ]; then
    fail "skills/$name has no SKILL.md"
    continue
  fi

  declared=$(sed -n 's/^name:[[:space:]]*"\{0,1\}\([^"]*\)"\{0,1\}[[:space:]]*$/\1/p' "$dir/SKILL.md" | head -n 1)
  [ "$declared" = "$name" ] || fail "skills/$name/SKILL.md declares name '$declared'"

  for doc in README.md SKILLS.md; do
    grep -q "skills/$name/SKILL.md" "$doc" || fail "$doc does not list $name"
  done
done

for doc in "${docs[@]}"; do
  for linked in $(grep -oE 'skills/[a-z0-9-]+/SKILL\.md' "$doc" | sort -u); do
    [ -f "$linked" ] || fail "$doc links to missing $linked"
  done

  # Numbers that claim to be the skill count.
  while IFS= read -r stated; do
    [ "$stated" = "$count" ] || fail "$doc says $stated skills, but skills/ has $count"
  done < <(grep -oE '((^|[ (*])[0-9]+ (Claude Code )?skills|all [0-9]+|skills-[0-9]+-|Skills: [0-9]+)' "$doc" | grep -oE '[0-9]+')
done

if [ "$errors" -gt 0 ]; then
  echo "$errors problem(s) found."
  exit 1
fi
echo "✓ $count skills; README.md, SKILLS.md, and INSTALL.md are consistent."
