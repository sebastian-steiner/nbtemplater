import click
from .functions import NotebookConverter

# show the command help on both short and long version
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


# always print the default value for every option
def click_option(*args, **kwargs):
    if 'show_default' not in kwargs:
        kwargs.update({'show_default': True})
    return click.option(*args, **kwargs)


@click.command(context_settings=CONTEXT_SETTINGS)
@click_option('-r', '--recurse', default=False, is_flag=True, help='Whether to recursively go through folders')
@click_option('-f', '--force', default=False, is_flag=True, help='Whether to overwrite an already existing file')
@click_option('-q', '--quiet', default=False, is_flag=True, help='Disable output during conversion')
@click_option('-p', '--pattern', default='*.ipynb', help='The pattern to search for in folders')
@click_option('--solution-suffix', default='solution',
              help='The file suffix to be used for the generated solution file')
@click_option('--task-suffix', default='student',
              help='The file suffix to be used for the generated task file')
@click_option('--start-solution', default='%%IF_SOL%%', help='The start of a solution block')
@click_option('--else-task', default='%%ELSE%%', help='The start of the optional task block')
@click_option('--end-if', default='%%END%%', help='The end of a solution/task if block')
@click.argument('paths', nargs=-1, type=click.Path(exists=True))
def run_cmd(recurse, force, quiet, pattern, solution_suffix, task_suffix, start_solution, else_task, end_if, paths):
    """Convert PATHS.

    PATHS is a list of directories or notebook files to convert to solution and task files.
    """
    conv = NotebookConverter(recurse,
                             force,
                             quiet,
                             pattern,
                             solution_suffix,
                             task_suffix,
                             start_solution,
                             else_task,
                             end_if)
    if not paths:
        print("Expecting at least one file or path specified:")
        with click.Context(run_cmd) as ctx:
            click.echo(run_cmd.get_help(ctx))
        exit(1)
    for path in paths:
        conv.convert(path)
    conv.print_statistics()


if __name__ == '__main__':
    run_cmd()
