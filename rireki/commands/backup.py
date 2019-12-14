import click

from rireki.core.projects_manager import get_projects, get_project_by_name

@click.command()
@click.argument('project', required=False)
def backup(project):
    """Perform pending backups"""

    if project:
        projects = [get_project_by_name(project)]
    else:
        projects = get_projects()

    if not projects:
        click.echo('No projects installed!')
        return

    process_backups(projects)


def process_backups(projects):
    for project in projects:
        process_backup(project)


def process_backup(project):
    if not project.has_pending_backup():
        click.echo('Project "%s" has not pending backups' % project.name)
        return

    click.echo('Backing up %s...' % project.name)
    project.backup()
