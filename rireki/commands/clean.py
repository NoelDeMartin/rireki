import click
from click.exceptions import Exit

from rireki.core.projects_manager import ProjectsManager
from rireki.utils.log_helpers import enable_timestamps, log


@click.command()
@click.argument('project', required=False)
@click.option(
    '--timestamps',
    is_flag=True,
    help='Include timestamps in logs',
)
def clean(project=None, timestamps=False):
    """Clean stale backups"""

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

    if not _process_cleanups(projects):
        raise Exit(1)


def _process_cleanups(projects):
    success = True
    for project in projects:
        if not _process_cleanup(project):
            success = False

    if success:
        log('Done!')

    return success


def _process_cleanup(project):
    stale_backups = project.get_stale_backups()

    if not stale_backups:
        log(f'Project "{project.name}" does not have any stale backups')
        return True

    log(f'Cleaning up {project.name}...')

    success = True
    for stale_backup in stale_backups:
        try:
            log(f'Removing {stale_backup.name}...')

            project.remove_backup(stale_backup)
        except Exception as e:  # noqa: BLE001
            error_message = click.style(f'Error: {e}', fg='red')

            click.echo(error_message, err=True)
            success = False

    return success
