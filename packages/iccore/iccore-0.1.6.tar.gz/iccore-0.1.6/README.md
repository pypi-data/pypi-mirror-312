# iccore

This package is part of the [Common Tooling Project](https://ichec-handbook.readthedocs.io/en/latest/src/common_tools.html) at the [Irish Centre for High End Computing](https://www.ichec.ie) toward creating a set of common tools and processes for our activities.

The package is a foundational collection of common data structures, data types and low-level utilities used in other ICHEC 'common tools'.

# Install  #

It is available on PyPI:

``` sh
pip install iccore
```

# Features #

The package consists of:

* `data structures` (list, strings, dicts etc.) and utilities for working with them
* tooling for interacting with `system resources`, such as external processes, the filesystem and network.
* basic `data types` for describing people, organizations, projects and code repositories - to support `process automation` and Open Science and FAIR activites. 

# Design Goals #

The ICHEC Common Tools (`ictools`) favour low dependencies and the use of low-level APIs over feature richness and 'quick wins'. The reasons for this are:

* transparency: given our focus on high performance computing we often want to know what is happening in a system at a low/detailed level. Abstraction layers and read-out modification by other libraries can hide outputs.
* control: It is useful to have access to tooling that we can quickly modify ourselves for our needs. 
* training: It is useful for us to gain an understanding of how software interacts with system resources at a low level to support our users. Working with and understanding these tools can help with this.

# Example Uses #

A basic CLI is included, mostly for testing, but it may be useful for getting ideas on what features the package can be used to support.

## System Resources ##

### Filesystem ###

You can replace all occurences of a string with another recursively in files with:

``` shell
iccore filesystem replace_in_files --target $REPLACE_DIR --search $FILE_WITH_SEARCH_TERM --replace $FILE_WITH_REPLACE_TERM 
```

The `search` and `replace` terms are, perhaps unusually, read from files. This can be handy to avoid shell escape sequences - as might be used in `sed`.

### Networking ###

You can download a file with:

``` shell
iccore network download --url $RESOURCE_URL --download_dir $WHERE_TO_PUT_DOWNLOAD
```

## Process Automation Data Types ##

### Project Management ###

You can get Gitlab Milestones given a project id and access token with:

``` shell
iccore gitlab --token $GITLAB_TOKEN milestone $PROJECT_ID
```

You can get the version number of the most recent project release with:

``` shell
iccore gitlab --token $GITLAB_TOKEN latest_release $PROJECT_ID
```

You can get info about a git repo with:

``` shell
iccore git info 
```

run in the repo.

# License #

This project is licensed under the GPLv3+. See the incluced `LICENSE.txt` file for details.
