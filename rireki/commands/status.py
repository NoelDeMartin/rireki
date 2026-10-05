import click

from rireki.core.projects_manager import ProjectsManager
from rireki.utils.array_helpers import array_map
from rireki.utils.log_helpers import enable_timestamps, log
from rireki.utils.output import display_table, format_time
from rireki.utils.time_helpers import now


@click.command()
@click.argument('project', required=False)
@click.option(
    '--timestamps',
    is_flag=True,
    help='Include timestamps in logs',
)
def status(project=None, timestamps=False):
    """Show status of installed projects"""

    if timestamps:
        enable_timestamps()

    if project:
        name = project
        project = ProjectsManager.get_project_by_name(name)

        if not project:
            raise click.ClickException(f'Project with name "{name}" is not installed!')

        _display_project_status(project)
    else:
        projects = ProjectsManager.get_projects()

        _display_projects_status(projects)


def _display_project_status(project):
    if project.has_pending_backups():
        log(click.style('Project needs to be backed up', fg='red'))
    else:
        log(
            click.style('Project ', fg='green') +
            click.style(project.name, bold=True, fg='green') +
            click.style(' is up to date', fg='green'),
        )

    backups = project.get_backups()
    stale_backups = project.get_stale_backups(backups)

    click.echo('')
    log(f'All backups ({len(backups)} total, {len(stale_backups)} stale):')

    for backup in backups:
        interval = format_time(now() - backup.time, 'interval')
        stale_label = ' (stale)' if backup in stale_backups else ''

        log(f'- {interval} ago{stale_label}')


def _display_projects_status(projects):
    if not projects:
        log('No projects installed!')
        return

    display_table(
        ('Name', 'Driver', 'Store', 'Status', 'Stale Backups'),
        array_map(_get_project_info, projects),
    )


def _get_project_info(project):
    if project.has_pending_backups():
        status = {
            'text': 'backup-pending',
            'color': 'red',
        }
    else:
        last_backup_interval = now() - project.get_last_backup().time
        status = {
            'text': f"Backed up {format_time(last_backup_interval, 'interval')} ago",
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
