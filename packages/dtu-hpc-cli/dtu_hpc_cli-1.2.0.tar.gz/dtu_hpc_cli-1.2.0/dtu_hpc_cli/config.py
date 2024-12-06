import dataclasses
import json
from hashlib import sha256
from pathlib import Path

from git import Repo

from dtu_hpc_cli.constants import CONFIG_FILENAME
from dtu_hpc_cli.constants import HISTORY_FILENAME
from dtu_hpc_cli.error import error_and_exit
from dtu_hpc_cli.types import Memory
from dtu_hpc_cli.types import Time

ACTIVE_BRANCH_KEY = "[[active_branch]]"

DEFAULT_HOSTNAME = "login1.hpc.dtu.dk"

DEFAULT_SUBMIT_BRANCH = "main"


@dataclasses.dataclass
class InstallConfig:
    commands: list[str]
    sync: bool

    @classmethod
    def load(cls, config: dict):
        if "install" not in config:
            return None

        install = config["install"]

        if isinstance(install, list):
            # We support this configuration for backwards compatibility
            return cls(commands=install, sync=True)

        if not isinstance(install, dict):
            error_and_exit(f"Invalid type for install option in config. Expected dictionary but got {type(install)}.")

        if "commands" not in install:
            error_and_exit('"commands" not found in install config.')

        commands = install["commands"]
        if not isinstance(commands, list):
            error_and_exit(
                f"Invalid type for commands option in install config. Expected list but got {type(commands)}."
            )

        sync = install.get("sync", True)
        if not isinstance(sync, bool):
            error_and_exit(f"Invalid type for sync option in install config. Expected boolean but got {type(sync)}.")

        return cls(commands=commands, sync=sync)


@dataclasses.dataclass
class SSHConfig:
    hostname: str
    user: str
    identityfile: str

    @classmethod
    def load(cls, config: dict):
        if "ssh" not in config:
            return None

        ssh = config["ssh"]

        if not isinstance(ssh, dict):
            error_and_exit(f"Invalid type for ssh option in config. Expected dictionary but got {type(ssh)}.")

        hostname = ssh.get("host", DEFAULT_HOSTNAME)

        if "user" not in ssh:
            error_and_exit('"user" not found in SSH config.')
        user = ssh["user"]

        if "identityfile" not in ssh:
            error_and_exit('"identityfile" not found in SSH config')
        identityfile = ssh["identityfile"]

        return cls(hostname=hostname, identityfile=identityfile, user=user)


@dataclasses.dataclass
class SubmitConfig:
    branch: str | None
    commands: list[str]
    cores: int
    feature: list[str] | None
    error: str | None
    gpus: int | None
    hosts: int
    memory: Memory
    model: str | None
    name: str
    output: str | None
    queue: str
    preamble: list[str]
    split_every: Time
    start_after: str | None
    sync: bool
    walltime: Time

    @classmethod
    def defaults(cls):
        return {
            "branch": ACTIVE_BRANCH_KEY,
            "commands": [],
            "cores": 4,
            "feature": None,
            "error": None,
            "gpus": None,
            "hosts": 1,
            "memory": "5GB",
            "model": None,
            "name": "NONAME",
            "output": None,
            "queue": "hpc",
            "preamble": [],
            "split_every": "1d",
            "start_after": None,
            "sync": True,
            "walltime": "1d",
        }

    @classmethod
    def load(cls, config: dict, project_root: Path):
        if "submit" not in config:
            return cls.defaults()

        submit = config["submit"]

        if not isinstance(submit, dict):
            error_and_exit(f"Invalid type for submit option in config. Expected dictionary but got {type(submit)}.")

        submit = {key.replace("-", "_"): value for key, value in submit.items()}
        for key in submit.keys():
            if key not in cls.__annotations__:
                error_and_exit(f"Unknown option in submit config: {key}")

        output = {**cls.defaults(), **submit}

        if output["branch"] == ACTIVE_BRANCH_KEY:
            with Repo(project_root) as repo:
                output["branch"] = repo.active_branch.name

        return output

    def to_dict(self):
        return {
            "branch": self.branch,
            "commands": self.commands,
            "cores": self.cores,
            "feature": self.feature,
            "error": self.error,
            "gpus": self.gpus,
            "hosts": self.hosts,
            "memory": str(self.memory),
            "model": self.model,
            "name": self.name,
            "output": self.output,
            "queue": self.queue,
            "preamble": self.preamble,
            "split_every": str(self.split_every),
            "start_after": self.start_after,
            "sync": self.sync,
            "walltime": str(self.walltime),
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            branch=data["branch"],
            commands=data["commands"],
            cores=data["cores"],
            feature=data["feature"],
            error=data["error"],
            gpus=data["gpus"],
            hosts=data["hosts"],
            memory=Memory.parse(data["memory"]),
            model=data["model"],
            name=data["name"],
            output=data["output"],
            queue=data["queue"],
            preamble=data["preamble"],
            split_every=Time.parse(data["split_every"]),
            start_after=data["start_after"],
            sync=data.get("sync", True),
            walltime=Time.parse(data["walltime"]),
        )


@dataclasses.dataclass
class CLIConfig:
    history_path: Path
    install: InstallConfig | None
    project_root: Path
    remote_path: str
    ssh: SSHConfig | None
    submit: SubmitConfig | None

    @classmethod
    def load(cls):
        project_root = cls.get_project_root()

        git_path = project_root / ".git"
        if not git_path.exists():
            error_and_exit(f"Could not find git repository at '{git_path}'.")

        path = project_root / CONFIG_FILENAME

        try:
            config = json.loads(path.read_text())
        except json.JSONDecodeError as e:
            error_and_exit(f"Error while parsing config file at '{path}':\n{e}")

        if not isinstance(config, dict):
            error_and_exit(f"Invalid type for config. Expected dictionary but got {type(config)}.")

        install = InstallConfig.load(config)

        history_path = cls.load_history_path(config, project_root)

        remote_path = cls.load_remote_path(config, project_root)
        ssh = SSHConfig.load(config)

        submit = SubmitConfig.load(config, project_root)

        return cls(
            history_path=history_path,
            install=install,
            project_root=project_root,
            remote_path=remote_path,
            ssh=ssh,
            submit=submit,
        )

    @classmethod
    def get_project_root(cls) -> Path:
        """Assume that config file exist in the project root and use that to get the project root."""
        root = Path("/")
        current_path = Path.cwd()
        while current_path != root:
            if (current_path / CONFIG_FILENAME).exists():
                return current_path
            current_path = current_path.parent

        if (root / CONFIG_FILENAME).exists():
            return root

        error_and_exit(
            f"Could not find project root. Make sure that '{CONFIG_FILENAME}' exists in the root of the project."
        )

    @classmethod
    def load_history_path(cls, config: dict, project_root: Path) -> Path:
        if "history_path" in config:
            history_path = config["history_path"]
            if not isinstance(history_path, str):
                error_and_exit(
                    f"Invalid type for history_path option in config. Expected string but got {type(history_path)}."
                )
            return Path(history_path)
        return project_root / HISTORY_FILENAME

    @classmethod
    def load_remote_path(cls, config: dict, project_root: Path) -> str:
        if "remote_path" in config:
            return config["remote_path"]

        name = project_root.name
        hash = sha256(str(project_root).encode()).hexdigest()[:8]
        return f"~/{name}-{hash}"

    def check_ssh(self, msg: str = "SSH configuration is required for this command."):
        if self.ssh is None:
            error_and_exit(msg)


cli_config = CLIConfig.load()
