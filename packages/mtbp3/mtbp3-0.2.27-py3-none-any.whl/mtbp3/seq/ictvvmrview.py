#  Copyright (C) 2023-2024 Y Hsu <yh202109@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public license as published by
#  the Free software Foundation, either version 3 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details
#
#  You should have received a copy of the GNU General Public license
#  along with this program. If not, see <https://www.gnu.org/license/>

import pandas as pd
import os
from mtbp3 import util
import warnings
import requests

warnings.simplefilter(action='ignore', category=FutureWarning)
    
class ictvvmr:
    """
    A class to handle ICTV Virus Metadata Resource (VMR) data.

    Attributes:
        vmr_file_path : str
            Path to the VMR file.
        vmr_file_fullpath : str
            Full path to the VMR file.
        vmr_version : str
            Version of the VMR.
        vmr_column_names : list
            List of column names in the VMR.
        vmr : DataFrame
            The VMR data loaded into a pandas DataFrame.

    Methods:
        update_vmr(self, version="current")
            Updates the VMR data by downloading the specified version from the ICTV website.
        make_narrow(vmr)
            Converts the VMR DataFrame to a narrower format by combining certain columns.
        find_rows_given_str(self, search_str="", search_rank="Species", color="", narrow=False, outfmt="simple", exact=False, search_within_subset=None)
            Finds rows in the VMR DataFrame that contain the given search string.
    """

    def __init__(self, vmr_file_path = ""):
        if not isinstance(vmr_file_path, str):
            raise TypeError("vmr_file_path must be a string")

        if vmr_file_path:
            self.vmr_file_path = vmr_file_path
            self.vmr_file_fullpath = vmr_file_path
            self.vmr_version = ""
        else:
            self.vmr_file_path = f'supp_seq/ICTV_VMR_MSL39v4_example.csv'
            self.vmr_file_fullpath = util.get_data(self.vmr_file_path)
            self.vmr_version = "example"

        self.vmr_column_names = []
        self.vmr = self.__load_list()

        if self.vmr is not None:
            self.vmr_column_names = self.vmr.columns.tolist()
            print(f"File {self.vmr_file_path} has been loaded")
            print("Column names:", self.vmr_column_names)
            print("Total number of rows:", len(self.vmr))

    def update_vmr(self, version="current"):
        all_url = {
            "current": "https://ictv.global/vmr/current",
            "39.v4": "https://ictv.global/sites/default/files/VMR/VMR_MSL39.v4_20241106.xlsx",
            "39.v2": "https://ictv.global/sites/default/files/VMR/VMR_MSL39.v2_20240920.xlsx",
            "39.v1": "https://ictv.global/sites/default/files/VMR/VMR_MSL39.v1_20240912.xlsx",
            "38.v3": "https://ictv.global/sites/default/files/VMR/VMR_MSL38_v3.xlsx",
            "38.v2": "https://ictv.global/sites/default/files/VMR/VMR_MSL38_v2.xlsx",
            "38.v1": "https://ictv.global/sites/default/files/VMR/VMR_MSL38_v1.xlsx",
        }
        if version in all_url:
            url = all_url[version]
        else:
            print(f"Version '{version}' is not supported. Supported versions are: {', '.join(all_url.keys())}")
            return

        response = requests.get(url)
        if response.status_code == 200:
            with open("temp.xlsx", "wb") as f:
                f.write(response.content)
            xls = pd.ExcelFile("temp.xlsx")
            sheet_name = next((sheet for sheet in xls.sheet_names if sheet.startswith("VMR")), None)
            if sheet_name is None:
                raise ValueError("No sheet name starting with 'VMR' found in the Excel file.")
            self.vmr = pd.read_excel("temp.xlsx", sheet_name=sheet_name)
            os.remove("temp.xlsx")
            self.vmr_column_names = self.vmr.columns.tolist()
            print(f"File of {version} version has been loaded")
            print("Column names:", self.vmr_column_names)
            print("Total number of rows:", len(self.vmr))/matc
            self.vmr_version = version
        else:
            raise Exception(f"Failed to download file from {url}. Status code: {response.status_code}")


    @staticmethod
    def make_narrow(vmr, method="concatenation"):
        if 'Species' in vmr.columns and 'Genome' in vmr.columns:
            index1 = vmr.columns.get_loc('Species')
            index2 = vmr.columns.get_loc('Genome')
            vmr.iloc[:, index1] = vmr.apply(lambda row: f"{row[index1]} ({row[index2]})" if pd.notna(row[index1]) and pd.notna(row[index2]) else row[index1], axis=1)
        if 'Virus name(s)' in vmr.columns:
            index1 = vmr.columns.get_loc('Virus name(s)')
            vmr.iloc[:, index1] = vmr.iloc[:, index1].str.replace(r'\/', '_', regex=False)
        if 'Virus GENBANK accession' in vmr.columns and 'Genome coverage' in vmr.columns:
            index2 = vmr.columns.get_loc('Virus isolate designation')
            index5 = vmr.columns.get_loc('Genome coverage')
            vmr.iloc[:, index2] = vmr.apply(lambda row: row[index5] if pd.isna(row[index2]) else row[index2], axis=1)
        if 'Virus isolate designation' in vmr.columns:
            index2 = vmr.columns.get_loc('Virus isolate designation')
            vmr.iloc[:, index2] = vmr.iloc[:, index2].str.replace(r'\/', '_', regex=False)
        if 'Virus name(s)' in vmr.columns and 'Virus isolate designation' in vmr.columns and 'Virus GENBANK accession' in vmr.columns and 'Exemplar or additional isolate' in vmr.columns:
            index1 = vmr.columns.get_loc('Virus name(s)')
            index2 = vmr.columns.get_loc('Virus isolate designation')
            index3 = vmr.columns.get_loc('Virus GENBANK accession')
            index4 = vmr.columns.get_loc('Exemplar or additional isolate')
            vmr.iloc[:, index4] = vmr.apply(lambda row: f"[{row[index4]}] {row[index1]} ({row[index2]}) (Genebank: {row[index3]})" if pd.notna(row[index1]) and pd.notna(row[index2]) and pd.notna(row[index3]) else f"[{row[index4]}] {row[index1]} (Genebank: {row[index3]})", axis=1)

        if method == "full":
            vmr = vmr.iloc[:, :-8]
            return vmr
        elif method == "concatenation":
            for col in vmr.columns:
                if col.lower().startswith('sub') and not vmr[col].isna().all():
                    index1 = vmr.columns.get_loc(col[3:].capitalize())
                    index2 = vmr.columns.get_loc(col)
                    vmr.iloc[:, index1] = vmr.apply(lambda row: f"{row[index1]}; [{col}] {row[index2]}" if pd.notna(row[index2]) else row[index1], axis=1)
            vmr = vmr.iloc[:, :-8]
            vmr = vmr.drop(columns=[col for col in vmr.columns if col.lower().startswith('sub')])
        elif method == "drop":
            for col in vmr.columns:
                if col.lower().startswith('sub') and vmr[col].isna().all():
                    vmr = vmr.drop(columns=[col])
            vmr = vmr.iloc[:, :-8]
        else: 
            raise ValueError("Unknown method. Supported methods are 'concatenation' and 'drop'")

        return vmr

    def __load_list(self):
        file_path = self.vmr_file_fullpath
        if os.path.isfile(file_path):
            df = pd.read_csv(file_path)
            return df
        else:
            raise FileNotFoundError(f"File not found: {file_path}")

    def find_rows_given_str(self, search_strings=None, search_rank_or_exemplar="Species", color="", narrow=False, outfmt="simple", exact=False, search_within_subset=None, tree_style="concatenation", start_with_rank=None):
        """
        Find rows in the dataset that match the given search strings.

        Parameters:
            search_strings (list or str): A list of strings or a single string to search for in the dataset.
            search_rank_or_exemplar (str): The rank (or exemplar) to search within (default is "Species"). Can be "all" or one of the column names in the dataset.
            color (str): Color to highlight the search strings in the results (default is "").
            narrow (bool): Whether to narrow the results (default is False).
            outfmt (str): The output format, either "simple" or "tree" (default is "simple").
            exact (bool): Whether to match the search strings exactly (default is False).
            search_within_subset (dict): A dictionary specifying a subset of the dataset to search within (default is None).
            tree_style (str): The style of the tree output if outfmt is "tree" (default is "concatenation").

        Returns:
            pandas.DataFrame or str: The filtered dataset in the specified format. If outfmt is "simple", returns a DataFrame. If outfmt is "tree", returns a string representing the tree structure.

        Raises:
            TypeError: If search_strings is not a list or a string, or if search_within_subset is not a dictionary or None.
            ValueError: If search_strings is empty, or if search_rank is not "all" and not in the column names, or if outfmt is not "simple" or "tree".
        """

        if not (isinstance(search_strings, list) or isinstance(search_strings, str)):
            raise TypeError("search_strings must be a list or a string")
        if not search_strings:
            raise ValueError("search_strings must be a nonempty list or a nonempty string")
        if isinstance(search_strings, str):
            search_strings = [search_strings]
        if search_rank_or_exemplar and search_rank_or_exemplar != "all" and search_rank_or_exemplar not in self.vmr_column_names:
            raise ValueError(f"search_rank_or_exemplar must be 'all' or one of the following: {', '.join(self.vmr_column_names)}")
        if outfmt not in ["simple", "tree"]:
            raise ValueError("outfmt must be 'simple' or 'tree'")
        if search_within_subset is not None and not isinstance(search_within_subset, dict):
            raise TypeError("search_within_subset must be a dictionary or None")

        vmr2 = self.vmr
        if search_within_subset is not None:
            for key, value in search_within_subset.items():
                if key in vmr2.columns and isinstance(value, str) and value:
                    index = vmr2.columns.get_loc(key)
                    vmr2 = vmr2[vmr2.iloc[:, index].str.lower() == value.lower()]

        if search_rank_or_exemplar and search_rank_or_exemplar != "all" and search_rank_or_exemplar not in vmr2.columns:
            raise ValueError(f"search_rank_or_exemplar must be 'all' or one of the following: {', '.join(vmr2.columns[3:19])}")

        if search_rank_or_exemplar == "all":
            if exact:
                filtered_df = vmr2[vmr2.iloc[:, 3:19].apply(lambda row: any(search_str.lower() == element.lower() for element in row.astype(str).values for search_str in search_strings), axis=1)]
            else:
                filtered_df = vmr2[vmr2.iloc[:, 3:19].apply(lambda row: any(search_str.lower() in element.lower() for element in row.astype(str).values for search_str in search_strings), axis=1)]
            if color:
                for col in filtered_df[3:19]:
                    filtered_df[col] = filtered_df[col].apply(lambda row: util.cdt.color_str(row, words=search_strings, colors=color, exact=exact) if pd.notna(row) else row)
        else:
            index = vmr2.columns.get_loc(search_rank_or_exemplar)
            if exact:
                filtered_df = vmr2[vmr2.iloc[:, index].apply(lambda x: any(search_str.lower() == x.lower() for search_str in search_strings) if pd.notna(x) else False)]
            else:
                filtered_df = vmr2[vmr2.iloc[:, index].apply(lambda x: any(search_str.lower() in x.lower() for search_str in search_strings) if pd.notna(x) else False)]
            if color:
                filtered_df.iloc[:, index] = filtered_df.iloc[:, index].apply(lambda row: util.cdt.color_str(row, words=search_strings, colors=color, exact=exact))


        if outfmt == "simple":
            if narrow:
                filtered_df = self.make_narrow(filtered_df, method="drop")
            return filtered_df
        elif outfmt == "tree":
            filtered_df = self.make_narrow(filtered_df, method=tree_style)
            filtered_df = filtered_df.fillna("NA")
            filtered_df = filtered_df.iloc[:, 3:]
            for col in filtered_df.columns[:-1]:
                filtered_df[col] = filtered_df[col].apply(lambda x: f"[{col}] {x}" if pd.notna(x) else x)
            tree_list = []

            for i in range(len(filtered_df.columns)):
                tmp = filtered_df.iloc[:, :i].drop_duplicates()
                tmp['concat'] = tmp.apply(lambda row: "/" + "/".join(row.astype(str)) + "/", axis=1)
                tree_list += tmp['concat'].unique().tolist()
            filtered_df['concat'] = filtered_df.apply(lambda row: "/" + "/".join(row.astype(str)), axis=1)
            tree_list += filtered_df['concat'].unique().tolist()
            tree_list = tree_list[1:]
            tree_list = sorted(tree_list)

            out_tree = util.cdt.ListTree(lst=tree_list)
            return out_tree.list_tree()
        else:
            return

if __name__ == "__main__":
    pass
