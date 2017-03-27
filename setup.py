from setuptools import setup

url = ""
version = "0.1.0"
readme = open('README.rst').read()
dsc = "Python tools to manage users/groups/quotas/namespaces in an irods zone",

setup(name="jicirodsmanager",
      packages=["jicirodsmanager"],
      version=version,
      description=dsc,
      long_description=readme,
      include_package_data=True,
      author="Tjelvar Olsson",
      author_email="tjelvar.olsson@jic.ac.uk",
      url=url,
      install_requires=[],
      download_url="{}/tarball/{}".format(url, version),
      license="MIT")
