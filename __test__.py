import json

# TODO:
# Read file
# Clean file
# Explore structure


def cleanFile():
    definition_file = open("./definition/event-scheduler.js")
    lines = definition_file.readlines()
    definition = open("./definition/event-scheduler.json", "w")
    mc = False  # To threat multiline comments

    for line in lines:
        if "/*" in line:
            if "*/" in line:
                print("antes", line)
                line = line[:line.index("/*")] + line[line.index("*/")+2:]
                print("despues", line)
            else:
                mc = True
        elif mc:
            if not "*/" in line:
                continue
            else:
                mc = False
                continue
        else:
            if " //" in line:
                _line = line[:line.index(" //")].strip()
                if bool(_line):
                    line = _line
                else:
                    continue

            line = line.replace("export default", "").replace("};", "}").replace("'", '"')
            definition.writelines(line)

    definition.close()


def readCleanFile(path):
    return json.load(open(path, "r"))


def getRelationTypes(models):
    relations_types = list()
    for m in models.keys():
        relations = models.get(m).get("relations").keys()
        for r in relations:
            if not bool(r in relations_types):
                relations_types.append(r)

    relations_types.sort()
    return relations_types


def createFieldTable(fields):
    '''
    _header = " | " + " | ".join(list(fields.keys())) + " | "
    print("_header", _header)
    '''

    # Extract properties
    _properties = []
    _separator = []
    for f in fields:
        for p in fields.get(f):
            if not bool(p in _properties):
                _properties.append(p)
                _separator.append("---")

    # Create table
    # 1. Header
    header = " | ".join(_properties) + " |"
    separator = "|---|" + "|".join(_separator) + "|"
    rows = ""

    for f in fields:
        rows += "| **_" + f + "_** | "
        for p in _properties:
            value = fields.get(f).get(p)
            if isinstance(value, list):
                for v in value:
                    print(v)
                    rows += " -```" + v + "```<br>"
                rows += " | "
            else:
                rows += "```" + str(value) + "``` | "
        rows += "\n"

    header = "| fieldName | " + header
    print(header)
    print(separator)
    print(rows)

    '''
    m_def.writelines("## " + i + "\n")
    m_def.writelines("```json \n")
    m_def.writelines(json.dumps(model.get(i), sort_keys=True, indent=4) + "\n")
    m_def.writelines("```\n")

    fields = list(model.get(i).keys())
    for f in fields:
        for p in model.get(i).get(f).keys():
            if not bool(p in properties):
                properties.append(p)

    m_def.writelines(" | " + " | ".join(properties) + " | ")
    row = " | "
    print("properties", properties)
    for p in properties:
        _p = model.get(i).get(f).get(p)
        if isinstance(_p, dict) or isinstance(_p, list):
            row += " _obj_ | \n"
        else:
            print(_p + " | ")
    m_def.writelines(row + "\n")
    '''


    return header + "\n" \
           + separator + "\n" \
           + rows + "\n```json \n" \
           + json.dumps(fields, sort_keys=True, indent=4) + "\n```"


def createModelFile(modelName, model):
    print("createModelFile", modelName)
    m_def = open("./docs/models/" + modelName + ".md", "w")

    m_def.writelines("# " + modelName + "\n")

    for i in model.keys():
        m_def.writelines("## " + i + "\n")
        if i == "fields":
            m_def.writelines(createFieldTable(model.get(i)))
        else:
            m_def.writelines("```json \n")
            m_def.writelines(json.dumps(model.get(i), sort_keys=True, indent=4) + "\n")
            m_def.writelines("```\n")

    '''
    for m in _e.keys():
        content_section += "### " + m + "\n"

        for n in _e.get(m):
            content_section += "#### " + n + "\n"
            _n = _e.get(m).get(n)
            if isinstance(_n, dict):
                for o in _n:
                    _o = _n.get(o)
                    content_section += "##### " + o + " \n"
                    content_section += "```json \n"
                    content_section += json.dumps(_o, sort_keys=True, indent=6) + "\n"
                    content_section += "```\n"
            else:
                content_section += "```json \n"
                content_section += json.dumps(_n, sort_keys=True, indent=4) + "\n"
                content_section += "```\n"                
    '''


def createDocFile(definition_path):
    d = readCleanFile(definition_path)
    md_path = "./docs/documentation.md"

    # Get main elements on definition file
    options = d.get("options")
    models = d.get("models")
    modules = d.get("modules")
    sources = d.get("sources")
    locale = d.get("locale")

    # Crear archivo markdown
    md = open(md_path, "w")

    md.writelines("# " + options.get("name") + " (" + options.get("project") + ")\n")

    menu_section = "\n## Contenido\n"
    content_section = "\n"

    for e in d.keys():
        menu_section += "* [" + e.capitalize() + "](#" + e.replace(" ", "-").lower() + ")\n"
        content_section += "## " + e.capitalize() + "\n"
        _e = d.get(e)

        if e != "models":
            content_section += "```json \n"
            content_section += json.dumps(_e, sort_keys=True, indent=4) + "\n"
            content_section += "```\n"
        else:
            for m in _e:
                content_section += "* [" + m + "](./models/" + m + ".md)\n"
                createModelFile(m, _e.get(m))

    menu_section += "\n"
    content_section += "\n"

    md.writelines(menu_section)
    md.writelines(content_section)


def analizeChild(name, content):
    if isinstance(content, str):
        return ""
    elif isinstance(content, dict):
        # print(name, content)
        return {}  # exploreNode(name, content)
    elif isinstance(content, list):
        # print(name, content)
        return exploreNode(name, content)
    elif isinstance(content, bool):
        return content
    else:
        print(type(content))
        return "undefined"


def exploreNode(name, content):
    print(name, content)

    server: [
        {
            "a": "",
            "b": ""
        }
    ]

    if isinstance(content, list):
        arr = []
        for c in content:
            arr.append({})
        print(arr)
        return []


def analizeDefinition(path_file):
    # Read definition file
    _definition = json.load(open(path_file, "r"))
    definition = {}

    for me in _definition:
        if me == "locale":
            definition[me] = {"word": "translation"}
            continue
        elif me == "models":
            models = _definition.get(me)

            model_props = {}
            field_props = {}
            field_relations = {}
            field_validations = []
            #field_val_errors = []
            #field_faker = []

            for m in models:
                model = models.get(m)
                for mk in list(model.keys()):
                    # Save distinct field props
                    if not bool(mk in model_props):
                        model_props[mk] = str(type(model.get(mk)))

                    # Extract props for fields
                    if mk == "fields":
                        field = model[mk]
                        for fp in list(field.keys()):
                            props = field.get(fp)
                            for p in props:
                                # Save distinct field props
                                if not bool(p in field_props):
                                    field_props[p] = str(type(props.get(p)))

                    # Extract props for fields
                    if mk == "relations":
                        relations = model[mk]
                        if bool(relations.keys()):
                            for r in list(relations.keys()):
                                if not bool(r in field_relations):
                                    field_relations[r] = str(type(relations.get(r)))

            print("modelprops", json.dumps(model_props, sort_keys=True, indent=4))
            print("fieldprops", json.dumps(field_props, sort_keys=True, indent=4))
            print("fieldrelations", json.dumps(field_relations, sort_keys=True, indent=4))

        else:
            definition[me] = {}
            parent = _definition.get(me)
        '''
        for ch in parent:
            definition[me][ch] = analizeChild(ch, parent.get(ch))
        '''

    print(definition)


analizeDefinition("./definition/event-scheduler.json")

