import re
import os
import pandas as pd
import datetime
from tabulate import tabulate


class ParseLogException(Exception):...
class LogAnalyzerException(ParseLogException):...



class Tool:

    @staticmethod
    def str2timestamp(time_str):
        return datetime.datetime.strptime(time_str, "%m/%d/%y %H:%M:%S:%f").timestamp()

    @staticmethod
    def df2excel(df: pd.DataFrame, writer: pd.ExcelWriter, sheet_name: str):
        df.to_excel(writer, sheet_name=sheet_name, startrow=0, index=True)
        df_index_len = len(df.index.names) if isinstance(df.index, pd.MultiIndex) else 1
        excel_head_high = 20

        # 获取 xlsxwriter 工作簿和工作表对象
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]

        # 设置一个合理的表头高度
        worksheet.set_row(0, excel_head_high)


        # 根据每列的最大长度动态调整列宽
        for i, column in enumerate(df.columns):
            # 获取列名的长度
            max_length = len(column)
            # 获取该列所有数据的最大长度
            for item in df[column]:
                max_length = max(max_length, len(str(item)))
            # 设置列宽（加上额外的空间 2）
            worksheet.set_column(i+df_index_len, i+df_index_len, max_length + 2)

        # 定义颜色格式
        light_green = workbook.add_format({'bg_color': '#D9EAD3', 'border': 1})  # 浅绿
        light_blue = workbook.add_format({'bg_color': '#B6D7A8', 'border': 1})   # 浅蓝
        light_gray = workbook.add_format({'bg_color': '#D3D3D3', 'border': 1})   # 浅灰

        # 找到数据的有效范围
        num_rows, num_cols = df.shape
        start_row = 1  # 数据开始行（考虑到标题行）
        start_col = df_index_len  # 数据开始列

        # 为有数据的区域设置背景颜色
        for col in range(num_cols):
            for row in range(num_rows):
                if pd.notna(df.iloc[row, col]):  # 检查单元格是否有数据
                    if col % 2 == 0:  # 偶数列
                        worksheet.write(row + start_row, col + start_col, df.iloc[row, col], light_green)
                    else:  # 奇数列
                        worksheet.write(row + start_row, col + start_col, df.iloc[row, col], light_blue)
                else:
                    worksheet.write(row + start_row, col + start_col, "", light_gray)

    @staticmethod
    def df2string(df: pd.DataFrame):
        return tabulate(df, headers='keys', tablefmt='pretty')



class BaseLogAnalyzer:

    def __init__(self, ignore_time):
        self.ignore_time = ignore_time
        self.time_regex = re.compile(r"^\[(?P<time_point>.*?)\].*")


    def _get_time(self, log_line: str):
        matched = re.match(self.time_regex, log_line)
        if not matched:
            raise LogAnalyzerException(f'time not found in "{log_line}"')
        return Tool.str2timestamp(matched.groupdict()['time_point'])



class LogFilter:

    def __init__(self, trait_regex:str):
        self.trait_regex = re.compile(trait_regex)


    def __call__(self, log_path) -> list[str]:
        if not os.path.exists(log_path):
            return []

        with open(log_path, 'r' , errors='ignore') as f:
            lines = [line for line in f if re.match(self.trait_regex, line)]
            return lines



class LogAnalyzer(BaseLogAnalyzer):

    def __init__(self, analytic_regex):
        self.analytic_regex = re.compile(analytic_regex)


    def __call__(self, log_lines: list[str]) -> pd.DataFrame:
        record = []
        for line in log_lines:
            match = re.search(self.analytic_regex, line)
            if match:
                record.append(match.groupdict())
        return pd.DataFrame(record)



class PartRepeatAnalyzer(BaseLogAnalyzer):

    def __init__(self, part_regex, ignore_time=True):
        super(PartRepeatAnalyzer, self).__init__(ignore_time=ignore_time)
        self.part_regex = part_regex

    def __call__(self, log_lines: list[str]) -> pd.DataFrame:
        record = []
        for line in log_lines:
            cols = re.findall(self.part_regex, line)
            if not self.ignore_time:
                cols.insert(0, ("time_point", self._get_time(log_line=line)))
            record.append(dict(cols))
        return pd.DataFrame(record)



class BaseStat:

    def __init__(self):
        self.df: pd.DataFrame = None
        self.df_funs = ["mean", "median", "std"]
        self.unconver_cols= []
        self.excluded_rows = (0, 0)
        self.ignore_cols = []
        self.index_cols = []
        self.decimals = 3
        if "STAT" not in self.index_cols:
            self.index_cols.append("STAT")


    def _exclude_row(self):
        if not self.excluded_rows or len(self.excluded_rows) != 2:
            return
        self.df = self.df.iloc[self.excluded_rows[0]:self.excluded_rows[1]].copy()


    def _ignore(self):
        if self.ignore_cols:
            columns = self.df.columns.to_list()
            columns = [column for column in columns if column not in self.ignore_cols]
            self.df = self.df[columns]


    def _to_numeric(self):
        columns = self.df.columns.to_list()
        if self.unconver_cols:
            columns = [column for column in columns if column not in self.unconver_cols]
        columns = [column for column in columns if column not in self.ignore_cols]
        columns = [column for column in columns if column not in self.index_cols]
        self.df[columns] = self.df[columns].apply(pd.to_numeric, errors='coerce')


    def _stat(self) -> list[pd.DataFrame]:
        stats = []
        for func in self.df_funs:
            self.df["STAT"] = func
            stats.append(
                getattr(self.df.groupby(by=self.index_cols), func)().reset_index()
            )
        return stats


    def _merge(self, stats: list[pd.DataFrame]) -> pd.DataFrame:
        merged = pd.concat(stats, ignore_index=True)
        merged = merged.sort_values(by=self.index_cols)
        merged.set_index(self.index_cols, inplace=True)
        return merged


    def __call__(self, df: pd.DataFrame, df_funs:list=None, unconvertible_cols:list=None, excluded_rows:tuple=None, ignore_cols:list=None, index_cols:list=None, decimals:int=3) -> pd.DataFrame:
        if df_funs:
            self.df_funs = df_funs
        if unconvertible_cols:
            self.unconver_cols = unconvertible_cols
        if excluded_rows:
            self.excluded_rows = excluded_rows
        if ignore_cols:
            self.ignore_cols = ignore_cols
        if index_cols:
            self.index_cols = index_cols
        if decimals:
            self.decimals = decimals
        self.df = df
        self._to_numeric()
        self._ignore()
        self._exclude_row()
        return self._merge(self._stat()).round(self.decimals)