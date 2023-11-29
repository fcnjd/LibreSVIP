import pathlib
import zipfile
from dataclasses import asdict
from typing import TYPE_CHECKING

import pytest
from rich import print

from libresvip.extension.manager import plugin_manager
from libresvip.utils import to_unicode

plugin_registry = plugin_manager.plugin_registry


def test_ust_write(shared_datadir: pathlib.Path) -> None:
    from libresvip.plugins.ust.model import UstVisitor, ust_grammar
    from libresvip.plugins.ust.template import render_ust

    proj_path = shared_datadir / "test.ust"
    tree = ust_grammar.parse(to_unicode(proj_path.read_bytes()))
    proj = UstVisitor().visit(tree)
    render_ust(proj, pathlib.Path("test.ust"), encoding="utf-8")


def test_nn_read(shared_datadir: pathlib.Path) -> None:
    from libresvip.plugins.nn.model import nn_grammar, nn_visitor

    proj_path = shared_datadir / "test.nn"
    tree = nn_grammar.parse(proj_path.read_text(encoding="utf-8"))
    proj = nn_visitor.visit(tree)
    for note in proj.notes:
        print(len(note.dynamics.points))


def test_vshp_read(shared_datadir: pathlib.Path) -> None:
    from libresvip.plugins.vshp.model import VocalShifterProjectData

    proj_path = shared_datadir / "test.vshp"
    vshp_data = VocalShifterProjectData.parse_file(proj_path)
    path_content = (
        vshp_data.pattern_metadatas[0].path_and_ext.split(b"\x00", 1)[0].decode("gbk")
    )
    normlized_path = pathlib.PureWindowsPath(path_content).as_posix()
    print(normlized_path)


def test_dv_read(shared_datadir: pathlib.Path, pretty_construct: None) -> None:
    from libresvip.plugins.dv.model import dv_project_struct

    proj_path = shared_datadir / "test.dv"
    proj = dv_project_struct.parse_file(proj_path)
    print(asdict(proj))


def test_mtp_read(shared_datadir: pathlib.Path, pretty_construct: None) -> None:
    from libresvip.plugins.mtp.model import muta_project_struct

    proj_path = shared_datadir / "test.mtp"
    proj = muta_project_struct.parse_file(proj_path)
    print(asdict(proj))
    # for track in proj.tracks:
    #     if track.track_type == MutaTrackType.SONG:
    #         for note in track.song_track_data.notes:
    #             print(chr(note.lyric[0]))


def test_tssln_write(shared_datadir: pathlib.Path, pretty_construct: None) -> None:
    from libresvip.plugins.tssln.model import VoiSonaProject, model_to_value_tree
    from libresvip.plugins.tssln.value_tree import JUCENode, build_tree_dict

    value_tree = JUCENode.parse_file(shared_datadir / "test.tssln")
    tree_dict = build_tree_dict(value_tree)
    project = VoiSonaProject.model_validate(tree_dict["TSSolution"])
    pathlib.Path("test.tssln").write_bytes(JUCENode.build(model_to_value_tree(project)))


def test_ustx_read(
    shared_datadir: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    import yaml

    from libresvip.plugins.ustx.model import USTXProject

    with capsys.disabled():
        proj_path = shared_datadir / "test.ustx"
        proj = USTXProject.model_validate(
            yaml.safe_load(to_unicode(proj_path.read_bytes()))
        )
        print(proj)


def test_ds_read(
    shared_datadir: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from libresvip.plugins.ds.model import DsProject

    with capsys.disabled():
        proj_path = shared_datadir / "test.ds"
        proj_text = proj_path.read_text(encoding="utf-8")
        print(DsProject.model_validate_json(proj_text))


def test_y77_read(
    shared_datadir: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from libresvip.plugins.y77.model import Y77Project

    with capsys.disabled():
        proj_path = shared_datadir / "test.y77"
        proj = Y77Project.model_validate_json(proj_path.read_text(encoding="utf-8"))
        print(proj)


def test_acep_read(
    shared_datadir: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from libresvip.plugins.acep.acep_io import decompress_ace_studio_project
    from libresvip.plugins.acep.model import AcepProject

    with capsys.disabled():
        proj_path = shared_datadir / "test.acep"
        proj = AcepProject.model_validate(decompress_ace_studio_project(proj_path))
        print(proj)


def test_ppsf_read(
    shared_datadir: pathlib.Path,
    capsys: pytest.CaptureFixture[str],
    pretty_construct: None,
) -> None:
    from libresvip.plugins.ppsf.legacy_model import PpsfLegacyProject
    from libresvip.plugins.ppsf.model import PpsfProject

    with capsys.disabled():
        proj_path = shared_datadir / "test.ppsf"
        try:
            proj_text = zipfile.ZipFile(proj_path, "r").read("ppsf.json")
            proj = PpsfProject.model_validate_json(proj_text)
            print(proj)
        except zipfile.BadZipFile:
            proj = PpsfLegacyProject.parse_file(proj_path)
            print(proj)


def test_vog_read(
    shared_datadir: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from libresvip.plugins.vog.model import VogenProject

    with capsys.disabled():
        proj_path = shared_datadir / "test.vog"
        proj_text = zipfile.ZipFile(proj_path, "r").read("chart.json")
        proj = VogenProject.model_validate_json(proj_text)
        print(proj)


def test_vpr_read(
    shared_datadir: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    import zipfile

    from libresvip.plugins.vpr.model import VocaloidProject

    with capsys.disabled():
        proj_path = shared_datadir / "test.vpr"
        proj_text = zipfile.ZipFile(proj_path, "r").read("Project/sequence.json")
        proj = VocaloidProject.model_validate_json(proj_text)
        print(proj)


def test_aisp_read(
    shared_datadir: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from libresvip.plugins.aisp.model import AISProjectBody, AISProjectHead

    with capsys.disabled():
        proj_path = shared_datadir / "test.aisp"
        proj_text = proj_path.read_text()
        first_two_lines = proj_text.splitlines()[:2]
        head = AISProjectHead.model_validate_json(first_two_lines[0])
        body = AISProjectBody.model_validate_json(first_two_lines[1])
        print(head)
        print(body)


def test_gj_read(
    shared_datadir: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from libresvip.plugins.gj.model import GjgjProject

    with capsys.disabled():
        proj_path = shared_datadir / "test.gj"
        proj = GjgjProject.model_validate_json(
            proj_path.read_text(encoding="utf-8-sig")
        )
        print(proj)


def test_dspx_read(
    shared_datadir: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from libresvip.plugins.dspx.model import DspxModel

    with capsys.disabled():
        proj_path = shared_datadir / "test.dspx"
        proj = DspxModel.model_validate_json(proj_path.read_text(encoding="utf-8"))
        print(proj)


def test_vspx_read(shared_datadir: pathlib.Path) -> None:
    from xsdata.formats.dataclass.parsers.xml import XmlParser

    from libresvip.plugins.vspx.model import VocalSharpProject

    proj_path = shared_datadir / "test.vspx"

    xml_parser = XmlParser()
    proj = xml_parser.from_path(proj_path, VocalSharpProject)
    print(proj)


def test_vsqx_read(shared_datadir: pathlib.Path) -> None:
    from xsdata.formats.dataclass.parsers.xml import XmlParser

    if TYPE_CHECKING:
        from libresvip.plugins.vsqx.model import Vsqx

    proj_path = shared_datadir / "test.vsqx"

    xml_parser = XmlParser()
    proj: Vsqx = xml_parser.from_path(proj_path)
    print(type(proj))


def test_musicxml_read(shared_datadir: pathlib.Path) -> None:
    from xsdata.formats.dataclass.parsers.config import ParserConfig
    from xsdata.formats.dataclass.parsers.xml import XmlParser

    from libresvip.plugins.musicxml.models.mxml2 import ScorePartwise

    proj_path = shared_datadir / "test.musicxml"
    xml_parser = XmlParser(config=ParserConfig(fail_on_unknown_properties=False))
    proj = xml_parser.from_path(proj_path, ScorePartwise)
    print(proj)


def test_ccs_read(shared_datadir: pathlib.Path) -> None:
    # from xsdata.formats.dataclass.parsers.config import ParserConfig
    from xsdata.formats.dataclass.parsers.xml import XmlParser

    from libresvip.plugins.ccs.model import CeVIOCreativeStudioProject

    proj_path = shared_datadir / "test.ccs"
    xml_parser = XmlParser(
        # config=ParserConfig(fail_on_unknown_attributes=True)
    )
    proj = xml_parser.from_path(proj_path, CeVIOCreativeStudioProject)
    print(proj)


def test_s5p_read(
    shared_datadir: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    with capsys.disabled():
        s5p_plugin = plugin_registry["s5p"].plugin_object
        proj_path = shared_datadir / "test.s5p"
        proj = s5p_plugin.load(proj_path, None)
        print(proj)


def test_svp_read(
    shared_datadir: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    with capsys.disabled():
        svp_plugin = plugin_registry["svp"].plugin_object
        proj_path = shared_datadir / "test.svp"
        proj = svp_plugin.load(proj_path, None)
        print(proj)


def test_svp_write(
    shared_datadir: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    with capsys.disabled():
        svp_plugin = plugin_registry["svp"].plugin_object
        proj_path = shared_datadir / "test.svp"
        proj = svp_plugin.load(proj_path, None)
        svp_plugin.dump("./test.svp", proj, None)


def test_svip_read(
    shared_datadir: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from libresvip.plugins.svip.msnrbf.svip_reader import SvipReader

    with capsys.disabled():
        # svip_plugin = plugin_registry["svip"].plugin_object
        # proj_path = shared_datadir / "test.svip"
        proj_path = pathlib.Path("./test.svip")
        with SvipReader() as reader:
            reader.read(proj_path)
        # proj = svip_plugin.load(proj_path, None)


def test_svip_write(
    shared_datadir: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    # from libresvip.plugins.svip.msnrbf.svip_reader import SvipReader
    # from libresvip.plugins.svip.msnrbf.svip_writer import SvipWriter

    with capsys.disabled():
        svip_plugin = plugin_registry["svip"].plugin_object
        proj_path = shared_datadir / "test.svip"
        proj = svip_plugin.load(proj_path, None)
        svip_plugin.dump("./test.svip", proj, None)
        # with SvipReader() as registry:
        #     version, proj = registry.read(proj_path)
        # with SvipWriter() as writer:
        #     writer.write(pathlib.Path("./test.svip"), version, proj)


def test_vsq_read(shared_datadir: pathlib.Path) -> None:
    import mido_fix as mido

    vsq_file = mido.MidiFile(
        shared_datadir / "test.vsq", charset="SHIFT-JIS", clip=True
    )

    for track in vsq_file.tracks:
        for msg in track:
            if isinstance(msg, mido.MetaMessage) and msg.type == "text":
                print(msg)
