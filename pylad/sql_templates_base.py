#===============================================================================
# MIT License
#
# Copyright (c) 2019 Sergei Izrailev
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#===============================================================================
# Source: https://github.com/sizrailev/life-around-data-code/blob/master/pylad/
#===============================================================================

'''
Helper functions for parameterizing SQL queries in Python using JinjaSql
'''

from copy import deepcopy

from six import string_types

from jinjasql import JinjaSql

__all__ = ['quote_sql_string', 'get_sql_from_template', 'apply_sql_template',
           'get_column_stats_sql']


def quote_sql_string(value):
    '''
    If `value` is a string type, escapes single quotes in the string
    and returns the string enclosed in single quotes.
    '''
    if isinstance(value, string_types):
        new_value = str(value)
        new_value = new_value.replace("'", "''")
        return "'{}'".format(new_value)
    return value


def get_sql_from_template(query, bind_params):
    '''
    Given a query and binding parameters produced by JinjaSql's prepare_query(),
    produce and return a complete SQL query string.
    '''
    if not bind_params:
        return query
    params = deepcopy(bind_params)
    for key, val in params.items():
        params[key] = quote_sql_string(val)
    return query % params


def apply_sql_template(template, parameters):
    '''
    Apply a JinjaSql template (string) substituting parameters (dict) and return
    the final SQL.
    '''
    j = JinjaSql(param_style='pyformat')
    query, bind_params = j.prepare_query(template, parameters)
    return get_sql_from_template(query, bind_params)


COLUMN_STATS_TEMPLATE = '''
select
    {{ column_name | sqlsafe }} as column_name
    , count(*) as num_rows
    , count(distinct {{ column_name | sqlsafe }}) as num_unique
    , sum(case when {{ column_name | sqlsafe }} is null then 1 else 0 end) as num_nulls
    {% if default_value %}
    , sum(case when {{ column_name | sqlsafe }} = {{ default_value }}
      then 1 else 0 end) as num_default
    {% else %}
    , 0 as num_default
    {% endif %}
    , min({{ column_name | sqlsafe }}) as min_value
    , max({{ column_name | sqlsafe }}) as max_value
from
    {{ table_name | sqlsafe }}
'''


def get_column_stats_sql(table_name, column_name, default_value):
    '''
    Returns the SQL for computing column statistics.
    Passing None for the default_value results in zero output for the number
    of default values.
    '''
    # Note that a string default needs to be quoted first.
    params = {
        'table_name': table_name,
        'column_name': column_name,
        'default_value': quote_sql_string(default_value),
    }
    return apply_sql_template(COLUMN_STATS_TEMPLATE, params)
