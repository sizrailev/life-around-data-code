# https://stackoverflow.com/questions/53645882/pandas-merging-101
# https://stackoverflow.com/questions/1299871/how-to-join-merge-data-frames-inner-outer-left-right
import numpy as np
import pandas as pd

np.random.seed(0)
left = pd.DataFrame({'transaction_id': ['A', 'B', 'C', 'D'],
                     'user_id': ['Peter', 'John', 'John', 'Anna'],
                     'value': np.random.randn(4),
                     })

right = pd.DataFrame({'user_id': ['Paul', 'Mary', 'John', 'Anna'],
                      'favorite_color': ['blue', 'blue', 'red', np.NaN],
                     })

left.merge(right, on='user_id', how='left')
left.merge(right, on='user_id', how='left', indicator=True)
left.merge(right.rename({'user_id': 'user_id_r'}, axis=1),
           left_on='user_id', right_on='user_id_r', how='left')

# this doesn't work
left.join(right, rsuffix='_r', how='left')

# set the index for user_id first
left1 = left.set_index('user_id', drop=False)
right1 = right.set_index('user_id', drop=False)
left1.join(right1, rsuffix='_r', how='left')
