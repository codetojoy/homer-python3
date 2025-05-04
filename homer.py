
class Config:
    def __init__(self):
        self.main_template_file = 'resources/main.template.html'
        self.link_template_file = 'resources/link.template.html'
        self.output_file = 'index.html'

class Token:
    def __init__(self, token, new_value):
        self.token = token
        self.new_value = new_value

class Stamper:
    def stamp(self, template_file, tokens):
        try:
            with open(template_file, 'r') as file:
                content = file.read()

            for token in tokens:
                placeholder = token.token
                value = token.new_value
                content = content.replace(placeholder, value)

        except Exception as e:
            print(f"An error occurred: {e}")

        return content

class LinkGroup:
    def __init__(self, name):
        self.name = name
        self.links = []

    def add_link(self, link):
        self.links.append(link) 

    def to_string(self, config):
        result = "<div class=\"my-item\">\n"
        result += "<h3>" + self.name + "</h3>\n"
        result += "<div>\n"
        for link in self.links:
            result += link.to_string(config)
        result += "</div>\n"
        result += "</div>\n"
        return result

class Link:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def to_string(self, config):
        template_file = config.link_template_file
        tokens = [Token("@URL", self.url), Token("@NAME", self.name)]
        content = Stamper().stamp(template_file, tokens)
        return content 

class HomerModel:
    def __init__(self):
        self.current_link_group = None
        self.link_groups = []

    def add_link_group(self, name):
        link_group = LinkGroup(name)
        self.link_groups.append(link_group)
        self.current_link_group = link_group

    def add_link(self, name, url):
        link = Link(name, url)
        self.current_link_group.add_link(link)

    def to_string(self, config):
        template = '<div class="my-items">\n@LINK_GROUPS\n</div>\n'
        link_groups_content = ''
        for link_group in self.link_groups:
            link_groups_content += link_group.to_string(config)
        return template.replace("@LINK_GROUPS", link_groups_content)

class Consumer:
    def __init__(self):
        self.homer_model = HomerModel()

    def process_line(self, line):
        trim_line = line.strip()
        is_empty = trim_line == ""

        if (is_empty):
            return

        orig_tokens = trim_line.split(",")
        tokens = list(map(lambda t: t.strip(), orig_tokens))
        is_link_group = len(tokens) == 1

        if (is_link_group):
            name = tokens[0]
            self.homer_model.add_link_group(name)
        else:
            name = tokens[0]
            url = tokens[1]
            self.homer_model.add_link(name, url)

    def process_file(self, file):
        for line in file:
            self.process_line(line)

    def get_homer_model(self):
        return self.homer_model

class ContentWriter:
    def __init__(self, config):
        self.main_template_file = config.main_template_file
        self.output_file = config.output_file

    def write(self, homer_model):
        token = Token("@HOMER_MODEL", homer_model.to_string(config))
        content = Stamper().stamp(self.main_template_file, [token])

        try:
            with open(self.output_file, 'w') as file:
                file.write(content)

        except Exception as e:
            print(f"An error occurred: {e}")

# ----------------------------
#

config = Config()
file = open('links.txt','r')

consumer = Consumer()
consumer.process_file(file)

homer_model = consumer.get_homer_model()

content_writer = ContentWriter(config)
content_writer.write(homer_model)

print("TRACER OK.")
