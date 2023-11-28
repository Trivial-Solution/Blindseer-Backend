#!/usr/bin/env bash
source /workspace/venv/bin/activate
pip3 install flask protobuf
cd /workspace/LLaVA
nohup python3 -m llava.serve.api \
  --host ${FLASK_HOST} \
  --port ${FLASK_PORT} > /workspace/logs/api.log 2>&1 &
deactivate