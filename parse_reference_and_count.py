import sys
import os
import logging

from tqdm import tqdm
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


logging.getLogger().setLevel(logging.ERROR)  # 忽略警告

def parse_and_count(path, save_folder='pdf2txts/', journal_path='journal_list.txt', csv=None):
    """
    解析论文 pdf文件， 生成对应 txt文件，并计算该论文的引文有多少属于目标期刊(由 journal_list.txt 自己设定)
    :param path:    pdf文件路径
    :param save_folder:     保存文件夹名
    :param journal_path:    目标期刊列表文件路径 (txt文件)
    :return:
    """
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    fp = open(path, 'rb')
    praser = PDFParser(fp)
    doc = PDFDocument()
    praser.set_document(doc)
    doc.set_parser(praser)
    doc.initialize()

    # 检测文档是否提供txt转换，不提供就忽略
    if not doc.is_extractable:
        raise PDFTextExtractionNotAllowed
    else:
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)

        # 循环遍历列表，每次处理一个page的内容
        save_path = save_folder + path.split('.')[0].split('/')[-1] + '.txt'

        results = []
        with open(save_path, 'w+', encoding='utf-8') as f:
            for page in doc.get_pages():  # doc.get_pages() 获取page列表

                interpreter.process_page(page)
                layout = device.get_result()
                for x in layout:
                    if isinstance(x, LTTextBoxHorizontal):
                        text = x.get_text()
                        # print([results])
                        results.append(text.replace('\n', ' '))
                        f.write(text.replace('\n', ' '))

        article = ''.join(results)

        # 截取reference之后
        refer_loc = 0  # reference在文章中对应的index
        try:
            refer_loc = article.index('References')
        except:
            try:
                refer_loc = article.index('REFERENCES')
            except:
                try:
                    refer_loc = article.index('Reference')
                except:
                    try:
                        refer_loc = article.index('REFERENCE')
                    except:
                        refer_loc = 0

        # print(article.index('References'))
        journal_list = load_journals(journal_path)
        counts = []
        for journal in journal_list:
            count = article[refer_loc:].replace(' ', '').count(journal.replace(' ', ''))
            count = solve_journal_repetition(journal, article, refer_loc, count)
            counts.append(str(count))
            # if count > 0:
            #     print(journal, count)
        write_line = path.split('.')[0].split('/')[-1].replace(',', ' ') + ',' + ','.join(counts)
        csv.write(write_line + '\n')


def load_journals(journal_path='journal_list.txt'):
    """
    加载期刊列表
    :param journal_path:   需要的期刊列表的文件路径
    :return:   期刊列表
    """
    journals = []
    for line in open(journal_path, 'r', encoding='utf-8'):
        journals.append(line.strip('\n'))
    return journals


def solve_journal_repetition(journal, article, refer_loc, count):
    """
    为了处理Journal of Marketing Research 和 Journal of Marketing 这种字段有重复的期刊，使其不重复计数
    :param journal:     期刊名称
    :return:    处理后的数量
    """
    if journal == 'Journal of Marketing':
        count -= article[refer_loc:].replace(' ', '').count('Journal of Marketing Research'.replace(' ', ''))
    elif journal == 'J. Marketing':
        count -= article[refer_loc:].replace(' ', '').count('J. Marketing Res.'.replace(' ', ''))

    return count


if __name__ == '__main__':
    folder = '2019-2020/'   # 作者的测试文件夹为 2019-2020  即2019-2020年的文献集
    subfolders = os.listdir(folder)
    print(subfolders)
    # subfolder = subfolders[1]

    subfolder = 'MISQ'    # 子文件夹名(某子论文集), 我只上传了MISQ期刊的部分论文集作为例子(10篇)

    files = os.listdir(folder + subfolder)

    with open(subfolder + '.csv', 'w+') as csv:
        csv.write(
            'article,' + ','.join(open('journal_list.txt', 'r', encoding='utf-8').readlines()).replace('\n', '') + '\n')
        for file in tqdm(files):
            # print(folder + subfolder + '/' + file)
            parse_and_count(path=folder + subfolder + '/' + file, save_folder='2019-2020/' + subfolder + 'txt/',
                            journal_path='journal_list.txt',
                            csv=csv)
