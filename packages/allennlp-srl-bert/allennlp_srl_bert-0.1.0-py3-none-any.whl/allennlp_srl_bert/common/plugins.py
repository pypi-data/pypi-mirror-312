import importlib
import logging
import os
from pathlib import Path
import sys
from typing import Iterable, Set

from allennlp_srl_bert.common.util import push_python_path, import_module_and_submodules


logger = logging.getLogger(__name__)


LOCAL_PLUGINS_FILENAME = ".srl_bert_plugins"
"""
Local plugin files should have this name.
"""

GLOBAL_PLUGINS_FILENAME = str(Path.home() / ".srl_bert" / "plugins")
"""
The global plugins file will be found here.
"""

DEFAULT_PLUGINS = ("srl_bert_models", "srl_bert_semparse", "srl_bert_server")
"""
Default plugins do not need to be declared in a plugins file. They will always
be imported when they are installed in the current Python environment.
"""


def discover_file_plugins(
    plugins_filename: str = LOCAL_PLUGINS_FILENAME,
) -> Iterable[str]:
    """
    Returns an iterable of the plugins found, declared within a file whose path is `plugins_filename`.
    """
    with open(plugins_filename) as file_:
        for module_name in file_.readlines():
            module_name = module_name.strip()
            if module_name:
                yield module_name


def discover_plugins() -> Iterable[str]:
    """
    Returns an iterable of the plugins found.
    """
    plugins: Set[str] = set()
    if os.path.isfile(LOCAL_PLUGINS_FILENAME):
        with push_python_path("."):
            for plugin in discover_file_plugins(LOCAL_PLUGINS_FILENAME):
                if plugin in plugins:
                    continue
                yield plugin
                plugins.add(plugin)
    if os.path.isfile(GLOBAL_PLUGINS_FILENAME):
        for plugin in discover_file_plugins(GLOBAL_PLUGINS_FILENAME):
            if plugin in plugins:
                continue
            yield plugin
            plugins.add(plugin)


def import_plugins() -> None:
    """
    Imports the plugins found with `discover_plugins()`.
    """
    # Ensure all relevant submodules of AllenNLP are imported.
    import_module_and_submodules(
        "allennlp_srl_bert",
        exclude={
            "allennlp_srl_bert.sanity_checks",  # deprecated
            "allennlp_srl_bert.tools",  # things in here are usually run as commands themselves
        },
    )

    # Workaround for a presumed Python issue where spawned processes can't find modules in the current directory.
    cwd = os.getcwd()
    if cwd not in sys.path:
        sys.path.append(cwd)

    for module_name in DEFAULT_PLUGINS:
        try:
            # For default plugins we recursively import everything.
            import_module_and_submodules(module_name)
            logger.info("Plugin %s available", module_name)
        except ModuleNotFoundError as e:
            if e.name != module_name:
                logger.error(f"Plugin {module_name} could not be loaded: {e}")
    for module_name in discover_plugins():
        try:
            importlib.import_module(module_name)
            logger.info("Plugin %s available", module_name)
        except ModuleNotFoundError as e:
            logger.error(f"Plugin {module_name} could not be loaded: {e}")
