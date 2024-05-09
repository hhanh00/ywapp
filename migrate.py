import os
import re
import json

def process_file(dir: str, file: str, meta: dict):
    is_index: bool
    if file.startswith("index") or file.startswith("_index"):
        target = f"{dir}.mdx"
        is_index = True
    else:
        target = f"{file}.mdx"
        is_index = False
    
    front_matter = 2
    title = ""
    weight = 0
    hidden = False
    page = os.path.basename(dir)
    with open(f"{dir}/{file}") as f:
        out = []
        has_callout = False
        for line in f.readlines():
            line = line.strip()
            if line == "---":
                front_matter -= 1
                continue
            if front_matter == 1:
                m = re.match("^title: (.*)$", line)
                if m:
                    title = m.group(1)
                m = re.match("^weight: (.*)$", line)
                if m:
                    weight = int(m.group(1))
                m = re.match("^hidden", line)
                if m:
                    hidden = True
            if front_matter == 0:
                line = re.sub('{{% relref "(.*)" %}}', '/\\1', line)
                m = re.match('{{% notice (.*) %}}', line)
                if m:
                    has_callout = True
                    type = m.group(1)
                    if type != 'note':
                        line = f'<Callout type = "{type}">'
                    else:
                        line = '<Callout>'
                line = re.sub('{{% /notice %}}', '</Callout>', line)
                if is_index:
                    line = re.sub('\((.*\.png)\)', f'(./{page}/\\1)', line)
                else:
                    line = re.sub('\((.*\.png)\)', '(./\\1)', line)
                
                out.append(line)
                out.append('\n')
        if has_callout:
            out.insert(0, 'import { Callout } from "nextra/components"\n')
        with open(target, 'w') as fout:
            fout.writelines(out)
                       
    print(f"{dir} {title} {weight}")
    if is_index:
        page = os.path.basename(dir)
        parent = os.path.dirname(dir)
    else:
        page = file
        parent = dir

    parent_meta: list = meta.get(parent, [])
    if not hidden: 
        parent_meta.append({
            'weight': weight,
            'name': page,
            'title': title,
        })
    meta[parent] = parent_meta

meta = {}            
for root, dirs, files in os.walk('.'):
    print(f"{root} {dirs} {files}")
    for file in files:
        if file.endswith(".md"):
            process_file(root, file, meta)

children: list
for (page, children) in meta.items():
    children.sort(key = lambda p: p['weight'])
    meta = {}
    for c in children:
        meta[c['name']] = c['title']
    if page != '':
        with open(f"{page}/_meta.json", "w") as f:
            f.write(json.dumps(meta, indent=2))