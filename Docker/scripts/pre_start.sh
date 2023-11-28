#!/usr/bin/env bash
export PYTHONUNBUFFERED=1

echo "Container is running"

# Sync venv to workspace to support Network volumes
echo "Syncing venv to workspace, please wait..."
rsync -au /venv/ /workspace/venv/

# Sync LLaVA to workspace to support Network volumes
echo "Syncing LLaVA to workspace, please wait..."
rsync -au /LLaVA/ /workspace/LLaVA/

# Fix the venv to make it work from /workspace
echo "Fixing venv..."
/fix_venv.sh /venv /workspace/venv

if [[ ${DISABLE_AUTOLAUNCH} ]]
then
    echo "Auto launching is disabled so the application will not be started automatically"
else
    # Configure environment variables
    export LLAVA_HOST="0.0.0.0"
    export LLAVA_CONTROLLER_PORT="10000"
    export LLAVA_MODEL_WORKER_PORT="40000"
    export FLASK_HOST="0.0.0.0"
    export FLASK_PORT="5000"
    export GRADIO_SERVER_NAME=${LLAVA_HOST}
    export GRADIO_SERVER_PORT="3001"
    export HF_HOME="/workspace"

    if [[ ${MODEL} ]]
    then
      export LLAVA_MODEL=${MODEL}
    else
      export LLAVA_MODEL="SkunkworksAI/BakLLaVA-1"
    fi

    mkdir -p /workspace/logs
    echo "Starting LLaVA"
    /start_flask.sh
    /start_controller.sh
    /start_model_worker.sh
    /start_webserver.sh
    echo "LLaVA started"
    echo "Log files: "
    echo "   - Flask:   /workspace/logs/api.log"
    echo "   - Controller:   /workspace/logs/controller.log"
    echo "   - Model Worker: /workspace/logs/model-worker.log"
    echo "   - Webserver:    /workspace/logs/webserver.log"
fi

echo "All services have been started"