import re


class DataUtils:

    @staticmethod
    def headers_depth(headers):
        if not headers:
            return 0
        if isinstance(headers, list) or isinstance(headers, tuple) or isinstance(headers, dict):
            if len(headers) == 0:
                return 1
            else:
                return len(headers[0])
        else:
            return 0

    @staticmethod
    def fill_down(values, regex=r'Unnamed:.*', boot_value='_'):
        """
        Replaces values matching regex pattern with the previous value in the list.
        if the list first value matches regex it will be replaced with boot_value.
        """
        if values is None or not isinstance(values, list) or len(values) == 0:
            return values
        if re.match(regex, values[0]):
            values[0] = boot_value
        for i in range(1, len(values)):
            if re.match(regex, values[i]):
                values[i] = values[i - 1]
        return values

    @staticmethod
    def get_cluster_type(data, selector=None):
        """
        Returns a list of tuples with the type of each attribute in a data frame.
        If the header is a tuple and a selector is passed, just the cluster where the
        first item of the tuple matches the selector is evaluated.
        :param data: source data frame to filter
        :param selector:
        :return: filtered data frame
        """
        if data is None:
            return None
        if selector is None:
            return [(item, str(data[item].dtype)) for item in data.columns]
        return [(*_, str(data[(cluster_name, *_)].dtype)) for cluster_name, *_ in data if (cluster_name == selector)]

    @staticmethod
    def change_object_to_category(data):
        """In a data frame replaces object type by category type."""
        source = data.select_dtypes(include=object)
        target = data.select_dtypes([object]).apply(lambda d_type: d_type.astype('category'))
        data[source.columns] = target

    @staticmethod
    def remove_duplicates(data):
        """
        Removes duplicates from a list preserving the order.
        :param data: list to prune
        :return: pruned list
        """
        return list(dict.fromkeys(data))

    @staticmethod
    def count_missing_values(data_frame):
        """
        Counts missing values for each column in a data frame.
        :param data_frame: data frame
        :return: {column_name: missing_values_count}
        """
        isna_count = {}
        for column in data_frame.columns:
            isna_count[column] = data_frame[column].isna().sum()
            # yield data_frame[column].isna().sum()
        return isna_count

    @staticmethod
    def choose_grid(items, tight=False, **kwargs):
        columns = min(items, 4 + (1 if tight else 0)) if not kwargs.get('columns') else kwargs.get('columns')
        rows = items // columns
        if items > rows * columns:
            rows = rows + 1
        return rows, columns

    @staticmethod
    def remove_tick_marks_1(axis):
        axis.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        axis.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

    @staticmethod
    def get_iterable_first(items):
        return next(iter(items))

    @staticmethod
    def position_window(position=None):
        fig_manager = get_current_fig_manager()
        fig_manager.window.wm_geometry("1528x830+0+0" if position is None else position)
