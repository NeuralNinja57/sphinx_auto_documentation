# Sphinx - Docstrings - Auto Documentation
[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://github.com/Shubham5798/sphinx_auto_documentation) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg?style=flat&logo=python&color=informational)](https://www.python.org/) 

### Introduction
Sphinx is a popular documentation generator for Python projects. It's often used to create documentation for Python packages, libraries, and frameworks. Sphinx uses reStructuredText format to write documentation, and it can generate documentation in several formats, including HTML, PDF, and man pages.

Sphinx has a rich ecosystem of extensions that can add additional functionality to your documentation, such as adding support for code snippets, mathematical equations, and more. It also integrates well with other tools in the Python ecosystem, such as the autodoc extension, which can automatically generate documentation for your Python code.

This project is focused on developing a single script which would automatically create an HTML documentation. THe end user would not be required to have in-depth knowledge of what is Sphinx and how to utilise the autodoc extension so as to generate the documentation using docstrings

### Step-by-Step Guide For Generating Documentation

1. **Getting Started With Docstrings:**
    * Add docstrings in your python code while following standard Google documentation practice: https://google.github.io/styleguide/pyguide.html
    * Sample Docstring for reference:
      ```
      def fetch_smalltable_rows(table_handle: smalltable.Table,
                          keys: Sequence[Union[bytes, str]],
                          require_all_keys: bool = False,
      ) -> Mapping[bytes, tuple[str, ...]]:
        """
        Fetches rows from a Smalltable.

        Retrieves rows pertaining to the given keys from the Table instance
        represented by table_handle.  String keys will be UTF-8 encoded.
    
        Args:
            table_handle: An open smalltable.Table instance.
            keys: A sequence of strings representing the key of each table
              row to fetch.  String keys will be UTF-8 encoded.
            require_all_keys: If True only rows with values set for all keys will be
              returned.
    
        Returns:
            A dict mapping keys to the corresponding table row data
            fetched. Each row is represented as a tuple of strings. For
            example:
    
            {b'Serak': ('Rigel VII', 'Preparer'),
             b'Zim': ('Irk', 'Invader'),
             b'Lrrr': ('Omicron Persei 8', 'Emperor')}
    
            Returned keys are always bytes.  If a key from the keys argument is
            missing from the dictionary, then that row was not found in the
            table (and require_all_keys must have been False).
    
        Raises:
            IOError: An error occurred accessing the smalltable.
        """
      ```

2. **Setting Up Sphinx Setup Script:**
    * Download the `sphinx_setup.py` file at the root location in your code so that the folder structure shall look like below
      ```
      -- root code repository
         -- orchestrator
            -- module 1
               -- __init__.py
               -- python_file.py
            -- module 2
               -- __init__.py
               -- python_file_1.py
               -- python_file_2.py
         -- sphinx_setup.py
      ```

3. **Running sphinx_setup.py**
    * Run the `sphinx_setup.py` from the root location
    * Following arguments are to be configured while running the script
      ```
      '-o' or '--orchestrator' ⟶ Specify folder name for documentation (REQUIRED)
      '-d' or '--docs' ⟶ Specify the folder name for storing all documentation files (default: docs)
      '-p' or '--projectname' ⟶ Specify the name of the project to be considered in the documentation (default: Sample Project)
      '-a' or '--author' ⟶ Specify the author for the project (default: Unknown)
      '-v' or '--version' ⟶ Specify the version tag of the project (default: 0.0)
      '-t' or '--theme' ⟶ Specify the HTML theme for the project documentation (default: alabaster) (choices: ['alabaster', 'sphinx_rtd_theme'])
      ```
    * Reference command: `python sphinx_setup.py -o sample_orchestrator -p "Sphinx Hello World" -a Shubham -t sphinx_rtd_theme`

Running the setup file will generate a docs folder in the root directory which will contain all the files corresponding to the Sphinx documentation of the project

Open the `docs/build/html/index.html` file to view the entire project documentation.

### References:
1. Sphinx Homepage: https://www.sphinx-doc.org/en/master/
2. Google Python Style Guide: https://google.github.io/styleguide/pyguide.html
3. Sphinx Themes: https://www.sphinx-doc.org/en/master/usage/theming.html
