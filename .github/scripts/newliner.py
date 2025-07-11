import json, re
from os import system
from sys import argv

PR_PATHS = 'pr-files.json'

# Search for added and modified files without a newline at the end.
file_paths = json.load(open(f'./{PR_PATHS}'))
mod_files = []
for file_path in file_paths:
  file = open(file_path).readlines()
  if len(file) > 0 and not re.match(r'.*\n', file[-1]):
    file.append('\n')
    open(file_path, 'w').write(''.join(file))
    mod_files.append(file_path)

# Remove PR_PATHS
system(f'rm -rf {PR_PATHS}')

# Create the commit message.
if len(mod_files) > 0:
  mod_files = '\\n'.join([
    'Optimized icons' if argv[1] == 'on' else 'Add newline at the end of files',
    *map(lambda e: f'- {e}', mod_files)
  ])

  [
    system(e) for e in [
      'echo "commit_msg<<EOF" >> $GITHUB_ENV',
      f'echo "{mod_files}" >> $GITHUB_ENV',
      'echo "EOF" >> $GITHUB_ENV'
    ]
  ]
