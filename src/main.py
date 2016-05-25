from pymlconf import *
import subprocess


__builtin_config = '''
before_install:
  - sudo apt-get update
  - sudo apt-get install python$( python -c 'import sys; print("%d.%d" % sys.version_info[:2])' )-dev || true
  - pip install -r requirement.txt

install:
  - sudo pip install requests

script:
  - coverage run --source khayyam $(which nosetests)

after_success:
  - coveralls

'''


def popen(executable, verbosity, args, timeout=None, **kwargs):
    sb = subprocess.Popen(
        '%s -v %s %s' % (executable, verbosity, args),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        **kwargs
    )
    stdout, stderr = sb.communicate(timeout=timeout)

    return stdout, stderr, sb.returncode


def init():
    config = ConfigManager(__builtin_config)
    commands = [config.before_install, config.install, config.script, config.after_success]
    for item in commands:
        print(popen(item, True, None))


if __name__ == '__main__':
    init()
