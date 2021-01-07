import os


def set_env_var(key: str, value: str, delimiter: str='~'):
    """
    Set the GitHub env variable of 'key' to 'value' using
    the method specified here:
    https://docs.github.com/en/free-pro-team@latest/actions/reference/workflow-commands-for-github-actions#setting-an-environment-variable

    Note: This assumes that we are on a Windows machine.
    :param: key, the name of the env variable.
    :param: value, the value of the env variable.
    :param: delimiter, the delimiter that you want to use
    to write to the file. Only applicable if the 'value' contains
    '\n' character aka a multiline string.
    """
    print('echo "{key}={value}" >> %GITHUB_ENV%')

    if "\n" in value:
        os.system(f'echo "{key}<<{delimiter}" >> %GITHUB_ENV%')
        os.system(f'echo {value} >> %GITHUB_ENV%')
        os.system(f'echo "{delimiter}" >> %GITHUB_ENV%')
    else:
        os.system(f'echo "{key}={value}" >> %GITHUB_ENV%')