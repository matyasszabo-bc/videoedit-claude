#!/bin/bash
# BrokerChooser Video Skill — Prerequisites Check
# Run this before the first session on a new machine.

PASS=0
FAIL=0

check() {
  local name="$1"
  local cmd="$2"
  local hint="$3"

  if eval "$cmd" &>/dev/null; then
    echo "  ✓ $name"
    ((PASS++))
  else
    echo "  ✗ $name"
    echo "    → $hint"
    ((FAIL++))
  fi
}

echo ""
echo "BrokerChooser Video Skill — Prerequisites Check"
echo "================================================"
echo ""

echo "Core tools:"
check "ffmpeg"    "ffmpeg -version"          "brew install ffmpeg"
check "Node.js"   "node --version"           "https://nodejs.org — install LTS"
check "Python 3"  "python3 --version"        "brew install python3"
check "git"       "git --version"            "brew install git"

echo ""
echo "Remotion:"
check "remotion (global)" "npx remotion --version 2>/dev/null || remotion --version" \
  "npm install -g remotion  OR  add to project: npm install remotion"

echo ""
echo "MCP configuration (~/.claude/mcp.json):"
MCP_FILE="$HOME/.claude/mcp.json"

if [ -f "$MCP_FILE" ]; then
  if grep -q "figma-brokerchooser" "$MCP_FILE"; then
    echo "  ✓ figma-brokerchooser entry found"
    ((PASS++))
  else
    echo "  ✗ figma-brokerchooser missing from mcp.json"
    echo "    → Add the figma-brokerchooser entry with design@brokerchooser.com PAT"
    ((FAIL++))
  fi

  if grep -q "brokerchooser" "$MCP_FILE"; then
    echo "  ✓ BrokerChooser Private MCP entry found"
    ((PASS++))
  else
    echo "  ✗ BrokerChooser Private MCP missing from mcp.json"
    echo "    → Add the internal BC MCP config entry"
    ((FAIL++))
  fi
else
  echo "  ✗ ~/.claude/mcp.json not found"
  echo "    → Create it and add figma-brokerchooser and brokerchooser-private entries"
  ((FAIL++))
  ((FAIL++))
fi

echo ""
echo "================================================"
echo "  Passed: $PASS"
if [ $FAIL -gt 0 ]; then
  echo "  Failed: $FAIL  ← install missing tools above"
  echo ""
  echo "See PREREQUISITES.md for detailed install instructions."
  exit 1
else
  echo "  All checks passed. Ready to edit."
fi
echo ""
