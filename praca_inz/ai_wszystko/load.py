import zipfile
from pathlib import Path
import tempfile
import pickle
from types import ModuleType
from typing import Union, Any
import shutil
import sys

__PKLX_SRC = 'pklx_src'
__PKL_OBJ = 'obj.pkl'
__NO_COMPILE = 'no_compile'


def load_object(model_path: Union[str, Path]) -> Any:
    """A function that loads an object from given '.pklx' file.
    Files that include source
    code and pickled object are extracted to a temporary directory and
    the definitions are loaded to python as modules at runtime. Temporary directory is later removed.

    Args:
        model_path (Union[str, Path]): a path to the model to be loaded (.pklx file).

    Raises:
        IOError: risen when file has not been found.

    Returns:
        Any: value depends on the object stored in .pklx file. Its definition is dynamically
        added to the running program.
    """
    path = Path(model_path) if isinstance(model_path, str) else model_path
    if not path.exists():
        raise IOError(f"No model file on the path '{model_path}'.")

    # Extractoin
    tmp_dir = get_temp_dir()
    __extract_to_dir(model_path, tmp_dir)

    # Checking python version
    unpickler = __get_unpickler(tmp_dir / __PKL_OBJ)
    python_version = next(unpickler)
    current_version = get_python_version()
    if python_version != __NO_COMPILE:
        if current_version != python_version:
            unpickler.close()
            shutil.rmtree(tmp_dir)
            raise Exception(f"Sourcecode in file '{model_path}' is compiled for python {python_version} "
                            f"(you have {current_version})")

    # Getting namespaces
    package_name = next(unpickler)
    package_structure = next(unpickler)

    # Preparing module structure
    mod = __mount_module(tmp_dir, package_name)
    __make_fake_modules(package_structure, mod)

    # Acquiring object
    obj = next(unpickler)

    # Cleanup
    unpickler.close()
    shutil.rmtree(tmp_dir)
    return obj


def __extract_to_dir(zip_path: Path, extract_dir: Path):
    """Private function that extracts .pklx files to a given directory.

    Args:
        zip_path (Path): path to the .pklx file.
        extract_dir (Path): path to the directory where the files are to be extracted.
    """
    with zipfile.ZipFile(str(zip_path)) as zip:
        zip.extractall(str(extract_dir))


def get_python_version():
    version_string = sys.version
    full_version = version_string.split()[0]
    main_version = '.'.join(full_version.split('.')[:2])
    return main_version


def get_temp_dir() -> Path:
    """A function that returns a path to a temporary directory.
    """
    return Path(tempfile.mkdtemp())


def __mount_module(temp_path: Path, model_name: str) -> ModuleType:
    """A private function that mounts python files as modules to the current running program.

    Args:
        temp_path (Path): path to the temporary directory that stores the source code to be used as a module.
        model_name (str): name of the model which definition is to be added to the currently running python program.

    Returns:
        ModuleType: dynamically loaded python module.
    """
    sys_path = str(temp_path/f'{__PKLX_SRC}.zip')
    sys.path.append(sys_path)
    mod = __import__(model_name)
    sys.path.pop(sys.path.index(sys_path))
    return mod


def __make_fake_modules(package_structure: str, final_module: ModuleType):
    """a private function that generates a scaffolded  module structure. This structure is later used by the 'pickle'
    lib to deserialize an object.

    Example:
        if the package_structure look like this: 'top_folder.middle_module.my_module' this string is split using '.' as
        the separator, and each part is treated as a name for a new module.

        Scaffolding of fake modules then looks like this:
         top_folder
            └── middle_module
                      └── my_module

    Args:
        package_structure (str): a string containing modules and submodules names.
        final_module (ModuleType): the final module imported from .pklx file.
    """
    submodule_names = package_structure.split('.')
    top_module_name = submodule_names[0]
    top_module = ModuleType(top_module_name)
    sys.modules[top_module_name] = top_module

    current = top_module
    current_name = top_module_name
    for submodule_name in submodule_names[1:]:
        setattr(current, submodule_name, ModuleType(submodule_name))
        current = getattr(current, submodule_name)
        current_name = f'{current_name}.{submodule_name}'
        sys.modules[current_name] = current
    sys.modules[package_structure] = final_module


def __get_unpickler(file_path: Path):
    with open(str(file_path), 'rb') as file:
        while True:
            try:
                yield pickle.load(file)
            except EOFError:
                break


if __name__ == '__main__':
    model = load_object('torch_model.pklx')
    print(model)
    print(model.name)
