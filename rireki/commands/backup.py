import click

from rireki.core.projects_manager import ProjectsManager

@click.command()
@click.argument('project', required=False)
def backup(project):
    """Perform pending backups"""

    if project:
        projects = [ProjectsManager.get_project_by_name(project)]
    else:
        projects = ProjectsManager.get_projects()

    if not projects:
        click.echo('No projects installed!')
        return

    __process_backups(projects)


def __process_backups(projects):
    for project in projects:
        __process_backup(project)

    click.echo('Done!')


def __process_backup(project):
    if not project.has_pending_backups():
        click.echo('Project "%s" does not have any pending backups' % project.name)
        return

    click.echo('Backing up %s...' % project.name)
    project.perform_backup()
