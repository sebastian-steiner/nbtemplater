import json
import os
from .line_status import LineStatus
import copy
import colorama
import fnmatch

NOTEBOOK_ENDING = '.ipynb'


class NotebookConverter:
    def __init__(self, recurse, force, quiet, pattern, solution_suffix, task_suffix, start_solution, else_task, end_if):
        self.recurse = recurse
        self.force = force
        self.quiet = quiet
        self.pattern = pattern
        self.solution_suffix = solution_suffix
        self.task_suffix = task_suffix
        self.start_solution = start_solution
        self.else_task = else_task
        self.end_if = end_if
        self.file_cnt = 0
        self.success_file_cnt = 0
        self.failed_files = set()

    def convert(self, path):
        if os.path.isdir(path):
            self.convert_folder(path)
        else:
            self.convert_file(path)

    def convert_folder(self, path):
        self.log('Converting directory: ' + colorama.Fore.GREEN + path + colorama.Style.RESET_ALL)
        if not self.recurse:
            for file in fnmatch.filter(os.listdir(path), self.pattern):
                self.convert_file(os.path.join(path, file))
        else:
            for root, dirs, files in os.walk(path):
                for file in fnmatch.filter(files, self.pattern):
                    self.convert_file(os.path.join(root, file))

    def convert_file(self, filename):
        self.log('Converting file: ' + colorama.Fore.GREEN + filename + colorama.Style.RESET_ALL)
        # get json from file
        try:
            with open(filename, 'r') as file:
                data = file.read()
        except Exception as e:
            self.failed_files.add(filename)
            self.log('\tCould not open file: ' + colorama.Fore.RED + filename + colorama.Style.RESET_ALL)
            return
        has_converted_part, task_json, solution_json = self.convert_json(json.loads(data))

        if has_converted_part:
            self.write_json(task_json, self.__task_filename(filename))
            self.write_json(solution_json, self.__solution_filename(filename))
        else:
            self.log('\tNo directives found, not converting')

    def convert_json(self, data_json):
        cells = data_json['cells']

        has_converted_part = False

        solution_cells = []
        task_cells = []

        # iterate through all cells in the notebook
        for cell in cells:
            task_lines = []
            solution_lines = []
            line_status = LineStatus.TEXT
            for line in cell['source']:
                if line_status is LineStatus.TEXT:
                    if self.start_solution in line:
                        line_status = LineStatus.SOLUTION
                    else:
                        task_lines.append(line)
                        solution_lines.append(line)
                elif line_status is LineStatus.SOLUTION:
                    if self.else_task in line:
                        line_status = LineStatus.TASK
                    elif self.end_if in line:
                        line_status = LineStatus.TEXT
                    else:
                        has_converted_part = True
                        solution_lines.append(line)
                else:
                    if self.end_if in line:
                        line_status = LineStatus.TEXT
                    else:
                        has_converted_part = True
                        task_lines.append(line)

            # add changed cell to solution/task object
            cell['source'] = task_lines
            task_cells.append(copy.deepcopy(cell))
            cell['source'] = solution_lines
            solution_cells.append(copy.deepcopy(cell))

        # create final objects to be written to disk
        task_json = copy.deepcopy(data_json)
        task_json['cells'] = task_cells
        solution_json = copy.deepcopy(data_json)
        solution_json['cells'] = solution_cells

        return has_converted_part, task_json, solution_json

    def write_json(self, json_data, filename):
        self.file_cnt += 1
        if os.path.exists(filename) and not self.force:
            self.log('\tCould not write to file', filename, ' (file exists)')
            self.log('\tSpecify --force to overwrite existing files')
            self.failed_files.add(filename)
        else:
            try:
                with open(filename, 'w') as file:
                    json.dump(json_data, file)
                self.success_file_cnt += 1
            except Exception as e:
                self.failed_files.add(filename)
                self.log('\tCould not write to file: ' + colorama.Fore.RED + filename + colorama.Style.RESET_ALL)

    def __solution_filename(self, filename):
        return os.path.splitext(filename)[0] + '_' + self.solution_suffix + NOTEBOOK_ENDING

    def __task_filename(self, filename):
        return os.path.splitext(filename)[0] + '_' + self.task_suffix + NOTEBOOK_ENDING

    def print_statistics(self):
        if not self.quiet:
            print('#' * os.get_terminal_size().columns)
        if self.success_file_cnt == self.file_cnt:
            print('Successfully wrote all', self.file_cnt, 'files')
        elif self.success_file_cnt == 0:
            print('Could not convert any files')
        else:
            print('Successfully wrote', self.success_file_cnt, 'out of', self.file_cnt)

        if self.failed_files:
            print('The following files could not be converted:')
            for filename in self.failed_files:
                print('\t' + colorama.Fore.RED + filename + colorama.Style.RESET_ALL)
        if not self.quiet:
            print('#' * os.get_terminal_size().columns)

    def log(self, *args):
        if not self.quiet:
            print(''.join(map(str, args)))

