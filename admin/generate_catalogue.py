import xml.etree.ElementTree as ET
import uuid
import requests
import re


def replace_image(match):
    # 获取匹配到的原始图片名称
    original_image_url = match.group(1)[1:]
    print("下载图片:", original_image_url)

    # 生成 UUID 作为新的图片名称
    image_name = str(uuid.uuid4()) + '.png'
    save_path = 'image/' + image_name

    # 下载图片
    response = requests.get(original_image_url)
    with open(save_path, "wb") as f:
        f.write(response.content)
    return f'![](../../image/{image_name}'


# 解析XML文件
tree = ET.parse('cnblogs.xml')
root = tree.getroot()

# 找到并获取<title type="text">标签中的内容
count = 1
# 定义正则表达式模式
pattern = r'!\[\](.+\.png)'

for entry_elem in root.findall('entry'):
    title = entry_elem.find('title').text.encode('utf-8').decode('utf-8')
    content = entry_elem.find('content').text.encode('utf-8').decode('utf-8')

    print(f'开始编辑文件：{title}')

    new_md_content = re.sub(pattern, replace_image, content)

    with open(f'notes/java/{title[:-4]}.md', 'w', encoding='utf-8') as f:
        # 写入Markdown文件
        f.write(new_md_content)
        f.write('\n')
    count += 1
print(f'自动化操作完成！一共{count}个文件')
