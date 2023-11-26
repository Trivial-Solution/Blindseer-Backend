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
        existing_containers = client.containers.list(all=True, filters={'ancestor': 'llavaapi:latest'})

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
                except Exception as e:
                    print(f"Error: {e}")
        else:
            # Docker run options
            docker_options = {
                'detach': True,
                'ports': {'3000': '3001', '8888': '8888', '5000': '5000'},
                'environment': {'JUPYTER_PASSWORD': 'Jup1t3R!'},
            }

            try:
                container = client.containers.run('ashleykza/llava:latest', **docker_options)
                print(f"Docker container {container.id} is now running.")

            except Exception as e:
                print(f"Error: {e}")
