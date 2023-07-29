import pathlib

from xsdata.formats.dataclass.parsers.xml import XmlParser
from xsdata.formats.dataclass.serializers.xml import (
    SerializerConfig,
    XmlSerializer,
)

from libresvip.extension import base as plugin_base
from libresvip.model.base import Project

from .cevio_generator import CeVIOGenerator
from .cevio_parser import CeVIOParser
from .model import CeVIOCreativeStudioProject
from .options import InputOptions, OutputOptions


class CeVIOConverter(plugin_base.SVSConverterBase):
    def load(self, path: pathlib.Path, options: InputOptions) -> Project:
        ccs_project = XmlParser().from_bytes(path.read_bytes(), CeVIOCreativeStudioProject)
        return CeVIOParser(options).parse_project(ccs_project)

    def dump(
        self, path: pathlib.Path, project: Project, options: OutputOptions,
    ) -> None:
        ccs_project = CeVIOGenerator(options).generate_project(project)
        serializer = XmlSerializer(
            config=SerializerConfig(pretty_print=True),
        )
        xml_text = serializer.render(ccs_project)
        path.write_text(xml_text, encoding="utf-8")