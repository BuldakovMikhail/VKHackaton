import re


def replace_words(text, replacements):
    def re_match(match):
        return str(eval(match.group(1), replacements))
    pattern = r"{{ (.+?) }}"
    result = re.sub(pattern, re_match, text)
    return result


def render_template(html_filename, context):
    with open(html_filename) as html:
        html_text = html.read()

    return replace_words(html_text, context)


def main():
    class User:
        def __init__(self, id):
            self.id = id


    def double_text(text):
        return text * 2


    title = 'TITLE'
    message = 'MESSAGE'
    usr = User(42)

    cntxt = locals()
    print(render_template('template_plain.html', cntxt))

if __name__ == '__main__':
    main()