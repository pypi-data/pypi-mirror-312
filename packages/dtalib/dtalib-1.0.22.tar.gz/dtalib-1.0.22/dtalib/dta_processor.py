
try:
    from pandas_reader import PandasReader
    from plot_builder import PlotBuilder
    from float_list_helper import FloatListHelper
except ImportError:
    from .pandas_reader import PandasReader
    from .plot_builder import PlotBuilder
    from .float_list_helper import FloatListHelper
    
import os

class DtaProcessor:
    def __init__(self, csv_file_path, model_colunm_index, 
            experimental_data_column_index, output_dir_path):
        self.csv_file_path = csv_file_path
        self.model_colunm_index = model_colunm_index
        self.experimental_data_column_index = experimental_data_column_index

        self.model_colunm_index = model_colunm_index
        self.experimental_data_column_index = experimental_data_column_index
        self.output_dir_path = output_dir_path


    def process(self):
        # Get model and difference lists
        model_list, difference_list = self.get_model_and_difference_lists()

        PlotBuilder.get_graph_image(
            model_list,
            difference_list,
            "Model vs Experimental Data",
            "Model",
            "Difference",
            os.path.join(self.output_dir_path, "model_vs_experimental_data.png")
        )

        line_1_coords = DtaProcessor.get_line_1_coords(model_list, difference_list)
        line_2_coords = DtaProcessor.get_line_2_coords(model_list, difference_list)

        PlotBuilder.get_graph_image_with_lines(
            model_list,
            difference_list,
            "Model vs Experimental Data",
            "Model",
            "Difference",
            os.path.join(self.output_dir_path, "model_vs_experimental_data_with_lines.png"),
            [line_1_coords, line_2_coords]
        )

        print("Line 1 Coords:", line_1_coords)
        print("Line 2 Coords:", line_2_coords)

        intersection_point = DtaProcessor.find_intersection(line_1_coords, line_2_coords)
        print("Intersection Point:", intersection_point)


    def get_line_1_coords(model_list, difference_list):
        max_index, max_val = FloatListHelper.find_max_index(model_list)

        model_list_cropped, difference_list_cropped = \
            FloatListHelper.crop_lists(
                model_list, 
                difference_list, 
                max_index
            )

        start_index = FloatListHelper.find_start_index(model_list_cropped, difference_list_cropped)
        end_index = FloatListHelper.find_end_index(model_list_cropped, difference_list_cropped)
        line_1_coords = {
            "x_0": model_list_cropped[start_index], 
            "y_0": difference_list_cropped[start_index], 
            "x_1": model_list_cropped[end_index], 
            "y_1": difference_list_cropped[end_index]
        }

        return line_1_coords


    def get_line_2_coords(model_list, difference_list):
        max_index, max_val = FloatListHelper.find_max_index(model_list)

        model_list_cropped, difference_list_cropped = \
            FloatListHelper.crop_lists(
                model_list, 
                difference_list, 
                max_index
            )
        
        start_index = FloatListHelper.find_start_index(model_list_cropped, difference_list_cropped, 0.3)
        difference_list_cropped_15 = difference_list_cropped[start_index:]
        model_list_cropped_15 = model_list_cropped[start_index:]
        
        max_index, max_val = FloatListHelper.find_max_index(difference_list_cropped_15)

        difference_list_cropped_2 = difference_list_cropped[start_index:start_index + max_index]
        min_index, min_val = FloatListHelper.find_min_index(difference_list_cropped_2)

        line_2_coords = {
            "x_0": model_list_cropped[start_index + min_index],
            "y_0": difference_list_cropped[start_index + min_index],
            "x_1": model_list_cropped_15[max_index],
            "y_1": difference_list_cropped_15[max_index]
        }

        return line_2_coords
    

    def find_intersection(line1_coords, line2_coords):
        """
        Find the intersection point of two lines.

        Args:
            line1_coords (dict): Dictionary with coordinates of the first line.
            line2_coords (dict): Dictionary with coordinates of the second line.

        Returns:
            tuple: Intersection point coordinates.

        """
        x1, y1 = line1_coords["x_0"], line1_coords["y_0"]
        x2, y2 = line1_coords["x_1"], line1_coords["y_1"]
        x3, y3 = line2_coords["x_0"], line2_coords["y_0"]
        x4, y4 = line2_coords["x_1"], line2_coords["y_1"]

        A1 = y2 - y1
        B1 = x1 - x2
        C1 = A1 * x1 + B1 * y1

        A2 = y4 - y3
        B2 = x3 - x4
        C2 = A2 * x3 + B2 * y3

        determinant = A1 * B2 - A2 * B1

        if determinant == 0:
            return None
        else:
            x = (B2 * C1 - B1 * C2) / determinant
            y = (A1 * C2 - A2 * C1) / determinant
            return (x, y)
        

    def get_model_and_difference_lists(self):
        """
        Get model and difference lists from the csv file.
        
        Returns:
            tuple: Model and difference lists.
            
        """
        pandas_reader = PandasReader(self.csv_file_path)
        pandas_data = pandas_reader.read()

        graph_data = PandasReader.extract_columns(
            pandas_data, 
            [self.model_colunm_index, self.experimental_data_column_index]
        )
        
        PandasReader.check_for_strings(graph_data)

        graph_data_2 = PandasReader.convert_strings_to_floats(graph_data)

        PandasReader.check_for_strings(graph_data_2)

        # Substract model column from experimental data column, adding new column to the data frame
        # and plot the graph
        
        try:
            difference = graph_data_2[self.experimental_data_column_index] - graph_data_2[self.model_colunm_index]
        except KeyError as e:
            print(f"KeyError: {e}")
            # Handle the error or re-raise
            raise

        difference_list = difference.values.tolist()
        model_list = graph_data_2[self.model_colunm_index].values.tolist()

        return model_list, difference_list