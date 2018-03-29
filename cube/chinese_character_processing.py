#coding: utf8


import os
import re
import pinyin
# print pinyin.get('你好', format="strip", delimiter=" ")

# 当中文转拼音后生成字符串长度大于15时会自动将转成只取中文拼音首字母(缩短文字长度)
MAX_LENGTH = 15

def clear_end_words(string):
    array = [
        u"（PC站）", u"（android站）", u"（ios）", u"（wap站）", u"系统",
        u"(PC站)", u"(android站)", u"(ios)", u"(wap站)", u"平台",
        u"(ios)", u"(android)", u"(PC)", u"(wap)",
        u"（ios）", u"（android）", u"（PC）", u"（wap）",
        u"(PC站）", u"(ios站)", u"(Android站)", u"(admin站)", u"(iOS站)",
        u"(IOS站)", u"(usimgredis站)"
    ]

    # 剔除数据
    for rep_str in array:
        # pattern = re.compile(rep_str)
        # string = pattern.sub('', string)
        string = string.replace(rep_str, '')

    return string


def clear_words_with_brackets(string):
    """去掉以括号开头Tag"""
    brackets = [u"(", u"（", u"?"]
    for bracket in brackets:
        index = string.rfind(bracket)
        if index != -1:
            string = string[:index]

    return string


def clear_specific_words(string):
    specifics = [u"系统", u"平台", u"项目", u"服务"]
    for specific in specifics:
        string = string.replace(specific, '')

    return string



def clear_zh_brackets(string):
    return string.replace(u'（', '(').replace(u'）', ')')


def convert_to_pinyin(string):
    """转换成拼音"""
    string = clear_zh_brackets(string)
    return pinyin.get(string, format="strip", delimiter="")


def conver_to_short_pinyin(string):
    """转成缩略版本"""
    string = clear_zh_brackets(string)
    string_array = breaking_word(string)
    container = []
    for letter in string_array:
        if letter in ['(', ')']:
            container.append(letter)
        elif 0 <= ord(letter) <= 255:
            container.append(letter)
        else:
            letter_pinyin = pinyin.get(letter, format="strip", delimiter="")
            container.append(letter_pinyin[0])

    return ''.join(container)


def breaking_word(string):
    """字符串"""
    zn_pattern = re.compile(ur'[\u4e00-\u9fa5]|\w|\(|\)')
    return zn_pattern.findall(string)


def main(filepath):
	"""Main portal program"""
    dirpath = os.path.dirname(filepath)
    name, ext = os.path.splitext(os.path.basename(filepath))
    output_filepath = os.path.join(dirpath, "%s_out.%s" % (name, ext))

    with open(filepath, 'r') as fin:
        list_rows = fin.readlines()

    if not list_rows:
        print 'filepath: %s has no rows' % filepath
        return

    with open(output_filepath, 'w') as fout:
        for row in list_rows:
            # print row
            original_cmdb_item_name = row.strip().decode('gbk')

            cmdb_item_name = clear_words_with_brackets(original_cmdb_item_name)
            cmdb_item_name = clear_specific_words(cmdb_item_name)
            cmdb_item_name = clear_end_words(cmdb_item_name)

            cmdb_convert_to_pinyin = convert_to_pinyin(cmdb_item_name)
            if len(cmdb_convert_to_pinyin) >= MAX_LENGTH:
                cmdb_convert_to_short_pinyin = conver_to_short_pinyin(cmdb_item_name)
            else:
                cmdb_convert_to_short_pinyin = cmdb_convert_to_pinyin

            unit_items = [original_cmdb_item_name, cmdb_item_name, cmdb_convert_to_pinyin, cmdb_convert_to_short_pinyin]
            unit_items = [x.encode('utf-8') for x in unit_items]

            new_line = "\t".join(unit_items) + "\n"
            fout.write(new_line)


if __name__ == "__main__":
	# 待转文件列表
    filepath_list = [
        r"cmdb-idc_1.txt",
        r"cmdb-itemname_1.txt"
    ]

    for filepath in filepath_list:
        main(filepath)
