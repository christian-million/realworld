import pandas as pd


class Schema:
    '''Maps data validation requirements to tabular data
    Parameters
    ----------
    *args : Column
        Instances of the Column class to map columnar requirements
    cross_funcs : list
        List of custom functions to validate data across columns.
        Should accept a dataframe and return a list of indices that are in violation of a given criteria
    nrows : int
        number of rows the data should have (if needed)
    ncols : int
        number of columns the data should have (if needed)
    colnames : list
        List of column names the data should have in the order expected
    '''
    def __init__(self, *args, cross_funcs=None, nrows=None, ncols=None, colnames=None):

        # Capture column schema instances into dictionary
        self.columns = {arg.name: arg for arg in args}

        self.cross_funcs = cross_funcs
        self.nrows = nrows
        self.ncols = ncols
        self.colnames = colnames

        # Stores indices of column schema violations
        self.col_violations = {}

        # Stores indices of crossfunc violations
        self.cross_func_violations = {}

    def eval_nrows(self, data):
        '''If `nrows` is provided, this will evalutate whether data has `nrows` rows'''
        pass

    def eval_ncols(self, data):
        '''If `ncols` is provided, this will evalutate whether data has `ncols` columns'''
        pass

    def eval_colnames(self, data):
        '''If `colnames` is provided, this evaluates whether all column names exist in `data` in the given order'''
        pass

    def eval_crossfuncs(self, data):
        '''Maps each of the provided crossfunctions to the data'''
        for func in self.cross_funcs:
            results = func(data)
            self.cross_func_violations[func.__name__] = results

    def eval_columns(self, data):
        '''Runs each column validation for provided columns'''
        for col_name, col_schema in self.columns.items():
            results = col_schema.eval(data[col_name])
            self.col_violations[col_name] = results

    def eval_meta(self, data):
        '''Evaluates whether the Schema can map appropriately to the data
        Intended to be run before other eval_* methods

        This should:
        - CHeck/Cast to DataFrame
        - Check if column names exist in data
        - Compare column length with self.columns
        - Evaluate which Columns have schema reqs
        - etc...
        '''
        pass

    def validate(self, data):
        '''User facing function that allows user to check data against a schema
        Parameters
        ----------
        data : pd.DataFrame
            The data to validate against a schema
        '''
        self.eval_columns(data)
        self.eval_crossfuncs(data)

    def col_summary(self):
        '''Provides a summary of column schema violations found'''
        out = {}
        for col_name, ind in self.col_violations.items():
            out[col_name] = {name: len(i) if i is not None else 0 for name, i in ind.items()}

        return pd.DataFrame(out)

    def cross_func_summary(self):
        '''Provides a summary of crossfunc schema violations found'''
        out = {}
        for col_name, i in self.cross_func_violations.items():
            out[col_name] = len(i) if i is not None else 0

        return pd.DataFrame(out, index=[0])
