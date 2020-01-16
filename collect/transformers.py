import re


class PercentageWithComma(object):

    pattern = re.compile(r"(\d+,\d+) *\%")

    @staticmethod
    def convert(match):
        return float(match.group(1).replace(",", ".")) / 100


class PercentageNoComma(object):

    pattern = re.compile(r"(\d+) *\%")

    @staticmethod
    def convert(match):
        return float(match.group(1)) / 100

class NoPercentageSignWithComma(object):

    pattern = re.compile(r"^(\d+,\d+)$")

    @staticmethod
    def convert(match):
        return float(match.group(1).replace(",", ".")) / 100

class NoPercentageSignNoComma(object):

    pattern = re.compile(r"^(\d+)$")

    @staticmethod
    def convert(match):
        return float(match.group(1)) / 100

def transform(text):
    transformers = [PercentageNoComma, PercentageWithComma,
                    NoPercentageSignWithComma, NoPercentageSignNoComma]
    matches = [t.pattern.match(text) for t in transformers]
    if not any(matches):
        return text
    match, transformer = next((m, t) for m, t in zip(matches, transformers) if m)
    return transformer.convert(match)
