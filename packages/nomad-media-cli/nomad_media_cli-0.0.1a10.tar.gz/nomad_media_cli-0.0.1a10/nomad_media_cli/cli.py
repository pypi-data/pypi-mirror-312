import click

import os
from platformdirs import user_config_dir

from nomad_media_cli.commands.init import init
from nomad_media_cli.commands.list_assets import list_assets
from nomad_media_cli.commands.list_buckets import list_buckets
from nomad_media_cli.commands.list_config_path import list_config_path
from nomad_media_cli.commands.login import login
from nomad_media_cli.commands.set_bucket import set_bucket
from nomad_media_cli.commands.update_config import update_config

# Set the configuration directory and path
CONFIG_DIR = user_config_dir("nomad_media_cli")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

@click.group()
@click.option("--config-path", default=CONFIG_PATH, help="Path to the configuration file (optional)")
@click.pass_context
def cli(ctx, config_path):
    """Nomad Media CLI"""
    ctx.ensure_object(dict)
    ctx.obj["config_path"] = config_path    
    
cli.add_command(init)
cli.add_command(login)
cli.add_command(list_assets)
cli.add_command(list_buckets)
cli.add_command(list_config_path)
cli.add_command(set_bucket)
cli.add_command(update_config)

if __name__ == "__main__":
    cli(obj={})
