import tasks  # noqa

from fabric.api import local, task


@task(default=True)
def list_tasks():
    """ List out all the tasks available. """
    local('fab --list')
