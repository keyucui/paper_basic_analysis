# paper_basic_analysis
该项目主要用于批量对论文进行分析，包括pdf转换、参考文献期刊分布、词频与关键词分析(暂未整理上传)等

## 说明
- 根据目标期刊(如管理学UT/DALLAS 24)，批量计算各篇论文的参考文献的组成并生成统计表格。如，某MISQ论文的参考文献有10篇来自MISQ，5篇来自ISR，2篇来自JOC。
- journal_list.txt 文件是需要的目标期刊列表，每行代表一个期刊全称(或论文中可能出现的缩写)
- 运行 parse_reference_and_count.py 即可生成论文pdf转化后的txt文件和参考文献组成统计表格

## 安装项目需要的库，主要是用于pdf转换的pdfminer库
> pip install -r requirements.txt



