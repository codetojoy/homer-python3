
class LinkGroup:
    def __init__(self, name):
        self.name = name
        self.links = []

    def add_link(self, link):
        self.links.append(link) 

    def to_string(self):
        result = "<div class=\"my-item\">\n"
        result += "<h3>" + self.name + "</h3>\n"
        result += "<div>\n"
        for link in self.links:
            result += link.to_string()
        result += "</div>\n"
        result += "</div>\n"
        return result

class Link:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def to_string(self):
        template = '<a class="link" href="@URL">@NAME</a><br/>\n'
        return template.replace("@URL", self.url).replace("@NAME", self.name)

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

    def to_string(self):
        result = '<div class="my-items">\n'
        for link_group in self.link_groups:
            result += link_group.to_string()
        result += '</div>\n'
        return result

class Consumer:
    def __init__(self):
        self.homer_model = HomerModel()

    def process_line(self, line):
        trim_line = line.strip()
        is_empty = trim_line == ""

        if (is_empty):
            return

        tokens = line.split(",")
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
    def __init__(self, template_file, output_file):
        self.template_file = template_file
        self.output_file = output_file

    def write(self, homer_model):
        try:
            with open(self.template_file, 'r') as file:
                content = file.read()

            placeholder = "@HOMER_MODEL"
            value = homer_model.to_string()
            content = content.replace(placeholder, value)

            with open(self.output_file, 'w') as file:
                file.write(content)

        except Exception as e:
            print(f"An error occurred: {e}")

# ----------------------------
#

file = open('links.txt','r')

consumer = Consumer()
consumer.process_file(file)

homer_model = consumer.get_homer_model()

content_writer = ContentWriter('resources/main.template.html', 'index.html')
content_writer.write(homer_model)

print("TRACER OK.")