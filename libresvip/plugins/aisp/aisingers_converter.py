import pathlib

from libresvip.extension import base as plugin_base
from libresvip.model.base import Project, json_dumps

from .aisingers_generator import AiSingersGenerator
from .aisingers_parser import AiSingersParser
from .model import AISProjectBody, AISProjectHead
from .options import InputOptions, OutputOptions


class AiSingersConverter(plugin_base.SVSConverterBase):
    def load(self, path: pathlib.Path, options: InputOptions) -> Project:
        content = path.read_text("utf-8")
        head, _, body = content.partition("\n")
        ais_project_head = AISProjectHead.model_validate_json(head.strip())
        ais_project_body = AISProjectBody.model_validate_json(body.strip())
        return AiSingersParser(options).parse_project(
            ais_project_head, ais_project_body
        )

    def dump(
        self, path: pathlib.Path, project: Project, options: OutputOptions
    ) -> None:
        ais_project_head, ais_project_body = AiSingersGenerator(
            options
        ).generate_project(project)
        path.write_text(
            json_dumps(
                ais_project_head.model_dump(mode="json", by_alias=True),
                separators=(", ", ": "),
            )
            + "\n"
            + json_dumps(
                ais_project_body.model_dump(mode="json", by_alias=True),
                separators=(", ", ": "),
            ),
            encoding="utf-8",
        )