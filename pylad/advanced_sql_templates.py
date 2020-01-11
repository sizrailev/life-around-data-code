#===============================================================================
# MIT License
#
# Copyright (c) 2019-2020 Sergei Izrailev
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
Examples for the blog on advanced SQL templates in Python using JinjaSql
'''

import os

from pylad.sql_templates_base import apply_sql_template

# A single dimension template
_BASIC_STATS_TEMPLATE = '''
select
    {{ dim | sqlsafe }}
    , count(*) as num_transactions
    , sum(amount) as total_amount
    , avg(amount) as avg_amount
from
    transactions
group by
    {{ dim | sqlsafe }}
order by total_amount desc
'''

# Apply the template
params = {
    'dim': 'payment_method'
}
print(apply_sql_template(_BASIC_STATS_TEMPLATE, params))


# Multiple columns joined outside of the template:
def get_basic_stats_sql(dimensions):
    '''
    Returns the sql computing the number of transactions,
    as well as the total and the average transaction amounts
    for the provided list of column names as dimensions.
    '''
    params = {
      'dim': '\n    , '.join(dimensions)
    }
    return apply_sql_template(_BASIC_STATS_TEMPLATE, params)


print(get_basic_stats_sql(['store_id', 'payment_method']))

dimension_lists = [
    ['user_id'],
    ['store_id'],
    ['payment_method'],
    ['store_id', 'payment_method'],
]

dimension_queries = [get_basic_stats_sql(dims) for dims in dimension_lists]


# Set a variable inside the template
_PRESET_VAR_STATS_TEMPLATE = '''
{% set dims = '\n    , '.join(dimensions) %}
select
    {{ dims | sqlsafe }}
    , count(*) as num_transactions
    , sum(amount) as total_amount
    , avg(amount) as avg_amount
from
    transactions
group by
    {{ dims | sqlsafe }}
order by total_amount desc
'''


def get_preset_stats_sql(dimensions):
    '''
    Returns the sql computing the number of transactions,
    as well as the total and the average transaction amounts
    for the provided list of column names as dimensions.
    '''
    params = {
      'dimensions': dimensions
    }
    return apply_sql_template(_PRESET_VAR_STATS_TEMPLATE, params)


print(get_preset_stats_sql(['store_id', 'payment_method']))

# Using loops
_LOOPS_STATS_TEMPLATE = '''
select
    {{ dimensions[0] | sqlsafe }}\
    {% for dim in dimensions[1:] %}
    , {{ dim | sqlsafe }}{% endfor %}
    , count(*) as num_transactions
    , sum(amount) as total_amount
    , avg(amount) as avg_amount
from
    transactions
group by
    {{ dimensions[0] | sqlsafe }}\
    {% for dim in dimensions[1:] %}
    , {{ dim | sqlsafe }}{% endfor %}
order by total_amount desc
'''


def get_loops_stats_sql(dimensions):
    '''
    Returns the sql computing the number of transactions,
    as well as the total and the average transaction amounts
    for the provided list of column names as dimensions.
    '''
    params = {
      'dimensions': dimensions
    }
    return apply_sql_template(_LOOPS_STATS_TEMPLATE, params)


print(get_loops_stats_sql(['store_id', 'payment_method']))


def strip_blank_lines(text):
    '''
    Removes blank lines from the text, including those containing only spaces.
    https://stackoverflow.com/questions/1140958/whats-a-quick-one-liner-to-remove-empty-lines-from-a-python-string
    '''
    return os.linesep.join([s for s in text.splitlines() if s.strip()])


_LOOPS_STATS_TEMPLATE = '''
select
    {{ dimensions[0] | sqlsafe }}
    {% for dim in dimensions[1:] %}
    , {{ dim | sqlsafe }}
    {% endfor %}
    , count(*) as num_transactions
    , sum(amount) as total_amount
    , avg(amount) as avg_amount
from
    transactions
group by
    {{ dimensions[0] | sqlsafe }}
    {% for dim in dimensions[1:] %}
    , {{ dim | sqlsafe }}
    {% endfor %}
order by total_amount desc
'''

# Formatted without blank lines
print(strip_blank_lines(get_loops_stats_sql(['store_id', 'payment_method'])))


# Custom dimensions and looping over a dictionary
custom_dimensions = {
    'store_id': 'store_id',
    'card_or_cash': "case when payment_method = 'cash' then 'cash' else 'card' end",
}

_CUSTOM_STATS_TEMPLATE = '''
{% set dims = '\n    , '.join(dimensions.keys()) %}
select
    sum(amount) as total_amount
    {% for dim, def in dimensions.items() %}
    , {{ def | sqlsafe }} as {{ dim | sqlsafe }}
    {% endfor %}
    , count(*) as num_transactions
    , avg(amount) as avg_amount
from
    transactions
group by
    {{ dims | sqlsafe }}
order by total_amount desc
'''


def get_custom_stats_sql(dimensions):
    '''
    Returns the sql computing the number of transactions,
    as well as the total and the average transaction amounts
    for the provided list of column names as dimensions.
    '''
    params = {
      'dimensions': dimensions
    }
    return apply_sql_template(_CUSTOM_STATS_TEMPLATE, params)


print(strip_blank_lines(get_custom_stats_sql(custom_dimensions)))
print(strip_blank_lines(
    apply_sql_template(template=_CUSTOM_STATS_TEMPLATE,
                       parameters={'dimensions': custom_dimensions})))


# Using custom functions
def transform_dimensions(dimensions: dict) -> str:
    '''
    Generate SQL for aliasing or transforming the dimension columns.
    '''
    return '\n    , '.join([
        '{val} as {key}'.format(val=val, key=key)
        for key, val in dimensions.items()
    ])


print(transform_dimensions(custom_dimensions))

_FUNCTION_STATS_TEMPLATE = '''
{% set dims = '\n    , '.join(dimensions.keys()) %}
select
    {{ transform_dimensions(dimensions) | sqlsafe }}
    , sum(amount) as total_amount
    , count(*) as num_transactions
    , avg(amount) as avg_amount
from
    transactions
group by
    {{ dims | sqlsafe }}
order by total_amount desc
'''

print(strip_blank_lines(
    apply_sql_template(template=_FUNCTION_STATS_TEMPLATE,
                       parameters={'dimensions': custom_dimensions},
                       func_list=[transform_dimensions])))
