import click

from rireki.core.projects_manager import ProjectsManager


@click.command()
@click.argument('project', required=False)
def clean(project=None):
    """Clean stale backups"""

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

    for project in projects:
        __process_cleanup(project)

    click.echo('Done!')


def __process_cleanup(project):
    stale_backups = project.get_stale_backups()

    if not stale_backups:
        click.echo('Project "%s" does not have any stale backups' % project.name)
        return

    click.echo('Cleaning up %s...' % project.name)

    try:
        for stale_backup in stale_backups:
            click.echo('Removing %s...' % stale_backup.name)

            project.remove_backup(stale_backup)
    except Exception as e:
        error_message = click.style('Error: %s' % e, fg='red')

        click.echo(error_message, err=True)
