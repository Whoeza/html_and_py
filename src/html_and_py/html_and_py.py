# html_and_py.py
# todo Make this a module of its own. (Python package?) Make it exportable
#  for use in the rest of the project. Upload it to the public repository of
#  Python packages.
# todo It would be nice to test the longevity of this solution by modifying
#  this prototype and seeing that the module adapts to it.
HTML_PROTOTYPE = {
    # For my purposes, any HTML element can have a tag, some attributes,
    # children elements and a text node
    'tag': '',
    'attributes': {},
    'children': [],
    'text': ''
}  # Retrieve keys from prototype at any time like so: HTML_PROTOTYPE.keys()

HTML_VOID_ELEMENTS = [
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'keygen',
    'link', 'meta', 'param', 'source', 'track', 'wbr']


# Auxiliary functions
def init_doctype(doctype: str) -> str:
    return "<!doctype %s>\n" % doctype


def is_self_enclosing(component_name: str) -> bool:
    if component_name.lower() in HTML_VOID_ELEMENTS:
        return True
    return False


# Creating an HTML element using the HTML_PROTOTYPE, a passed prototype,
# and an optional additional setting
def create_html(*args: dict, **kwargs) -> dict:
    # print("create_html: args = ", args)
    # print("create_html: unpacked args = ", *args)
    # print("create_html: kwargs = ", kwargs)

    new_from_prototype = {}
    # Creating from the vanilla HTML_PROTOTYPE
    new_from_prototype.update(**HTML_PROTOTYPE)

    if len(args):
        # Can instantiate a clone from an existing HTML element
        new_from_prototype.update(**args[0])

    # Additionally, can override specific values if they are passed in kwargs
    if kwargs:
        new_from_prototype.update(**kwargs)

    return new_from_prototype


# Rendering Python dictionaries describing HTML objects into strings,
# configured with HTML_PROTOTYPE
def render_html(*args: dict, **kwargs) -> str:
    # The usage is one of two:
    # 1- optionally pass 1 argument and treat it as a dictionary that follows
    #    the HTML_PROTOTYPE keys configuration
    # 2- or take kwargs respecting the HTML_PROTOTYPE keys configuration
    if 1 == len(args):
        html_pack = args[0]
        [html_tag, html_attributes, html_children, html_text] = \
            [html_pack[key] for key in HTML_PROTOTYPE.keys()]
    else:
        [html_tag, html_attributes, html_children, html_text] = \
            [kwargs[val] for val in HTML_PROTOTYPE.keys()]

    # print("working")
    # print('html_tag: ' + str(html_tag))
    # print('html_attributes: ' + str(html_attributes))
    # print('html_children: ' + str(html_children))
    # print('html_text: ' + str(html_text))

    # do stuff

    # Attributes first
    html_attributes_str = ""
    for key, value in html_attributes.items():
        # convert syntax
        # from:  'key': 'value'
        #   to:    key="value"
        html_attributes_str += " %s=\"%s\"" % (str(key), str(value))

    # Then determine open & close tags
    html_open_tag = "<" + html_tag + html_attributes_str
    if is_self_enclosing(html_tag):
        html_open_tag += " />"
        html_close_tag = ""
    else:
        html_open_tag += ">"
        html_close_tag = "</" + html_tag + ">"

    # Finally, render children elements to text, and append these texts
    # then append the text of the current element.
    # to do so, first render children to text
    contents = []
    for child in html_children:
        contents.append(render_html(child))
    # then, append the text node
    contents.append(html_text)

    # and process all the text
    indent = 2
    indent_spaces = " " * indent
    indented_content = ""
    for content in contents:
        # contents is a list of strings, representing HTML elements and/or text
        # nodes
        # fixed https://github.com/Whoeza/html_and_py/issues/6
        for line in str(content).splitlines():
            indented_line = indent_spaces + line + "\n"
            indented_content += indented_line

    html_full = html_open_tag + "\n" + indented_content + html_close_tag
    return html_full


# Update an arbitrary number of HTML elements with the kwargs
def update_html(*args: dict, **kwargs) -> [dict]:
    # print("update_html: args = ", args)
    # print("update_html: unpacked args = ", *args)
    # print("update_html: kwargs = ", kwargs)

    if len(args):
        # Updating one or more HTML elements in one pass with args
        html_objects = [html_object for html_object in args]
    else:
        html_objects = []

    # Using kwargs as the prototype for the update
    if kwargs:
        apply_change = kwargs
    else:
        apply_change = {}

    for html_object in html_objects:
        html_object.update(**apply_change)
    return html_objects


if __name__ == "__main__":
    DEV_STAGE = False
    if DEV_STAGE:
        print("Build a test page. Can go top-down, as well as bottom-up.")
        html_page = {
            'tag': 'html',
            'attributes': {'name': 'myName', 'value': 'myValue'},
            'children': [],
            'text': ""
        }
        html_page['children'].append({
            'tag': 'head',
            'attributes': {},
            'children': [{
                'tag': 'title',
                'attributes': {},
                'children': [],
                'text': 0.1
            }],
            'text': ''
        })
        html_page['children'].append({
            'tag': 'body',
            'attributes': {},
            'children': [{
                'tag': 'p',
                'attributes': {},
                'children': [],
                'text': "Hello World!"
            }],
            'text': 'This is the HTML body!'
        })
        print("HTML object described as a Python dict:", html_page)

        ##
        # Testing rendering a dictionary of nested HTML elements
        ##
        rendered_html = render_html(**html_page)
        print(rendered_html)

        ##
        # Testing creating HTML elements from prototype with create_html
        ##
        print("HTML prototype:", HTML_PROTOTYPE)
        html_div = {}
        html_div.update(**HTML_PROTOTYPE)
        html_div.update({
            'tag': 'div'
        })
        print("  >>  does this make a DIV?", html_div)
        html_div.update({})
        print("  >>  does this not change anything?", html_div)
        html_paragraph = create_html({'tag': 'p'})
        print("  >>  is this a vanilla HTML with a <p> tag?", html_paragraph)
        html_paragraph = create_html({
            'tag': 'a',
            'attributes': {
                'href': '#'
            }
        })
        print("  >>  is this a vanilla HTML with a new <a> element?",
              html_paragraph)
        html_paragraph = create_html({'tag': 'p'})
        print("  >>  is this back to vanilla HTML with a <p> tag?", html_paragraph)
        html_paragraph = create_html(**{'text': 'What Happens Now?'})
        print("  >>  is this a vanilla HTML with a <p> tag and updated text?",
              html_paragraph)

        # Testing updating HTML elements, in batches or individually with
        # update_html
        html_component_one = create_html({'tag': 'componentOne'})
        html_component_two = create_html({'tag': 'componentTwo'})

        html_component_one, html_component_two = update_html(
            html_component_one, html_component_two,
            **{}
        )
        print("  >> Did this leave components one and two unchanged?")
        print("One (before)", create_html({'tag': 'componentOne'}))
        print("One (after)", html_component_one)
        print("Two (before)", create_html({'tag': 'componentTwo'}))
        print("Two (after)", html_component_two)

        html_component_one, html_component_two = update_html(
            html_component_one, html_component_two,
            **HTML_PROTOTYPE
        )
        print("  >> Did this reset both components?")
        print("One", html_component_one)
        print("Two", html_component_two)

        html_component_one = update_html(html_component_one, **{
            'tag': 'componentOne'
        })
        print("  >> Did this bring back component one?")
        print("One", html_component_one)
        print("Two", html_component_two)

        html_component_two = update_html(html_component_two, **{
            'tag': 'componentTwo'
        })
        print("  >> Did this bring back component two?")
        print("One", html_component_one)
        print("Two", html_component_two)
