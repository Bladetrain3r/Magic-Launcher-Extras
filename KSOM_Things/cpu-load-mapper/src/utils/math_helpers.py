def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

def mean(values):
    return sum(values) / len(values) if values else 0

def variance(values):
    if len(values) < 2:
        return 0
    mean_value = mean(values)
    return sum((x - mean_value) ** 2 for x in values) / (len(values) - 1)

def standard_deviation(values):
    return variance(values) ** 0.5

def z_score(value, mean, std_dev):
    if std_dev == 0:
        raise ValueError("Standard deviation cannot be zero.")
    return (value - mean) / std_dev