#!/usr/bin/env python3
"""Quick validation script for skills.

Validates:
1. Core skill structure (`SKILL.md`)
2. Optional OpenAI/Codex UI metadata (`agents/openai.yaml`)
3. Basic consistency between the two when metadata exists
"""

import sys
import re
import yaml
from pathlib import Path

def _validate_frontmatter(skill_md):
    """Validate SKILL.md frontmatter and return parsed values."""
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "No YAML frontmatter found", None

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "Invalid frontmatter format", None

    frontmatter_text = match.group(1)

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary", None
    except yaml.YAMLError as e:
        return False, f"Invalid YAML in frontmatter: {e}", None

    allowed_properties = {
        'name',
        'description',
        'license',
        'allowed-tools',
        'metadata',
        'compatibility',
    }
    unexpected_keys = set(frontmatter.keys()) - allowed_properties
    if unexpected_keys:
        return False, (
            f"Unexpected key(s) in SKILL.md frontmatter: {', '.join(sorted(unexpected_keys))}. "
            f"Allowed properties are: {', '.join(sorted(allowed_properties))}"
        ), None

    if 'name' not in frontmatter:
        return False, "Missing 'name' in frontmatter", None
    if 'description' not in frontmatter:
        return False, "Missing 'description' in frontmatter", None

    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"Name must be a string, got {type(name).__name__}", None
    name = name.strip()
    if name:
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, (
                f"Name '{name}' should be kebab-case "
                "(lowercase letters, digits, and hyphens only)"
            ), None
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, (
                f"Name '{name}' cannot start/end with hyphen "
                "or contain consecutive hyphens"
            ), None
        if len(name) > 64:
            return False, (
                f"Name is too long ({len(name)} characters). Maximum is 64 characters."
            ), None

    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, (
            f"Description must be a string, got {type(description).__name__}"
        ), None
    description = description.strip()
    if description:
        if '<' in description or '>' in description:
            return False, "Description cannot contain angle brackets (< or >)", None
        if len(description) > 1024:
            return False, (
                f"Description is too long ({len(description)} characters). "
                "Maximum is 1024 characters."
            ), None

    compatibility = frontmatter.get('compatibility', '')
    if compatibility:
        if not isinstance(compatibility, str):
            return False, (
                f"Compatibility must be a string, got {type(compatibility).__name__}"
            ), None
        if len(compatibility) > 500:
            return False, (
                f"Compatibility is too long ({len(compatibility)} characters). "
                "Maximum is 500 characters."
            ), None

    return True, "Frontmatter is valid", frontmatter


def _validate_openai_yaml(skill_path, skill_name):
    """Validate optional agents/openai.yaml metadata."""
    warnings = []
    openai_yaml = skill_path / 'agents' / 'openai.yaml'

    if not openai_yaml.exists():
        warnings.append(
            "Optional file missing: agents/openai.yaml "
            "(recommended for OpenAI/Codex UI metadata)"
        )
        return True, warnings

    try:
        metadata = yaml.safe_load(openai_yaml.read_text()) or {}
    except yaml.YAMLError as e:
        return False, [f"Invalid YAML in agents/openai.yaml: {e}"]

    if not isinstance(metadata, dict):
        return False, ["agents/openai.yaml must be a YAML dictionary"]

    interface = metadata.get("interface", {})
    if interface and not isinstance(interface, dict):
        return False, ["'interface' in agents/openai.yaml must be a dictionary"]

    policy = metadata.get("policy", {})
    if policy and not isinstance(policy, dict):
        return False, ["'policy' in agents/openai.yaml must be a dictionary"]

    display_name = interface.get("display_name")
    short_description = interface.get("short_description")
    default_prompt = interface.get("default_prompt")

    if display_name is not None:
        if not isinstance(display_name, str) or not display_name.strip():
            return False, ["interface.display_name must be a non-empty string"]

    if short_description is not None:
        if not isinstance(short_description, str) or not short_description.strip():
            return False, ["interface.short_description must be a non-empty string"]
        short_len = len(short_description.strip())
        if short_len < 25 or short_len > 64:
            warnings.append(
                "interface.short_description is recommended to be 25-64 characters"
            )

    if default_prompt is not None:
        if not isinstance(default_prompt, str) or not default_prompt.strip():
            return False, ["interface.default_prompt must be a non-empty string"]
        expected_skill_ref = f"${skill_name}"
        if expected_skill_ref not in default_prompt:
            return False, [
                "interface.default_prompt must explicitly mention the skill as "
                f"'{expected_skill_ref}'"
            ]

    allow_implicit = policy.get("allow_implicit_invocation")
    if allow_implicit is not None and not isinstance(allow_implicit, bool):
        return False, ["policy.allow_implicit_invocation must be a boolean"]

    return True, warnings


def validate_skill(skill_path, require_openai_yaml=False):
    """Validate skill structure and optional UI metadata."""
    skill_path = Path(skill_path)
    warnings = []

    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md not found", warnings

    valid, message, frontmatter = _validate_frontmatter(skill_md)
    if not valid:
        return False, message, warnings

    openai_valid, openai_messages = _validate_openai_yaml(
        skill_path, frontmatter["name"]
    )
    if not openai_valid:
        return False, openai_messages[0], warnings + openai_messages[1:]

    warnings.extend(openai_messages)
    if require_openai_yaml and not (skill_path / 'agents' / 'openai.yaml').exists():
        return False, "agents/openai.yaml is required but missing", warnings

    return True, "Skill is valid!", warnings

if __name__ == "__main__":
    args = sys.argv[1:]
    require_openai = False

    if not args or len(args) > 2:
        print("Usage: python quick_validate.py <skill_directory> [--require-openai-yaml]")
        sys.exit(1)

    if len(args) == 2:
        if args[1] != "--require-openai-yaml":
            print("Unknown flag:", args[1])
            sys.exit(1)
        require_openai = True

    valid, message, warnings = validate_skill(args[0], require_openai)
    print(message)
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")
    sys.exit(0 if valid else 1)
