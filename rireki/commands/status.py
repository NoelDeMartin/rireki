import click

from rireki.core.projects_manager import get_projects
from rireki.utils.output import display_table, format_time
from rireki.utils.time_helpers import now


@click.command()
def status():
    """Show status of installed projects"""

    projects = get_projects()

    print_projects_status(projects)


def print_projects_status(projects):
    if not projects:
        click.echo('No projects installed!')
        return

    display_table(('Name', 'Driver', 'Status'), map(get_project_info, projects))


def get_project_info(project):
    if project.has_pending_backups():
        status = {
            'text': 'backup-pending',
            'color': 'red',
        }
    else:
        status = {
            'text': 'Backed up %s ago' % format_time(now() - project.get_last_backup().time),
            'color': 'green',
        }

    return (
        project.name,
        project.driver.name,
        status,
    )
