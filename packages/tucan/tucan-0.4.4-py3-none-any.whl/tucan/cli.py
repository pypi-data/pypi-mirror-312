"""Module helper for the CLI of tucan"""

import click
from tucan import __version__ as _ver_
from tucan import __name__ as _name_


def add_version(f):
    """
    Add the version of the tool to the help heading.
    :param f: function to decorate
    :return: decorated function
    """
    doc = f.__doc__
    f.__doc__ = "Package " + _name_ + " v" + _ver_ + "\n\n" + doc
    return f


@click.group()
@add_version
def main():
    r"""
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣤⣄⢀⡀⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣼⣿⣿⣃⠀⠀⠀⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⠴⢶⡶⣖⣒⠒⡺⣏⠙⡏⠉⠀⢀⣀⠀⠈⠙⠲⣄⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⣫⣤⠀⠀⡰⣿⡇⠀⠁⣽⡆⢷⡖⠛⢉⣭⣉⠳⣄⠀⠈⢧⡀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣟⠀⠈⠁⠀⠀⠀⠀⠀⠀⠘⣽⣟⠈⣷⡀⣿⣼⢿⠀⢹⠀⠀⠈⢧⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠙⠀⠀⠀⠀⠀⢠⢄⣤⣠⣰⣽⣿⡀⠘⡇⠙⠛⢋⣠⡾⠀⠀⠀⢸⡆⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠓⣸⢼⣟⣛⣛⣿⡿⠻⠛⠻⠏⠁⣉⡽⠋⠉⠉⢉⡞⠁⠀⠀⠀⠀⡇⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠟⠛⠉⠁⠀⠈⠉⠉⠛⠒⡶⠖⠋⠉⠀⠀⠀⣰⠏⠀⠀⠀⠀⠀⠀⡇⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠁⠀⠀⠀⠀⠀⣰⠇⠀⠀⠀⠀⠀⠤⢤⣷⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⡤⠞⠉⠙⢦⠀⠀⠀⠀⠀⠀⣠⢰⠇⠀⠀⠀⠀⠀⢀⡏⢀⡼⠃⠀⠀⠀⠀⠀⢿⡀⠀
                ⠀⠀⠀⠀⠀⠀⢸⡁⠀⠀⠀⠈⢧⡀⠀⠀⠀⠀⠁⣸⠀⠀⠀⠀⠀⠀⣼⠁⡾⠁⠀⠀⠀⠀⠀⠀⠘⡇⠀
                ⠀⠀⠀⠀⠀⠀⠈⢳⡄⠀⠀⠀⠀⢳⡄⠀⠀⠀⠀⡏⠀⠀⠀⠀⠀⢀⡏⢸⠇⠀⠀⠀⠀⠀⠀⠀⠀⢿⠀
                ⠀⠀⡴⠲⠦⣤⣀⡀⢹⡄⠀⠀⠀⠀⠹⡄⠀⠀⠀⡟⢦⡀⠀⢀⣠⠞⠀⢸⡀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀
                ⠀⠈⠳⠤⣄⣀⠈⠉⠉⠁⠀⠀⠀⡤⠖⠛⡲⣄⠀⡇⠀⠈⠉⠉⠀⠀⠀⠸⣇⠀⠀⠀⠀⠀⠀⠀⠀⢸⡄
                ⠀⠀⠀⣠⣤⣨⣽⡓⠲⢤⣄⡀⠀⠙⢻⠟⣵⣾⣧⣻⡀⠀⠀⠀⠀⠀⠀⠀⠹⣦⡇⠀⠀⠀⠀⠀⠀⢸⡇
                ⠀⠀⡾⣡⣿⡟⣸⢿⣷⡄⠀⠙⣆⠀⠘⠛⠁⠈⢿⠻⣷⡀⠀⢰⡀⠀⠀⠀⠀⠈⣷⠀⢰⠀⢀⠀⠀⢸⠃
                ⠀⠸⠓⠛⠉⠀⠸⣮⣃⡷⠀⠀⠘⣦⠀⠀⠀⠀⠈⠧⣾⠻⣦⡈⢷⣄⠀⠀⠀⢀⣹⣆⣿⡀⢹⠀⠀⣸⠀
                ⠀⠐⠊⠀⠀⠀⠀⠀⠉⠁⠀⠀⠀⠈⢳⡀⠀⠀⠀⠀⠘⣧⠈⠙⣦⣟⢿⡖⠚⠋⠀⠉⠙⣧⣿⡆⢀⡏⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣄⠀⠀⠀⢀⣸⣷⣴⠏⣠⡞⢹⡗⠒⠛⠀⠀⠀⠘⣧⣼⠁⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣦⠀⠰⣏⣡⠾⠋⠻⢯⡀⠀⡇⠀⠀⠀⠀⠀⠀⢹⡃⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣦⠀⢸⣇⡶⠟⠻⣼⠇⠀⡇⠀⠀⠀⠀⠀⠀⠸⡇⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢷⡄⠀⠀⠀⠀⢘⣧⡀⣟⠲⣤⣀⠀⠀⠀⠀⢷⠀⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡄⣠⣶⣿⢿⡏⣿⢹⣄⠀⠉⠛⠲⠶⠶⢾⡆⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣋⣿⣷⣯⠿⠃⠀⠉⢷⣄⣄⠀⠀⠀⠈⡇⠀
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠚⠲⣴⡇⠀

    -----------------------------   TUCAN   -----------------------------

    You are now using the Command line interface of Tucan package,
    a set of tools created at CERFACS (https://cerfacs.fr).
    It is a set of basic helpers around Fortran and Python language

    Checkout anubis and marauder's map packages, two Cerfacs tools
    able to explore respectively the history and geography of codes,
    which both are based upon Tucan.

    """
    pass


@main.command()
@click.argument("filename", type=str, nargs=1)
@click.option(
    "-d",
    "--dump",
    is_flag=True,
    help="dump json data",
)
@click.option(
    "-cpp",
    "--cppdefinitions",
    type=str,
    default=None,
    help="definitions to resolve CPP directives. Comma separated ',', no spaces : -v ARG1,ARG2",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="verbose mode",
)
def clean(filename: str, dump: bool, verbose: bool, cppdefinitions:str):
    """
    Unformat a fortran of python single file.

    \b
    - Merge multiline statements to one line
    - Split ';' statements
    - Strip comments.
    - Strip blank lines.
    """
    from tucan.unformat_main import unformat_main
    from tucan.tucanlogging import startlog

    startlog(verbose)

    if cppdefinitions is not None:
        cppdirectives = cppdefinitions.split(",")
    else:
        cppdirectives = []

    statements = unformat_main(filename, verbose, cppdirectives=cppdirectives)
    if statements is None:
        print("No statements found...")
        return

    base = filename.split("/")[-1].split(".")[0]
    print(statements)

    statements.dump_code("./" + base + "._rfmt")

    if dump:
        statements.dump_json("./" + base + ".json")


# @main.command()
# @click.argument("path", type=str, nargs=1)
# def package_clean(path):
#     """
#     Unformat a fortran and / or python folder.
#     """

#     import json
#     from loguru import logger

#     from tucan.package_analysis import (
#         rec_travel_through_package,
#         clean_extensions_in_paths,
#         run_unformat,
#     )

#     logger.info("Recursive path gathering ...")
#     paths = rec_travel_through_package(path)
#     logger.info("Cleaning the paths ...")
#     paths = clean_extensions_in_paths(paths)
#     logger.info("Running unformat ...")
#     statements = run_unformat(paths)

#     newfile = "statements_cleaned.json"
#     logger.info(f"Data dumped to {newfile}")
#     with open(newfile, "w") as fout:
#         json.dump(statements, fout, indent=2, sort_keys=True)


@main.command()
@click.argument("filename", type=str, nargs=1)
@click.option(
    "-d",
    "--dump",
    is_flag=True,
    help="dump json data",
)
@click.option(
    "-cpp",
    "--cppdefinitions",
    type=str,
    default=None,
    help="definitions to resolve CPP directives. Comma separated ',', no spaces : -v ARG1,ARG2",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="verbose mode",
)
def struct(filename, dump, verbose, cppdefinitions):
    """
    Extract structure of a fortran or python single file.

    \b
    - Find the nested structures of a code
    - Find the callables in each structure
    - Evaluate sizes, CCN
    """
    import json
    from loguru import logger

    from tucan.struct_main import struct_main
    from tucan.cli_pprinter import struct_summary_file
    from tucan.tucanlogging import startlog
    from tucan.tucanexceptions import TucanError

    startlog(verbose)

    if cppdefinitions is not None:
        cppdirectives = cppdefinitions.split(",")
    else:
        cppdirectives = []

    try:
        struct_ = struct_main(filename, verbose,cpp_directives=cppdirectives)
    except TucanError:
        return
    logger.info("Found following structure:\n" + struct_summary_file(struct_))
    base = filename.split("/")[-1].split(".")[0]
    if dump:
        newfile = base + ".json"
        logger.info(f"Data dumped to {newfile}")
        with open(newfile, "w") as fout:
            json.dump(struct_, fout, indent=2, sort_keys=True)


@main.command()
@click.argument("filename", type=str, nargs=1)
@click.option(
    "-d",
    "--dump",
    is_flag=True,
    help="dump json data",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="verbose mode",
)
def imports(filename, dump, verbose):
    """
    Extract imports of a single file FILENAME
    """
    import json
    from loguru import logger
    from tucan.imports_main import imports_of_file
    from tucan.tucanlogging import startlog

    startlog(verbose)

    imports_, _ = imports_of_file(filename)
    logger.info(json.dumps(imports_, indent=2))
    if dump:
        with open("imports.json", "w") as fout:
            json.dump(imports_, fout, indent=2)


@main.command()
@click.argument("path", type=str, nargs=1)
@click.option(
    "-d",
    "--dump",
    is_flag=True,
    help="dump json data",
)
@click.option(
    "-x",
    "--forbiddenpatterns",
    type=str,
    help="Exclude path matching the given patterns (-x *CHEM*;*.cuda)",
)
@click.option(
    "-m",
    "--mandatorypatterns",
    type=str,
    help="Exclude path not matching any of the mandatory patterns (-x */src/*;*/SOURCES/*)",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="verbose mode",
)
def imports_repo(path, dump, verbose, mandatorypatterns, forbiddenpatterns):
    """
    Extract imports of a full repository PATH
    """
    import json
    from loguru import logger

    from tucan.imports_main import imports_of_repository
    from tucan.tucanlogging import startlog

    startlog(verbose)

    if mandatorypatterns is not None:
        mandatorypatterns = mandatorypatterns.split(";")
    if forbiddenpatterns is not None:
        forbiddenpatterns = forbiddenpatterns.split(";")

    imports_, _ = imports_of_repository(
        path, mandatory_patterns=mandatorypatterns, forbidden_patterns=forbiddenpatterns
    )
    logger.info(json.dumps(imports_, indent=2))
    if dump:
        with open("imports.json", "w") as fout:
            json.dump(imports_, fout, indent=2)


@main.command()
@click.argument("filename", type=str, nargs=1)
@click.option(
    "-d",
    "--dump",
    is_flag=True,
    help="dump json data",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="verbose mode",
)
def cpp_scan(filename, dump, verbose):
    """
    Extract CPP declarations of a single file FILENAME.
    """
    import json
    from loguru import logger
    from tucan.clean_ifdef import scan_cpp_variables
    from tucan.tucanlogging import startlog

    startlog(verbose)

    with open(filename, "r") as fin:
        lines = fin.read().split("\n")

    gv_, lv_ = scan_cpp_variables(lines)
    gv_s = ", ".join(gv_)
    lv_s = ", ".join(lv_)

    logger.info(f"Global CPP declarations : {gv_s}")
    if lv_:
        logger.info(f"Found local CPP definitions : {lv_s}")
    else:
        logger.info("No local CPP definitions")

    if dump:
        base = filename.split("/")[-1].split(".")[0]
        newfile = base + "_cpp.json"
        logger.info(f"Data dumped to {newfile}")
        out = {"global": gv_, "local": lv_}
        with open(newfile, "w") as fout:
            json.dump(out, fout, indent=2, sort_keys=True)


@main.command()
@click.argument("filename", type=str, nargs=1)
@click.option(
    "-cpp",
    "--cppdefinitions",
    type=str,
    default=None,
    # multiple=True,
    help="definitions to resolve CPP directives. Comma separated ',', no spaces : -v ARG1,ARG2",
)
@click.option(
    "-d",
    "--dump",
    is_flag=True,
    help="dump json data",
)
@click.option(
    "-f",
    "--fortran",
    is_flag=True,
    help=" fortran mode (avoid  stripping //)",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="verbose execution",
)
def cpp_clean(filename, cppdefinitions, dump, fortran, verbose):
    """
    Show a file FILENAME with idefs resolved
    """
    from loguru import logger
    from tucan.clean_ifdef import remove_cpp_from_module
    from tucan.unformat_common import read_lines_with_encoding
    from tucan.tucanlogging import startlog

    startlog(verbose)

    if cppdefinitions is None:
        cppdefinitions = []
    else:
        cppdefinitions = cppdefinitions.split(",")

    # with open(filename, "r") as fin:
    #     lines = fin.read().split("\n")
    lines = read_lines_with_encoding(filename)

    lines = remove_cpp_from_module(
        lines, cppdefinitions, verbose=verbose, fortran=fortran
    )
    logger.success("CPP definitions resolved:")
    for line in lines:
        print(line)
    if dump:
        newfile = filename + "_cpp_resolved"
        lines.append("# the CPP directives were resolved by tucan")
        v_s = ", ".join(cppdefinitions)
        lines.append(f"# CPP definitions: {cppdefinitions}")
        with open(newfile, "w") as fout:
            fout.write("\n".join(lines))


@main.command()
@click.argument("path", type=str, nargs=1)
@click.option(
    "-d",
    "--dump",
    is_flag=True,
    help="dump json data",
)
@click.option(
    "-x",
    "--forbiddenpatterns",
    type=str,
    help="Exclude path matching the given patterns (-x *CHEM*;*.cuda)",
)
@click.option(
    "-m",
    "--mandatorypatterns",
    type=str,
    help="Exclude path not matching any of the mandatory patterns (-x */src/*;*/SOURCES/*)",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="verbose execution",
)
def cpp_scan_repo(path, dump, verbose, forbiddenpatterns, mandatorypatterns):
    """
    Extract CPP definitions of a full repository PATH
    """
    import json
    from loguru import logger
    from tucan.clean_ifdef import run_cpp_pkg_analysis
    from tucan.travel_in_package import find_package_files_and_folders
    from tucan.tucanlogging import startlog

    startlog(verbose)
    if mandatorypatterns is not None:
        mandatorypatterns = mandatorypatterns.split(";")
    if forbiddenpatterns is not None:
        forbiddenpatterns = forbiddenpatterns.split(";")

    logger.info("Gathering paths ...")
    files = find_package_files_and_folders(
        path, mandatory_patterns=mandatorypatterns, forbidden_patterns=forbiddenpatterns
    )

    out = run_cpp_pkg_analysis(files)
    gv_s = ", ".join(out["global"])
    logger.info(f"Global CPP variables : {gv_s}")
    for file, lv_ in out["local"].items():
        if lv_:
            lv_s = ", ".join(lv_)
            logger.info(f"Local to {file} : {lv_s}")

    if dump:
        newfile = path + "package_cpp_directives.json"
        logger.info(f"Data dumped to {newfile}")
        with open(newfile, "w") as fout:
            json.dump(out, fout, indent=2, sort_keys=True)


@main.command()
@click.argument("path", type=str, nargs=1)
@click.option(
    "-i",
    "--ignoreerrors",
    is_flag=True,
    help="verbose execution",
)
@click.option(
    "-cpp",
    "--cppdefinitions",
    type=str,
    default=None,
    help="definitions to resolve CPP directives. Comma separated ',', no spaces : -v ARG1,ARG2",
)
@click.option(
    "-x",
    "--forbiddenpatterns",
    type=str,
    help="Exclude path matching the given patterns (-x *CHEM*;*.cuda)",
)
@click.option(
    "-m",
    "--mandatorypatterns",
    type=str,
    help="Exclude path not matching any of the mandatory patterns (-x */src/*;*/SOURCES/*)",
)
@click.option(
    "-l",
    "--levelsoutput",
    type=int,
    default=2,
    help="Nb of levels output in console",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="verbose execution",
)
def struct_repo(
    path, ignoreerrors, levelsoutput, verbose, forbiddenpatterns, mandatorypatterns,cppdefinitions
):
    """
    Extract struct of a repository PATH
    """
    from loguru import logger
    import json
    from tucan.package_analysis import (
        run_struct_all_repo,
    )
    from tucan.tucanlogging import startlog
    from tucan.cli_pprinter import struct_summary_repo

    startlog(verbose)

    if cppdefinitions is None:
        cpp_directives = []
    else:
        cpp_directives = cppdefinitions.split(",")
    if mandatorypatterns is not None:
        mandatorypatterns = mandatorypatterns.split(";")
    if forbiddenpatterns is not None:
        forbiddenpatterns = forbiddenpatterns.split(";")

    struct_repo, full_analysis = run_struct_all_repo(
        path,
        verbose=verbose,
        ignoreerrors=ignoreerrors,
        mandatory_patterns=mandatorypatterns,
        forbidden_patterns=forbiddenpatterns,
        cpp_directives=cpp_directives
    )
    print(struct_summary_repo(struct_repo, depth=levelsoutput))
    newfile = "struct_repo.json"
    logger.info(f"Repo Data dumped to {newfile}")
    with open(newfile, "w") as fout:
        json.dump(struct_repo, fout, indent=2, sort_keys=True)
    newfile = "struct_files.json"
    logger.info(f"File Data dumped to {newfile}")
    with open(newfile, "w") as fout:
        json.dump(full_analysis, fout, indent=2, sort_keys=True)


@main.command()
@click.argument("filename", type=str, nargs=1)
@click.option(
    "-n",
    "--nfunc",
    type=int,
    help="Number of worst performers to keep. If not specified, keep all functions.",
)
@click.option(
    "-c",
    "--ctype",
    type=str,
    default="score",
    help="Complexity metrics to target for ranking. Defaults to 'score'",
)
def worstfunc(filename, nfunc, ctype):
    """
    Identify worst performers in complexity.

    filename : Struc / complexity analysis output (.json).
    """

    import json
    from loguru import logger
    from tucan.struct_common import rearrange_complexity_db, complexity_N_performers
    from pathlib import Path

    filename = Path(filename)

    if not filename.suffix:
        filename = filename.with_suffix(".json")

    try:
        with open(filename, "r") as fin:
            struct_db = json.load(fin)
    except FileNotFoundError:
        logger.info(
            f"Can't find {filename}. Please check the path and the type of the file (must be '.json')"
        )
    except Exception:
        logger.info(
            f"An exception occurs when reaching for {filename}. Please check the path and the type of the file (must be '.json') "
        )

    struct_db_rearrange = rearrange_complexity_db(struct_db)
    dict_top = complexity_N_performers(struct_db_rearrange, ctype, nfunc)

    newfile = f"worst_functions_by_{ctype}.json"
    with open(newfile, "w") as fout:
        json.dump(dict_top, fout, indent=2)
    logger.info(f"Data dumped to {newfile}")
