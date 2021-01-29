#!/usr/bin/env bash
set -ex

pip3 install -r ./test/requirements.txt

export PYTHONPATH="$PYTHONPATH:$(pwd)/test/:$(pwd)/src/"

echo "Running tests..."
if pytest .; then
  sam build -t sam-template.yaml && sam deploy -t sam-template.yaml
else
  echo "Tests failed..."
  exit 1
fi

echo "Running external tests..."

export TEST_DEPLOYMENT=true

pytest ./test/test_external.py