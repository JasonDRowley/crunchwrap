#    _____                            _                                 
#   / ____|                          | |                                
#  | |      _ __  _   _  _ __    ___ | |__ __      __ _ __  __ _  _ __  
#  | |     | '__|| | | || '_ \  / __|| '_ \\ \ /\ / /| '__|/ _` || '_ \ 
#  | |____ | |   | |_| || | | || (__ | | | |\ V  V / | |  | (_| || |_) |
#   \_____||_|    \__,_||_| |_| \___||_| |_| \_/\_/  |_|   \__,_|| .__/ 
#                                                                | |    
#                                                                |_|  
# 
# Crunchwrap: 	A simple pandas wrapper for Crunchbase API v3.1 CSVs
# Version: 		0.1
# Author: 		Jason D. Rowley
# License: 		MIT (See Below)
# 
# 
# 

# 
#     __    _                            
#    / /   (_)____ ___  ___   ___ ___    
#   / /__ / // __// -_)/ _ \ (_-</ -_)   
#  /____//_/ \__/ \__//_//_//___/\__/    
#                                       
# MIT License
# 
# Copyright (c) 2019 Jason D. Rowley
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
# 

#
#     ___                    _                            __     
#    / _ \ ___  ___ _ __ __ (_)____ ___  __ _  ___  ___  / /_ ___
#   / , _// -_)/ _ `// // // // __// -_)/  ' \/ -_)/ _ \/ __/(_-<
#  /_/|_| \__/ \_, / \_,_//_//_/   \__//_/_/_/\__//_//_/\__//___/
#              /_/                                              
# 
# To run this code you will need:
# 	- A fresh copy of the `rounds.csv` 
# 		- Documentation/access instructions can be found here: 
# 		  https://data.crunchbase.com/docs/daily-csv-export
#   - Pandas, and its Python dependencies
# 		- This code works at least as far back as Pandas v0.20.0, but I
# 		  haven't tested it with older versions.
#   - The editor environment of your choice
#       - I personally recommend JupyterLab notebooks
#  

# 
#   _____         __       ____ __              __         __ __              
#  / ___/___  ___/ /___   / __// /_ ___ _ ____ / /_ ___   / // /___  ____ ___ 
# / /__ / _ \/ _  // -_) _\ \ / __// _ `// __// __/(_-<  / _  // -_)/ __// -_)
# \___/ \___/\_,_/ \__/ /___/ \__/ \_,_//_/   \__//___/ /_//_/ \__//_/   \__/ 
#                                                                             

import pandas as pd
rounds = pd.read_csv('~/Downloads/csv_export/funding_rounds.csv', # or whatever filepath
					 low_memory=False, 
					 encoding = "ISO-8859-1")



#
#    ____              __  ____ __                  
#   / __/___  ___  ___/ / / __// /_ ___ _ ___ _ ___ 
#  _\ \ / -_)/ -_)/ _  / _\ \ / __// _ `// _ `// -_)
# /___/ \__/ \__/ \_,_/ /___/ \__/ \_,_/ \_, / \__/ 
#                                       /___/      
#

# Investment types and conditional logic

seed_rounds = rounds[rounds.investment_type == 'seed']
angel_rounds = rounds[rounds.investment_type == 'angel']
preseed_rounds = rounds[rounds.investment_type == 'pre-seed']

venture_noseries_seed = rounds[
    (rounds.investment_type == 'series_unknown') & 
    (rounds.raised_amount_usd <= int(1000000))
    ]

conv_note_seed = rounds[
    (rounds.investment_type == 'convertible_note') & 
    (rounds.raised_amount_usd <= int(1000000))
    ]

venture_undisclosed_seed = rounds[
    (rounds.investment_type == 'undisclosed') & 
    (rounds.raised_amount_usd <= int(1000000))
    ]

equity_crowdfunding_nan = rounds[
    (rounds.investment_type == 'equity_crowdfunding') & 
    (rounds.raised_amount_usd != rounds.raised_amount_usd)
    ]

equity_crowdfunding_seed = rounds[
    (rounds.investment_type == 'equity_crowdfunding') & 
    (rounds.raised_amount_usd <= int(5000000))
    ]

## Stage Aggregation

seed_stage_rounds = pd.concat([
    seed_rounds,
    angel_rounds,
    preseed_rounds,
    venture_noseries_seed,
    conv_note_seed,
    venture_undisclosed_seed,
    equity_crowdfunding_nan,
    equity_crowdfunding_seed
])


#
#    ____            __        ____ __                  
#   / __/___ _ ____ / /__ __  / __// /_ ___ _ ___ _ ___ 
#  / _/ / _ `// __// // // / _\ \ / __// _ `// _ `// -_)
# /___/ \_,_//_/  /_/ \_, / /___/ \__/ \_,_/ \_, / \__/ 
#                    /___/                  /___/       
#

# Investment types and conditional logic

series_a_rounds = rounds[rounds.investment_type == 'series_a']
series_b_rounds = rounds[rounds.investment_type == 'series_b']

venture_noseries_early = rounds[
    (rounds.investment_type == 'series_unknown') & 
    (rounds.raised_amount_usd >= int(1000001)) & 
    (rounds.raised_amount_usd <= int(15000000))
    ]

venture_undisclosed_early = rounds[
    (rounds.investment_type == 'undisclosed') & 
    (rounds.raised_amount_usd >= int(1000001)) & 
    (rounds.raised_amount_usd <= int(15000000))
    ]

equity_crowdfunding_early = rounds[
    (rounds.investment_type == 'equity_crowdfunding') & 
    (rounds.raised_amount_usd >= int(5000001)) & 
    (rounds.raised_amount_usd <= int(15000000))
    ]

conv_note_early = rounds[
    (rounds.investment_type == 'convertible_note') & 
    (rounds.raised_amount_usd >= int(1000001)) & 
    (rounds.raised_amount_usd <= int(15000000))
    ]

conv_note_nan = rounds[
    (rounds.investment_type == 'convertible_note') & 
    (rounds.raised_amount_usd != rounds.raised_amount_usd)
    ]

## Stage Aggregation

early_stage_rounds = pd.concat([
    series_a_rounds,
    series_b_rounds,
    venture_noseries_early,
    venture_undisclosed_early,
    equity_crowdfunding_early,
    conv_note_early,
    conv_note_nan
    ])
    
#
#    __         __         ____ __                  
#   / /  ___ _ / /_ ___   / __// /_ ___ _ ___ _ ___ 
#  / /__/ _ `// __// -_) _\ \ / __// _ `// _ `// -_)
# /____/\_,_/ \__/ \__/ /___/ \__/ \_,_/ \_, / \__/ 
#                                       /___/       
#
    
# Investment types and conditional logic

series_c_rounds = rounds[rounds.investment_type == 'series_c']
series_d_rounds = rounds[rounds.investment_type == 'series_d']
series_e_rounds = rounds[rounds.investment_type == 'series_e']
series_f_rounds = rounds[rounds.investment_type == 'series_f']
series_g_rounds = rounds[rounds.investment_type == 'series_g']
series_h_rounds = rounds[rounds.investment_type == 'series_h']
series_i_rounds = rounds[rounds.investment_type == 'series_i']
series_j_rounds = rounds[rounds.investment_type == 'series_j']
series_k_rounds = rounds[rounds.investment_type == 'series_k']
series_l_rounds = rounds[rounds.investment_type == 'series_l']

venture_noseries_late = rounds[
    (rounds.investment_type == 'series_unknown') & 
    (rounds.raised_amount_usd >= int(15000001))
    ]

conv_note_late = rounds[
    (rounds.investment_type == 'convertible_note') & 
    (rounds.raised_amount_usd >= int(15000001))
    ]

venture_undisclosed_late = rounds[
    (rounds.investment_type == 'undisclosed') & 
    (rounds.raised_amount_usd >= int(15000001))
    ]

equity_crowdfunding_late = rounds[
    (rounds.investment_type == 'equity_crowdfunding') & 
    (rounds.raised_amount_usd >= int(15000001))
    ]

## Stage Aggregation

late_stage_rounds = pd.concat([
    series_c_rounds, 
    series_d_rounds, 
    series_e_rounds, 
    series_f_rounds, 
    series_g_rounds, 
    series_h_rounds, 
    series_i_rounds, 
    series_j_rounds, 
    series_k_rounds, 
    series_l_rounds,
    venture_noseries_late, 
    conv_note_late,
    venture_undisclosed_late,
    equity_crowdfunding_late
    ])    
    
#    ___    __ __  _   __           __                 
#   / _ |  / // / | | / /___  ___  / /_ __ __ ____ ___ 
#  / __ | / // /  | |/ // -_)/ _ \/ __// // // __// -_)
# /_/ |_|/_//_/   |___/ \__//_//_/\__/ \_,_//_/   \__/ 
#                                                          

all_venture_rounds = pd.concat([
	seed_stage_rounds,
	early_stage_rounds,
	late_stage_rounds])    
