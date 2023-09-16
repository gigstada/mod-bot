import re

def get_file_contents_string(src_paths):
    file_contents = []
    for src_path in src_paths:
        start_line, end_line = None, None
        
        # Check if the src_path has slice notation
        has_slice = re.search(r'(.*)\[(\d+):(\d+)\]$', src_path)
        if has_slice:
            groups = has_slice.groups()
            src_path = groups[0]
            try:
                start_line = int(groups[1])
                end_line = int(groups[2])
            except ValueError:
                start_line, end_line = None, None
            is_partial = True
        else:
            is_partial = False

        with open(src_path, 'r') as file:
            contents = file.readlines()
            if is_partial:
                contents = ''.join(contents[start_line - 1:end_line - 1])
            else:
                contents = ''.join(contents)

        file_contents.append(
            '<<< {} {} OF {} FILE >>>\n{}'.format(src_path, 'START', 'FULL' if not is_partial else 'FILE FRAGMENT', contents))
        file_contents.append(
            '<<< {} END OF {} FILE >>>'.format(src_path, 'FULL' if not is_partial else 'FILE FRAGMENT'))

    return '\n'.join(file_contents)