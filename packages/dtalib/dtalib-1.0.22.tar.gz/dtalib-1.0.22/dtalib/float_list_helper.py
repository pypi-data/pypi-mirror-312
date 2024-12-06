

class FloatListHelper:
    @staticmethod
    def crop_lists(x, y, start_index):
        """
        Crop lists to the same length starting from the specified index.

        Args:
            x (list): List of x values.
            y (list): List of y values.
            start (int): Index to start cropping from.

        Returns:
            tuple: Cropped lists.

        """
        x_cropped = x[start_index:]
        y_cropped = y[start_index:]

        return x_cropped, y_cropped
    
    def find_max_index(lst):
        """
        Find the index of the maximum value in the list.

        Args:
            lst (list): List of float values.

        Returns:
            int: Index of the maximum value.
        """
        return lst.index(max(lst)), max(lst)
    

    def find_min_index(lst):
        """
        Find the index of the minimum value in the list.

        Args:
            lst (list): List of float values.

        Returns:
            int: Index of the minimum value.
        """
        return lst.index(min(lst)), min(lst)
    

    @staticmethod
    def find_end_index(x, y):
        """
        Find the index of the end of the list.

        Args:
            x (list): List of x values.
            y (list): List of y values.

        Returns:
            int: Index of the end of the list.
        """
        return len(x) - 1
    
    
    def find_start_index(x_cropped, y_cropped, coefficient=0.75):
        """
        Find the index of the start of the list.

        Args:
            x_cropped (list): List of x values.
            y_cropped (list): List of y values.
            coefficient (float): Coefficient to estimate the start index.

        Returns:
            int: Index of the start of the list.

        """
        
        min_x = min(x_cropped)
        max_x = max(x_cropped)

        estimated_start = min_x + (max_x - min_x) * coefficient

        start_index, start_val = FloatListHelper.find_closest_index(x_cropped, estimated_start)

        return start_index


    def find_closest_index(lst, value):
        """
        Find the index of the closest value in the list.

        Args:
            lst (list): List of float values.
            value (float): Value to find.

        Returns:
            int: Index of the closest value.

        """
        return min(range(len(lst)), key=lambda i: abs(lst[i] - value)), min(lst, key=lambda x:abs(x-value))