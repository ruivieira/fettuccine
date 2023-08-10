import pygit2
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class Git:
    def __init__(self, path: str):
        repo_path = pygit2.discover_repository(path)
        if repo_path is None:
            raise Exception("No repository found containing the given folder")

        # Open the repository
        self._repo = pygit2.Repository(repo_path)

    def branch_exists(self, branch_name: str):
        """Check if a branch with the given name exists in the repository."""
        return branch_name in self._repo.branches.local

    def create_branch(self, branch_name: str):
        """Create a branch with the given name in the repository."""
        if self.branch_exists(branch_name):
            logging.warning(f"Branch {branch_name} already exists!")
        else:
            commit = self._repo.revparse_single('HEAD')
            self._repo.branches.local.create(branch_name, commit)
            logging.debug(f"Branch {branch_name} created!")