from loguru import logger
import docker


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
        # Connect to the Docker daemon using environment settings
        # (respects DOCKER_HOST, DOCKER_TLS_VERIFY, etc.)
        client = docker.from_env()
        logger.info(f"Attempting to run image '{image_name}' in detached mode...")

        # Verify Docker daemon is responding (optional but good practice)
        client.ping()
        logger.info("Docker daemon connection successful.")

        # Run the container
        # - detach=True: Run in the background and return a Container object immediately.
        # - environment: Pass the environment variables dictionary.
        # - remove=False (default): Container won't be automatically removed on exit.
        #                 Set to True if you want automatic cleanup for short-lived containers.
        container = client.containers.run(
            image=image_name,
            name=f"sandbox_{env_vars.get('TWITTER_ACCOUNT_ID')}",
            environment=env_vars,
            detach=True
            # remove=True # Uncomment if you want auto-removal on exit
        )

        logger.info(f"Container '{container.short_id}' ({image_name}) started successfully.")
        # Return the full container ID
        return container.id

    except docker.errors.ImageNotFound:
        logger.error(f"Docker image '{image_name}' not found. "
                      f"Please ensure it exists locally or can be pulled.")
        raise # Re-raise the specific exception
    except docker.errors.APIError as e:
        logger.error(f"Docker API error encountered: {e}")
        raise # Re-raise the specific exception
    except docker.errors.DockerException as e:
         # Covers connection errors and other Docker issues
         logger.error(f"Docker client/daemon error: {e}")
         raise # Re-raise the specific exception
    except Exception as e:
        # Catch any other unexpected errors
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        raise # Re-raise the generic exception


if __name__ == "__main__":
    # Example image - make sure you have it locally (e.g., docker pull alpine:latest)
    test_image = "alpine:latest"
    # Example command for the container to run something simple in the background
    # Alpine needs a command to stay running, like sleep. Many real images
    # have default commands (e.g., a web server). Add command=["sleep", "infinity"] if needed.
    # Example environment variables, including the requested one
    test_environment = {
        "LOG_LEVEL": "debug",
        "API_KEY": "secret123",
        "TWITTER_ACCOUNT_ID": "your_twitter_id_here"
    }

    container_id = None
    try:
        # Call the function
        container_id = run_container_detached(test_image, test_environment)

        if container_id:
            print(f"\nSuccessfully started container.")
            print(f"  Image: {test_image}")
            print(f"  Container ID: {container_id}")
            print(f"  Short ID: {container_id[:12]}")
            print("\nUse 'docker ps' to see the running container.")
            print(f"Use 'docker logs {container_id[:12]}' to see its logs.")
            print(f"Use 'docker stop {container_id[:12]}' to stop it.")

    except Exception as e:
         # Catch exceptions raised by the function for cleaner example output
         print(f"\nFailed to start container. Error: {e}")