import click

from rireki.core.projects_manager import ProjectsManager


@click.command()
@click.argument('project', required=False)
@click.option(
    '--force',
    is_flag=True,
    help='Perform backups regardless of project being up to date or not',
)
def backup(project=None, force=False):
    """Perform pending backups"""

    if project:
        name = project
        project = ProjectsManager.get_project_by_name(name)

        if not project:
            click.echo('Project with name "%s" is not installed!' % name)
            return

        projects = [project]
    else:
        projects = ProjectsManager.get_projects()

    if not projects:
        click.echo('No projects installed!')
        return

    __process_backups(projects, force)


def __process_backups(projects, force):
    for project in projects:
        __process_backup(project, force)

    click.echo('Done!')


def __process_backup(project, force):
    if not force and not project.has_pending_backups():
        click.echo('Project "%s" does not have any pending backups' % project.name)
        return

    click.echo('Backing up %s...' % project.name)

    try:
        project.perform_backup()
    except Exception as e:
        error_message = click.style('Error: %s' % e.message, fg='red')

        click.echo(error_message, err=True)
