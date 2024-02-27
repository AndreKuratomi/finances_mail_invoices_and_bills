from pathlib import Path


def join_reports(not_found: str, sent: str, final_list: str, report_path: Path) -> None:
    """From two files given create a third one in a speficific directory."""
    
    with report_path.joinpath(not_found).open("r") as file:
        not_found_list_content = file.read()

    with report_path.joinpath(sent).open("r") as file:
        sent_list_content = file.read()

    combination: str = f"{sent_list_content}\n\n{not_found_list_content}"

    with report_path.joinpath(final_list).open("w") as final_report_file:
        final_report_file.write(combination)
