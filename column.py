import pandas as pd


class Column:
    '''Details the requirements of an individual column of a DataFrame
    Parameters
    ----------
    col_type : type
        Specifies desired column type, if any. One of "string", "float", "integer"
        Uses infer_type until I can think of a better solution
        https://pandas.pydata.org/docs/reference/api/pandas.api.types.infer_dtype.html
    allow_missing : bool
        Can this column contain missing values
    allow_duplicates : bool
        Can this column conatin duplicate values
    one_of : list
        A list that designates the only values the column is allowed
    starts_with : str
        A string that the column must start with
    pattern : str
        A regex pattern that the data must conform to
    '''
    def __init__(self, name, col_type=None, allow_missing=True, allow_duplicates=True, one_of=None, starts_with=None, pattern=None):
        self.name = name
        self.col_type = col_type
        self.missing = allow_missing
        self.duplicates = allow_duplicates
        self.one_of = one_of
        self.starts = starts_with
        self.pattern = pattern

        # A place to capture violations of the Column schema
        self.violations = {"col_type": None, "missing": None,
                           "duplicates": None, "one_of": None,
                           "starts": None, "pattern": None}

    def eval_col_type(self, column):
        '''Compares infered column type to expected column type'''
        guess = pd.api.types.infer_dtype(column)
        same = guess == self.col_type

        self.violations["col_type"] = [1 if same else 0]

    def eval_missing(self, column):
        '''Identifies indices of missing data'''
        nulls = column.isnull()
        ind = column[nulls].index
        if not ind.empty:
            self.violations["missing"] = list(ind)

    def eval_duplicates(self, column):
        '''Identifies indices of duplicated data (Missing Values Count as Duplicates)'''
        dups = column.duplicated(keep=False)
        ind = column[dups].index
        if not ind.empty:
            self.violations["duplicates"] = list(ind)

    def eval_one_of(self, column):
        '''Identifies which indices do NOT contain one of self.one_of'''
        contains = ~ column.isin(self.one_of).astype(bool)
        ind = column[contains].index
        if not ind.empty:
            self.violations["one_of"] = list(ind)

    def eval_starts(self, column):
        '''Identifies which indices do NOT start with self.starts'''
        starts = ~ column.str.startswith(self.starts).astype(bool)
        ind = column[starts].index
        if not ind.empty:
            self.violations["starts"] = list(ind)

    def eval_pattern(self, column):
        '''Identifies which indices violates the provided regex self.pattern'''
        pattern = ~ column.str.fullmatch(self.pattern).astype(bool)
        ind = column[pattern].index
        if not ind.empty:
            self.violations["pattern"] = list(ind)

    def eval(self, column):
        '''Runs all applicable evaluations on the column and saves violations to warning'''

        if self.col_type is not None:
            self.eval_col_type(column)

        if not self.missing:
            self.eval_missing(column)

        if not self.duplicates:
            self.eval_duplicates(column)

        if self.one_of is not None:
            self.eval_one_of(column)

        if self.starts is not None:
            self.eval_starts(column)

        if self.pattern is not None:
            self.eval_pattern(column)

        return self.violations
