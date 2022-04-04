import cli_sols_auto.tools
from cli_sols_auto.parser_sols_auto.old import (
    parse,
    parse_sales,
    parse_interstore_transfer,
    parse_traffic,
    parse_delivery_validation
)


from cli_sols_auto.parser_sols_auto.tools import FileType


# Test parsing a line
def test_line_old2new_ven():
    expect = "JAC-778;2022-03-23;;4132369;3603652236628;1;395.00;1"
    old = "0007782022032336036522366280004132369000010000395001"
    assert parse_sales(old, 'JAC') == expect


def test_line_old2new_trs():
    expect = "2021-11-01;;OKA-1210;OKA-1889;3604277211410;5"
    old = "2021110100121000188936042772114100005"
    assert parse_interstore_transfer(old, 'OKA') == expect


def test_line_old2new_trf():
    expect = "JAC-778;2022-03-29;8"
    old = "000778202203290008"
    assert parse_traffic(old, 'JAC') == expect


def test_line_old2new_val():
    expect = "JAC-778;00000999993057074313;3603652347409;1;2021-04-19"
    old = "0007780000099999305707431336036523474090000120210419"
    assert parse_delivery_validation(old, 'JAC') == expect


# Test parsing a file
def test_new2old_ven(new_ven_file_light, old_ven_file):
    expect = new_ven_file_light.read_text(encoding="utf-8")
    assert parse(old_ven_file, FileType('VEN'), 'JAC') == expect


def test_new2old_val(new_val_file_light, old_val_file):
    expect = new_val_file_light.read_text(encoding="utf-8")
    assert parse(old_val_file, FileType('VAL'), 'JAC') == expect


def test_new2old_trf(new_trf_file_light, old_trf_file):
    expect = new_trf_file_light.read_text(encoding="utf-8")
    assert parse(old_trf_file, FileType('TRF'), 'JAC') == expect


def test_new2old_trs(new_trs_file_light, old_trs_file):
    expect = new_trs_file_light.read_text(encoding="utf-8")
    assert parse(old_trs_file, FileType('TRS'), 'OKA') == expect
