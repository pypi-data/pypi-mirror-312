import subprocess

class GitInfo:
    def __init__(self):
        self.repo_path = '.'  # Default to current directory

    def run_command(self, command):
        """Run a Git command and return its output."""
        result = subprocess.run(
            command,
            cwd=self.repo_path,
            text=True,
            capture_output=True,
            shell=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"Command '{command}' failed with error: {result.stderr.strip()}")
        return result.stdout.strip()

    def get_git_info(self):
        """Get various Git information."""
        info = {
            'branch': self.get_current_branch(),
            'commit_hash': self.get_commit_hash(),
            'commit_message': self.get_commit_message(),
            # 'status': self.get_status(),
            'remote_url': self.get_remote_url(),
            'last_commit_author': self.get_last_commit_author(),
            # 'untracked_files': self.get_untracked_files()
        }
        return info

    def get_current_branch(self):
        """Get the current branch name."""
        return self.run_command('git rev-parse --abbrev-ref HEAD')

    def get_commit_hash(self):
        """Get the latest commit hash."""
        return self.run_command('git rev-parse HEAD')

    def get_commit_message(self):
        """Get the latest commit message."""
        return self.run_command('git log -1 --pretty=%B')

    def get_status(self):
        """Get the Git status."""
        return self.run_command('git status --short')

    def get_remote_url(self):
        """Get the remote repository URL."""
        return self.run_command('git remote get-url origin')

    def get_last_commit_author(self):
        """Get the author of the latest commit."""
        return self.run_command('git log -1 --pretty=%an')

    def get_untracked_files(self):
        """Get a list of untracked files."""
        status = self.run_command('git status --porcelain')
        untracked_files = [line[3:] for line in status.splitlines() if line.startswith('??')]
        return untracked_files

    def print_all(self):
        """Print all Git information."""
        info = self.get_git_info()
        # for key, value in info.items():
        #     print(f"{key}: {value}")
        print("DEBUG ONLY ===============================================================")
        print(info)
        print("DEBUG ONLY ===============================================================")
