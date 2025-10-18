#!/bin/bash

echo "Testing Claude Skills Builder..."
echo ""

cd /Users/jaytarzwell/skills/skills-builder

echo "1. Testing validation on best-practices example..."
python3 -m code.cli validate --spec examples/best-practices/skill.spec.json
echo ""

echo "2. Testing validation on minimal example..."
python3 -m code.cli validate --spec examples/minimal/skill.spec.json
echo ""

echo "3. Testing skill generation..."
python3 -m code.cli new --spec examples/minimal/skill.spec.json --out dist/test-output/
echo ""

echo "4. Testing packaging..."
python3 -m code.cli pack --dir dist/test-output/document-summarizer --out dist/test-output.zip
echo ""

echo "✅ All tests complete!"
