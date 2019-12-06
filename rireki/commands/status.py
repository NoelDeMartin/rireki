import click

from rireki.main import cli
from rireki.lib.projects_manager import get_projects
from rireki.lib.output import display_table

@cli.command()
def status():
    """Show status of installed projects"""

    projects = get_projects()

    print_projects_status(projects)

def print_projects_status(projects):
    if not projects:
        click.echo('No projects installed!')
        return

    display_table(('Name', 'Status'), map(get_project_info, projects))

def get_project_info(project):
    return (
        project.name,
        {
            'text': 'backup-pending',
            'color': 'red',
        },
    )
