from loguru import logger
import docker
from sandbox.core.config import settings
from sandbox.sb.models import Event


def run_container_detached(image_name: str, env_vars: dict[str, str]) -> str | None:
    """
    Starts a Docker container in the background (detached) with specified
    environment variables and returns its ID.

    Args:
        image_name: The name of the Docker image to use (e.g., 'ubuntu:latest').
        env_vars: A dictionary of environment variables to set in the container
                  (e.g., {'VAR_NAME': 'value', 'TWITTER_ACCOUNT_ID': 'xyz'}).

    Returns:
        The full container ID (string) if successful, None otherwise.

    Raises:
        docker.errors.DockerException: If there's an issue communicating with the Docker daemon
                                       or other Docker-specific errors occur.
        docker.errors.ImageNotFound: If the specified image does not exist locally and cannot be pulled.
        docker.errors.APIError: For other errors returned by the Docker daemon API.
        Exception: For any other unexpected errors during execution.
    """
    try:
        client = docker.from_env()
        client.ping()
        logger.info(f"Attempting to run image '{image_name}' in detached mode...")
        logger.info("Docker daemon connection successful.")

        container = client.containers.run(
            image=image_name,
            name=f"sandbox_{env_vars.get('TWITTER_ACCOUNT_ID')}",
            environment=env_vars,
            detach=False,
            command="python3 -m src.agents",
            stream=True, tty=True
        )

        logger.info(f"Container '{container.short_id}' ({image_name}) started successfully.")
        return container.id

    except docker.errors.ImageNotFound:
        logger.error(f"Docker image '{image_name}' not found. "
                      f"Please ensure it exists locally or can be pulled.")
        raise
    except docker.errors.APIError as e:
        logger.error(f"Docker API error encountered: {e}")
        raise
    except docker.errors.DockerException as e:
        logger.error(f"Docker client/daemon error: {e}")
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    image = "registry.digitalocean.com/eavelabs/pipeline_prod:v1"
    container_id = run_container_detached(image, '67ad97fd69696f74dc6cfb68')
    if container_id:
        print(f"\nSuccessfully started container.")
        print(f"  Image: {image}")
        print(f"  Container ID: {container_id}")
        print(f"  Short ID: {container_id[:12]}")
        print("\nUse 'docker ps' to see the running container.")
        print(f"Use 'docker logs {container_id[:12]}' to see its logs.")
        print(f"Use 'docker stop {container_id[:12]}' to stop it.")
