import json
import sys
import os

if (len(sys.argv) < 2):
    print("请输入文件路径")
else:
    filePath = sys.argv[1]

    if (not os.path.exists(filePath)):
        print("文件不存在")
    else:
        data = None
        with open(filePath) as f:
            data = json.load(f)

        md = ""

        md += f"# {data['info']['name']}\n\n"

        md += f"> {data['info']['description']}\n\n"

        md += f"## 所有接口\n"

        for item in data['item']:

            if item['request']['method'] == 'GET':

                md += f"### {item['request']['method']} {item['name']}\n"
                md += f"```\n{item['request']['url']['raw']}\n```\n"
                md += f"#### 说明\n"
                md += f"{item['request']['description']}\n\n"
                md += f"#### 参数列表\n"
                md += "| 参数名 | 值 | 说明 |\n"
                md += "| ----- | ----- | ------ |\n"
                for query in item['request']['url']['query']:
                    value = query['value'] if 'value' in query else ""
                    description = query['description'] if 'description' in query else ""
                    md += f"| {query['key']}| {value}|{description}|\n"

            else:
                md += "post not support\n"

        outName = sys.argv[2] if len(sys.argv) > 2 else f"{data['info']['name']}.md"

        with open(outName, 'w') as f:
            f.write(md)
