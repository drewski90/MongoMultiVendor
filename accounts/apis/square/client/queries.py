from typing import List

def add_text_filter(fuzzy:str=None, exact:str=None):
  entry = {}
  if exact:
    entry['exact'] = exact
  if fuzzy:
    entry['fuzzy'] = fuzzy
  return entry

def add_value_rule_filter(values:List[str], include_values=True):
  rule = 'INCLUDE' if include_values else "EXCLUDE"
  return {
    "values": dict(values),
    "rule": rule
  }

def add_date_range_filter(start:str=None, end:str=None):
  entry = {}
  if start:
    entry['start'] = start
  if end:
    entry['end'] = end
  return entry

def add_value_filter(
  all:List[str], 
  any:List[str], 
  none:List[str]
  ):
  entry = {}
  if all:
    entry['all'] = all,
  if any:
    entry['any'] = any,
  if none:
    entry['none'] = none
  return entry