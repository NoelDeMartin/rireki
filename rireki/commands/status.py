import click

from rireki.core.projects_manager import get_projects
from rireki.utils.output import display_table


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
    return (
        project.name,
        project.driver.name,
        {
            'text': 'backup-pending',
            'color': 'red',
        },
    )
