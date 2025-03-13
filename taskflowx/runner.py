#  ████████╗ █████╗ ███████╗██╗  ███████╗██╗      ██████╗ ██╗  ██╗
#  ╚══██╔══╝██╔══██╗██╔════╝██║  ██╔════╝██║     ██╔═══██╗██║  ██║
#     ██║   ███████║███████╗██║  █████╗  ██║     ██║   ██║███████║
#     ██║   ██╔══██║╚════██║██║  ██╔══╝  ██║     ██║   ██║██╔══██║
#     ██║   ██║  ██║███████║██║  ██║     ███████╗╚██████╔╝██║  ██║
#     ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝
#
#  TaskFlowX - A lightweight and modular workflow automation engine
#
#  This code is licensed under the GNU General Public License (GPL).
#  You are free to modify and distribute it under the terms of the GPL.
#
#  (c) 2025 TaskFlowX Nils Schaetti <n.schaetti@gmail.com>

import importlib
import importlib.util
import os
import inspect
import taskflowx.triggers as tfx_triggers
from .logger import logger
from .workflows.base import Workflow
from .triggers.base import Trigger


# Load classes from a directory
def load_classes_from_directory(
        directory: str,
        base_class=None
):
    """
    Load classes from a directory.

    Args:
    - directory: The directory to load classes from.
    - base_class: The base class to filter classes.

    Returns:
    - A dictionary of classes.
    """
    # Classes
    classes = {}

    # Check if its a directory
    if not os.path.isdir(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")
    # end if

    # List all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            module_path = os.path.join(directory, filename)

            # Load dynamically the module without package format
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Get all classes in the module
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if obj.__module__ == module_name:
                    if base_class is None or issubclass(obj, base_class):
                        classes[obj.trigger_name()] = obj
                    # end if
                # end if
            # end for
        # end if
    # end for

    return classes
# end load_classes_from_directory

def load_dynamic_classes(directory):
    """
    Load Python trigger classes dynamically from a given directory.
    """
    # Loaded classes
    loaded_classes = {}

    # Check if the directory exists
    if not os.path.exists(directory):
        return loaded_classes
    # end if

    # List all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]
            module_path = f"{directory.replace('/', '.')}.{module_name}"
            try:
                module = importlib.import_module(module_path)
                loaded_classes[module.trigger_name()] = module
                logger.info(f"Module loaded: {module_name} from {module_path}")
            except Exception as e:
                logger.error(f"Error loading module {module_name}: {e}")
            # end try
        # end if
    # end for

    return loaded_classes
# end load_dynamic_modules


# Get base trigger classes
def get_base_trigger_classes():
    """
    Get the base trigger classes.
    """
    # Add basic modules
    return {
        obj.trigger_name(): obj for name, obj in inspect.getmembers(tfx_triggers, inspect.isclass)
        if issubclass(obj, Trigger) and obj is not Trigger
    }
# end get_base_trigger_classes


# Instantiate triggers
def instantiate_triggers(
        triggers_config,
        triggers_path: str
):
    """
    Instantiate triggers from configuration and dynamic modules.

    Args:
    - triggers_config: The triggers configuration.
    - triggers_path: The triggers directory.
    """
    # Base trigger
    base_triggers = get_base_trigger_classes()

    # Load dynamic trigger modules
    if triggers_path:
        # outer_triggers = load_dynamic_classes(triggers_path)
        outer_triggers = load_classes_from_directory(triggers_path, Trigger)
    else:
        outer_triggers = {}
    # end if

    # Merge triggers
    trigger_classes = {**base_triggers, **outer_triggers}
    logger.info(trigger_classes)
    # Triggers
    triggers = []

    # Instantiate triggers
    for trigger_conf in triggers_config:
        # Get the trigger type
        trigger_type = trigger_conf["type"]

        # Check if it is a base trigger or a dynamic trigger
        if trigger_type in trigger_classes:
            trigger_class = trigger_classes[trigger_type]

            # Instantiate the trigger
            trigger = trigger_class(**{k: v for k, v in trigger_conf.items() if k != "type"})

            # Add to trigger list
            if trigger:
                triggers.append(trigger)
                logger.info(f"Trigger '{trigger_type}' loaded")
            else:
                logger.error(f"No class found for type '{trigger_type}'")
            # end if
        else:
            logger.error(f"Unknown trigger: {trigger_type}")
        # end if
    # end for

    return triggers
# end instantiate_triggers


def run(
        config,
        triggers_path: str,
        workflows_path: str
):
    """
    Start TaskFlowX

    Args:
    - config: The configuration object.
    - triggers_path: The triggers directory.
    - workflows_path: The workflows directory.
    """
    # Log
    logger.info("Starting TaskFlowX")

    # Load workflows dynamically from the workflows directory
    workflow_modules = load_dynamic_classes(workflows_path)
    workflows = []

    # Instantiate workflows
    for module in workflow_modules.values():
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Workflow) and obj is not Workflow:
                workflows.append(obj())
                logger.info(f"Workflow '{name}' chargé")
            # end if
        # end for
    # end for

    # Charger les triggers
    triggers = instantiate_triggers(
        triggers_config=config.get("triggers", []),
        triggers_path=triggers_path
    )

    # Lancer les triggers
    for trigger in triggers:
        for workflow in workflows:
            logger.info(f"Starting trigger {trigger.__class__.__name__} for workflow {workflow.__class__.__name__}")
            trigger.start(workflow.run)
        # end for
    # end for

    # Log stop
    logger.info("TaskFlowX stopped")
# end run

