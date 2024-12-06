import pandas as pd

class PandasReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.encoding = 'utf-8'
        self.windows_encoding = 'windows-1251'


    def read(self):
        """
        Reads a CSV file and returns a DataFrame.
        
        Returns:
            pd.DataFrame: DataFrame with the data from the CSV file.

        """
        rows_to_skip = 5
        try:
            return pd.read_csv(
                self.file_path, 
                encoding=self.encoding, 
                header=None,
                skiprows=rows_to_skip,
                skipfooter=1,
            )
        except UnicodeDecodeError:
            print("Error: utf-8 encoding not working. Trying windows-1251 encoding")
            # skip the first row
            return pd.read_csv(
                self.file_path, 
                encoding=self.windows_encoding,
                header=None,
                skiprows=rows_to_skip,
                skipfooter=1,
            )
        except Exception as e:
            return str(e)
        

    @staticmethod
    def count_numbers(row):
        """
        Counts the number of non-null values in a row.

        Args:
            row (pd.Series): Row of a DataFrame.

        Returns:
            int: Number of non-null values.
        """
        count = 0
        print(row)
        for val in row:
            print(val)
            if not pd.isnull(val):
                count += 1
        print(count)
        return count


    def find_essential_start(self, df, n):
        """
        Finds the index of the first row with at least n non-null values.
        
        Args:
            df (pd.DataFrame): DataFrame with the data.
            n (int): Minimum number of non-null values.

        Returns:
            int: Index of the first row with at least n non-null values.

        """
        return 0


    def extract_essential(self, df, start_index):
        """
        Extracts rows starting from the specified index.

        Args:
            df (pd.DataFrame): DataFrame with the data.
            start_index (int): Index to start extracting from.

        Returns:
            pd.DataFrame: DataFrame with the extracted rows.

        """
        return df[start_index:] if df is not None else None


    @staticmethod
    def extract_columns(df, col_indices):
        """
        Extracts specified columns from a DataFrame.

        Args:
            df (pd.DataFrame): DataFrame with the data.
            col_indices (list): List of column indices to extract.

        Returns:
            pd.DataFrame: DataFrame with the extracted columns.

        """
        # Разбиваем строки на отдельные колонки по разделителю
        split_df = df.iloc[:, 0].str.split(';', expand=True)
        
        # Извлекаем указанные колонки
        extracted_df = split_df.iloc[:, col_indices]
        
        return extracted_df
    

    @staticmethod
    def substract_columns(df, col1, col2):
        """
        Subtracts values of two columns in a DataFrame.

        """
        new_column = df[col1] - df[col2]
        return new_column
    
    @staticmethod
    def dataframe_to_list(df):
        """
        Converts a DataFrame to a list of lists.

        Args:
            df (pd.DataFrame): DataFrame to convert.

        Returns:
            list: List of lists.
        """
        return df.values.tolist()
    

    @staticmethod
    def check_for_strings(df):
        """
        Checks for string values in a DataFrame and prints them.

        Args:
            df (pd.DataFrame): DataFrame

        """
        for column in df.columns:
            string_values = df[df[column].apply(lambda x: isinstance(x, str))]
            if not string_values.empty:
                pass


    @staticmethod
    def convert_strings_to_floats(df):
        """
        Converts string values in a DataFrame to floats.

        Args:
            df (pd.DataFrame): DataFrame

        Returns:
            pd.DataFrame: DataFrame with converted values.

        """
        return df.apply(pd.to_numeric, errors='coerce')

