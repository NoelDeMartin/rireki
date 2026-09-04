import click
from click.exceptions import Exit

from rireki.core.projects_manager import ProjectsManager
from rireki.utils.log_helpers import log, enable_timestamps


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
            raise click.ClickException('Project with name "%s" is not installed!' % name)

        projects = [project]
    else:
        projects = ProjectsManager.get_projects()

    if not projects:
        log('No projects installed!')
        return

    if not __process_cleanups(projects):
        raise Exit(1)


def __process_cleanups(projects):
    success = True
    for project in projects:
        if not __process_cleanup(project):
            success = False

    if success:
        log('Done!')

    return success


def __process_cleanup(project):
    stale_backups = project.get_stale_backups()

    if not stale_backups:
        log('Project "%s" does not have any stale backups' % project.name)
        return True

    log('Cleaning up %s...' % project.name)

    success = True
    for stale_backup in stale_backups:
        try:
            log('Removing %s...' % stale_backup.name)

            project.remove_backup(stale_backup)
        except Exception as e:
            error_message = click.style('Error: %s' % e, fg='red')

            click.echo(error_message, err=True)
            success = False

    return success
