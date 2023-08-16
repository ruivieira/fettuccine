import pygit2
import logging
import re
import semver

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class Git:
    def __init__(self, path: str):
        repo_path = pygit2.discover_repository(path)
        if repo_path is None:
            raise Exception("No repository found containing the given folder")

        # Open the repository
        self._repo = pygit2.Repository(repo_path)
        self.branches = Branches(self)

    def has_changes(self) -> bool:
        """Check if there are any changes in the repository.

        Returns:
            bool: True if there are changes, False otherwise.
        """
        # Check the status of the files
        status = self._repo.status()

        # Iterate through the status to see if there are any changes
        has_changes = False
        for filepath, flags in status.items():
            # Check if the file is untracked, modified, or staged
            if flags != pygit2.GIT_STATUS_CURRENT:
                has_changes = True
                break

        return has_changes


class Branches:
    def __init__(self, git: Git):
        self._git = git

    def branch_exists(self, branch_name: str):
        """Check if a branch with the given name exists in the repository."""
        return branch_name in self._git._repo.branches.local

    def create_branch(self, branch_name: str):
        """Create a branch with the given name in the repository."""
        if self.branch_exists(branch_name):
            logging.warning(f"Branch {branch_name} already exists!")
        else:
            commit = self._git._repo.revparse_single('HEAD')
            self._git._repo.branches.local.create(branch_name, commit)
            logging.debug(f"Branch {branch_name} created!")

    def _get_latest_version(self, pattern):
        pattern_regex = re.compile(pattern.replace("$version", "(.*)"))

        matching_branches = [branch for branch in self._git._repo.branches.local if pattern_regex.match(branch)]

        versions = [semver.Version.parse(branch_match.group(1)) for branch in matching_branches if
                    (branch_match := pattern_regex.match(branch))]
        latest_version = max(versions) if versions else None
        return latest_version

    def create_minor_branch(self, pattern):

        latest_version = self._get_latest_version(pattern)

        if latest_version:
            new_version = latest_version.bump_minor()
            new_branch_name = pattern.replace("$version", str(new_version))
        else:
            new_version = semver.Version.parse("1.0.0")
            new_branch_name = pattern.replace("$version", str(new_version))

        self.create_branch(new_branch_name)
        return new_branch_name

    def create_major_branch(self, pattern):

        latest_version = self._get_latest_version(pattern)

        if latest_version:
            new_version = latest_version.bump_major()
            new_branch_name = pattern.replace("$version", str(new_version))
        else:
            new_version = semver.Version.parse("1.0.0")
            new_branch_name = pattern.replace("$version", str(new_version))

        self.create_branch(new_branch_name)
        return new_branch_name

    def create_patch_branch(self, pattern):

        latest_version = self._get_latest_version(pattern)

        if latest_version:
            new_version = latest_version.bump_patch()
            new_branch_name = pattern.replace("$version", str(new_version))
        else:
            new_version = semver.Version.parse("1.0.0")
            new_branch_name = pattern.replace("$version", str(new_version))

        self.create_branch(new_branch_name)
        return new_branch_name

    def checkout(self, name: str):
        """Checkout the branch with the given name."""
        # Check if the branch exists
        if name in self._git._repo.branches:
            # Get the branch reference
            branch_ref = self._git._repo.branches[name]

            # Check out the branch (this will update the HEAD and the working directory)
            self._git._repo.checkout(branch_ref)
        else:
            logging.error(f"Branch '{name}' does not exist.")
