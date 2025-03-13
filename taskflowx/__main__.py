#  ████████╗ █████╗ ███████╗██╗  ███████╗██╗      ██████╗ ██╗  ██╗
#  ╚══██╔══╝██╔══██╗██╔════╝██║  ██╔════╝██║     ██╔═══██╗██║  ██║
#     ██║   ███████║███████╗██║  █████╗  ██║     ██║   ██║███████║
#     ██║   ██╔══██║╚════██║██║  ██╔══╝  ██║     ██║   ██║██╔══██║
#     ██║   ██║  ██║███████║██║  ██║     ███████╗╚██████╔╝██║  ██║
#     ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝
#
#  TaskFlowX - A lightweight and modular workflow automation engine
#
#  This code is licensed under the GNU General Public License (GPL).
#  You are free to modify and distribute it under the terms of the GPL.
#
#  (c) 2025 TaskFlowX Nils Schaetti <n.schaetti@gmail.com>


# Imports
import click
from rich.console import Console
from rich.traceback import install
from taskflowx.config import Config
from taskflowx.logger import logger
from taskflowx.runner import run


# Backtrack with Rick
console = Console()
install()


# Main command
@click.command()
@click.option("--config", help="Path to the configuration file.", required=True)
@click.option("--triggers", help="Directory containing trigger modules.")
@click.option("--workflows", help="Directory containing workflow modules.", required=True)
def main(
        config: str,
        triggers: str,
        workflows: str
):
    """
    Main function for the TaskFlowX command line interface.

    Args:
        config (str): Path to the configuration file.
        triggers (str): Directory containing trigger modules.
        workflows (str): Directory containing workflow modules.
    """
    try:
        config_instance = Config(config)
        run(
            config=config_instance,
            triggers_path=triggers,
            workflows_path=workflows
        )
    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] Configuration file '{config}' not found.", style="bold red")
        logger.error(f"Configuration file '{config}' not found.")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}", style="bold red")
        logger.exception("Critical error encountered.", exc_info=e)
    # end try
# end main


if __name__ == "__main__":
    main()
# end if
