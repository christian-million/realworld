from schema import Schema
from column import Column
from crossfunc import check_functions
import pandas as pd
import numpy as np

# Read in data to evaluate against a pre-defined schema
data = pd.read_excel('import.xlsx', engine='openpyxl')

# Define a schema for the data
# Only needs Columns for which there are specific requirements
curriculum_schema = Schema(
    Column("Course Control Number (CB00)", starts_with="CCC000", allow_missing=False, allow_duplicates=False),
    Column("Course Code (CB01)", pattern="[A-Z]+[0-9]+[A-Z]*"),
    Column("Course Credit Status (CB04)", one_of=['D', 'C', 'N']),
    Column("Course Transfer Status (CB05)", one_of=['A', 'B', 'C']),
    Column("Course Units of Credit Maximum (CB06)", allow_missing=False),
    Column("Course Units of Credit Minimum (CB07)", allow_missing=False),
    Column("Course Basic Skills Status (CB08)", one_of=['B', 'N']),
    Column("SAM Priority Code (CB09)", one_of=['A', 'B', 'C', 'D', 'E']),
    Column("Cooperative Work Experience Education Status (CB10)", one_of=['C', 'N']),
    Column("Course Classification Code (CB11)", one_of=['Y', 'J', 'K', 'L']),
    Column("Course Special Class Status (CB13)", one_of=['S', 'N']),
    Column("Course Prior to College Level (CB21)", one_of=['Y', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']),
    Column("Course Non-Credit Category (CB22)", one_of=['Y', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']),
    Column("Funding Agency Category (CB23)", one_of=['A', 'B', 'Y']),
    Column("Course Program Status (CB24)", one_of=[1, 2]),
    Column("Curriculum Id*", allow_duplicates=False, allow_missing=False, starts_with="C", pattern="^C[A-Z]+-[0-9]+[A-Z]*"),
    cross_funcs=check_functions
)

# Validate the data against the Schema
curriculum_schema.validate(data)

# Show me how many Column Schemas resulted in violations
print(curriculum_schema.col_summary())

# Show me which cross_funcs resulted in violations
print(curriculum_schema.cross_func_summary())

# Give me the indices of column violations for the pattern requirement of the "Curriculum ID*" Column
print(curriculum_schema.col_violations["Curriculum Id*"]["pattern"])

# Give me the indices of crossfunc violations for the `check_subj_num_id` function
print(curriculum_schema.cross_func_violations["check_subj_num_id"])