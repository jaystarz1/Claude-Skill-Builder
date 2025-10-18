#!/usr/bin/env python3
"""
Skills Builder CLI
Minimal command-line interface for creating, validating, and packaging Claude Skills.
"""
import argparse
import sys
from pathlib import Path

# Import our modules with relative imports
from .scaffold import scaffold_skill
from .validate import validate_spec
from .pack import pack_skill


def main():
    parser = argparse.ArgumentParser(
        description="Skills Builder: Create domain-agnostic Claude Skills"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # NEW command
    new_parser = subparsers.add_parser("new", help="Create a new skill from spec")
    new_parser.add_argument("--spec", required=True, help="Path to skill.spec.json")
    new_parser.add_argument("--out", default="dist/", help="Output directory")

    # VALIDATE command
    validate_parser = subparsers.add_parser("validate", help="Validate a skill spec")
    validate_parser.add_argument("--spec", required=True, help="Path to skill.spec.json")

    # PACK command
    pack_parser = subparsers.add_parser("pack", help="Package a skill into .zip")
    pack_parser.add_argument("--dir", required=True, help="Skill directory to pack")
    pack_parser.add_argument("--out", required=True, help="Output .zip file path")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "new":
            print(f"Creating new skill from {args.spec}...")
            skill_path = scaffold_skill(args.spec, args.out)
            print(f"✓ Skill created at: {skill_path}")

        elif args.command == "validate":
            print(f"Validating spec: {args.spec}...")
            errors = validate_spec(args.spec)
            if errors:
                print("✗ Validation failed:")
                for error in errors:
                    print(f"  - {error}")
                sys.exit(1)
            else:
                print("✓ Spec is valid!")

        elif args.command == "pack":
            print(f"Packing skill from {args.dir}...")
            zip_path = pack_skill(args.dir, args.out)
            print(f"✓ Skill packaged: {zip_path}")

    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
