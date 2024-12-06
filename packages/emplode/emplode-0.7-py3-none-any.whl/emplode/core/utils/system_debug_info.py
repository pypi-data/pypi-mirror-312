import platform
import subprocess

import pkg_resources
import psutil
import toml


def get_python_version():
    return platform.python_version()


def get_pip_version():
    try:
        pip_version = subprocess.check_output(["pip", "--version"]).decode().split()[1]
    except Exception as e:
        pip_version = str(e)
    return pip_version


def get_em_version():
    try:
        em_version_cmd = subprocess.check_output(
            ["emplode", "--version"], text=True
        )
    except Exception as e:
        em_version_cmd = str(e)
    em_version_pkg = pkg_resources.get_distribution("emplode").version
    em_version = em_version_cmd, em_version_pkg
    return em_version


def get_os_version():
    return platform.platform()


def get_cpu_info():
    return platform.processor()


def get_ram_info():
    vm = psutil.virtual_memory()
    used_ram_gb = vm.used / (1024**3)
    free_ram_gb = vm.free / (1024**3)
    total_ram_gb = vm.total / (1024**3)
    return f"{total_ram_gb:.2f} GB, used: {used_ram_gb:.2f}, free: {free_ram_gb:.2f}"


def get_package_mismatches(file_path="pyproject.toml"):
    with open(file_path, "r") as file:
        pyproject = toml.load(file)
    dependencies = pyproject["tool"]["poetry"]["dependencies"]
    dev_dependencies = pyproject["tool"]["poetry"]["group"]["dev"]["dependencies"]
    dependencies.update(dev_dependencies)

    installed_packages = {pkg.key: pkg.version for pkg in pkg_resources.working_set}

    mismatches = []
    for package, version_info in dependencies.items():
        if isinstance(version_info, dict):
            version_info = version_info["version"]
        installed_version = installed_packages.get(package)
        if installed_version and version_info.startswith("^"):
            expected_version = version_info[1:]
            if not installed_version.startswith(expected_version):
                mismatches.append(
                    f"\t  {package}: Mismatch, pyproject.toml={expected_version}, pip={installed_version}"
                )
        else:
            mismatches.append(f"\t  {package}: Not found in pip list")

    return "\n" + "\n".join(mismatches)


def emplode_info(emplode):
    try:
        if emplode.offline and emplode.llm.api_base:
            try:
                curl = subprocess.check_output(f"curl {emplode.llm.api_base}")
            except Exception as e:
                curl = str(e)
        else:
            curl = "Not local"

        messages_to_display = []
        for message in emplode.messages:
            message = str(message.copy())
            try:
                if len(message) > 2000:
                    message = message[:1000]
            except Exception as e:
                print(str(e), "for message:", message)
            messages_to_display.append(message)

        return f"""

        # Emplode Info
        
        Vision: {emplode.llm.supports_vision}
        Model: {emplode.llm.model}
        Function calling: {emplode.llm.supports_functions}
        Context window: {emplode.llm.context_window}
        Max tokens: {emplode.llm.max_tokens}
        Computer API: {emplode.computer.import_computer_api}

        Auto run: {emplode.auto_run}
        API base: {emplode.llm.api_base}
        Offline: {emplode.offline}

        Curl output: {curl}

        # Messages

        System Message: {emplode.system_message}

        """ + "\n\n".join(
            [str(m) for m in messages_to_display]
        )
    except:
        return "Error, couldn't get emplode info"


def system_info(emplode):
    em_version = get_em_version()
    print(
        f"""
        Python Version: {get_python_version()}
        Pip Version: {get_pip_version()}
        Emplode Version: cmd: {em_version[0]}, pkg: {em_version[1]}
        OS Version and Architecture: {get_os_version()}
        CPU Info: {get_cpu_info()}
        RAM Info: {get_ram_info()}
        {emplode_info(emplode)}
    """
    )

    # Removed the following, as it causes `FileNotFoundError: [Errno 2] No such file or directory: 'pyproject.toml'`` on prod
    # (i think it works on dev, but on prod the pyproject.toml will not be in the cwd. might not be accessible at all)
    # Package Version Mismatches:
    # {get_package_mismatches()}
