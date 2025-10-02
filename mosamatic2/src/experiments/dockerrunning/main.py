def is_docker_running():
    import docker
    try:
        client = docker.from_env()
        client.ping()
        return True
    except Exception:
        return False


print(is_docker_running())