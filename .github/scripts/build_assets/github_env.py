import os
import platform


def set_env_var(key: str, value: str, delimiter: str='~'):
    """
    Set the GitHub env variable of 'key' to 'value' using
    the method specified here:
    https://docs.github.com/en/free-pro-team@latest/actions/reference/workflow-commands-for-github-actions#setting-an-environment-variable
    Support both Windows and Ubuntu machines provided by GitHub Actions.

    :param: key, the name of the env variable.
    :param: value, the value of the env variable.
    :param: delimiter, the delimiter that you want to use
    to write to the file. Only applicable if the 'value' contains
    '\n' character aka a multiline string.
    """
    if platform.system() == "Windows":
        if "\n" in value:
            os.system(f'echo "{key}<<{delimiter}" >> %GITHUB_ENV%')
            os.system(f'echo "{value}" >> %GITHUB_ENV%')
            os.system(f'echo "{delimiter}" >> %GITHUB_ENV%')
        else:
            os.system(f'echo "{key}={value}" >> %GITHUB_ENV%')
    elif platform.system() == "Linux":
        if "\n" in value:
            os.system(f'echo "{key}<<{delimiter}" >> $GITHUB_ENV')
            os.system(f'echo "{value}" >> $GITHUB_ENV')
            os.system(f'echo "{delimiter}" >> $GITHUB_ENV')
        else:
            os.system(f'echo "{key}={value}" >> $GITHUB_ENV')
    else:
        raise Exception("This function doesn't support this platform: " + platform.system())