def system(*args):
    from subprocess import Popen, PIPE
    p = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    if err:
        raise Exception, err
    return out

def get_revision():
    from os import popen3
    import re, os

    try:
        project_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../../")
        m = re.match(':?(\d*).*[MS]?$', system('svnversion', project_path))
        return m.group(1)
    except:
        return 'Versioning Unavailable'

REVISION = get_revision()