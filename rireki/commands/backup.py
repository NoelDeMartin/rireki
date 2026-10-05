import click
from click.exceptions import Exit

from rireki.core.projects_manager import ProjectsManager
from rireki.utils.log_helpers import enable_timestamps, log


@click.command()
@click.argument('project', required=False)
@click.option(
    '--force',
    is_flag=True,
    help='Perform backups regardless of project being up to date or not',
)
@click.option(
    '--timestamps',
    is_flag=True,
    help='Include timestamps in logs',
)
def backup(project=None, force=False, timestamps=False):
    """Perform pending backups"""

    if timestamps:
        enable_timestamps()

    if project:
        name = project
        project = ProjectsManager.get_project_by_name(name)

        if not project:
            raise click.ClickException(f'Project with name "{name}" is not installed!')

        projects = [project]
    else:
        projects = ProjectsManager.get_projects()

    if not projects:
        log('No projects installed!')
        return

    if not _process_backups(projects, force):
        raise Exit(1)


def _process_backups(projects, force):
    success = True
    for project in projects:
        if not _process_backup(project, force):
            success = False

    if success:
        log('Done!')

    return success


def _process_backup(project, force):
    if not force and not project.has_pending_backups():
        log(f'Project "{project.name}" does not have any pending backups')
        return True

    log(f'Backing up {project.name}...')

    try:
        project.perform_backup()
        return True
    except Exception as e:  # noqa: BLE001
        error_message = click.style(f'Error: {e}', fg='red')

        click.echo(error_message, err=True)
        return False
