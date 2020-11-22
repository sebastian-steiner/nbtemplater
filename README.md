# nbtemplater
A utility to convert a template [Jupyter](https://jupyter.org/) notebook into separate
solution and task versions based on simple directives.

```bash
# this converts template.ipynb to template_solution.ipynb and template_task.ipynb
nbtemplater template.ipynb
```

In addition to being able to convert a single file, `nbtemplater.py` can also be
used to (recursively) convert all notebook files in a given directory like:

```bash
# this converts all .ipynb files in notebook-folders/
nbtemplater notebook-folders/

# this recursively converts all .ipynb files in notebook-folders/
# so e.g. notebook-folders/bar/template.ipynb
nbtemplater -r notebook-folders/
```

## Installation
For easy installation, you can install `nbtemplater` directly
[here from PyPI](https://pypi.org/project/nbtemplater). So you can
install it using:
```bash
pip install nbtemplater
```

### Manual installation
If you prefer not to install from `pip` you can get the source code at
[the GitHub repository](https://github.com/sebastian-steiner/nbtemplater), where
you can also find a `requirements.txt` file, listing all dependencies.

## Sample conversion
If the following text is included in any part or cell of the template notebook, it is
split up into the appropriate versions:

### Template
```markdown
# This is some basic content
%%IF_SOL%%
any text before the next directive is
only going to be visible in the solution
version of this notebook
%%ELSE%%
this **optional** section is going to be copied
into the task version
%%END%%
```

### Solution
```markdown
# This is some basic content
any text before the next directive is
only going to be visible in the solution
version of this notebook
```

### Task
```markdown
# This is some basic content
this **optional** section is going to be copied
into the task version
```

## Help text
```
Usage: nbtemplater [OPTIONS] [PATHS]...

  Convert PATHS.

  PATHS is a list of directories or notebook files to convert to solution
  and task files.

Options:
  -r, --recurse           Whether to recursively go through folders  [default:
                          False]

  -f, --force             Whether to overwrite an already existing file
                          [default: False]

  -q, --quiet             Disable output during conversion  [default: False]
  -p, --pattern TEXT      The pattern to search for in folders  [default:
                          *.ipynb]

  --solution-suffix TEXT  The file suffix to be used for the generated
                          solution file  [default: solution]

  --task-suffix TEXT      The file suffix to be used for the generated task
                          file  [default: student]

  --start-solution TEXT   The start of a solution block  [default: %%IF_SOL%%]
  --else-task TEXT        The start of the optional task block  [default:
                          %%ELSE%%]

  --end-if TEXT           The end of a solution/task if block  [default:
                          %%FI%%]

  -h, --help              Show this message and exit.
```