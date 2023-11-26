import re
import os


def replace_ifs(text, replacements):

    def re_match(match):
        condition = bool(eval(match.group(1).strip(), replacements))
        code_if = match.group(2).strip()
        code_else = match.group(3).strip()

        code_to_replace = code_if if condition else code_else

        return code_to_replace

    pattern = r"{%\s*if(.+?)%}(.+?){%\s*else\s*%}(.+?){%\s*endif\s*%}"
    result = re.sub(pattern, re_match, text, flags=re.DOTALL)
    return result


def replace_fors(text, replacements):
    return text


def replace_vars(text, replacements):

    def re_match(match):
        return str(eval(match.group(1), replacements))

    pattern = r"{{(.+?)}}"
    result = re.sub(pattern, re_match, text)
    return result


def make_replaces(text, replacements):
    
    text = replace_ifs(text, replacements)
    text = replace_fors(text, replacements)
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
    print(render_template(os.path.join(os.path.dirname(__file__), 'template_plain.html'), cntxt))

if __name__ == '__main__':
    main()