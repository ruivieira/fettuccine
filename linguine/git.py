import pygit2


class Git:
    def __init__(self, path):
        repo_path = pygit2.discover_repository(path)
        if repo_path is None:
            raise Exception("No repository found containing the given folder")

        # Open the repository
        self._repo = pygit2.Repository(repo_path)
