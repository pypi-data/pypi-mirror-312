import sys
import os
from setuptools import setup
import sysconfig
from pathlib import Path

# Normally packages don't have to do this - the dist_conda command should be
# automatically available. But since we're installing it, it isn't there yet!
from ci_helper.ci_distinfo import ci_distinfo
CMDCLASS = {'ci_distinfo': ci_distinfo}

VERSION_SCHEME = {
    "version_scheme": os.getenv("SCM_VERSION_SCHEME", "guess-next-dev"),
    "local_scheme": os.getenv("SCM_LOCAL_SCHEME", "node-and-date"),
}

SITE_PACKAGES = sysconfig.get_path('purelib')

# Add the dist_conda command to the distlib vendored in setuptools:
setuptools_distutils = Path(SITE_PACKAGES) / 'setuptools' / '_distutils' / 'command'
DATA_FILES = [
    (str(setuptools_distutils.relative_to(sys.prefix)), ["ci_distinfo.py"]),
]
setup(
    use_scm_version=VERSION_SCHEME,
    cmdclass=CMDCLASS,
    data_files=DATA_FILES,
)

