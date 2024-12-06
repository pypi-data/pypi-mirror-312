import matplotlib.pyplot as plt

class PlotBuilder:

    @staticmethod
    def get_graph_image(x, y, title, x_label, y_label, output_path):
        """
        Create a graph.

        Args:
            x (list): List of x values.
            y (list): List of y values.
            title (str): Title of the graph.
            x_label (str): Label for the x axis.
            y_label (str): Label for the y axis.
            output_path (str): Path to save the graph image.

        """
        plt.plot(x, y)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid()
        plt.savefig(output_path)
        plt.close()

    
    @staticmethod
    def get_graph_image_with_lines(x, y, title, x_label, y_label, output_path, lines_coords):
        """
        Create a graph with lines.
        
        Args:
            x (list): List of x values.
            y (list): List of y values.
            title (str): Title of the graph.
            x_label (str): Label for the x axis.
            y_label (str): Label for the y axis.
            output_path (str): Path to save the graph image.
            lines_coords (list[dict]): List of dictionaries with line coordinates.

        """
        plt.plot(x, y)
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid()
        colors = ['r', 'g', 'b', 'y', 'm', 'c']
        for line_coords in lines_coords:
            plt.axline((line_coords["x_0"], line_coords["y_0"]), (line_coords["x_1"], line_coords["y_1"]), color=colors.pop(0))
        plt.savefig(output_path)
        plt.close()