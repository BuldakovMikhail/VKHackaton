import functools
import os
import re

RE_TEMPLATE_IFS = r"{%\s*if(.+?)%}(.+?){%\s*else\s*%}(.+?){%\s*endif\s*%}"
RE_TEMPLATE_FORS = r"{%\s*for\s*(.+?)\s*in\s*(.+?)\s*%}(.+?){%\s*endfor\s*%}"
RE_TEMPLATE_VARS = r"{{(.+?)}}"


def re_match_ifs(match, reprs):
    condition = bool(eval(match.group(1).strip(), reprs))
    code_if = match.group(2).strip()
    code_else = match.group(3).strip()

    code_to_replace = code_if if condition else code_else

    return code_to_replace


def re_match_fors(match, reprs):
    variable = match.group(1).strip()
    iterable = eval(match.group(2).strip(), reprs)
    code = match.group(3).strip()

    code_to_replace = []
    for item in iterable:
        current_code_part = replace_vars(code, reprs, {variable: item})
        code_to_replace.append(current_code_part)

    return '\n'.join(code_to_replace)


def re_match_vars(match, reprs, lcls=None):
    return str(eval(match.group(1).strip(), reprs, lcls))


def replace_vars(text, replacements, lcls_=None):
    return replace_html(text,
                        functools.partial(re_match_vars,
                                          reprs=replacements,
                                          lcls=lcls_),
                        RE_TEMPLATE_VARS)


def replace_html(text, re_match_with_replacements, pattern):
    return re.sub(pattern, re_match_with_replacements, text, flags=re.DOTALL)


def make_replaces(text, replacements):
    text = replace_html(text,
                        functools.partial(re_match_ifs,
                                          reprs=replacements),
                        RE_TEMPLATE_IFS)
    text = replace_html(text,
                        functools.partial(re_match_fors,
                                          reprs=replacements),
                        RE_TEMPLATE_FORS)
    text = replace_vars(text, replacements)
    return text


def render_template(html_filename, context):
    with open(html_filename) as html:
        html_text = html.read()

    return make_replaces(html_text, context)


def main():
    class User:
        def __init__(self, id):
            self.id = id

    def double_text(text):
        return text * 2

    title = 'TITLE'
    message = 'MESSAGE'
    usr = User(32)

    cntxt = locals()
    print(render_template(os.path.join(os.path.dirname(__file__),
                                       'template_plain.html'), cntxt))


if __name__ == '__main__':
    main()
