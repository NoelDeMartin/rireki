import click

from rireki.core.projects_manager import ProjectsManager
from rireki.utils.array_helpers import array_map
from rireki.utils.output import display_table, format_time
from rireki.utils.time_helpers import now


@click.command()
def status():
    """Show status of installed projects"""

    projects = ProjectsManager.get_projects()

    __display_projects_status(projects)


def __display_projects_status(projects):
    if not projects:
        click.echo('No projects installed!')
        return

    display_table(('Name', 'Driver', 'Status'), array_map(__get_project_info, projects))


def __get_project_info(project):
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
