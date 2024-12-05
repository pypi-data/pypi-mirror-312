import re
from typing import List

from bibtexparser.model import Entry, Field
from lsprotocol.types import MessageType, Position, ShowMessageParams
from pygls.lsp.server import LanguageServer
from pygls.workspace import TextDocument
from typing_extensions import assert_type

from .bibli_config import BibliTomlConfig, DocFormatingConfig


def show_message(
    ls: LanguageServer, msg: str, msg_type: MessageType = MessageType.Info
):
    ls.window_show_message(
        ShowMessageParams(
            msg_type,
            msg,
        )
    )


def cite_at_position(
    doc: TextDocument, position: Position, config: BibliTomlConfig
) -> str | None:
    line = doc.lines[position.line]

    # TODO: Check if encapsulated in "[]"
    for match in re.finditer(config.cite.regex, line):
        (start, end) = match.span(1)
        if (
            start - len(config.cite.prefix) <= position.character
            and end + len(config.cite.postfix) >= position.character
        ):
            return match.group(1)

    return None


def preprocess_bib_entry(entry: Entry, config: DocFormatingConfig):
    replace_list = ["{{", "}}", "\\vphantom", "\\{", "\\}"]
    for f in entry.fields:
        if isinstance(f.value, str):
            for r in replace_list:
                f.value = f.value.replace(r, "")

            f.value = f.value.replace("\n", " ")
            if len(f.value) > config.character_limit:
                f.value = f.value[: config.character_limit] + "..."

            entry.set_field(Field(f.key, f.value))


def build_doc_string(
    entry: Entry, config: DocFormatingConfig, bibfile: str | None = None
):
    import mdformat

    preprocess_bib_entry(entry, config)

    field_dict = {f.key: f.value for f in entry.fields}

    field_dict["entry_type"] = entry.entry_type
    if bibfile:
        field_dict["bibfile"] = bibfile

    doc_string = ""

    while True:
        try:
            if isinstance(config.header_format, List):
                doc_string += "\n".join(config.header_format).format(**field_dict)
            else:
                assert_type(config.header_format, str)
                doc_string += config.header_format.format(**field_dict)
        except KeyError as e:
            # Unknown key in the header format
            field_dict[e.args[0]] = "Unknown"
            continue
        break

    doc_string += "\n"

    # Entry type no longer needed
    field_dict.pop("entry_type")
    if config.show_fields == []:
        show_field_dict = {k: v for k, v in field_dict.items()}
    else:
        show_field_dict = {
            k: v for k, v in field_dict.items() if config.show_fields.count(k) > 0
        }

    match config.format:
        case "table":
            from py_markdown_table.markdown_table import markdown_table

            table_content = [{"Key": k, "Value": v} for k, v in show_field_dict.items()]
            # NOTE: sometimes table formatting fails with long entries
            table = (
                markdown_table(table_content)
                .set_params(
                    row_sep="markdown",
                    padding_weight="right",
                    multiline={
                        "Key": 20,
                        "Value": 80,
                    },
                    quote=False,
                )
                .get_markdown()
            )
            doc_string += table
        case "list":
            for k, v in show_field_dict.items():
                doc_string += f"- __{k}__: {v}\n"

            # Do one last beautifying for list
            doc_string = mdformat.text(
                doc_string,
                options={"wrap": config.wrap},
            )

    while True:
        try:
            if isinstance(config.footer_format, List):
                doc_string += "\n".join(config.footer_format).format(**field_dict)
            else:
                assert_type(config.footer_format, str)
                doc_string += config.footer_format.format(**field_dict)
        except KeyError as e:
            # Unknown key in the header format
            field_dict[e.args[0]] = "Unknown"
            continue
        break

    return doc_string
