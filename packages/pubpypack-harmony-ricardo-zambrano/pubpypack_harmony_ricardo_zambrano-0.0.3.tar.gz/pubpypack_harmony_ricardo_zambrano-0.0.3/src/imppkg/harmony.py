import sys
from imppkg.harmonic_mean import harmonic_mean
from termcolor import cprint
from termcolor import colored


def _parse_num(inputs: list[str]) -> list[float]:

    try:
        nums = [float(arg) for arg in inputs]
    except ValueError:
        # If input cannot be converted to float, proceed as if there was no input
        nums = []

    return nums


def _calculate_results(nums: list[float]) -> float:

    try:
        result = harmonic_mean(nums)
        return result
    except ZeroDivisionError:
        # If there is no input or if the input is zero, rpoceed with the default result
        result = 0.0  # The result will be zero unless succesfully calculated
        return result


def _format_output(result: float) -> str:

    result_str = str(result)
    formated_result = colored(result_str, "red", "on_cyan", attrs=["bold"])

    return formated_result


def main():

    numbers = _parse_num(sys.argv[1:])

    results = _calculate_results(numbers)

    out = _format_output(results)

    cprint(out)


# def main():

#     result = 0.0 # The result will be zero unless succesfully calculated

#     try:
#         nums = [float(arg) for arg in sys.argv[1:]]

#     except ValueError:
#         # If input cannot be converted to float, proceed as if there was no input
#         nums = []

#     try:
#         result = harmonic_mean(nums)
#     except ZeroDivisionError:
#         # If there is no input or if the input is zero, rpoceed with the default result
#         pass

#     cprint(result, 'red', 'on_cyan', attrs=['bold'])
