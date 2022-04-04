from cli_sols_auto.app import get_file_list


def test_new2old_file(new_trs_file):
    expect = get_file_list(str(new_trs_file))
    assert len(expect) == 1


def test_new_dir_files(tmp_new_dir, new_trs_file, new_val_file):
    expect = get_file_list(str(tmp_new_dir))
    assert len(expect) == 2


def test_new_dir_files(tmp_new_dir, new_trf_file, new_val_file, new_trf_file_light):
    tmp_file = f"{tmp_new_dir}/Traffic*.csv"
    expect = get_file_list(str(tmp_file))
    assert len(expect) == 2
