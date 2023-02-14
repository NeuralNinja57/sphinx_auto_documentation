import subprocess
import argparse


class SphinxAutoDocument:
    def __init__(self, orchestrator, docs_folder_name):
        self.docs_folder_name = docs_folder_name
        self.orchestrator = orchestrator

        self.installation_timeout = 10
        self.quickstart_timeout = 10
        self.autodoc_timeout = 10
        self.html_timeout = 10

        self.sphinx_install_cmd = 'pip install -U Sphinx'
        self.sphinx_quickstart_cmd = f'sphinx-quickstart {self.docs_folder_name}'
        self.sphinx_autodoc_cmd = f'sphinx-apidoc -o {self.docs_folder_name}/source {self.orchestrator}'
        self.sphinx_make_html_cmd = 'make html'
        self.sphinx_install_theme_cmds = {"sphinx_rtd_theme": "pip install sphinx-rtd-theme"}

    def install_sphinx_and_dependencies(self):
        try:
            popen = subprocess.Popen(self.sphinx_install_cmd,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     shell=True)
            _, error = popen.communicate(timeout=self.installation_timeout)
            if error not in [None, b'']:
                print(f"Error while installing sphinx - {error}")
                return False

            print(f"Sphinx Installation Completed Successfully")
            return True

        except subprocess.TimeoutExpired:
            print(f"Subprocess Timeout: Try increasing the installation_timeout parameter in __init__")
            return False

        except Exception as err:
            print(f"Exception: install_sphinx_and_dependencies: {err}")
            return False

    def install_sphinx_theme(self, theme):
        try:
            popen = subprocess.Popen(self.sphinx_install_theme_cmds[theme],
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     shell=True)
            _, error = popen.communicate(timeout=self.installation_timeout)
            if error not in [None, b'']:
                print(f"Error while installing sphinx theme - {error}")
                return False
            print(f"Sphinx Theme Installation Completed")
            return True

        except subprocess.TimeoutExpired:
            print(f"Subprocess Timeout: Try increasing the installation_timeout parameter in __init__")
            return False

        except Exception as err:
            print(f"Exception: install_sphinx_theme: {err}")
            return False

    def sphinx_quickstart(self, name, author, version):
        try:
            popen = subprocess.Popen(
                self.sphinx_quickstart_cmd,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

            responses = ['y', name, author, version, 'en']
            for response in responses:
                popen.stdin.write(f'{response}\n'.encode())
                popen.stdin.flush()

            _, error = popen.communicate(timeout=self.quickstart_timeout)
            if error.decode():
                print(f"Error while initializing sphinx - {error}")
                return False
            print("Sphinx Setup Completed Successfully")
            return True

        except subprocess.TimeoutExpired:
            print(f"Subprocess Timeout: Try increasing the quickstart_timeout parameter in __init__")
            return False

        except Exception as err:
            print(f"Exception: sphinx_quickstart: {err}")
            return False

    def update_configuration_file(self, theme):
        try:
            updated_conf = []

            with open(f"{self.docs_folder_name}/source/conf.py") as f:
                conf = f.readlines()

            for line in conf:
                if 'extensions' in line:
                    updated_conf.append('extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]\n')
                elif 'html_theme' in line:
                    updated_conf.append(f'html_theme = "{theme}"\n')
                else:
                    updated_conf.append(line)

            updated_conf.append("\nimport os\n"
                                "import sys\n"
                                f"sys.path.insert(0, os.path.abspath('../../{self.orchestrator}/.'))\n"
                                f"add_module_names = False\n")

            with open(f"{self.docs_folder_name}/source/conf.py", "w") as f:
                f.write("".join(updated_conf))
                print("Configuration File Updated Successfully")
            return True

        except FileNotFoundError as err:
            print(f"File Not Found: {err}")
            return False

        except Exception as err:
            print(f"Exception: update_configuration_file: {err}")
            return False

    def run_sphinx_autodoc(self):
        try:
            popen = subprocess.Popen(self.sphinx_autodoc_cmd,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     shell=True)
            _, error = popen.communicate(timeout=self.autodoc_timeout)
            if error not in [None, b'']:
                print(f"Error while running sphinx-autodoc - {error}")
                return False
            print(f"Sphinx Documentation Raw Files Generated Successfully")
            return True

        except subprocess.TimeoutExpired:
            print(f"Subprocess Timeout: Try increasing the autodoc_timeout parameter in __init__")
            return False

        except Exception as err:
            print(f"Exception: run_sphinx_autodoc: {err}")
            return False

    def add_modules_to_toctree(self):
        try:
            updated_index = []

            with open(f"{self.docs_folder_name}/source/index.rst") as f:
                index = f.readlines()

            for line in index:
                updated_index.append(line)
                if 'caption: Contents' in line:
                    updated_index.append('\n   modules\n')

            with open(f"{self.docs_folder_name}/source/index.rst", "w") as f:
                f.write("".join(updated_index))
                print("Modules Added to Toctree")
            return True

        except FileNotFoundError as err:
            print(f"File Not Found: {err}")
            return False

        except Exception as err:
            print(f"Exception: add_modules_to_toctree: {err}")
            return False

    def generate_html(self):
        try:
            popen = subprocess.Popen(self.sphinx_make_html_cmd,
                                     cwd=f'{self.docs_folder_name}/',
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     shell=True)
            output, error = popen.communicate(timeout=self.html_timeout)

            if error not in [None, b'']:
                print(f"Error while generating html - {error}")
                return False
            print(f"HTML Files Generated Successfully")
            return True

        except subprocess.TimeoutExpired:
            print(f"Subprocess Timeout: Try increasing the html_timeout parameter in __init__")
            return False

        except Exception as err:
            print(f"Exception: generate_html: {err}")
            return False

    def generate_documentation(self, name, author, version, theme):
        try:
            install_status = self.install_sphinx_and_dependencies()
            if not install_status:
                return False
            if theme in self.sphinx_install_theme_cmds.keys():
                self.install_sphinx_theme(theme=theme)
            else:
                theme = "alabaster"
            quickstart_status = self.sphinx_quickstart(name=name, author=author, version=version)
            if not quickstart_status:
                return False
            self.update_configuration_file(theme=theme)
            autodoc_status = self.run_sphinx_autodoc()
            if not autodoc_status:
                return False
            self.add_modules_to_toctree()
            html_status = self.generate_html()
            if not html_status:
                return False
        except Exception as err:
            print(f"Exception: generate_documentation: {err}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sphinx Auto Documentation")
    parser.add_argument('-o', '--orchestrator', type=str, required=True,
                        help="Specify folder name for documentation")
    parser.add_argument('-d', '--docs', default='docs', type=str,
                        help="Specify the folder name for storing all documentation files")
    parser.add_argument('-p', '--projectname', default='Sample Project', type=str,
                        help="Specify the name of the project to be considered in the documentation")
    parser.add_argument('-a', '--author', default='Unknown', type=str,
                        help="Specify the author for the project")
    parser.add_argument('-v', '--version', default='0.0', type=str,
                        help="Specify the version tag of the project")
    parser.add_argument('-t', '--theme', default='alabaster', type=str,
                        choices=['alabaster', 'sphinx_rtd_theme'],
                        help="Specify the HTML theme for the project")
    parsed_args = parser.parse_args()
    sphinx_obj = SphinxAutoDocument(orchestrator=parsed_args.orchestrator,
                                    docs_folder_name=parsed_args.docs)
    sphinx_obj.generate_documentation(name=parsed_args.projectname,
                                      author=parsed_args.author,
                                      version=parsed_args.version,
                                      theme=parsed_args.theme)
