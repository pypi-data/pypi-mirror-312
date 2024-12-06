def harmonic_mean(*args):
    if type(args[0]) == list:
        measurements = args[0]
    else:
        measurements = list(args)
    num_measurements = len(measurements)
    inverse_args = [1/arg for arg in measurements]
    return num_measurements / sum(inverse_args)