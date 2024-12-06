import sys
from termcolor import colored
import pytest

# from imppkg.harmonic_mean import harmonic_mean
from imppkg.harmony import main


def test_always_passes():
    assert True


@pytest.mark.parametrize(
    "input_one, input_two, input_three, expected",
    [("1", "4", "4", 2.0), (0, 0, 0, 0.0), ("a", "b", "c", 0.0)],
)
def test_harmony_parametrized(input_one, input_two, input_three, expected, monkeypatch, capsys):
    inputs = [input_one, input_two, input_three]
    monkeypatch.setattr(sys, "argv", ["harmony"] + inputs)

    main()

    expected_value = colored(expected, "red", "on_cyan", attrs=["bold"])
    actual_output = capsys.readouterr().out.strip().replace("\x1b[0m\x1b[0m", "\x1b[0m")
    assert actual_output == expected_value


# def test_harmony_happy_path(monkeypatch, capsys):
#     inputs = ["1", "4", "4"]
#     monkeypatch.setattr(sys, "argv", ["harmony"] + inputs)

#     main()

#     expected_value = 2.0
#     assert capsys.readouterr().out.strip() == colored(
#         expected_value,
#         "red",
#         "on_cyan",
#         attrs = ["bold"]
#     )

# def test_harmony_non_num_imput(monkeypatch, capsys):
#     inputs = ["a", "b", "c"]

#     monkeypatch.setattr(sys, "argv", ["harmony"] + inputs)

#     main()

#     expected_value = 0.0
#     assert capsys.readouterr().out.strip() == colored(
#         expected_value,
#         "red",
#         "on_cyan",
#         attrs = ["bold"]
#     )
