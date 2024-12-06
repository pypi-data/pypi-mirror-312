import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from dtalib import DtaProcessor

def main():
    dta_processor = DtaProcessor(
        csv_file_path="data/test_data_5.csv", 
        model_colunm_index=17,
        experimental_data_column_index=16,
        output_dir_path="data"
    )

    dta_processor.process()

if __name__ == "__main__":
    main()