import click
import sys

from rireki.core.projects_manager import ProjectsManager
from rireki.utils.log_helpers import log, enable_timestamps


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
            log('Project with name "%s" is not installed!' % name)
            sys.exit(1)

        projects = [project]
    else:
        projects = ProjectsManager.get_projects()

    if not projects:
        log('No projects installed!')
        return

    if not __process_backups(projects, force):
        sys.exit(1)


def __process_backups(projects, force):
    success = True
    for project in projects:
        if not __process_backup(project, force):
            success = False

    if success:
        log('Done!')

    return success


def __process_backup(project, force):
    if not force and not project.has_pending_backups():
        log('Project "%s" does not have any pending backups' % project.name)
        return True

    log('Backing up %s...' % project.name)

    try:
        project.perform_backup()
        return True
    except Exception as e:
        error_message = click.style('Error: %s' % e, fg='red')

        click.echo(error_message, err=True)
        return False
