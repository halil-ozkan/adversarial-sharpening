#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FAILS=0
WARNS=0

section() {
  echo
  echo "$1"
  printf '%*s\n' "${#1}" '' | tr ' ' '-'
}

ok() {
  echo "ok: $1"
}

warn() {
  WARNS=$((WARNS + 1))
  echo "warn: $1"
}

fail() {
  FAILS=$((FAILS + 1))
  echo "fail: $1"
}

count_files() {
  local dir="$1"
  if [[ -d "$ROOT_DIR/$dir" ]]; then
    find "$ROOT_DIR/$dir" -type f | wc -l | tr -d ' '
  else
    echo "0"
  fi
}

print_section() {
  local dir="$1"
  local label="$2"

  echo "$label: $(count_files "$dir")"
  if [[ -d "$ROOT_DIR/$dir" ]]; then
    find "$ROOT_DIR/$dir" -type f | sort | sed "s#^$ROOT_DIR/##"
  else
    echo "missing: $dir/"
  fi
  echo
}

check_required_file() {
  local path="$1"
  if [[ -e "$ROOT_DIR/$path" ]]; then
    ok "$path exists"
  else
    fail "$path is missing"
  fi
}

check_gitignore_pattern() {
  local pattern="$1"
  if [[ -f "$ROOT_DIR/.gitignore" ]] && grep -Fxq "$pattern" "$ROOT_DIR/.gitignore"; then
    ok ".gitignore excludes $pattern"
  else
    fail ".gitignore does not exclude $pattern"
  fi
}

echo "Artifact audit"
echo "=============="
echo
echo "Root: $ROOT_DIR"

section "Required files"
check_required_file ".gitignore"
check_required_file "README.md"
check_required_file "ARTIFACT_INDEX.md"
check_required_file "PROJECT_STATUS.md"
check_required_file "AGENTS.md"
check_required_file "cases"
check_required_file "benchmarks"
check_required_file "evals"
check_required_file "protocols"
check_required_file "scripts"

section "Artifact inventory"
print_section "evals" "Evals"
print_section "benchmarks" "Benchmarks"
print_section "protocols" "Protocols"
print_section "cases" "Cases"

section "AGENTS.md checks"
if [[ -f "$ROOT_DIR/AGENTS.md" ]]; then
  if grep -q "Slippery Stone Protocol" "$ROOT_DIR/AGENTS.md"; then
    ok "Slippery Stone Protocol is logged"
  else
    fail "Slippery Stone Protocol is missing"
  fi

  if grep -q "Track dumpsite automation" "$ROOT_DIR/AGENTS.md"; then
    ok "Track dumpsite automation is logged"
  else
    warn "Track dumpsite automation is missing"
  fi
else
  fail "AGENTS.md is missing"
fi

section "Anonymity scan"
TMP_MARKERS="$(mktemp)"
grep -RInEi \
  --include='*.md' \
  --exclude-dir='private' \
  "halil|mayor|codex|chatgpt\.com|github\.dev|samsung|android|mx keys|cafe|phone app|ritual timing|hallelujah|found and explained|tremor|adhd|health|medical|accessibility" \
  "$ROOT_DIR" > "$TMP_MARKERS" || true

if [[ -s "$TMP_MARKERS" ]]; then
  fail "public anonymity markers found"
  cat "$TMP_MARKERS"
else
  ok "no obvious public anonymity markers found"
fi
rm -f "$TMP_MARKERS"

section "Upload hazards"
check_gitignore_pattern "ffmpeg.exe"
check_gitignore_pattern "ffprobe.exe"
check_gitignore_pattern "delivery/"
check_gitignore_pattern "*.zip"
check_gitignore_pattern "private/"

if [[ -e "$ROOT_DIR/ffmpeg.exe" || -e "$ROOT_DIR/ffprobe.exe" ]]; then
  warn "local media binaries exist; do not manually upload the whole folder"
else
  ok "no local media binaries found"
fi

if [[ -d "$ROOT_DIR/delivery" ]]; then
  ok "delivery bundle folder exists locally and is ignored"
else
  ok "no local delivery folder found"
fi

section "Delivery bundle"
ZIP_PATH="$ROOT_DIR/delivery/AS-010-03.07.2026-00-37-artifacts-github-bundle.zip"
if [[ -f "$ZIP_PATH" ]]; then
  ok "delivery zip exists"
  if command -v tar >/dev/null 2>&1; then
    TMP_ZIP_LIST="$(mktemp)"
    tar -tf "$ZIP_PATH" > "$TMP_ZIP_LIST"
    cat "$TMP_ZIP_LIST"

    if grep -E '\.exe$|^delivery/|\.zip$' "$TMP_ZIP_LIST" >/dev/null; then
      fail "delivery zip contains excluded files"
    else
      ok "delivery zip excludes binaries, nested zips, and delivery folder"
    fi

    TMP_EXPECTED_LIST="$(mktemp)"
    (
      cd "$ROOT_DIR"
      find . -type f \
        ! -path './delivery/*' \
        ! -path './private/*' \
        ! -name '*.zip' \
        ! -name 'ffmpeg.exe' \
        ! -name 'ffprobe.exe' |
        sed 's#^\./##' |
        sort
    ) > "$TMP_EXPECTED_LIST"

    TMP_ZIP_SORTED="$(mktemp)"
    sort "$TMP_ZIP_LIST" > "$TMP_ZIP_SORTED"

    TMP_MISSING="$(mktemp)"
    TMP_EXTRA="$(mktemp)"
    comm -23 "$TMP_EXPECTED_LIST" "$TMP_ZIP_SORTED" > "$TMP_MISSING"
    comm -13 "$TMP_EXPECTED_LIST" "$TMP_ZIP_SORTED" > "$TMP_EXTRA"

    if [[ -s "$TMP_MISSING" ]]; then
      warn "delivery zip is missing current artifact files; manual upload mode treats this as non-blocking"
      cat "$TMP_MISSING"
    fi

    if [[ -s "$TMP_EXTRA" ]]; then
      warn "delivery zip contains stale or unexpected files; manual upload mode treats this as non-blocking"
      cat "$TMP_EXTRA"
    fi

    if [[ ! -s "$TMP_MISSING" && ! -s "$TMP_EXTRA" ]]; then
      ok "delivery zip matches current artifact files"
    fi

    rm -f "$TMP_EXPECTED_LIST" "$TMP_ZIP_SORTED" "$TMP_MISSING" "$TMP_EXTRA"
    rm -f "$TMP_ZIP_LIST"
  else
    warn "tar is unavailable; could not inspect zip contents"
  fi
else
  warn "delivery zip not found"
fi

section "Focused AS-010 update bundle"
UPDATE_ZIP_PATH="$ROOT_DIR/delivery/AS-010-03.07.2026-00-37-boundary-drift-contextual-fog-update.zip"
if [[ -f "$UPDATE_ZIP_PATH" ]]; then
  ok "AS-010 focused update zip exists"
  if command -v tar >/dev/null 2>&1; then
    TMP_UPDATE_ZIP_LIST="$(mktemp)"
    tar -tf "$UPDATE_ZIP_PATH" > "$TMP_UPDATE_ZIP_LIST"
    cat "$TMP_UPDATE_ZIP_LIST"

    REQUIRED_UPDATE_ENTRIES=(
      "evals/AS-010-03.07.2026-00-00-boundary-drift-contextual-fog.md"
      "ARTIFACT_INDEX.md"
      "PROJECT_STATUS.md"
      "README.md"
      "scripts/audit_artifacts.ps1"
      "scripts/audit_artifacts.sh"
    )

    for entry in "${REQUIRED_UPDATE_ENTRIES[@]}"; do
      if ! grep -Fxq "$entry" "$TMP_UPDATE_ZIP_LIST"; then
        fail "AS-010 focused update zip is missing $entry"
      fi
    done

    if [[ "$FAILS" -eq 0 ]]; then
      ok "AS-010 focused update zip contains required files"
    fi

    rm -f "$TMP_UPDATE_ZIP_LIST"
  else
    warn "tar is unavailable; could not inspect AS-010 focused update zip"
  fi
else
  fail "AS-010 focused update zip is missing"
fi

section "Git state"
if [[ -d "$ROOT_DIR/.git" ]]; then
  ok "git repository is initialized"
  if command -v git >/dev/null 2>&1; then
    git -C "$ROOT_DIR" status --short
  else
    warn "git command is unavailable"
  fi
else
  ok "this folder is not initialized as a git repository"
fi

echo
echo "Summary"
echo "-------"
echo "Failures: $FAILS"
echo "Warnings: $WARNS"

if [[ "$FAILS" -gt 0 ]]; then
  exit 1
fi
