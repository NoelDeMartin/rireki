import click

from rireki.core.projects_manager import ProjectsManager
from rireki.utils.array_helpers import array_map
from rireki.utils.output import display_table, format_time
from rireki.utils.time_helpers import now


@click.command()
@click.argument('project', required=False)
def status(project=None):
    """Show status of installed projects"""

    if project:
        name = project
        project = ProjectsManager.get_project_by_name(name)

        if not project:
            click.echo('Project with name "%s" is not installed!' % name)
            return

        __display_project_status(project)
    else:
        projects = ProjectsManager.get_projects()

        __display_projects_status(projects)


def __display_project_status(project):
    if project.has_pending_backups():
        click.echo(click.style('Project needs to be backed up', fg='red'))
    else:
        click.echo(
            click.style('Project ', fg='green') +
            click.style(project.name, bold=True, fg='green') +
            click.style(' is up to date', fg='green'),
        )

    backups = project.get_backups()
    stale_backups = project.get_stale_backups(backups)

    click.echo('')
    click.echo('All backups (%s total, %s stale):' % (len(backups), len(stale_backups)))

    for backup in backups:
        click.echo(
            '- %s ago%s' % (
                format_time(now() - backup.time, 'interval'),
                ' (stale)' if backup in stale_backups else '',
            ),
        )


def __display_projects_status(projects):
    if not projects:
        click.echo('No projects installed!')
        return

    display_table(
        ('Name', 'Driver', 'Store', 'Status', 'Stale Backups'),
        array_map(__get_project_info, projects),
    )


def __get_project_info(project):
    if project.has_pending_backups():
        status = {
            'text': 'backup-pending',
            'color': 'red',
        }
    else:
        last_backup_interval = now() - project.get_last_backup().time
        status = {
            'text': 'Backed up %s ago' % format_time(last_backup_interval, 'interval'),
            'color': 'green',
        }

    stale_backups = len(project.get_stale_backups())
    stale_backups_status = {
        'text': str(stale_backups),
        'color': 'red' if stale_backups > 0 else 'green',
    }

    return (
        project.name,
        project.driver.name,
        project.store.name,
        status,
        stale_backups_status,
    )
