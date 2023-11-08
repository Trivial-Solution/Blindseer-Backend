import os
import docker


class DockerService:
    @staticmethod
    def start_docker():
        """
        Starts a Docker container.
        """
        client = docker.from_env()

        # Check if the container already exists
        existing_containers = client.containers.list(all=True, filters={'ancestor': 'ashleykza/llava:latest'})

        if existing_containers:
            print("Docker container already exists")
            # Check if any of the existing containers are running
            running_containers = [container for container in existing_containers if container.status == 'running']
            if running_containers:
                print("The Docker container is already running.")
            else:
                # Start the existing container that is not running
                try:
                    container = existing_containers[0]
                    container.start()
                    # Install dependencies and check the result
                    result = container.exec_run("fuser -k 10000/tcp 40000/tcp")
                    if result.exit_code == 0:
                        print("fuser command ran successfully.")
                    else:
                        print(f"fuser command failed: {result.output}")

                    # Install dependencies and check the result
                    result = container.exec_run("/workspace/venv/bin/pip3 install flask protobuf")
                    if result.exit_code == 0:
                        print("Dependencies installed successfully.")
                    else:
                        print(f"Dependency installation failed: {result.output}")

                    # Start the LLaVA API server with environment variable and check the result
                    result = container.exec_run(
                        "/bin/bash -c 'export HF_HOME=\"/workspace\" && python -m llava.serve.api -H 0.0.0.0 -p 5000'")
                    if result.exit_code == 0:
                        print("LLaVA API server started successfully.")
                    else:
                        print(f"LLaVA API server start failed: {result.output}")
                except Exception as e:
                    print(f"Error: {e}")
        else:
            # Docker run options
            docker_options = {
                'detach': True,
                'ports': {'3000': '3001', '8888': '8888', '5000': '5000'},
                'environment': {'JUPYTER_PASSWORD': 'Jup1t3R!'},
                'volumes': {'/workspace': {'bind': '/workspace', 'mode': 'rw'}},
                'runtime': 'nvidia',  # This is equivalent to --gpus all in the command line
            }

            try:
                container = client.containers.run('ashleykza/llava:latest', **docker_options)
                print(f"Docker container {container.id} is now running.")

                result = container.exec_run("fuser -k 10000/tcp 40000/tcp")
                if result.exit_code == 0:
                    print("fuser command ran successfully.")
                else:
                    print(f"fuser command failed: {result.output}")

                # Install dependencies and check the result
                result = container.exec_run("/workspace/venv/bin/pip3 install flask protobuf")
                if result.exit_code == 0:
                    print("Dependencies installed successfully.")
                else:
                    print(f"Dependency installation failed: {result.output}")

                # Start the LLaVA API server with environment variable and check the result
                result = container.exec_run(
                    "/bin/bash -c 'export HF_HOME=\"/workspace\" && python -m llava.serve.api -H 0.0.0.0 -p 5000'",
                    detach=True)
                if result.exit_code == 0:
                    print("LLaVA API server started successfully.")
                else:
                    print(f"LLaVA API server start failed: {result.output}")

            except Exception as e:
                print(f"Error: {e}")
