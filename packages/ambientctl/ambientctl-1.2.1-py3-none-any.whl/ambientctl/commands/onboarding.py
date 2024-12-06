import subprocess
import time
from typing import Dict, Optional

import click

from ambientctl import config
from ambientctl.commands import auth, daemon, health


def run_onboarding():
    # welcome message
    click.secho(
        "Welcome to the Ambient Edge Server onboarding process.",
        fg="white",
        bold=True,
        reverse=True,
    )

    # check all packages are installed
    check_packages()

    # install, restart, and verify daemon
    env_vars = ""
    if config.settings.ambient_dev_mode:
        env_vars = set_server_env_vars()
    install_and_verify_daemon(env_vars=env_vars)

    # authorize with backend
    authorize_backend()

    # ensure server is authorized
    ensure_authorized()

    # run health check-in
    run_health_check()

    # done
    done()


def set_server_env_vars() -> str:
    click.secho("Warning: You are running in development mode.", fg="yellow", bold=True)
    env_vars = click.prompt(
        text="Enter environment variables to pass to the server. \
E.g., 'VAR1=VALUE1,VAR2=VALUE2'",
        default="BACKEND_API_URL=https://api.ambientlabsdev.io,\
EVENT_BUS_API=https://events.ambientlabsdev.io,\
CONNECTION_SERVICE_URL=wss://sockets.ambientlabsdev.io,\
AMBIENT_LOG_LEVEL=DEBUG",
    )
    return env_vars


def check_packages():
    click.echo("Checking for required packages...")
    # run pip list
    result = subprocess.run(["pip", "list"], capture_output=True, text=True)
    output = result.stdout

    # parse output
    lines = output.split("\n")
    if len(lines) < 2:
        click.secho(
            "Unexpected behavior: No packages installed. Please check your \
python environment configuration",
            fg="red",
            bold=True,
        )
        raise click.Abort()

    # ensure all required packages are installed
    expected_version = config.settings.version
    expected_packages = [
        "ambient-backend-api-client",
        "ambient-base-plugin",
        "ambient-client-common",
        "ambient-docker-swarm-plugin",
        "ambient-edge-server",
        "ambient-event-bus-client",
        "ambient-run-command-plugin",
    ]
    package_report = {package: {} for package in expected_packages}
    for line in lines[2:]:
        try:
            package, version = line.split()[:2]
        except ValueError:
            continue
        if package in expected_packages:
            package_report[package] = {
                "version": version,
                "ok": version == expected_version,
            }
    return handle_package_report(package_report, expected_version)


def handle_package_report(package_report: Dict[str, dict], expected_version: str):
    if all([report["ok"] for report in package_report.values()]):
        click.secho("All required packages are installed.", fg="green", bold=True)
        return
    else:
        click.secho(
            "Some required packages are missing or incorrect.", fg="red", bold=True
        )
        for package, report in package_report.items():
            if not report["ok"]:
                message = f"Package {package} is"
                if report.get("version", "") == "":
                    message += " not installed."
                else:
                    message += " not the correct version."
                click.echo(message)
                click.echo(f"   Expected version: {expected_version}")
                click.echo(
                    f"   Installed version: {report.get('version', 'Not installed')}"
                )
        handle_missing_packages(package_report)


def handle_missing_packages(
    package_report: Dict[str, dict],
):
    click.echo("Would you like to install the required packages? [y/n]")
    install = click.getchar(echo=True)
    if install.lower() == "y":
        install_missing_packages(package_report)
    else:
        click.secho(
            "Please install the required packages before continuing.",
            fg="red",
            bold=True,
        )
        raise click.Abort()


def install_missing_packages(package_report: Dict[str, dict]):
    click.echo("Installing required packages...")
    for package, report in package_report.items():
        if not report["ok"]:
            version = config.settings.version
            click.echo(f"Installing {package}={version}...")
            if config.settings.ambient_dev_mode:
                time.sleep(0.5)
                click.echo(f"Successfully installed {package}.")
                continue
            result = subprocess.run(
                ["pip", "install", f"{package}=={version}"], capture_output=True
            )
            if result.returncode != 0:
                click.secho(
                    f"Failed to install {package}. Please install manually.",
                    fg="red",
                    bold=True,
                )
            else:
                click.echo(f"Successfully installed {package}.")
    click.secho("All required packages are installed.", fg="green", bold=True)


def install_daemon(env_vars: Optional[str] = None):
    daemon.install(env_vars=env_vars, silent=True)


def restart_daemon():
    daemon.restart(silent=True)


def verify_daemon():
    daemon.status(silent=True)


def wait_untiL_daemon_is_running():
    daemon.wait_until_service_is_running()


def install_and_verify_daemon(env_vars: Optional[str] = None):
    steps = [
        install_daemon,
        wait_untiL_daemon_is_running,
        verify_daemon,
    ]
    progress_weights = [13, 68, 19]
    with click.progressbar(
        length=100, label="Installing Ambient Edge Server daemon"
    ) as bar:
        for i, step in enumerate(steps):
            # run the first step with env_vars
            if i == 0:
                step(env_vars)
            else:
                step()
            bar.update(progress_weights[i])


def authorize_backend():
    node_id = click.prompt("Enter the node ID", type=int)
    token = click.prompt("Enter the token", type=str, hide_input=True)
    click.echo(f"Authorizing node {node_id} with token [{len(token)} chars] ...")
    daemon.wait_until_service_is_running()
    auth.authorize_node(node_id, token)
    daemon.restart(silent=False)
    daemon.wait_until_service_is_running()
    click.echo("Node authorized.")


def ensure_authorized():
    click.echo("Ensuring node is authorized...")
    auth.check_status()


def run_health_check():
    click.echo("Running health check-in...")
    health.check_in()


def done():
    click.secho("Onboarding complete.", fg="green", bold=True)
