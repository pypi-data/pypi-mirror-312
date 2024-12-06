import sys #line:1
import time #line:2
import copy #line:3
from time import strftime #line:5
from time import gmtime #line:6
import pandas as pd #line:8
import numpy as np #line:9
from pandas .api .types import CategoricalDtype #line:10
import progressbar #line:11
import re #line:12
from textwrap import wrap #line:13
import seaborn as sns #line:14
import matplotlib .pyplot as plt #line:15
class cleverminer :#line:17
    version_string ="1.1.1"#line:19
    def __init__ (O0000O0O0OO0OO000 ,**OOOO00O0O0O000O0O ):#line:21
        ""#line:50
        O0000O0O0OO0OO000 ._print_disclaimer ()#line:51
        O0000O0O0OO0OO000 .stats ={'total_cnt':0 ,'total_ver':0 ,'total_valid':0 ,'control_number':0 ,'start_prep_time':time .time (),'end_prep_time':time .time (),'start_proc_time':time .time (),'end_proc_time':time .time ()}#line:60
        O0000O0O0OO0OO000 .options ={'max_categories':100 ,'max_rules':None ,'optimizations':True ,'automatic_data_conversions':True ,'progressbar':True ,'keep_df':False }#line:68
        O0000O0O0OO0OO000 .df =None #line:69
        O0000O0O0OO0OO000 .kwargs =None #line:70
        if len (OOOO00O0O0O000O0O )>0 :#line:71
            O0000O0O0OO0OO000 .kwargs =OOOO00O0O0O000O0O #line:72
        O0000O0O0OO0OO000 .profiles ={}#line:73
        O0000O0O0OO0OO000 .verbosity ={}#line:74
        O0000O0O0OO0OO000 .verbosity ['debug']=False #line:75
        O0000O0O0OO0OO000 .verbosity ['print_rules']=False #line:76
        O0000O0O0OO0OO000 .verbosity ['print_hashes']=True #line:77
        O0000O0O0OO0OO000 .verbosity ['last_hash_time']=0 #line:78
        O0000O0O0OO0OO000 .verbosity ['hint']=False #line:79
        if "opts"in OOOO00O0O0O000O0O :#line:80
            O0000O0O0OO0OO000 ._set_opts (OOOO00O0O0O000O0O .get ("opts"))#line:81
        if "opts"in OOOO00O0O0O000O0O :#line:82
            if "verbose"in OOOO00O0O0O000O0O .get ('opts'):#line:83
                OO00000O0000OOOO0 =OOOO00O0O0O000O0O .get ('opts').get ('verbose')#line:84
                if OO00000O0000OOOO0 .upper ()=='FULL':#line:85
                    O0000O0O0OO0OO000 .verbosity ['debug']=True #line:86
                    O0000O0O0OO0OO000 .verbosity ['print_rules']=True #line:87
                    O0000O0O0OO0OO000 .verbosity ['print_hashes']=False #line:88
                    O0000O0O0OO0OO000 .verbosity ['hint']=True #line:89
                    O0000O0O0OO0OO000 .options ['progressbar']=False #line:90
                elif OO00000O0000OOOO0 .upper ()=='RULES':#line:91
                    O0000O0O0OO0OO000 .verbosity ['debug']=False #line:92
                    O0000O0O0OO0OO000 .verbosity ['print_rules']=True #line:93
                    O0000O0O0OO0OO000 .verbosity ['print_hashes']=True #line:94
                    O0000O0O0OO0OO000 .verbosity ['hint']=True #line:95
                    O0000O0O0OO0OO000 .options ['progressbar']=False #line:96
                elif OO00000O0000OOOO0 .upper ()=='HINT':#line:97
                    O0000O0O0OO0OO000 .verbosity ['debug']=False #line:98
                    O0000O0O0OO0OO000 .verbosity ['print_rules']=False #line:99
                    O0000O0O0OO0OO000 .verbosity ['print_hashes']=True #line:100
                    O0000O0O0OO0OO000 .verbosity ['last_hash_time']=0 #line:101
                    O0000O0O0OO0OO000 .verbosity ['hint']=True #line:102
                    O0000O0O0OO0OO000 .options ['progressbar']=False #line:103
                elif OO00000O0000OOOO0 .upper ()=='DEBUG':#line:104
                    O0000O0O0OO0OO000 .verbosity ['debug']=True #line:105
                    O0000O0O0OO0OO000 .verbosity ['print_rules']=True #line:106
                    O0000O0O0OO0OO000 .verbosity ['print_hashes']=True #line:107
                    O0000O0O0OO0OO000 .verbosity ['last_hash_time']=0 #line:108
                    O0000O0O0OO0OO000 .verbosity ['hint']=True #line:109
                    O0000O0O0OO0OO000 .options ['progressbar']=False #line:110
        O0000O0O0OO0OO000 ._is_py310 =sys .version_info [0 ]>=4 or (sys .version_info [0 ]>=3 and sys .version_info [1 ]>=10 )#line:111
        if not (O0000O0O0OO0OO000 ._is_py310 ):#line:112
            print ("Warning: Python 3.10+ NOT detected. You should upgrade to Python 3.10 or greater to get better performance")#line:113
        else :#line:114
            if (O0000O0O0OO0OO000 .verbosity ['debug']):#line:115
                print ("Python 3.10+ detected.")#line:116
        O0000O0O0OO0OO000 ._initialized =False #line:117
        O0000O0O0OO0OO000 ._init_data ()#line:118
        O0000O0O0OO0OO000 ._init_task ()#line:119
        if len (OOOO00O0O0O000O0O )>0 :#line:120
            if "df"in OOOO00O0O0O000O0O :#line:121
                O0000O0O0OO0OO000 ._prep_data (OOOO00O0O0O000O0O .get ("df"))#line:122
            else :#line:123
                print ("Missing dataframe. Cannot initialize.")#line:124
                O0000O0O0OO0OO000 ._initialized =False #line:125
                return #line:126
            OO0O0O00O00O0O0O0 =OOOO00O0O0O000O0O .get ("proc",None )#line:127
            if not (OO0O0O00O00O0O0O0 ==None ):#line:128
                O0000O0O0OO0OO000 ._calculate (**OOOO00O0O0O000O0O )#line:129
            else :#line:130
                if O0000O0O0OO0OO000 .verbosity ['debug']:#line:131
                    print ("INFO: just initialized")#line:132
                O0OO00OO000O0O00O ={}#line:133
                OO0000OOOO0000000 ={}#line:134
                OO0000OOOO0000000 ["varname"]=O0000O0O0OO0OO000 .data ["varname"]#line:135
                OO0000OOOO0000000 ["catnames"]=O0000O0O0OO0OO000 .data ["catnames"]#line:136
                O0OO00OO000O0O00O ["datalabels"]=OO0000OOOO0000000 #line:137
                O0000O0O0OO0OO000 .result =O0OO00OO000O0O00O #line:138
        O0000O0O0OO0OO000 ._initialized =True #line:140
    def _set_opts (O0O000OO0000OOO00 ,O0000OOOO0O000OO0 ):#line:142
        if "no_optimizations"in O0000OOOO0O000OO0 :#line:143
            O0O000OO0000OOO00 .options ['optimizations']=not (O0000OOOO0O000OO0 ['no_optimizations'])#line:144
            print ("No optimization will be made.")#line:145
        if "disable_progressbar"in O0000OOOO0O000OO0 :#line:146
            O0O000OO0000OOO00 .options ['progressbar']=False #line:147
            print ("Progressbar will not be shown.")#line:148
        if "max_rules"in O0000OOOO0O000OO0 :#line:149
            O0O000OO0000OOO00 .options ['max_rules']=O0000OOOO0O000OO0 ['max_rules']#line:150
        if "max_categories"in O0000OOOO0O000OO0 :#line:151
            O0O000OO0000OOO00 .options ['max_categories']=O0000OOOO0O000OO0 ['max_categories']#line:152
            if O0O000OO0000OOO00 .verbosity ['debug']==True :#line:153
                print (f"Maximum number of categories set to {O0O000OO0000OOO00.options['max_categories']}")#line:154
        if "no_automatic_data_conversions"in O0000OOOO0O000OO0 :#line:155
            O0O000OO0000OOO00 .options ['automatic_data_conversions']=not (O0000OOOO0O000OO0 ['no_automatic_data_conversions'])#line:156
            print ("No automatic data conversions will be made.")#line:157
        if "keep_df"in O0000OOOO0O000OO0 :#line:158
            O0O000OO0000OOO00 .options ['keep_df']=O0000OOOO0O000OO0 ['keep_df']#line:159
    def _init_data (OOO0OOOO0OO0O0OOO ):#line:162
        OOO0OOOO0OO0O0OOO .data ={}#line:164
        OOO0OOOO0OO0O0OOO .data ["varname"]=[]#line:165
        OOO0OOOO0OO0O0OOO .data ["catnames"]=[]#line:166
        OOO0OOOO0OO0O0OOO .data ["vtypes"]=[]#line:167
        OOO0OOOO0OO0O0OOO .data ["dm"]=[]#line:168
        OOO0OOOO0OO0O0OOO .data ["rows_count"]=int (0 )#line:169
        OOO0OOOO0OO0O0OOO .data ["data_prepared"]=0 #line:170
    def _init_task (OOO0OOOO0O00O0000 ):#line:172
        if "opts"in OOO0OOOO0O00O0000 .kwargs :#line:174
            OOO0OOOO0O00O0000 ._set_opts (OOO0OOOO0O00O0000 .kwargs .get ("opts"))#line:175
        OOO0OOOO0O00O0000 .cedent ={'cedent_type':'none','defi':{},'num_cedent':0 ,'trace_cedent':[],'trace_cedent_asindata':[],'traces':[],'generated_string':'','rule':{},'filter_value':int (0 )}#line:185
        OOO0OOOO0O00O0000 .task_actinfo ={'proc':'','cedents_to_do':[],'cedents':[]}#line:189
        OOO0OOOO0O00O0000 .rulelist =[]#line:190
        OOO0OOOO0O00O0000 .stats ['total_cnt']=0 #line:191
        OOO0OOOO0O00O0000 .stats ['total_valid']=0 #line:192
        OOO0OOOO0O00O0000 .stats ['control_number']=0 #line:193
        OOO0OOOO0O00O0000 .result ={}#line:194
        OOO0OOOO0O00O0000 ._opt_base =None #line:195
        OOO0OOOO0O00O0000 ._opt_relbase =None #line:196
        OOO0OOOO0O00O0000 ._opt_base1 =None #line:197
        OOO0OOOO0O00O0000 ._opt_relbase1 =None #line:198
        OOO0OOOO0O00O0000 ._opt_base2 =None #line:199
        OOO0OOOO0O00O0000 ._opt_relbase2 =None #line:200
        O00000O000OO00O00 =None #line:201
        if not (OOO0OOOO0O00O0000 .kwargs ==None ):#line:202
            O00000O000OO00O00 =OOO0OOOO0O00O0000 .kwargs .get ("quantifiers",None )#line:203
            if not (O00000O000OO00O00 ==None ):#line:204
                for O00O0O000OOO0O000 in O00000O000OO00O00 .keys ():#line:205
                    if O00O0O000OOO0O000 .upper ()=='BASE':#line:206
                        OOO0OOOO0O00O0000 ._opt_base =O00000O000OO00O00 .get (O00O0O000OOO0O000 )#line:207
                    if O00O0O000OOO0O000 .upper ()=='RELBASE':#line:208
                        OOO0OOOO0O00O0000 ._opt_relbase =O00000O000OO00O00 .get (O00O0O000OOO0O000 )#line:209
                    if (O00O0O000OOO0O000 .upper ()=='FRSTBASE')|(O00O0O000OOO0O000 .upper ()=='BASE1'):#line:210
                        OOO0OOOO0O00O0000 ._opt_base1 =O00000O000OO00O00 .get (O00O0O000OOO0O000 )#line:211
                    if (O00O0O000OOO0O000 .upper ()=='SCNDBASE')|(O00O0O000OOO0O000 .upper ()=='BASE2'):#line:212
                        OOO0OOOO0O00O0000 ._opt_base2 =O00000O000OO00O00 .get (O00O0O000OOO0O000 )#line:213
                    if (O00O0O000OOO0O000 .upper ()=='FRSTRELBASE')|(O00O0O000OOO0O000 .upper ()=='RELBASE1'):#line:214
                        OOO0OOOO0O00O0000 ._opt_relbase1 =O00000O000OO00O00 .get (O00O0O000OOO0O000 )#line:215
                    if (O00O0O000OOO0O000 .upper ()=='SCNDRELBASE')|(O00O0O000OOO0O000 .upper ()=='RELBASE2'):#line:216
                        OOO0OOOO0O00O0000 ._opt_relbase2 =O00000O000OO00O00 .get (O00O0O000OOO0O000 )#line:217
            else :#line:218
                print ("Warning: no quantifiers found. Optimization will not take place (1)")#line:219
        else :#line:220
            print ("Warning: no quantifiers found. Optimization will not take place (2)")#line:221
    def mine (OO0O0OO00OOOO0000 ,**O00OO000OO0OOO0OO ):#line:224
        ""#line:229
        if not (OO0O0OO00OOOO0000 ._initialized ):#line:230
            print ("Class NOT INITIALIZED. Please call constructor with dataframe first")#line:231
            return #line:232
        OO0O0OO00OOOO0000 .kwargs =None #line:233
        if len (O00OO000OO0OOO0OO )>0 :#line:234
            OO0O0OO00OOOO0000 .kwargs =O00OO000OO0OOO0OO #line:235
        OO0O0OO00OOOO0000 ._init_task ()#line:236
        if len (O00OO000OO0OOO0OO )>0 :#line:237
            OO00OO0O0OO00O0OO =O00OO000OO0OOO0OO .get ("proc",None )#line:238
            if not (OO00OO0O0OO00O0OO ==None ):#line:239
                OO0O0OO00OOOO0000 ._calc_all (**O00OO000OO0OOO0OO )#line:240
            else :#line:241
                print ("Rule mining procedure missing")#line:242
    def _get_ver (O0OO0OOO0O0O00OO0 ):#line:245
        return O0OO0OOO0O0O00OO0 .version_string #line:246
    def _print_disclaimer (OOOO0OO0000OO0OO0 ):#line:248
        print (f"Cleverminer version {OOOO0OO0000OO0OO0._get_ver()}.")#line:249
    def _automatic_data_conversions (O0O00O00O0OO00000 ,O0O00OO0O0O00OOO0 ):#line:250
        print ("Automatically reordering numeric categories ...")#line:251
        for OO000OO0OO0OO00O0 in range (len (O0O00OO0O0O00OOO0 .columns )):#line:252
            if O0O00O00O0OO00000 .verbosity ['debug']:#line:253
                print (f"#{OO000OO0OO0OO00O0}: {O0O00OO0O0O00OOO0.columns[OO000OO0OO0OO00O0]} : {O0O00OO0O0O00OOO0.dtypes[OO000OO0OO0OO00O0]}.")#line:254
            try :#line:255
                O0O00OO0O0O00OOO0 [O0O00OO0O0O00OOO0 .columns [OO000OO0OO0OO00O0 ]]=O0O00OO0O0O00OOO0 [O0O00OO0O0O00OOO0 .columns [OO000OO0OO0OO00O0 ]].astype (str ).astype (float )#line:256
                if O0O00O00O0OO00000 .verbosity ['debug']:#line:257
                    print (f"CONVERTED TO FLOATS #{OO000OO0OO0OO00O0}: {O0O00OO0O0O00OOO0.columns[OO000OO0OO0OO00O0]} : {O0O00OO0O0O00OOO0.dtypes[OO000OO0OO0OO00O0]}.")#line:258
                O0O000OOOOOOO0OOO =pd .unique (O0O00OO0O0O00OOO0 [O0O00OO0O0O00OOO0 .columns [OO000OO0OO0OO00O0 ]])#line:259
                O000OO000OOO00O00 =True #line:260
                for OOOO0000OOO0OO0OO in O0O000OOOOOOO0OOO :#line:261
                    if OOOO0000OOO0OO0OO %1 !=0 :#line:262
                        O000OO000OOO00O00 =False #line:263
                if O000OO000OOO00O00 :#line:264
                    O0O00OO0O0O00OOO0 [O0O00OO0O0O00OOO0 .columns [OO000OO0OO0OO00O0 ]]=O0O00OO0O0O00OOO0 [O0O00OO0O0O00OOO0 .columns [OO000OO0OO0OO00O0 ]].astype (int )#line:265
                    if O0O00O00O0OO00000 .verbosity ['debug']:#line:266
                        print (f"CONVERTED TO INT #{OO000OO0OO0OO00O0}: {O0O00OO0O0O00OOO0.columns[OO000OO0OO0OO00O0]} : {O0O00OO0O0O00OOO0.dtypes[OO000OO0OO0OO00O0]}.")#line:267
                O0O0OOOOO0O00O000 =pd .unique (O0O00OO0O0O00OOO0 [O0O00OO0O0O00OOO0 .columns [OO000OO0OO0OO00O0 ]])#line:268
                O000OOOOOO0OOOOOO =CategoricalDtype (categories =O0O0OOOOO0O00O000 .sort (),ordered =True )#line:269
                O0O00OO0O0O00OOO0 [O0O00OO0O0O00OOO0 .columns [OO000OO0OO0OO00O0 ]]=O0O00OO0O0O00OOO0 [O0O00OO0O0O00OOO0 .columns [OO000OO0OO0OO00O0 ]].astype (O000OOOOOO0OOOOOO )#line:270
                if O0O00O00O0OO00000 .verbosity ['debug']:#line:271
                    print (f"CONVERTED TO CATEGORY #{OO000OO0OO0OO00O0}: {O0O00OO0O0O00OOO0.columns[OO000OO0OO0OO00O0]} : {O0O00OO0O0O00OOO0.dtypes[OO000OO0OO0OO00O0]}.")#line:272
            except :#line:274
                if O0O00O00O0OO00000 .verbosity ['debug']:#line:275
                    print ("...cannot be converted to int")#line:276
                try :#line:277
                    O00O00000O0000000 =O0O00OO0O0O00OOO0 [O0O00OO0O0O00OOO0 .columns [OO000OO0OO0OO00O0 ]].unique ()#line:278
                    if O0O00O00O0OO00000 .verbosity ['debug']:#line:279
                        print (f"Values: {O00O00000O0000000}")#line:280
                    OOO0OO0OO0O00O0OO =True #line:281
                    O0OOO0OOOO0O0000O =[]#line:282
                    for OOOO0000OOO0OO0OO in O00O00000O0000000 :#line:283
                        OO00OO0O00O0O00OO =re .findall (r"-?\d+",OOOO0000OOO0OO0OO )#line:286
                        if len (OO00OO0O00O0O00OO )>0 :#line:288
                            O0OOO0OOOO0O0000O .append (int (OO00OO0O00O0O00OO [0 ]))#line:289
                        else :#line:290
                            OOO0OO0OO0O00O0OO =False #line:291
                    if O0O00O00O0OO00000 .verbosity ['debug']:#line:292
                        print (f"Is ok: {OOO0OO0OO0O00O0OO}, extracted {O0OOO0OOOO0O0000O}")#line:293
                    if OOO0OO0OO0O00O0OO :#line:294
                        OO00000000O0O00OO =copy .deepcopy (O0OOO0OOOO0O0000O )#line:295
                        OO00000000O0O00OO .sort ()#line:296
                        O0OOOOO0OOO0OOO0O =[]#line:298
                        for OOO0000OOOO0OOOOO in OO00000000O0O00OO :#line:299
                            O0O0OO000OOOOO0O0 =O0OOO0OOOO0O0000O .index (OOO0000OOOO0OOOOO )#line:300
                            O0OOOOO0OOO0OOO0O .append (O00O00000O0000000 [O0O0OO000OOOOO0O0 ])#line:302
                        if O0O00O00O0OO00000 .verbosity ['debug']:#line:303
                            print (f"Sorted list: {O0OOOOO0OOO0OOO0O}")#line:304
                        O000OOOOOO0OOOOOO =CategoricalDtype (categories =O0OOOOO0OOO0OOO0O ,ordered =True )#line:305
                        O0O00OO0O0O00OOO0 [O0O00OO0O0O00OOO0 .columns [OO000OO0OO0OO00O0 ]]=O0O00OO0O0O00OOO0 [O0O00OO0O0O00OOO0 .columns [OO000OO0OO0OO00O0 ]].astype (O000OOOOOO0OOOOOO )#line:306
                except :#line:307
                    if O0O00O00O0OO00000 .verbosity ['debug']:#line:308
                        print ("...cannot extract numbers from all categories")#line:309
        print ("Automatically reordering numeric categories ...done")#line:311
    def _prep_data (O0OO00O00O0OOO0OO ,O00OOO000000OO000 ):#line:313
        print ("Starting data preparation ...")#line:314
        O0OO00O00O0OOO0OO ._init_data ()#line:315
        O0OO00O00O0OOO0OO .stats ['start_prep_time']=time .time ()#line:316
        if O0OO00O00O0OOO0OO .options ['automatic_data_conversions']:#line:317
            O0OO00O00O0OOO0OO ._automatic_data_conversions (O00OOO000000OO000 )#line:318
        O0OO00O00O0OOO0OO .data ["rows_count"]=O00OOO000000OO000 .shape [0 ]#line:319
        for O000OO0OOO000OOO0 in O00OOO000000OO000 .select_dtypes (exclude =['category']).columns :#line:320
            O00OOO000000OO000 [O000OO0OOO000OOO0 ]=O00OOO000000OO000 [O000OO0OOO000OOO0 ].apply (str )#line:321
        try :#line:322
            OO0OOOO00000OOO00 =pd .DataFrame .from_records ([(OO0OOOO0O00000OOO ,O00OOO000000OO000 [OO0OOOO0O00000OOO ].nunique ())for OO0OOOO0O00000OOO in O00OOO000000OO000 .columns ],columns =['Column_Name','Num_Unique']).sort_values (by =['Num_Unique'])#line:324
        except :#line:325
            print ("Error in input data, probably unsupported data type. Will try to scan for column with unsupported type.")#line:326
            O0OO0000OOOO0O0OO =""#line:327
            try :#line:328
                for O000OO0OOO000OOO0 in O00OOO000000OO000 .columns :#line:329
                    O0OO0000OOOO0O0OO =O000OO0OOO000OOO0 #line:330
                    print (f"...column {O000OO0OOO000OOO0} has {int(O00OOO000000OO000[O000OO0OOO000OOO0].nunique())} values")#line:331
            except :#line:332
                print (f"... detected : column {O0OO0000OOOO0O0OO} has unsupported type: {type(O00OOO000000OO000[O000OO0OOO000OOO0])}.")#line:333
                exit (1 )#line:334
            print (f"Error in data profiling - attribute with unsupported type not detected. Please profile attributes manually, only simple attributes are supported.")#line:335
            exit (1 )#line:336
        if O0OO00O00O0OOO0OO .verbosity ['hint']:#line:339
            print ("Quick profile of input data: unique value counts are:")#line:340
            print (OO0OOOO00000OOO00 )#line:341
            for O000OO0OOO000OOO0 in O00OOO000000OO000 .columns :#line:342
                if O00OOO000000OO000 [O000OO0OOO000OOO0 ].nunique ()<O0OO00O00O0OOO0OO .options ['max_categories']:#line:343
                    O00OOO000000OO000 [O000OO0OOO000OOO0 ]=O00OOO000000OO000 [O000OO0OOO000OOO0 ].astype ('category')#line:344
                else :#line:345
                    print (f"WARNING: attribute {O000OO0OOO000OOO0} has more than {O0OO00O00O0OOO0OO.options['max_categories']} values, will be ignored.\r\n If you haven't set maximum number of categories and you really need more categories and you know what you are doing, please use max_categories option to increase allowed number of categories.")#line:346
                    del O00OOO000000OO000 [O000OO0OOO000OOO0 ]#line:347
        for O000OO0OOO000OOO0 in O00OOO000000OO000 .columns :#line:349
            if O00OOO000000OO000 [O000OO0OOO000OOO0 ].nunique ()>O0OO00O00O0OOO0OO .options ['max_categories']:#line:350
                print (f"WARNING: attribute {O000OO0OOO000OOO0} has more than {O0OO00O00O0OOO0OO.options['max_categories']} values, will be ignored.\r\n If you haven't set maximum number of categories and you really need more categories and you know what you are doing, please use max_categories option to increase allowed number of categories.")#line:351
                del O00OOO000000OO000 [O000OO0OOO000OOO0 ]#line:352
        if O0OO00O00O0OOO0OO .options ['keep_df']:#line:353
            if O0OO00O00O0OOO0OO .verbosity ['debug']:#line:354
                print ("Keeping df.")#line:355
            O0OO00O00O0OOO0OO .df =O00OOO000000OO000 #line:356
        print ("Encoding columns into bit-form...")#line:357
        O00000OO0O00000OO =0 #line:358
        OO00OOO000000OO00 =0 #line:359
        for OO00OO00O00OO0O0O in O00OOO000000OO000 :#line:360
            if O0OO00O00O0OOO0OO .verbosity ['debug']:#line:361
                print ('Column: '+OO00OO00O00OO0O0O +' @ '+str (time .time ()))#line:362
            if O0OO00O00O0OOO0OO .verbosity ['debug']:#line:363
                print ('Column: '+OO00OO00O00OO0O0O )#line:364
            O0OO00O00O0OOO0OO .data ["varname"].append (OO00OO00O00OO0O0O )#line:365
            O0OO0O0O00OOO0O00 =pd .get_dummies (O00OOO000000OO000 [OO00OO00O00OO0O0O ])#line:366
            O0O0O00000OO0000O =0 #line:367
            if (O00OOO000000OO000 .dtypes [OO00OO00O00OO0O0O ].name =='category'):#line:368
                O0O0O00000OO0000O =1 #line:369
            O0OO00O00O0OOO0OO .data ["vtypes"].append (O0O0O00000OO0000O )#line:370
            if O0OO00O00O0OOO0OO .verbosity ['debug']:#line:371
                print (O0OO0O0O00OOO0O00 )#line:372
                print (O00OOO000000OO000 [OO00OO00O00OO0O0O ])#line:373
            O0O000OO000OO000O =0 #line:374
            O00000O0OO00O0O0O =[]#line:375
            O00O0O00OO000OOO0 =[]#line:376
            if O0OO00O00O0OOO0OO .verbosity ['debug']:#line:377
                print ('...starting categories '+str (time .time ()))#line:378
            for OOOO0OO00000O000O in O0OO0O0O00OOO0O00 :#line:379
                if O0OO00O00O0OOO0OO .verbosity ['debug']:#line:380
                    print ('....category : '+str (OOOO0OO00000O000O )+' @ '+str (time .time ()))#line:381
                O00000O0OO00O0O0O .append (OOOO0OO00000O000O )#line:382
                OO0OOO000O00OOO00 =int (0 )#line:383
                O00OOOO0O000O0O0O =O0OO0O0O00OOO0O00 [OOOO0OO00000O000O ].values #line:384
                if O0OO00O00O0OOO0OO .verbosity ['debug']:#line:385
                    print (O00OOOO0O000O0O0O .ndim )#line:386
                O0O00OO0O0OOOOO0O =np .packbits (O00OOOO0O000O0O0O ,bitorder ='little')#line:387
                OO0OOO000O00OOO00 =int .from_bytes (O0O00OO0O0OOOOO0O ,byteorder ='little')#line:388
                O00O0O00OO000OOO0 .append (OO0OOO000O00OOO00 )#line:389
                if O0OO00O00O0OOO0OO .verbosity ['debug']:#line:391
                    for O000OO000OO0O0OO0 in range (O0OO00O00O0OOO0OO .data ["rows_count"]):#line:393
                        if O00OOOO0O000O0O0O [O000OO000OO0O0OO0 ]>0 :#line:394
                            OO0OOO000O00OOO00 +=1 <<O000OO000OO0O0OO0 #line:395
                            O00O0O00OO000OOO0 .append (OO0OOO000O00OOO00 )#line:396
                    print ('....category ATTEMPT 2: '+str (OOOO0OO00000O000O )+" @ "+str (time .time ()))#line:399
                    O0OOO0OOOOO0OO00O =int (0 )#line:400
                    O0OO0OO0O000000OO =int (1 )#line:401
                    for O000OO000OO0O0OO0 in range (O0OO00O00O0OOO0OO .data ["rows_count"]):#line:402
                        if O00OOOO0O000O0O0O [O000OO000OO0O0OO0 ]>0 :#line:403
                            O0OOO0OOOOO0OO00O +=O0OO0OO0O000000OO #line:404
                            O0OO0OO0O000000OO *=2 #line:405
                            O0OO0OO0O000000OO =O0OO0OO0O000000OO <<1 #line:406
                            print (str (OO0OOO000O00OOO00 ==O0OOO0OOOOO0OO00O )+" @ "+str (time .time ()))#line:407
                O0O000OO000OO000O +=1 #line:408
                OO00OOO000000OO00 +=1 #line:409
                if O0OO00O00O0OOO0OO .verbosity ['debug']:#line:410
                    print (O00000O0OO00O0O0O )#line:411
            O0OO00O00O0OOO0OO .data ["catnames"].append (O00000O0OO00O0O0O )#line:412
            O0OO00O00O0OOO0OO .data ["dm"].append (O00O0O00OO000OOO0 )#line:413
        print ("Encoding columns into bit-form...done")#line:415
        if O0OO00O00O0OOO0OO .verbosity ['hint']:#line:416
            print (f"List of attributes for analysis is: {O0OO00O00O0OOO0OO.data['varname']}")#line:417
            print (f"List of category names for individual attributes is : {O0OO00O00O0OOO0OO.data['catnames']}")#line:418
        if O0OO00O00O0OOO0OO .verbosity ['debug']:#line:419
            print (f"List of vtypes is (all should be 1) : {O0OO00O00O0OOO0OO.data['vtypes']}")#line:420
        O0OO00O00O0OOO0OO .data ["data_prepared"]=1 #line:421
        print ("Data preparation finished.")#line:422
        if O0OO00O00O0OOO0OO .verbosity ['debug']:#line:423
            print ('Number of variables : '+str (len (O0OO00O00O0OOO0OO .data ["dm"])))#line:424
            print ('Total number of categories in all variables : '+str (OO00OOO000000OO00 ))#line:425
        O0OO00O00O0OOO0OO .stats ['end_prep_time']=time .time ()#line:426
        if O0OO00O00O0OOO0OO .verbosity ['debug']:#line:427
            print ('Time needed for data preparation : ',str (O0OO00O00O0OOO0OO .stats ['end_prep_time']-O0OO00O00O0OOO0OO .stats ['start_prep_time']))#line:428
    def _bitcount (O000O0OO0OOOO0OOO ,OO0OOOOO0O00O00OO ):#line:430
        OOOO0OOO0OO000O0O =None #line:431
        if (O000O0OO0OOOO0OOO ._is_py310 ):#line:432
            OOOO0OOO0OO000O0O =OO0OOOOO0O00O00OO .bit_count ()#line:433
        else :#line:434
            OOOO0OOO0OO000O0O =bin (OO0OOOOO0O00O00OO ).count ("1")#line:435
        return OOOO0OOO0OO000O0O #line:436
    def _verifyCF (O00OOOO00OO0O0OO0 ,_O00OOOO0OOO0O0O00 ):#line:439
        OOO0O0OO000O00000 =O00OOOO00OO0O0OO0 ._bitcount (_O00OOOO0OOO0O0O00 )#line:440
        O0O0O0O00OOOOOO00 =[]#line:441
        OOO0O00OOO00OOO0O =[]#line:442
        OO0O00OOOOO00OOO0 =0 #line:443
        O000O0000OOO0OOOO =0 #line:444
        OO00O00O0O0OO0OOO =0 #line:445
        O0O0000O0OOO0OO0O =0 #line:446
        O000O00OOO000OO00 =0 #line:447
        O0OO00O00000OO0O0 =0 #line:448
        O0000O0OOO00OOO0O =0 #line:449
        O0OOO00O0OO0OOOO0 =0 #line:450
        O0OOOOO0O00O0OOO0 =0 #line:451
        O0OO0O0000O00O0OO =None #line:452
        O0000O000OOOO0OOO =None #line:453
        OOOOO000OOOO0OOO0 =None #line:454
        if ('min_step_size'in O00OOOO00OO0O0OO0 .quantifiers ):#line:455
            O0OO0O0000O00O0OO =O00OOOO00OO0O0OO0 .quantifiers .get ('min_step_size')#line:456
        if ('min_rel_step_size'in O00OOOO00OO0O0OO0 .quantifiers ):#line:457
            O0000O000OOOO0OOO =O00OOOO00OO0O0OO0 .quantifiers .get ('min_rel_step_size')#line:458
            if O0000O000OOOO0OOO >=1 and O0000O000OOOO0OOO <100 :#line:459
                O0000O000OOOO0OOO =O0000O000OOOO0OOO /100 #line:460
        OOOO00O00OOOOO0O0 =0 #line:461
        O0OO00O0OO00O00OO =0 #line:462
        O000OOOOO0OOO0000 =[]#line:463
        if ('aad_weights'in O00OOOO00OO0O0OO0 .quantifiers ):#line:464
            OOOO00O00OOOOO0O0 =1 #line:465
            O00OO0O0OO0O0OOOO =[]#line:466
            O000OOOOO0OOO0000 =O00OOOO00OO0O0OO0 .quantifiers .get ('aad_weights')#line:467
        OO0O0O000O00OO00O =O00OOOO00OO0O0OO0 .data ["dm"][O00OOOO00OO0O0OO0 .data ["varname"].index (O00OOOO00OO0O0OO0 .kwargs .get ('target'))]#line:468
        def OO0O0O00OOOO000O0 (O0OO00O000OOO00OO ,OOOOO0OO00O00OOO0 ):#line:469
            O0OOO00O0O0000O0O =True #line:470
            if (O0OO00O000OOO00OO >OOOOO0OO00O00OOO0 ):#line:471
                if not (O0OO0O0000O00O0OO is None or O0OO00O000OOO00OO >=OOOOO0OO00O00OOO0 +O0OO0O0000O00O0OO ):#line:472
                    O0OOO00O0O0000O0O =False #line:473
                if not (O0000O000OOOO0OOO is None or O0OO00O000OOO00OO >=OOOOO0OO00O00OOO0 *(1 +O0000O000OOOO0OOO )):#line:474
                    O0OOO00O0O0000O0O =False #line:475
            if (O0OO00O000OOO00OO <OOOOO0OO00O00OOO0 ):#line:476
                if not (O0OO0O0000O00O0OO is None or O0OO00O000OOO00OO <=OOOOO0OO00O00OOO0 -O0OO0O0000O00O0OO ):#line:477
                    O0OOO00O0O0000O0O =False #line:478
                if not (O0000O000OOOO0OOO is None or O0OO00O000OOO00OO <=OOOOO0OO00O00OOO0 *(1 -O0000O000OOOO0OOO )):#line:479
                    O0OOO00O0O0000O0O =False #line:480
            return O0OOO00O0O0000O0O #line:481
        for O0OOOO0OOO0OOO0OO in range (len (OO0O0O000O00OO00O )):#line:482
            O000O0000OOO0OOOO =OO0O00OOOOO00OOO0 #line:484
            OO0O00OOOOO00OOO0 =O00OOOO00OO0O0OO0 ._bitcount (_O00OOOO0OOO0O0O00 &OO0O0O000O00OO00O [O0OOOO0OOO0OOO0OO ])#line:485
            O0O0O0O00OOOOOO00 .append (OO0O00OOOOO00OOO0 )#line:486
            if O0OOOO0OOO0OOO0OO >0 :#line:487
                if (OO0O00OOOOO00OOO0 >O000O0000OOO0OOOO ):#line:488
                    if (OO00O00O0O0OO0OOO ==1 )and (OO0O0O00OOOO000O0 (OO0O00OOOOO00OOO0 ,O000O0000OOO0OOOO )):#line:489
                        O0OOO00O0OO0OOOO0 +=1 #line:490
                    else :#line:491
                        if OO0O0O00OOOO000O0 (OO0O00OOOOO00OOO0 ,O000O0000OOO0OOOO ):#line:492
                            O0OOO00O0OO0OOOO0 =1 #line:493
                        else :#line:494
                            O0OOO00O0OO0OOOO0 =0 #line:495
                    if O0OOO00O0OO0OOOO0 >O0O0000O0OOO0OO0O :#line:496
                        O0O0000O0OOO0OO0O =O0OOO00O0OO0OOOO0 #line:497
                    OO00O00O0O0OO0OOO =1 #line:498
                    if OO0O0O00OOOO000O0 (OO0O00OOOOO00OOO0 ,O000O0000OOO0OOOO ):#line:499
                        O0OO00O00000OO0O0 +=1 #line:500
                if (OO0O00OOOOO00OOO0 <O000O0000OOO0OOOO ):#line:501
                    if (OO00O00O0O0OO0OOO ==-1 )and (OO0O0O00OOOO000O0 (OO0O00OOOOO00OOO0 ,O000O0000OOO0OOOO )):#line:502
                        O0OOOOO0O00O0OOO0 +=1 #line:503
                    else :#line:504
                        if OO0O0O00OOOO000O0 (OO0O00OOOOO00OOO0 ,O000O0000OOO0OOOO ):#line:505
                            O0OOOOO0O00O0OOO0 =1 #line:506
                        else :#line:507
                            O0OOOOO0O00O0OOO0 =0 #line:508
                    if O0OOOOO0O00O0OOO0 >O000O00OOO000OO00 :#line:509
                        O000O00OOO000OO00 =O0OOOOO0O00O0OOO0 #line:510
                    OO00O00O0O0OO0OOO =-1 #line:511
                    if OO0O0O00OOOO000O0 (OO0O00OOOOO00OOO0 ,O000O0000OOO0OOOO ):#line:512
                        O0000O0OOO00OOO0O +=1 #line:513
                if (OO0O00OOOOO00OOO0 ==O000O0000OOO0OOOO ):#line:514
                    OO00O00O0O0OO0OOO =0 #line:515
                    O0OOOOO0O00O0OOO0 =0 #line:516
                    O0OOO00O0OO0OOOO0 =0 #line:517
            if (OOOO00O00OOOOO0O0 ):#line:519
                O0O0000O0OO0OOOOO =O00OOOO00OO0O0OO0 ._bitcount (OO0O0O000O00OO00O [O0OOOO0OOO0OOO0OO ])#line:520
                O00OO0O0OO0O0OOOO .append (O0O0000O0OO0OOOOO )#line:521
        if (OOOO00O00OOOOO0O0 &sum (O0O0O0O00OOOOOO00 )>0 ):#line:523
            for O0OOOO0OOO0OOO0OO in range (len (OO0O0O000O00OO00O )):#line:524
                if O00OO0O0OO0O0OOOO [O0OOOO0OOO0OOO0OO ]>0 :#line:525
                    if O0O0O0O00OOOOOO00 [O0OOOO0OOO0OOO0OO ]/sum (O0O0O0O00OOOOOO00 )>O00OO0O0OO0O0OOOO [O0OOOO0OOO0OOO0OO ]/sum (O00OO0O0OO0O0OOOO ):#line:526
                        O0OO00O0OO00O00OO +=O000OOOOO0OOO0000 [O0OOOO0OOO0OOO0OO ]*((O0O0O0O00OOOOOO00 [O0OOOO0OOO0OOO0OO ]/sum (O0O0O0O00OOOOOO00 ))/(O00OO0O0OO0O0OOOO [O0OOOO0OOO0OOO0OO ]/sum (O00OO0O0OO0O0OOOO ))-1 )#line:527
        O0OO0O0O0000OOO00 =True #line:530
        for OO000O00O0OOO00OO in O00OOOO00OO0O0OO0 .quantifiers .keys ():#line:531
            if OO000O00O0OOO00OO .upper ()=='BASE':#line:532
                O0OO0O0O0000OOO00 =O0OO0O0O0000OOO00 and (O00OOOO00OO0O0OO0 .quantifiers .get (OO000O00O0OOO00OO )<=OOO0O0OO000O00000 )#line:533
            if OO000O00O0OOO00OO .upper ()=='RELBASE':#line:534
                O0OO0O0O0000OOO00 =O0OO0O0O0000OOO00 and (O00OOOO00OO0O0OO0 .quantifiers .get (OO000O00O0OOO00OO )<=OOO0O0OO000O00000 *1.0 /O00OOOO00OO0O0OO0 .data ["rows_count"])#line:535
            if OO000O00O0OOO00OO .upper ()=='S_UP':#line:536
                O0OO0O0O0000OOO00 =O0OO0O0O0000OOO00 and (O00OOOO00OO0O0OO0 .quantifiers .get (OO000O00O0OOO00OO )<=O0O0000O0OOO0OO0O )#line:537
            if OO000O00O0OOO00OO .upper ()=='S_DOWN':#line:538
                O0OO0O0O0000OOO00 =O0OO0O0O0000OOO00 and (O00OOOO00OO0O0OO0 .quantifiers .get (OO000O00O0OOO00OO )<=O000O00OOO000OO00 )#line:539
            if OO000O00O0OOO00OO .upper ()=='S_ANY_UP':#line:540
                O0OO0O0O0000OOO00 =O0OO0O0O0000OOO00 and (O00OOOO00OO0O0OO0 .quantifiers .get (OO000O00O0OOO00OO )<=O0O0000O0OOO0OO0O )#line:541
            if OO000O00O0OOO00OO .upper ()=='S_ANY_DOWN':#line:542
                O0OO0O0O0000OOO00 =O0OO0O0O0000OOO00 and (O00OOOO00OO0O0OO0 .quantifiers .get (OO000O00O0OOO00OO )<=O000O00OOO000OO00 )#line:543
            if OO000O00O0OOO00OO .upper ()=='MAX':#line:544
                O0OO0O0O0000OOO00 =O0OO0O0O0000OOO00 and (O00OOOO00OO0O0OO0 .quantifiers .get (OO000O00O0OOO00OO )<=max (O0O0O0O00OOOOOO00 ))#line:545
            if OO000O00O0OOO00OO .upper ()=='MIN':#line:546
                O0OO0O0O0000OOO00 =O0OO0O0O0000OOO00 and (O00OOOO00OO0O0OO0 .quantifiers .get (OO000O00O0OOO00OO )<=min (O0O0O0O00OOOOOO00 ))#line:547
            if OO000O00O0OOO00OO .upper ()=='RELMAX':#line:548
                if sum (O0O0O0O00OOOOOO00 )>0 :#line:549
                    O0OO0O0O0000OOO00 =O0OO0O0O0000OOO00 and (O00OOOO00OO0O0OO0 .quantifiers .get (OO000O00O0OOO00OO )<=max (O0O0O0O00OOOOOO00 )*1.0 /sum (O0O0O0O00OOOOOO00 ))#line:550
                else :#line:551
                    O0OO0O0O0000OOO00 =False #line:552
            if OO000O00O0OOO00OO .upper ()=='RELMAX_LEQ':#line:553
                if sum (O0O0O0O00OOOOOO00 )>0 :#line:554
                    O0OO0O0O0000OOO00 =O0OO0O0O0000OOO00 and (O00OOOO00OO0O0OO0 .quantifiers .get (OO000O00O0OOO00OO )>=max (O0O0O0O00OOOOOO00 )*1.0 /sum (O0O0O0O00OOOOOO00 ))#line:555
                else :#line:556
                    O0OO0O0O0000OOO00 =False #line:557
            if OO000O00O0OOO00OO .upper ()=='RELMIN':#line:558
                if sum (O0O0O0O00OOOOOO00 )>0 :#line:559
                    O0OO0O0O0000OOO00 =O0OO0O0O0000OOO00 and (O00OOOO00OO0O0OO0 .quantifiers .get (OO000O00O0OOO00OO )<=min (O0O0O0O00OOOOOO00 )*1.0 /sum (O0O0O0O00OOOOOO00 ))#line:560
                else :#line:561
                    O0OO0O0O0000OOO00 =False #line:562
            if OO000O00O0OOO00OO .upper ()=='RELMIN_LEQ':#line:563
                if sum (O0O0O0O00OOOOOO00 )>0 :#line:564
                    O0OO0O0O0000OOO00 =O0OO0O0O0000OOO00 and (O00OOOO00OO0O0OO0 .quantifiers .get (OO000O00O0OOO00OO )>=min (O0O0O0O00OOOOOO00 )*1.0 /sum (O0O0O0O00OOOOOO00 ))#line:565
                else :#line:566
                    O0OO0O0O0000OOO00 =False #line:567
            if OO000O00O0OOO00OO .upper ()=='AAD':#line:568
                O0OO0O0O0000OOO00 =O0OO0O0O0000OOO00 and (O00OOOO00OO0O0OO0 .quantifiers .get (OO000O00O0OOO00OO )<=O0OO00O0OO00O00OO )#line:569
            if OO000O00O0OOO00OO .upper ()=='RELRANGE_LEQ':#line:570
                OOOOOO0O0OO00O0O0 =O00OOOO00OO0O0OO0 .quantifiers .get (OO000O00O0OOO00OO )#line:571
                if OOOOOO0O0OO00O0O0 >=1 and OOOOOO0O0OO00O0O0 <100 :#line:572
                    OOOOOO0O0OO00O0O0 =OOOOOO0O0OO00O0O0 *1.0 /100 #line:573
                O000OOO00OOO0O0OO =min (O0O0O0O00OOOOOO00 )*1.0 /sum (O0O0O0O00OOOOOO00 )#line:574
                OO0OOOO0O0O0O0000 =max (O0O0O0O00OOOOOO00 )*1.0 /sum (O0O0O0O00OOOOOO00 )#line:575
                O0OO0O0O0000OOO00 =O0OO0O0O0000OOO00 and (OOOOOO0O0OO00O0O0 >=OO0OOOO0O0O0O0000 -O000OOO00OOO0O0OO )#line:576
        OOO000O0OO0O0OO00 ={}#line:577
        if O0OO0O0O0000OOO00 ==True :#line:578
            if O00OOOO00OO0O0OO0 .verbosity ['debug']:#line:579
                print ("Rule found: base: "+str (OOO0O0OO000O00000 )+", hist: "+str (O0O0O0O00OOOOOO00 )+", max: "+str (max (O0O0O0O00OOOOOO00 ))+", min: "+str (min (O0O0O0O00OOOOOO00 ))+", s_up: "+str (O0O0000O0OOO0OO0O )+", s_down: "+str (O000O00OOO000OO00 ))#line:580
            O00OOOO00OO0O0OO0 .stats ['total_valid']+=1 #line:581
            OOO000O0OO0O0OO00 ["base"]=OOO0O0OO000O00000 #line:582
            OOO000O0OO0O0OO00 ["rel_base"]=OOO0O0OO000O00000 *1.0 /O00OOOO00OO0O0OO0 .data ["rows_count"]#line:583
            OOO000O0OO0O0OO00 ["s_up"]=O0O0000O0OOO0OO0O #line:584
            OOO000O0OO0O0OO00 ["s_down"]=O000O00OOO000OO00 #line:585
            OOO000O0OO0O0OO00 ["s_any_up"]=O0OO00O00000OO0O0 #line:586
            OOO000O0OO0O0OO00 ["s_any_down"]=O0000O0OOO00OOO0O #line:587
            OOO000O0OO0O0OO00 ["max"]=max (O0O0O0O00OOOOOO00 )#line:588
            OOO000O0OO0O0OO00 ["min"]=min (O0O0O0O00OOOOOO00 )#line:589
            if O00OOOO00OO0O0OO0 .verbosity ['debug']:#line:590
                OOO000O0OO0O0OO00 ["rel_max"]=max (O0O0O0O00OOOOOO00 )*1.0 /O00OOOO00OO0O0OO0 .data ["rows_count"]#line:591
                OOO000O0OO0O0OO00 ["rel_min"]=min (O0O0O0O00OOOOOO00 )*1.0 /O00OOOO00OO0O0OO0 .data ["rows_count"]#line:592
            if sum (O0O0O0O00OOOOOO00 )>0 :#line:593
                OOO000O0OO0O0OO00 ["rel_max"]=max (O0O0O0O00OOOOOO00 )*1.0 /sum (O0O0O0O00OOOOOO00 )#line:594
                OOO000O0OO0O0OO00 ["rel_min"]=min (O0O0O0O00OOOOOO00 )*1.0 /sum (O0O0O0O00OOOOOO00 )#line:595
            else :#line:596
                OOO000O0OO0O0OO00 ["rel_max"]=0 #line:597
                OOO000O0OO0O0OO00 ["rel_min"]=0 #line:598
            OOO000O0OO0O0OO00 ["hist"]=O0O0O0O00OOOOOO00 #line:599
            if OOOO00O00OOOOO0O0 :#line:600
                OOO000O0OO0O0OO00 ["aad"]=O0OO00O0OO00O00OO #line:601
                OOO000O0OO0O0OO00 ["hist_full"]=O00OO0O0OO0O0OOOO #line:602
                OOO000O0OO0O0OO00 ["rel_hist"]=[O00000O0OOO000O0O /sum (O0O0O0O00OOOOOO00 )for O00000O0OOO000O0O in O0O0O0O00OOOOOO00 ]#line:603
                OOO000O0OO0O0OO00 ["rel_hist_full"]=[OOO0000OOO00OOOO0 /sum (O00OO0O0OO0O0OOOO )for OOO0000OOO00OOOO0 in O00OO0O0OO0O0OOOO ]#line:604
        if O00OOOO00OO0O0OO0 .verbosity ['debug']:#line:605
            print ("Info: base: "+str (OOO0O0OO000O00000 )+", hist: "+str (O0O0O0O00OOOOOO00 )+", max: "+str (max (O0O0O0O00OOOOOO00 ))+", min: "+str (min (O0O0O0O00OOOOOO00 ))+", s_up: "+str (O0O0000O0OOO0OO0O )+", s_down: "+str (O000O00OOO000OO00 ))#line:606
        return O0OO0O0O0000OOO00 ,OOO000O0OO0O0OO00 #line:607
    def _verifyUIC (OO000OO00OO000000 ,_O0000O0O0O0OO0OOO ):#line:609
        O0000OO0O0O0O0O00 ={}#line:610
        O000OOO0OO0O0O0OO =0 #line:611
        for OOO0O0O00O0000000 in OO000OO00OO000000 .task_actinfo ['cedents']:#line:612
            O0000OO0O0O0O0O00 [OOO0O0O00O0000000 ['cedent_type']]=OOO0O0O00O0000000 ['filter_value']#line:613
            O000OOO0OO0O0O0OO =O000OOO0OO0O0O0OO +1 #line:614
        if OO000OO00OO000000 .verbosity ['debug']:#line:615
            print (OOO0O0O00O0000000 ['cedent_type']+" : "+str (OOO0O0O00O0000000 ['filter_value']))#line:616
        O0OO00O0O0OO00OOO =OO000OO00OO000000 ._bitcount (_O0000O0O0O0OO0OOO )#line:617
        OOO0OO000OO00000O =[]#line:618
        OO0OO0O0OO00OOOO0 =0 #line:619
        OOOOOO0O00O0O000O =0 #line:620
        O0000OOOOO0000O0O =0 #line:621
        O0000O00O0OOOO00O =[]#line:622
        O0OOO0O00000O00O0 =[]#line:623
        if ('aad_weights'in OO000OO00OO000000 .quantifiers ):#line:624
            O0000O00O0OOOO00O =OO000OO00OO000000 .quantifiers .get ('aad_weights')#line:625
            OOOOOO0O00O0O000O =1 #line:626
        OOO000OO0OOOO0000 =OO000OO00OO000000 .data ["dm"][OO000OO00OO000000 .data ["varname"].index (OO000OO00OO000000 .kwargs .get ('target'))]#line:627
        for OO0O0OOOO0OO00O0O in range (len (OOO000OO0OOOO0000 )):#line:628
            OOOOOOO0OO0O0OOO0 =OO0OO0O0OO00OOOO0 #line:630
            OO0OO0O0OO00OOOO0 =OO000OO00OO000000 ._bitcount (_O0000O0O0O0OO0OOO &OOO000OO0OOOO0000 [OO0O0OOOO0OO00O0O ])#line:631
            OOO0OO000OO00000O .append (OO0OO0O0OO00OOOO0 )#line:632
            O0000OOOOOO000OOO =OO000OO00OO000000 ._bitcount (O0000OO0O0O0O0O00 ['cond']&OOO000OO0OOOO0000 [OO0O0OOOO0OO00O0O ])#line:634
            O0OOO0O00000O00O0 .append (O0000OOOOOO000OOO )#line:635
        O0OOO0OOO0O00O000 =0 #line:637
        OO0OOO0O0OOO0O0O0 =0 #line:638
        if (OOOOOO0O00O0O000O &sum (OOO0OO000OO00000O )>0 ):#line:639
            for OO0O0OOOO0OO00O0O in range (len (OOO000OO0OOOO0000 )):#line:640
                if O0OOO0O00000O00O0 [OO0O0OOOO0OO00O0O ]>0 :#line:641
                    if OOO0OO000OO00000O [OO0O0OOOO0OO00O0O ]/sum (OOO0OO000OO00000O )>O0OOO0O00000O00O0 [OO0O0OOOO0OO00O0O ]/sum (O0OOO0O00000O00O0 ):#line:642
                        O0000OOOOO0000O0O +=O0000O00O0OOOO00O [OO0O0OOOO0OO00O0O ]*((OOO0OO000OO00000O [OO0O0OOOO0OO00O0O ]/sum (OOO0OO000OO00000O ))/(O0OOO0O00000O00O0 [OO0O0OOOO0OO00O0O ]/sum (O0OOO0O00000O00O0 ))-1 )#line:643
                if O0000O00O0OOOO00O [OO0O0OOOO0OO00O0O ]>0 :#line:644
                    O0OOO0OOO0O00O000 +=OOO0OO000OO00000O [OO0O0OOOO0OO00O0O ]#line:645
                    OO0OOO0O0OOO0O0O0 +=O0OOO0O00000O00O0 [OO0O0OOOO0OO00O0O ]#line:646
        O0O0O0O0O0OO0O0O0 =0 #line:647
        if sum (OOO0OO000OO00000O )>0 and OO0OOO0O0OOO0O0O0 >0 :#line:648
            O0O0O0O0O0OO0O0O0 =(O0OOO0OOO0O00O000 /sum (OOO0OO000OO00000O ))/(OO0OOO0O0OOO0O0O0 /sum (O0OOO0O00000O00O0 ))#line:649
        OOO0O0OO0OO0O00OO =True #line:653
        for O00OO0OO0O000O0OO in OO000OO00OO000000 .quantifiers .keys ():#line:654
            if O00OO0OO0O000O0OO .upper ()=='BASE':#line:655
                OOO0O0OO0OO0O00OO =OOO0O0OO0OO0O00OO and (OO000OO00OO000000 .quantifiers .get (O00OO0OO0O000O0OO )<=O0OO00O0O0OO00OOO )#line:656
            if O00OO0OO0O000O0OO .upper ()=='RELBASE':#line:657
                OOO0O0OO0OO0O00OO =OOO0O0OO0OO0O00OO and (OO000OO00OO000000 .quantifiers .get (O00OO0OO0O000O0OO )<=O0OO00O0O0OO00OOO *1.0 /OO000OO00OO000000 .data ["rows_count"])#line:658
            if O00OO0OO0O000O0OO .upper ()=='AAD_SCORE':#line:659
                OOO0O0OO0OO0O00OO =OOO0O0OO0OO0O00OO and (OO000OO00OO000000 .quantifiers .get (O00OO0OO0O000O0OO )<=O0000OOOOO0000O0O )#line:660
            if O00OO0OO0O000O0OO .upper ()=='RELEVANT_CAT_BASE':#line:661
                OOO0O0OO0OO0O00OO =OOO0O0OO0OO0O00OO and (OO000OO00OO000000 .quantifiers .get (O00OO0OO0O000O0OO )<=O0OOO0OOO0O00O000 )#line:662
            if O00OO0OO0O000O0OO .upper ()=='RELEVANT_BASE_LIFT':#line:663
                OOO0O0OO0OO0O00OO =OOO0O0OO0OO0O00OO and (OO000OO00OO000000 .quantifiers .get (O00OO0OO0O000O0OO )<=O0O0O0O0O0OO0O0O0 )#line:664
        O00OOOOOO0OO000OO ={}#line:665
        if OOO0O0OO0OO0O00OO ==True :#line:666
            OO000OO00OO000000 .stats ['total_valid']+=1 #line:667
            O00OOOOOO0OO000OO ["base"]=O0OO00O0O0OO00OOO #line:668
            O00OOOOOO0OO000OO ["rel_base"]=O0OO00O0O0OO00OOO *1.0 /OO000OO00OO000000 .data ["rows_count"]#line:669
            O00OOOOOO0OO000OO ["hist"]=OOO0OO000OO00000O #line:670
            O00OOOOOO0OO000OO ["aad_score"]=O0000OOOOO0000O0O #line:671
            O00OOOOOO0OO000OO ["hist_cond"]=O0OOO0O00000O00O0 #line:672
            O00OOOOOO0OO000OO ["rel_hist"]=[OOOOOOOOO00OOOOOO /sum (OOO0OO000OO00000O )for OOOOOOOOO00OOOOOO in OOO0OO000OO00000O ]#line:673
            O00OOOOOO0OO000OO ["rel_hist_cond"]=[OO00O0O0OOOO0O000 /sum (O0OOO0O00000O00O0 )for OO00O0O0OOOO0O000 in O0OOO0O00000O00O0 ]#line:674
            O00OOOOOO0OO000OO ["relevant_base_lift"]=O0O0O0O0O0OO0O0O0 #line:675
            O00OOOOOO0OO000OO ["relevant_cat_base"]=O0OOO0OOO0O00O000 #line:676
            O00OOOOOO0OO000OO ["relevant_cat_base_full"]=OO0OOO0O0OOO0O0O0 #line:677
        return OOO0O0OO0OO0O00OO ,O00OOOOOO0OO000OO #line:678
    def _verify4ft (O000OO000OO000OO0 ,_OO000OO00O00O0OOO ,_trace_cedent =None ,_traces =None ):#line:680
        OO00OOOOO0O00000O ={}#line:681
        OO0O0OO00O0000O00 =0 #line:682
        for O0OO00000O0OO0OOO in O000OO000OO000OO0 .task_actinfo ['cedents']:#line:683
            OO00OOOOO0O00000O [O0OO00000O0OO0OOO ['cedent_type']]=O0OO00000O0OO0OOO ['filter_value']#line:684
            OO0O0OO00O0000O00 =OO0O0OO00O0000O00 +1 #line:685
        OOOOO000O00O0OOOO =O000OO000OO000OO0 ._bitcount (OO00OOOOO0O00000O ['ante']&OO00OOOOO0O00000O ['succ']&OO00OOOOO0O00000O ['cond'])#line:686
        OOOOO0O000000OOO0 =None #line:687
        OOOOO0O000000OOO0 =0 #line:688
        if OOOOO000O00O0OOOO >0 :#line:689
            OOOOO0O000000OOO0 =O000OO000OO000OO0 ._bitcount (OO00OOOOO0O00000O ['ante']&OO00OOOOO0O00000O ['succ']&OO00OOOOO0O00000O ['cond'])*1.0 /O000OO000OO000OO0 ._bitcount (OO00OOOOO0O00000O ['ante']&OO00OOOOO0O00000O ['cond'])#line:690
        O00OO0O0OO0OOO0O0 =1 <<O000OO000OO000OO0 .data ["rows_count"]#line:692
        OOO0O0OO00O00OO00 =O000OO000OO000OO0 ._bitcount (OO00OOOOO0O00000O ['ante']&OO00OOOOO0O00000O ['succ']&OO00OOOOO0O00000O ['cond'])#line:693
        OO0OOO0O0O0OO0OOO =O000OO000OO000OO0 ._bitcount (OO00OOOOO0O00000O ['ante']&~(O00OO0O0OO0OOO0O0 |OO00OOOOO0O00000O ['succ'])&OO00OOOOO0O00000O ['cond'])#line:694
        O0OO00000O0OO0OOO =O000OO000OO000OO0 ._bitcount (~(O00OO0O0OO0OOO0O0 |OO00OOOOO0O00000O ['ante'])&OO00OOOOO0O00000O ['succ']&OO00OOOOO0O00000O ['cond'])#line:695
        O0OOOOOOOO00OO0O0 =O000OO000OO000OO0 ._bitcount (~(O00OO0O0OO0OOO0O0 |OO00OOOOO0O00000O ['ante'])&~(O00OO0O0OO0OOO0O0 |OO00OOOOO0O00000O ['succ'])&OO00OOOOO0O00000O ['cond'])#line:696
        OO0OO00OO0OOOO0OO =0 #line:697
        O00OOOOO0000O00OO =0 #line:698
        if (OOO0O0OO00O00OO00 +OO0OOO0O0O0OO0OOO )*(OOO0O0OO00O00OO00 +O0OO00000O0OO0OOO )>0 :#line:699
            OO0OO00OO0OOOO0OO =OOO0O0OO00O00OO00 *(OOO0O0OO00O00OO00 +OO0OOO0O0O0OO0OOO +O0OO00000O0OO0OOO +O0OOOOOOOO00OO0O0 )/(OOO0O0OO00O00OO00 +OO0OOO0O0O0OO0OOO )/(OOO0O0OO00O00OO00 +O0OO00000O0OO0OOO )-1 #line:700
            O00OOOOO0000O00OO =OO0OO00OO0OOOO0OO +1 #line:701
        else :#line:702
            OO0OO00OO0OOOO0OO =None #line:703
            O00OOOOO0000O00OO =None #line:704
        O0OOOOO0OO0OOO000 =0 #line:705
        if (OOO0O0OO00O00OO00 +OO0OOO0O0O0OO0OOO )*(OOO0O0OO00O00OO00 +O0OO00000O0OO0OOO )>0 :#line:706
            O0OOOOO0OO0OOO000 =1 -OOO0O0OO00O00OO00 *(OOO0O0OO00O00OO00 +OO0OOO0O0O0OO0OOO +O0OO00000O0OO0OOO +O0OOOOOOOO00OO0O0 )/(OOO0O0OO00O00OO00 +OO0OOO0O0O0OO0OOO )/(OOO0O0OO00O00OO00 +O0OO00000O0OO0OOO )#line:707
        else :#line:708
            O0OOOOO0OO0OOO000 =None #line:709
        O0O0OO00000OOOO0O =True #line:710
        for OOO00O0000O000000 in O000OO000OO000OO0 .quantifiers .keys ():#line:711
            if OOO00O0000O000000 .upper ()=='BASE':#line:712
                O0O0OO00000OOOO0O =O0O0OO00000OOOO0O and (O000OO000OO000OO0 .quantifiers .get (OOO00O0000O000000 )<=OOOOO000O00O0OOOO )#line:713
            if OOO00O0000O000000 .upper ()=='RELBASE':#line:714
                O0O0OO00000OOOO0O =O0O0OO00000OOOO0O and (O000OO000OO000OO0 .quantifiers .get (OOO00O0000O000000 )<=OOOOO000O00O0OOOO *1.0 /O000OO000OO000OO0 .data ["rows_count"])#line:715
            if (OOO00O0000O000000 .upper ()=='PIM')or (OOO00O0000O000000 .upper ()=='CONF'):#line:716
                O0O0OO00000OOOO0O =O0O0OO00000OOOO0O and (O000OO000OO000OO0 .quantifiers .get (OOO00O0000O000000 )<=OOOOO0O000000OOO0 )#line:717
            if OOO00O0000O000000 .upper ()=='AAD':#line:718
                if OO0OO00OO0OOOO0OO !=None :#line:719
                    O0O0OO00000OOOO0O =O0O0OO00000OOOO0O and (O000OO000OO000OO0 .quantifiers .get (OOO00O0000O000000 )<=OO0OO00OO0OOOO0OO )#line:720
                else :#line:721
                    O0O0OO00000OOOO0O =False #line:722
            if OOO00O0000O000000 .upper ()=='BAD':#line:723
                if O0OOOOO0OO0OOO000 !=None :#line:724
                    O0O0OO00000OOOO0O =O0O0OO00000OOOO0O and (O000OO000OO000OO0 .quantifiers .get (OOO00O0000O000000 )<=O0OOOOO0OO0OOO000 )#line:725
                else :#line:726
                    O0O0OO00000OOOO0O =False #line:727
            if OOO00O0000O000000 .upper ()=='LAMBDA'or OOO00O0000O000000 .upper ()=='FN':#line:728
                OO00O00O0OO0OOOOO =O000OO000OO000OO0 .quantifiers .get (OOO00O0000O000000 )#line:729
                OO0OOO0OOO0OO0000 =[OOO0O0OO00O00OO00 ,OO0OOO0O0O0OO0OOO ,O0OO00000O0OO0OOO ,O0OOOOOOOO00OO0O0 ]#line:730
                OOOO0OOOO0O0O00OO =OO00O00O0OO0OOOOO .__code__ .co_argcount #line:731
                if OOOO0OOOO0O0O00OO ==1 :#line:733
                    O0O0OO00000OOOO0O =O0O0OO00000OOOO0O and OO00O00O0OO0OOOOO (OO0OOO0OOO0OO0000 )#line:734
                elif OOOO0OOOO0O0O00OO ==2 :#line:735
                    O0OO00OO0O0O00O0O ={}#line:736
                    O0OO00O0O0OOOO000 ={}#line:737
                    O0OO00O0O0OOOO000 ["varname"]=O000OO000OO000OO0 .data ["varname"]#line:738
                    O0OO00O0O0OOOO000 ["catnames"]=O000OO000OO000OO0 .data ["catnames"]#line:739
                    O0OO00OO0O0O00O0O ['datalabels']=O0OO00O0O0OOOO000 #line:740
                    O0OO00OO0O0O00O0O ['trace_cedent']=_trace_cedent #line:741
                    O0OO00OO0O0O00O0O ['traces']=_traces #line:742
                    O0O0OO00000OOOO0O =O0O0OO00000OOOO0O and OO00O00O0OO0OOOOO (OO0OOO0OOO0OO0000 ,O0OO00OO0O0O00O0O )#line:745
                else :#line:746
                    print (f"Unsupported number of arguments for lambda function ({OOOO0OOOO0O0O00OO} for procedure SD4ft-Miner")#line:747
            O000O0O00O00OO000 ={}#line:748
        if O0O0OO00000OOOO0O ==True :#line:749
            O000OO000OO000OO0 .stats ['total_valid']+=1 #line:750
            O000O0O00O00OO000 ["base"]=OOOOO000O00O0OOOO #line:751
            O000O0O00O00OO000 ["rel_base"]=OOOOO000O00O0OOOO *1.0 /O000OO000OO000OO0 .data ["rows_count"]#line:752
            O000O0O00O00OO000 ["conf"]=OOOOO0O000000OOO0 #line:753
            O000O0O00O00OO000 ["aad"]=OO0OO00OO0OOOO0OO #line:754
            O000O0O00O00OO000 ["bad"]=O0OOOOO0OO0OOO000 #line:755
            O000O0O00O00OO000 ["fourfold"]=[OOO0O0OO00O00OO00 ,OO0OOO0O0O0OO0OOO ,O0OO00000O0OO0OOO ,O0OOOOOOOO00OO0O0 ]#line:756
        return O0O0OO00000OOOO0O ,O000O0O00O00OO000 #line:757
    def _verifysd4ft (OO0OO00OO0OOO0O00 ,_OOO0O0OOO0OO0OOO0 ):#line:759
        OOO0O0O0O0OO00OO0 ={}#line:760
        OOO00O000O0OOOO0O =0 #line:761
        for O00O00OO000OO0O0O in OO0OO00OO0OOO0O00 .task_actinfo ['cedents']:#line:762
            OOO0O0O0O0OO00OO0 [O00O00OO000OO0O0O ['cedent_type']]=O00O00OO000OO0O0O ['filter_value']#line:763
            OOO00O000O0OOOO0O =OOO00O000O0OOOO0O +1 #line:764
        O00OOOO00O00OOOOO =OO0OO00OO0OOO0O00 ._bitcount (OOO0O0O0O0OO00OO0 ['ante']&OOO0O0O0O0OO00OO0 ['succ']&OOO0O0O0O0OO00OO0 ['cond']&OOO0O0O0O0OO00OO0 ['frst'])#line:765
        O0O0O00OO0OOO0O00 =OO0OO00OO0OOO0O00 ._bitcount (OOO0O0O0O0OO00OO0 ['ante']&OOO0O0O0O0OO00OO0 ['succ']&OOO0O0O0O0OO00OO0 ['cond']&OOO0O0O0O0OO00OO0 ['scnd'])#line:766
        OO0OO0OOOO000O0O0 =None #line:767
        O000OOOO0O000O000 =0 #line:768
        O0OO000O0OOO00OOO =0 #line:769
        if O00OOOO00O00OOOOO >0 :#line:770
            O000OOOO0O000O000 =OO0OO00OO0OOO0O00 ._bitcount (OOO0O0O0O0OO00OO0 ['ante']&OOO0O0O0O0OO00OO0 ['succ']&OOO0O0O0O0OO00OO0 ['cond']&OOO0O0O0O0OO00OO0 ['frst'])*1.0 /OO0OO00OO0OOO0O00 ._bitcount (OOO0O0O0O0OO00OO0 ['ante']&OOO0O0O0O0OO00OO0 ['cond']&OOO0O0O0O0OO00OO0 ['frst'])#line:771
        if O0O0O00OO0OOO0O00 >0 :#line:772
            O0OO000O0OOO00OOO =OO0OO00OO0OOO0O00 ._bitcount (OOO0O0O0O0OO00OO0 ['ante']&OOO0O0O0O0OO00OO0 ['succ']&OOO0O0O0O0OO00OO0 ['cond']&OOO0O0O0O0OO00OO0 ['scnd'])*1.0 /OO0OO00OO0OOO0O00 ._bitcount (OOO0O0O0O0OO00OO0 ['ante']&OOO0O0O0O0OO00OO0 ['cond']&OOO0O0O0O0OO00OO0 ['scnd'])#line:773
        OO00O000OO00000OO =1 <<OO0OO00OO0OOO0O00 .data ["rows_count"]#line:775
        O000OOOO00O00OO0O =OO0OO00OO0OOO0O00 ._bitcount (OOO0O0O0O0OO00OO0 ['ante']&OOO0O0O0O0OO00OO0 ['succ']&OOO0O0O0O0OO00OO0 ['cond']&OOO0O0O0O0OO00OO0 ['frst'])#line:776
        O000OOO0000O00OOO =OO0OO00OO0OOO0O00 ._bitcount (OOO0O0O0O0OO00OO0 ['ante']&~(OO00O000OO00000OO |OOO0O0O0O0OO00OO0 ['succ'])&OOO0O0O0O0OO00OO0 ['cond']&OOO0O0O0O0OO00OO0 ['frst'])#line:777
        OOOO0OOO0O000O0OO =OO0OO00OO0OOO0O00 ._bitcount (~(OO00O000OO00000OO |OOO0O0O0O0OO00OO0 ['ante'])&OOO0O0O0O0OO00OO0 ['succ']&OOO0O0O0O0OO00OO0 ['cond']&OOO0O0O0O0OO00OO0 ['frst'])#line:778
        OOO00OOO000OOO0O0 =OO0OO00OO0OOO0O00 ._bitcount (~(OO00O000OO00000OO |OOO0O0O0O0OO00OO0 ['ante'])&~(OO00O000OO00000OO |OOO0O0O0O0OO00OO0 ['succ'])&OOO0O0O0O0OO00OO0 ['cond']&OOO0O0O0O0OO00OO0 ['frst'])#line:779
        OO0OO00O0O000OO00 =OO0OO00OO0OOO0O00 ._bitcount (OOO0O0O0O0OO00OO0 ['ante']&OOO0O0O0O0OO00OO0 ['succ']&OOO0O0O0O0OO00OO0 ['cond']&OOO0O0O0O0OO00OO0 ['scnd'])#line:780
        O0O00O0O000OOO00O =OO0OO00OO0OOO0O00 ._bitcount (OOO0O0O0O0OO00OO0 ['ante']&~(OO00O000OO00000OO |OOO0O0O0O0OO00OO0 ['succ'])&OOO0O0O0O0OO00OO0 ['cond']&OOO0O0O0O0OO00OO0 ['scnd'])#line:781
        O00O0000O0OO00OOO =OO0OO00OO0OOO0O00 ._bitcount (~(OO00O000OO00000OO |OOO0O0O0O0OO00OO0 ['ante'])&OOO0O0O0O0OO00OO0 ['succ']&OOO0O0O0O0OO00OO0 ['cond']&OOO0O0O0O0OO00OO0 ['scnd'])#line:782
        OOO0O0000O0OO00OO =OO0OO00OO0OOO0O00 ._bitcount (~(OO00O000OO00000OO |OOO0O0O0O0OO00OO0 ['ante'])&~(OO00O000OO00000OO |OOO0O0O0O0OO00OO0 ['succ'])&OOO0O0O0O0OO00OO0 ['cond']&OOO0O0O0O0OO00OO0 ['scnd'])#line:783
        OOOO0000O00OO0O0O =True #line:784
        for OO0O0OOOOO0OOOO0O in OO0OO00OO0OOO0O00 .quantifiers .keys ():#line:785
            if (OO0O0OOOOO0OOOO0O .upper ()=='FRSTBASE')|(OO0O0OOOOO0OOOO0O .upper ()=='BASE1'):#line:786
                OOOO0000O00OO0O0O =OOOO0000O00OO0O0O and (OO0OO00OO0OOO0O00 .quantifiers .get (OO0O0OOOOO0OOOO0O )<=O00OOOO00O00OOOOO )#line:787
            if (OO0O0OOOOO0OOOO0O .upper ()=='SCNDBASE')|(OO0O0OOOOO0OOOO0O .upper ()=='BASE2'):#line:788
                OOOO0000O00OO0O0O =OOOO0000O00OO0O0O and (OO0OO00OO0OOO0O00 .quantifiers .get (OO0O0OOOOO0OOOO0O )<=O0O0O00OO0OOO0O00 )#line:789
            if (OO0O0OOOOO0OOOO0O .upper ()=='FRSTRELBASE')|(OO0O0OOOOO0OOOO0O .upper ()=='RELBASE1'):#line:790
                OOOO0000O00OO0O0O =OOOO0000O00OO0O0O and (OO0OO00OO0OOO0O00 .quantifiers .get (OO0O0OOOOO0OOOO0O )<=O00OOOO00O00OOOOO *1.0 /OO0OO00OO0OOO0O00 .data ["rows_count"])#line:791
            if (OO0O0OOOOO0OOOO0O .upper ()=='SCNDRELBASE')|(OO0O0OOOOO0OOOO0O .upper ()=='RELBASE2'):#line:792
                OOOO0000O00OO0O0O =OOOO0000O00OO0O0O and (OO0OO00OO0OOO0O00 .quantifiers .get (OO0O0OOOOO0OOOO0O )<=O0O0O00OO0OOO0O00 *1.0 /OO0OO00OO0OOO0O00 .data ["rows_count"])#line:793
            if (OO0O0OOOOO0OOOO0O .upper ()=='FRSTPIM')|(OO0O0OOOOO0OOOO0O .upper ()=='PIM1')|(OO0O0OOOOO0OOOO0O .upper ()=='FRSTCONF')|(OO0O0OOOOO0OOOO0O .upper ()=='CONF1'):#line:794
                OOOO0000O00OO0O0O =OOOO0000O00OO0O0O and (OO0OO00OO0OOO0O00 .quantifiers .get (OO0O0OOOOO0OOOO0O )<=O000OOOO0O000O000 )#line:795
            if (OO0O0OOOOO0OOOO0O .upper ()=='SCNDPIM')|(OO0O0OOOOO0OOOO0O .upper ()=='PIM2')|(OO0O0OOOOO0OOOO0O .upper ()=='SCNDCONF')|(OO0O0OOOOO0OOOO0O .upper ()=='CONF2'):#line:796
                OOOO0000O00OO0O0O =OOOO0000O00OO0O0O and (OO0OO00OO0OOO0O00 .quantifiers .get (OO0O0OOOOO0OOOO0O )<=O0OO000O0OOO00OOO )#line:797
            if (OO0O0OOOOO0OOOO0O .upper ()=='DELTAPIM')|(OO0O0OOOOO0OOOO0O .upper ()=='DELTACONF'):#line:798
                OOOO0000O00OO0O0O =OOOO0000O00OO0O0O and (OO0OO00OO0OOO0O00 .quantifiers .get (OO0O0OOOOO0OOOO0O )<=O000OOOO0O000O000 -O0OO000O0OOO00OOO )#line:799
            if (OO0O0OOOOO0OOOO0O .upper ()=='RATIOPIM')|(OO0O0OOOOO0OOOO0O .upper ()=='RATIOCONF'):#line:800
                if (O0OO000O0OOO00OOO >0 ):#line:801
                    OOOO0000O00OO0O0O =OOOO0000O00OO0O0O and (OO0OO00OO0OOO0O00 .quantifiers .get (OO0O0OOOOO0OOOO0O )<=O000OOOO0O000O000 *1.0 /O0OO000O0OOO00OOO )#line:802
                else :#line:803
                    OOOO0000O00OO0O0O =False #line:804
            if (OO0O0OOOOO0OOOO0O .upper ()=='RATIOPIM_LEQ')|(OO0O0OOOOO0OOOO0O .upper ()=='RATIOCONF_LEQ'):#line:805
                if (O0OO000O0OOO00OOO >0 ):#line:806
                    OOOO0000O00OO0O0O =OOOO0000O00OO0O0O and (OO0OO00OO0OOO0O00 .quantifiers .get (OO0O0OOOOO0OOOO0O )>=O000OOOO0O000O000 *1.0 /O0OO000O0OOO00OOO )#line:807
                else :#line:808
                    OOOO0000O00OO0O0O =False #line:809
            if OO0O0OOOOO0OOOO0O .upper ()=='LAMBDA'or OO0O0OOOOO0OOOO0O .upper ()=='FN':#line:810
                O0OOO00000OOOO0OO =OO0OO00OO0OOO0O00 .quantifiers .get (OO0O0OOOOO0OOOO0O )#line:811
                OOOOOO0OOO00000O0 =O0OOO00000OOOO0OO .func_code .co_argcount #line:812
                O00OOOOOO0O00OO0O =[O000OOOO00O00OO0O ,O000OOO0000O00OOO ,OOOO0OOO0O000O0OO ,OOO00OOO000OOO0O0 ]#line:813
                O0000OO0O0OO0OOO0 =[OO0OO00O0O000OO00 ,O0O00O0O000OOO00O ,O00O0000O0OO00OOO ,OOO0O0000O0OO00OO ]#line:814
                if OOOOOO0OOO00000O0 ==2 :#line:815
                    OOOO0000O00OO0O0O =OOOO0000O00OO0O0O and O0OOO00000OOOO0OO (O00OOOOOO0O00OO0O ,O0000OO0O0OO0OOO0 )#line:816
                elif OOOOOO0OOO00000O0 ==3 :#line:817
                    OOOO0000O00OO0O0O =OOOO0000O00OO0O0O and O0OOO00000OOOO0OO (O00OOOOOO0O00OO0O ,O0000OO0O0OO0OOO0 ,None )#line:818
                else :#line:819
                    print (f"Unsupported number of arguments for lambda function ({OOOOOO0OOO00000O0} for procedure SD4ft-Miner")#line:820
        OOO00O00O0OO00OOO ={}#line:821
        if OOOO0000O00OO0O0O ==True :#line:822
            OO0OO00OO0OOO0O00 .stats ['total_valid']+=1 #line:823
            OOO00O00O0OO00OOO ["base1"]=O00OOOO00O00OOOOO #line:824
            OOO00O00O0OO00OOO ["base2"]=O0O0O00OO0OOO0O00 #line:825
            OOO00O00O0OO00OOO ["rel_base1"]=O00OOOO00O00OOOOO *1.0 /OO0OO00OO0OOO0O00 .data ["rows_count"]#line:826
            OOO00O00O0OO00OOO ["rel_base2"]=O0O0O00OO0OOO0O00 *1.0 /OO0OO00OO0OOO0O00 .data ["rows_count"]#line:827
            OOO00O00O0OO00OOO ["conf1"]=O000OOOO0O000O000 #line:828
            OOO00O00O0OO00OOO ["conf2"]=O0OO000O0OOO00OOO #line:829
            OOO00O00O0OO00OOO ["deltaconf"]=O000OOOO0O000O000 -O0OO000O0OOO00OOO #line:830
            if (O0OO000O0OOO00OOO >0 ):#line:831
                OOO00O00O0OO00OOO ["ratioconf"]=O000OOOO0O000O000 *1.0 /O0OO000O0OOO00OOO #line:832
            else :#line:833
                OOO00O00O0OO00OOO ["ratioconf"]=None #line:834
            OOO00O00O0OO00OOO ["fourfold1"]=[O000OOOO00O00OO0O ,O000OOO0000O00OOO ,OOOO0OOO0O000O0OO ,OOO00OOO000OOO0O0 ]#line:835
            OOO00O00O0OO00OOO ["fourfold2"]=[OO0OO00O0O000OO00 ,O0O00O0O000OOO00O ,O00O0000O0OO00OOO ,OOO0O0000O0OO00OO ]#line:836
        return OOOO0000O00OO0O0O ,OOO00O00O0OO00OOO #line:837
    def _verify_opt (OOOOO00000OO00O00 ,O0000OOO0O00OO00O ,OOOOO0000OOO0000O ):#line:840
        OOOOO00000OO00O00 .stats ['total_ver']+=1 #line:841
        OO00OOOOO00O0OO0O =False #line:842
        if not (O0000OOO0O00OO00O ['optim'].get ('only_con')):#line:843
            return False #line:844
        if OOOOO00000OO00O00 .verbosity ['debug']:#line:845
            print (OOOOO00000OO00O00 .options ['optimizations'])#line:846
        if not (OOOOO00000OO00O00 .options ['optimizations']):#line:847
            if OOOOO00000OO00O00 .verbosity ['debug']:#line:848
                print ("NO OPTS")#line:849
            return False #line:850
        if OOOOO00000OO00O00 .verbosity ['debug']:#line:851
            print ("OPTS")#line:852
        OO000OOOO00O000O0 ={}#line:853
        for O0O0OO0OOO0O000OO in OOOOO00000OO00O00 .task_actinfo ['cedents']:#line:854
            if OOOOO00000OO00O00 .verbosity ['debug']:#line:855
                print (O0O0OO0OOO0O000OO ['cedent_type'])#line:856
            OO000OOOO00O000O0 [O0O0OO0OOO0O000OO ['cedent_type']]=O0O0OO0OOO0O000OO ['filter_value']#line:857
            if OOOOO00000OO00O00 .verbosity ['debug']:#line:858
                print (O0O0OO0OOO0O000OO ['cedent_type']+" : "+str (O0O0OO0OOO0O000OO ['filter_value']))#line:859
        O0OOOO000O000OOOO =1 <<OOOOO00000OO00O00 .data ["rows_count"]#line:860
        OO0OOOO000O00O000 =O0OOOO000O000OOOO -1 #line:861
        OO00O0O00000O00O0 =""#line:862
        O00OOOOOO0OO0OO00 =0 #line:863
        if (OO000OOOO00O000O0 .get ('ante')!=None ):#line:864
            OO0OOOO000O00O000 =OO0OOOO000O00O000 &OO000OOOO00O000O0 ['ante']#line:865
        if (OO000OOOO00O000O0 .get ('succ')!=None ):#line:866
            OO0OOOO000O00O000 =OO0OOOO000O00O000 &OO000OOOO00O000O0 ['succ']#line:867
        if (OO000OOOO00O000O0 .get ('cond')!=None ):#line:868
            OO0OOOO000O00O000 =OO0OOOO000O00O000 &OO000OOOO00O000O0 ['cond']#line:869
        OO0O0O0O0O0OOO00O =None #line:870
        if (OOOOO00000OO00O00 .proc =='CFMiner')|(OOOOO00000OO00O00 .proc =='4ftMiner')|(OOOOO00000OO00O00 .proc =='UICMiner'):#line:871
            O0OO00OO0O0000O0O =OOOOO00000OO00O00 ._bitcount (OO0OOOO000O00O000 )#line:872
            if not (OOOOO00000OO00O00 ._opt_base ==None ):#line:873
                if not (OOOOO00000OO00O00 ._opt_base <=O0OO00OO0O0000O0O ):#line:874
                    OO00OOOOO00O0OO0O =True #line:875
            if not (OOOOO00000OO00O00 ._opt_relbase ==None ):#line:876
                if not (OOOOO00000OO00O00 ._opt_relbase <=O0OO00OO0O0000O0O *1.0 /OOOOO00000OO00O00 .data ["rows_count"]):#line:877
                    OO00OOOOO00O0OO0O =True #line:878
        if (OOOOO00000OO00O00 .proc =='SD4ftMiner'):#line:879
            O0OO00OO0O0000O0O =OOOOO00000OO00O00 ._bitcount (OO0OOOO000O00O000 )#line:880
            if (not (OOOOO00000OO00O00 ._opt_base1 ==None ))&(not (OOOOO00000OO00O00 ._opt_base2 ==None )):#line:881
                if not (max (OOOOO00000OO00O00 ._opt_base1 ,OOOOO00000OO00O00 ._opt_base2 )<=O0OO00OO0O0000O0O ):#line:882
                    OO00OOOOO00O0OO0O =True #line:883
            if (not (OOOOO00000OO00O00 ._opt_relbase1 ==None ))&(not (OOOOO00000OO00O00 ._opt_relbase2 ==None )):#line:884
                if not (max (OOOOO00000OO00O00 ._opt_relbase1 ,OOOOO00000OO00O00 ._opt_relbase2 )<=O0OO00OO0O0000O0O *1.0 /OOOOO00000OO00O00 .data ["rows_count"]):#line:885
                    OO00OOOOO00O0OO0O =True #line:886
        return OO00OOOOO00O0OO0O #line:888
    def _print (O00O0O000O0OOOOOO ,O0O0OOO0OO0OOOO0O ,_OO0O00OO000O000OO ,_OO00O00OO0OO000O0 ):#line:891
        if (len (_OO0O00OO000O000OO ))!=len (_OO00O00OO0OO000O0 ):#line:892
            print ("DIFF IN LEN for following cedent : "+str (len (_OO0O00OO000O000OO ))+" vs "+str (len (_OO00O00OO0OO000O0 )))#line:893
            print ("trace cedent : "+str (_OO0O00OO000O000OO )+", traces "+str (_OO00O00OO0OO000O0 ))#line:894
        O00OOO0OOO0OO0O00 =''#line:895
        OO0O00OOO0O00O0OO ={}#line:896
        O0OOO0OOO0OOOOOO0 =[]#line:897
        for O00OOO0000O0OO0O0 in range (len (_OO0O00OO000O000OO )):#line:898
            OO0000OOO0O0O0O0O =O00O0O000O0OOOOOO .data ["varname"].index (O0O0OOO0OO0OOOO0O ['defi'].get ('attributes')[_OO0O00OO000O000OO [O00OOO0000O0OO0O0 ]].get ('name'))#line:899
            O00OOO0OOO0OO0O00 =O00OOO0OOO0OO0O00 +O00O0O000O0OOOOOO .data ["varname"][OO0000OOO0O0O0O0O ]+'('#line:900
            O0OOO0OOO0OOOOOO0 .append (OO0000OOO0O0O0O0O )#line:901
            OO00OO0OOOOOO0000 =[]#line:902
            for OO00000000OO0OOOO in _OO00O00OO0OO000O0 [O00OOO0000O0OO0O0 ]:#line:903
                O00OOO0OOO0OO0O00 =O00OOO0OOO0OO0O00 +str (O00O0O000O0OOOOOO .data ["catnames"][OO0000OOO0O0O0O0O ][OO00000000OO0OOOO ])+" "#line:904
                OO00OO0OOOOOO0000 .append (str (O00O0O000O0OOOOOO .data ["catnames"][OO0000OOO0O0O0O0O ][OO00000000OO0OOOO ]))#line:905
            O00OOO0OOO0OO0O00 =O00OOO0OOO0OO0O00 [:-1 ]+')'#line:906
            OO0O00OOO0O00O0OO [O00O0O000O0OOOOOO .data ["varname"][OO0000OOO0O0O0O0O ]]=OO00OO0OOOOOO0000 #line:907
            if O00OOO0000O0OO0O0 +1 <len (_OO0O00OO000O000OO ):#line:908
                O00OOO0OOO0OO0O00 =O00OOO0OOO0OO0O00 +' & '#line:909
        return O00OOO0OOO0OO0O00 ,OO0O00OOO0O00O0OO ,O0OOO0OOO0OOOOOO0 #line:910
    def _print_hypo (OOO0OO00O0O00O000 ,OO0OOO00O00O0O000 ):#line:912
        OOO0OO00O0O00O000 .print_rule (OO0OOO00O00O0O000 )#line:913
    def _print_rule (O0O00O00O00O0OO0O ,O0O000O0OOOO000O0 ):#line:915
        if O0O00O00O00O0OO0O .verbosity ['print_rules']:#line:916
            print ('Rules info : '+str (O0O000O0OOOO000O0 ['params']))#line:917
            for OOOOO0000O0OOOO00 in O0O00O00O00O0OO0O .task_actinfo ['cedents']:#line:918
                print (OOOOO0000O0OOOO00 ['cedent_type']+' = '+OOOOO0000O0OOOO00 ['generated_string'])#line:919
    def _genvar (O0O000O000O00O00O ,O0O0O000O00000000 ,O0O0OO000OOOO0O0O ,_OO000O00O0O000000 ,_O0OO0O00O00O00O00 ,_O0OOOO000OO0O0OO0 ,_OO00OO0O0O00O0OOO ,_O00000O00OO000O00 ,_O0OO0O0O0OOO00000 ,_OOOO0O00OOO0OO000 ):#line:921
        _O00O000000O0OOO0O =0 #line:922
        _OOOO00O0OO0OO00OO =[]#line:923
        for OOOOOOOOOOOOO00O0 in range (O0O0OO000OOOO0O0O ['num_cedent']):#line:924
            if ('force'in O0O0OO000OOOO0O0O ['defi'].get ('attributes')[OOOOOOOOOOOOO00O0 ]and O0O0OO000OOOO0O0O ['defi'].get ('attributes')[OOOOOOOOOOOOO00O0 ].get ('force')):#line:926
                _OOOO00O0OO0OO00OO .append (OOOOOOOOOOOOO00O0 )#line:927
        if O0O0OO000OOOO0O0O ['num_cedent']>0 :#line:928
            _O00O000000O0OOO0O =(_OOOO0O00OOO0OO000 -_O0OO0O0O0OOO00000 )/O0O0OO000OOOO0O0O ['num_cedent']#line:929
        if O0O0OO000OOOO0O0O ['num_cedent']==0 :#line:930
            if len (O0O0O000O00000000 ['cedents_to_do'])>len (O0O0O000O00000000 ['cedents']):#line:931
                O0O0OO0OOOOOO0OO0 ,O000OOOOOOOOOO000 ,O0O000O0000O0O0OO =O0O000O000O00O00O ._print (O0O0OO000OOOO0O0O ,_OO000O00O0O000000 ,_O0OO0O00O00O00O00 )#line:932
                O0O0OO000OOOO0O0O ['generated_string']=O0O0OO0OOOOOO0OO0 #line:933
                O0O0OO000OOOO0O0O ['rule']=O000OOOOOOOOOO000 #line:934
                O0O0OO000OOOO0O0O ['filter_value']=(1 <<O0O000O000O00O00O .data ["rows_count"])-1 #line:935
                O0O0OO000OOOO0O0O ['traces']=[]#line:936
                O0O0OO000OOOO0O0O ['trace_cedent']=[]#line:937
                O0O0OO000OOOO0O0O ['trace_cedent_asindata']=[]#line:938
                O0O0O000O00000000 ['cedents'].append (O0O0OO000OOOO0O0O )#line:939
                _OO000O00O0O000000 .append (None )#line:940
                O0O000O000O00O00O ._start_cedent (O0O0O000O00000000 ,_O0OO0O0O0OOO00000 ,_OOOO0O00OOO0OO000 )#line:941
                O0O0O000O00000000 ['cedents'].pop ()#line:942
        for OOOOOOOOOOOOO00O0 in range (O0O0OO000OOOO0O0O ['num_cedent']):#line:945
            _O00O0O0OO00OO0OOO =True #line:946
            for O000O00OO000O000O in range (len (_OOOO00O0OO0OO00OO )):#line:947
                if O000O00OO000O000O <OOOOOOOOOOOOO00O0 and O000O00OO000O000O not in _OO000O00O0O000000 and O000O00OO000O000O in _OOOO00O0OO0OO00OO :#line:948
                    _O00O0O0OO00OO0OOO =False #line:949
            if (len (_OO000O00O0O000000 )==0 or OOOOOOOOOOOOO00O0 >_OO000O00O0O000000 [-1 ])and _O00O0O0OO00OO0OOO :#line:951
                _OO000O00O0O000000 .append (OOOOOOOOOOOOO00O0 )#line:952
                O0OOOO0O00OOOOO0O =O0O000O000O00O00O .data ["varname"].index (O0O0OO000OOOO0O0O ['defi'].get ('attributes')[OOOOOOOOOOOOO00O0 ].get ('name'))#line:953
                _O00O0OOOO00O00OO0 =O0O0OO000OOOO0O0O ['defi'].get ('attributes')[OOOOOOOOOOOOO00O0 ].get ('minlen')#line:954
                _O00O0O0OOOO000OOO =O0O0OO000OOOO0O0O ['defi'].get ('attributes')[OOOOOOOOOOOOO00O0 ].get ('maxlen')#line:955
                _OO00OO000OO0OOO0O =O0O0OO000OOOO0O0O ['defi'].get ('attributes')[OOOOOOOOOOOOO00O0 ].get ('type')#line:956
                OOO0OOOOOO00000OO =len (O0O000O000O00O00O .data ["dm"][O0OOOO0O00OOOOO0O ])#line:957
                _O0O00OOOO00O000OO =[]#line:958
                _O0OO0O00O00O00O00 .append (_O0O00OOOO00O000OO )#line:959
                _O0O0OO000OOOO0OO0 =int (0 )#line:960
                O0O000O000O00O00O ._gencomb (O0O0O000O00000000 ,O0O0OO000OOOO0O0O ,_OO000O00O0O000000 ,_O0OO0O00O00O00O00 ,_O0O00OOOO00O000OO ,_O0OOOO000OO0O0OO0 ,_O0O0OO000OOOO0OO0 ,OOO0OOOOOO00000OO ,_OO00OO000OO0OOO0O ,_OO00OO0O0O00O0OOO ,_O00000O00OO000O00 ,_O00O0OOOO00O00OO0 ,_O00O0O0OOOO000OOO ,_O0OO0O0O0OOO00000 +OOOOOOOOOOOOO00O0 *_O00O000000O0OOO0O ,_O0OO0O0O0OOO00000 +(OOOOOOOOOOOOO00O0 +1 )*_O00O000000O0OOO0O )#line:961
                _O0OO0O00O00O00O00 .pop ()#line:962
                _OO000O00O0O000000 .pop ()#line:963
    def _gencomb (O0O0OO0O00OOO0O00 ,O0O0O0OO00OOOOOOO ,O0O0O000O00OOO0O0 ,_O00OOOO0000OOOOOO ,_O0O0O00000000OOO0 ,_O000OO0OOOOOO0O0O ,_O0OO00O00OOO0OOO0 ,_O0OOO0O00OOO00OOO ,O0OO00OO000000O00 ,_O00O0O0O000O0OO00 ,_O0OOO0000O0O000OO ,_O0000O0000000O000 ,_O0OO000O000OO0OO0 ,_O00OOOOO000O00OOO ,_O00OO000OOO00OOOO ,_OO0O0O0OO0O00OO0O ,val_list =None ):#line:965
        _OOOO0O000O0OO000O =[]#line:966
        _O0OOO0O000OO0O0OO =val_list #line:967
        if _O00O0O0O000O0OO00 =="subset":#line:968
            if len (_O000OO0OOOOOO0O0O )==0 :#line:969
                _OOOO0O000O0OO000O =range (O0OO00OO000000O00 )#line:970
            else :#line:971
                _OOOO0O000O0OO000O =range (_O000OO0OOOOOO0O0O [-1 ]+1 ,O0OO00OO000000O00 )#line:972
        elif _O00O0O0O000O0OO00 =="seq":#line:973
            if len (_O000OO0OOOOOO0O0O )==0 :#line:974
                _OOOO0O000O0OO000O =range (O0OO00OO000000O00 -_O0OO000O000OO0OO0 +1 )#line:975
            else :#line:976
                if _O000OO0OOOOOO0O0O [-1 ]+1 ==O0OO00OO000000O00 :#line:977
                    return #line:978
                O0OO000000O00O000 =_O000OO0OOOOOO0O0O [-1 ]+1 #line:979
                _OOOO0O000O0OO000O .append (O0OO000000O00O000 )#line:980
        elif _O00O0O0O000O0OO00 =="lcut":#line:981
            if len (_O000OO0OOOOOO0O0O )==0 :#line:982
                O0OO000000O00O000 =0 ;#line:983
            else :#line:984
                if _O000OO0OOOOOO0O0O [-1 ]+1 ==O0OO00OO000000O00 :#line:985
                    return #line:986
                O0OO000000O00O000 =_O000OO0OOOOOO0O0O [-1 ]+1 #line:987
            _OOOO0O000O0OO000O .append (O0OO000000O00O000 )#line:988
        elif _O00O0O0O000O0OO00 =="rcut":#line:989
            if len (_O000OO0OOOOOO0O0O )==0 :#line:990
                O0OO000000O00O000 =O0OO00OO000000O00 -1 ;#line:991
            else :#line:992
                if _O000OO0OOOOOO0O0O [-1 ]==0 :#line:993
                    return #line:994
                O0OO000000O00O000 =_O000OO0OOOOOO0O0O [-1 ]-1 #line:995
                if O0O0OO0O00OOO0O00 .verbosity ['debug']:#line:996
                    print ("Olditem: "+str (_O000OO0OOOOOO0O0O [-1 ])+", Newitem : "+str (O0OO000000O00O000 ))#line:997
            _OOOO0O000O0OO000O .append (O0OO000000O00O000 )#line:998
        elif _O00O0O0O000O0OO00 =="one":#line:999
            if len (_O000OO0OOOOOO0O0O )==0 :#line:1000
                O0O0O000OO0O0000O =O0O0OO0O00OOO0O00 .data ["varname"].index (O0O0O000O00OOO0O0 ['defi'].get ('attributes')[_O00OOOO0000OOOOOO [-1 ]].get ('name'))#line:1001
                try :#line:1002
                    O0OO000000O00O000 =O0O0OO0O00OOO0O00 .data ["catnames"][O0O0O000OO0O0000O ].index (O0O0O000O00OOO0O0 ['defi'].get ('attributes')[_O00OOOO0000OOOOOO [-1 ]].get ('value'))#line:1003
                except :#line:1004
                    print (f"ERROR: attribute '{O0O0O000O00OOO0O0['defi'].get('attributes')[_O00OOOO0000OOOOOO[-1]].get('name')}' has not value '{O0O0O000O00OOO0O0['defi'].get('attributes')[_O00OOOO0000OOOOOO[-1]].get('value')}'")#line:1005
                    exit (1 )#line:1006
                _OOOO0O000O0OO000O .append (O0OO000000O00O000 )#line:1007
                _O0OO000O000OO0OO0 =1 #line:1008
                _O00OOOOO000O00OOO =1 #line:1009
            else :#line:1010
                print ("DEBUG: one category should not have more categories")#line:1011
                return #line:1012
        elif _O00O0O0O000O0OO00 =="list":#line:1014
            if _O0OOO0O000OO0O0OO is None :#line:1015
                O0O0O000OO0O0000O =O0O0OO0O00OOO0O00 .data ["varname"].index (O0O0O000O00OOO0O0 ['defi'].get ('attributes')[_O00OOOO0000OOOOOO [-1 ]].get ('name'))#line:1016
                O00OOOOO00O00OOOO =None #line:1017
                _O0O0O0OO0O0OOO000 =[]#line:1018
                try :#line:1019
                    O0O000000OOO0OOOO =O0O0O000O00OOO0O0 ['defi'].get ('attributes')[_O00OOOO0000OOOOOO [-1 ]].get ('value')#line:1020
                    for O0O0O00OOOO0OO000 in O0O000000OOO0OOOO :#line:1021
                        O00OOOOO00O00OOOO =O0O0O00OOOO0OO000 #line:1022
                        O0OO000000O00O000 =O0O0OO0O00OOO0O00 .data ["catnames"][O0O0O000OO0O0000O ].index (O0O0O00OOOO0OO000 )#line:1023
                        _O0O0O0OO0O0OOO000 .append (O0OO000000O00O000 )#line:1024
                except :#line:1025
                    print (f"ERROR: attribute '{O0O0O000O00OOO0O0['defi'].get('attributes')[_O00OOOO0000OOOOOO[-1]].get('name')}' has not value '{O0O0O00OOOO0OO000}'")#line:1027
                    exit (1 )#line:1028
                _O0OOO0O000OO0O0OO =_O0O0O0OO0O0OOO000 #line:1029
                _O0OO000O000OO0OO0 =len (_O0OOO0O000OO0O0OO )#line:1030
                _O00OOOOO000O00OOO =len (_O0OOO0O000OO0O0OO )#line:1031
            _OOOO0O000O0OO000O .append (_O0OOO0O000OO0O0OO [len (_O000OO0OOOOOO0O0O )])#line:1032
        else :#line:1034
            print ("Attribute type "+_O00O0O0O000O0OO00 +" not supported.")#line:1035
            return #line:1036
        if len (_OOOO0O000O0OO000O )>0 :#line:1038
            _OOOO000000OOO00OO =(_OO0O0O0OO0O00OO0O -_O00OO000OOO00OOOO )/len (_OOOO0O000O0OO000O )#line:1039
        else :#line:1040
            _OOOO000000OOO00OO =0 #line:1041
        _O00OO00000OOOO0OO =0 #line:1043
        for O000O0000OO0OOOOO in _OOOO0O000O0OO000O :#line:1045
                _O000OO0OOOOOO0O0O .append (O000O0000OO0OOOOO )#line:1046
                _O0O0O00000000OOO0 .pop ()#line:1047
                _O0O0O00000000OOO0 .append (_O000OO0OOOOOO0O0O )#line:1048
                _OOOOOOOO000OO000O =_O0OOO0O00OOO00OOO |O0O0OO0O00OOO0O00 .data ["dm"][O0O0OO0O00OOO0O00 .data ["varname"].index (O0O0O000O00OOO0O0 ['defi'].get ('attributes')[_O00OOOO0000OOOOOO [-1 ]].get ('name'))][O000O0000OO0OOOOO ]#line:1049
                _O00O0OOO0O0O000OO =1 #line:1050
                if (len (_O00OOOO0000OOOOOO )<_O0OOO0000O0O000OO ):#line:1051
                    _O00O0OOO0O0O000OO =-1 #line:1052
                    if O0O0OO0O00OOO0O00 .verbosity ['debug']:#line:1053
                        print ("DEBUG: will not verify, low cedent length")#line:1054
                if (len (_O0O0O00000000OOO0 [-1 ])<_O0OO000O000OO0OO0 ):#line:1055
                    _O00O0OOO0O0O000OO =0 #line:1056
                    if O0O0OO0O00OOO0O00 .verbosity ['debug']:#line:1057
                        print ("DEBUG: will not verify, low attribute length")#line:1058
                _OO000O00OO000OOO0 =0 #line:1059
                if O0O0O000O00OOO0O0 ['defi'].get ('type')=='con':#line:1060
                    _OO000O00OO000OOO0 =_O0OO00O00OOO0OOO0 &_OOOOOOOO000OO000O #line:1061
                else :#line:1062
                    _OO000O00OO000OOO0 =_O0OO00O00OOO0OOO0 |_OOOOOOOO000OO000O #line:1063
                O0O0O000O00OOO0O0 ['trace_cedent']=_O00OOOO0000OOOOOO #line:1064
                O0O0O000O00OOO0O0 ['traces']=_O0O0O00000000OOO0 #line:1065
                O0000O00O000OO00O ,O0OO0O00OOO0O00OO ,OOOO00OO000OOO0O0 =O0O0OO0O00OOO0O00 ._print (O0O0O000O00OOO0O0 ,_O00OOOO0000OOOOOO ,_O0O0O00000000OOO0 )#line:1066
                O0O0O000O00OOO0O0 ['generated_string']=O0000O00O000OO00O #line:1067
                O0O0O000O00OOO0O0 ['rule']=O0OO0O00OOO0O00OO #line:1068
                O0O0O000O00OOO0O0 ['filter_value']=_OO000O00OO000OOO0 #line:1069
                O0O0O000O00OOO0O0 ['traces']=copy .deepcopy (_O0O0O00000000OOO0 )#line:1070
                O0O0O000O00OOO0O0 ['trace_cedent']=copy .deepcopy (_O00OOOO0000OOOOOO )#line:1071
                O0O0O000O00OOO0O0 ['trace_cedent_asindata']=copy .deepcopy (OOOO00OO000OOO0O0 )#line:1072
                if O0O0OO0O00OOO0O00 .verbosity ['debug']:#line:1073
                    print (f"TC :{O0O0O000O00OOO0O0['trace_cedent_asindata']}")#line:1074
                O0O0O0OO00OOOOOOO ['cedents'].append (O0O0O000O00OOO0O0 )#line:1075
                O0O00000000000000 =O0O0OO0O00OOO0O00 ._verify_opt (O0O0O0OO00OOOOOOO ,O0O0O000O00OOO0O0 )#line:1076
                if O0O0OO0O00OOO0O00 .verbosity ['debug']:#line:1077
                    print (f"DEBUG: {O0O0O000O00OOO0O0['generated_string']}.")#line:1078
                    print (f"DEBUG: {_O00OOOO0000OOOOOO},{_O0OOO0000O0O000OO}.")#line:1079
                    if O0O00000000000000 :#line:1080
                        print ("DEBUG: Optimization: cutting")#line:1081
                if not (O0O00000000000000 ):#line:1082
                    if _O00O0OOO0O0O000OO ==1 :#line:1083
                        if O0O0OO0O00OOO0O00 .verbosity ['debug']:#line:1084
                            print ("DEBUG: verifying")#line:1085
                        if len (O0O0O0OO00OOOOOOO ['cedents_to_do'])==len (O0O0O0OO00OOOOOOO ['cedents']):#line:1086
                            if O0O0OO0O00OOO0O00 .proc =='CFMiner':#line:1087
                                O00OOO000000O0000 ,OOOO00OOOOOOO00OO =O0O0OO0O00OOO0O00 ._verifyCF (_OO000O00OO000OOO0 )#line:1088
                            elif O0O0OO0O00OOO0O00 .proc =='UICMiner':#line:1089
                                O00OOO000000O0000 ,OOOO00OOOOOOO00OO =O0O0OO0O00OOO0O00 ._verifyUIC (_OO000O00OO000OOO0 )#line:1090
                            elif O0O0OO0O00OOO0O00 .proc =='4ftMiner':#line:1091
                                O00OOO000000O0000 ,OOOO00OOOOOOO00OO =O0O0OO0O00OOO0O00 ._verify4ft (_OOOOOOOO000OO000O ,_O00OOOO0000OOOOOO ,_O0O0O00000000OOO0 )#line:1092
                            elif O0O0OO0O00OOO0O00 .proc =='SD4ftMiner':#line:1093
                                O00OOO000000O0000 ,OOOO00OOOOOOO00OO =O0O0OO0O00OOO0O00 ._verifysd4ft (_OOOOOOOO000OO000O )#line:1094
                            else :#line:1095
                                print ("Unsupported procedure : "+O0O0OO0O00OOO0O00 .proc )#line:1096
                                exit (0 )#line:1097
                            if O00OOO000000O0000 ==True :#line:1098
                                O0O0OOOOO0OO0O00O ={}#line:1099
                                O0O0OOOOO0OO0O00O ["rule_id"]=O0O0OO0O00OOO0O00 .stats ['total_valid']#line:1100
                                O0O0OOOOO0OO0O00O ["cedents_str"]={}#line:1101
                                O0O0OOOOO0OO0O00O ["cedents_struct"]={}#line:1102
                                O0O0OOOOO0OO0O00O ['traces']={}#line:1103
                                O0O0OOOOO0OO0O00O ['trace_cedent_taskorder']={}#line:1104
                                O0O0OOOOO0OO0O00O ['trace_cedent_dataorder']={}#line:1105
                                for O0OO00OOO00OOOO00 in O0O0O0OO00OOOOOOO ['cedents']:#line:1106
                                    if O0O0OO0O00OOO0O00 .verbosity ['debug']:#line:1107
                                        print (O0OO00OOO00OOOO00 )#line:1108
                                    O0O0OOOOO0OO0O00O ['cedents_str'][O0OO00OOO00OOOO00 ['cedent_type']]=O0OO00OOO00OOOO00 ['generated_string']#line:1109
                                    O0O0OOOOO0OO0O00O ['cedents_struct'][O0OO00OOO00OOOO00 ['cedent_type']]=O0OO00OOO00OOOO00 ['rule']#line:1110
                                    O0O0OOOOO0OO0O00O ['traces'][O0OO00OOO00OOOO00 ['cedent_type']]=O0OO00OOO00OOOO00 ['traces']#line:1111
                                    O0O0OOOOO0OO0O00O ['trace_cedent_taskorder'][O0OO00OOO00OOOO00 ['cedent_type']]=O0OO00OOO00OOOO00 ['trace_cedent']#line:1112
                                    O0O0OOOOO0OO0O00O ['trace_cedent_dataorder'][O0OO00OOO00OOOO00 ['cedent_type']]=O0OO00OOO00OOOO00 ['trace_cedent_asindata']#line:1113
                                O0O0OOOOO0OO0O00O ["params"]=OOOO00OOOOOOO00OO #line:1114
                                if O0O0OO0O00OOO0O00 .verbosity ['debug']:#line:1115
                                    O0O0OOOOO0OO0O00O ["trace_cedent"]=copy .deepcopy (_O00OOOO0000OOOOOO )#line:1116
                                O0O0OO0O00OOO0O00 ._print_rule (O0O0OOOOO0OO0O00O )#line:1117
                                O0O0OO0O00OOO0O00 .rulelist .append (O0O0OOOOO0OO0O00O )#line:1118
                            O0O0OO0O00OOO0O00 .stats ['total_cnt']+=1 #line:1119
                            O0O0OO0O00OOO0O00 .stats ['total_ver']+=1 #line:1120
                    if _O00O0OOO0O0O000OO >=1 :#line:1121
                        if len (O0O0O0OO00OOOOOOO ['cedents_to_do'])>len (O0O0O0OO00OOOOOOO ['cedents']):#line:1122
                            O0O0OO0O00OOO0O00 ._start_cedent (O0O0O0OO00OOOOOOO ,_O00OO000OOO00OOOO +_O00OO00000OOOO0OO *_OOOO000000OOO00OO ,_O00OO000OOO00OOOO +(_O00OO00000OOOO0OO +0.33 )*_OOOO000000OOO00OO )#line:1123
                    O0O0O0OO00OOOOOOO ['cedents'].pop ()#line:1124
                    if (not (_O00O0OOO0O0O000OO ==0 ))and (len (_O00OOOO0000OOOOOO )<_O0000O0000000O000 ):#line:1125
                        O0O0OO0O00OOO0O00 ._genvar (O0O0O0OO00OOOOOOO ,O0O0O000O00OOO0O0 ,_O00OOOO0000OOOOOO ,_O0O0O00000000OOO0 ,_OO000O00OO000OOO0 ,_O0OOO0000O0O000OO ,_O0000O0000000O000 ,_O00OO000OOO00OOOO +(_O00OO00000OOOO0OO +0.33 )*_OOOO000000OOO00OO ,_O00OO000OOO00OOOO +(_O00OO00000OOOO0OO +0.66 )*_OOOO000000OOO00OO )#line:1126
                else :#line:1127
                    O0O0O0OO00OOOOOOO ['cedents'].pop ()#line:1128
                if len (_O000OO0OOOOOO0O0O )<_O00OOOOO000O00OOO :#line:1129
                    O0O0OO0O00OOO0O00 ._gencomb (O0O0O0OO00OOOOOOO ,O0O0O000O00OOO0O0 ,_O00OOOO0000OOOOOO ,_O0O0O00000000OOO0 ,_O000OO0OOOOOO0O0O ,_O0OO00O00OOO0OOO0 ,_OOOOOOOO000OO000O ,O0OO00OO000000O00 ,_O00O0O0O000O0OO00 ,_O0OOO0000O0O000OO ,_O0000O0000000O000 ,_O0OO000O000OO0OO0 ,_O00OOOOO000O00OOO ,_O00OO000OOO00OOOO +_OOOO000000OOO00OO *(_O00OO00000OOOO0OO +0.66 ),_O00OO000OOO00OOOO +_OOOO000000OOO00OO *(_O00OO00000OOOO0OO +1 ),_O0OOO0O000OO0O0OO )#line:1130
                _O000OO0OOOOOO0O0O .pop ()#line:1131
                _O00OO00000OOOO0OO +=1 #line:1132
                if O0O0OO0O00OOO0O00 .options ['progressbar']:#line:1133
                    O0O0OO0O00OOO0O00 .bar .update (min (100 ,_O00OO000OOO00OOOO +_OOOO000000OOO00OO *_O00OO00000OOOO0OO ))#line:1134
                if O0O0OO0O00OOO0O00 .verbosity ['debug']:#line:1135
                    print (f"Progress : lower: {_O00OO000OOO00OOOO}, step: {_OOOO000000OOO00OO}, step_no: {_O00OO00000OOOO0OO} overall: {_O00OO000OOO00OOOO+_OOOO000000OOO00OO*_O00OO00000OOOO0OO}")#line:1136
    def _start_cedent (OO0O0O0O000OO000O ,O000O0000OOO0O00O ,_O00000OO0000OO0OO ,_O0O0000OOOO000O0O ):#line:1138
        if len (O000O0000OOO0O00O ['cedents_to_do'])>len (O000O0000OOO0O00O ['cedents']):#line:1139
            _O0O00OO0OO0OO00O0 =[]#line:1140
            _O00O00O000O0O00OO =[]#line:1141
            OOO0OO00O0000000O ={}#line:1142
            OOO0OO00O0000000O ['cedent_type']=O000O0000OOO0O00O ['cedents_to_do'][len (O000O0000OOO0O00O ['cedents'])]#line:1143
            O00O000OOO00O0000 =OOO0OO00O0000000O ['cedent_type']#line:1144
            if ((O00O000OOO00O0000 [-1 ]=='-')|(O00O000OOO00O0000 [-1 ]=='+')):#line:1145
                O00O000OOO00O0000 =O00O000OOO00O0000 [:-1 ]#line:1146
            OOO0OO00O0000000O ['defi']=OO0O0O0O000OO000O .kwargs .get (O00O000OOO00O0000 )#line:1148
            if (OOO0OO00O0000000O ['defi']==None ):#line:1149
                print ("Error getting cedent ",OOO0OO00O0000000O ['cedent_type'])#line:1150
            _O000O0O000OO000O0 =int (0 )#line:1151
            OOO0OO00O0000000O ['num_cedent']=len (OOO0OO00O0000000O ['defi'].get ('attributes'))#line:1152
            if (OOO0OO00O0000000O ['defi'].get ('type')=='con'):#line:1153
                _O000O0O000OO000O0 =(1 <<OO0O0O0O000OO000O .data ["rows_count"])-1 #line:1154
            OO0O0O0O000OO000O ._genvar (O000O0000OOO0O00O ,OOO0OO00O0000000O ,_O0O00OO0OO0OO00O0 ,_O00O00O000O0O00OO ,_O000O0O000OO000O0 ,OOO0OO00O0000000O ['defi'].get ('minlen'),OOO0OO00O0000000O ['defi'].get ('maxlen'),_O00000OO0000OO0OO ,_O0O0000OOOO000O0O )#line:1155
    def _calc_all (OOO0O00O0000O0OO0 ,**O0OO0OOO0OO0000O0 ):#line:1158
        if "df"in O0OO0OOO0OO0000O0 :#line:1159
            OOO0O00O0000O0OO0 ._prep_data (OOO0O00O0000O0OO0 .kwargs .get ("df"))#line:1160
        if not (OOO0O00O0000O0OO0 ._initialized ):#line:1161
            print ("ERROR: dataframe is missing and not initialized with dataframe")#line:1162
        else :#line:1163
            OOO0O00O0000O0OO0 ._calculate (**O0OO0OOO0OO0000O0 )#line:1164
    def _check_cedents (O0OO000OO00000O00 ,OOO00OO0OO0OO0000 ,**OOOO00O00OO000O0O ):#line:1166
        OO0OO000O0O000O00 =True #line:1167
        if (OOOO00O00OO000O0O .get ('quantifiers',None )==None ):#line:1168
            print (f"Error: missing quantifiers.")#line:1169
            OO0OO000O0O000O00 =False #line:1170
            return OO0OO000O0O000O00 #line:1171
        if (type (OOOO00O00OO000O0O .get ('quantifiers'))!=dict ):#line:1172
            print (f"Error: quantifiers are not dictionary type.")#line:1173
            OO0OO000O0O000O00 =False #line:1174
            return OO0OO000O0O000O00 #line:1175
        for OOOO0O0OO0O0O0O00 in OOO00OO0OO0OO0000 :#line:1177
            if (OOOO00O00OO000O0O .get (OOOO0O0OO0O0O0O00 ,None )==None ):#line:1178
                print (f"Error: cedent {OOOO0O0OO0O0O0O00} is missing in parameters.")#line:1179
                OO0OO000O0O000O00 =False #line:1180
                return OO0OO000O0O000O00 #line:1181
            O000000OOOOO00O0O =OOOO00O00OO000O0O .get (OOOO0O0OO0O0O0O00 )#line:1182
            if (O000000OOOOO00O0O .get ('minlen'),None )==None :#line:1183
                print (f"Error: cedent {OOOO0O0OO0O0O0O00} has no minimal length specified.")#line:1184
                OO0OO000O0O000O00 =False #line:1185
                return OO0OO000O0O000O00 #line:1186
            if not (type (O000000OOOOO00O0O .get ('minlen'))is int ):#line:1187
                print (f"Error: cedent {OOOO0O0OO0O0O0O00} has invalid type of minimal length ({type(O000000OOOOO00O0O.get('minlen'))}).")#line:1188
                OO0OO000O0O000O00 =False #line:1189
                return OO0OO000O0O000O00 #line:1190
            if (O000000OOOOO00O0O .get ('maxlen'),None )==None :#line:1191
                print (f"Error: cedent {OOOO0O0OO0O0O0O00} has no maximal length specified.")#line:1192
                OO0OO000O0O000O00 =False #line:1193
                return OO0OO000O0O000O00 #line:1194
            if not (type (O000000OOOOO00O0O .get ('maxlen'))is int ):#line:1195
                print (f"Error: cedent {OOOO0O0OO0O0O0O00} has invalid type of maximal length.")#line:1196
                OO0OO000O0O000O00 =False #line:1197
                return OO0OO000O0O000O00 #line:1198
            if (O000000OOOOO00O0O .get ('type'),None )==None :#line:1199
                print (f"Error: cedent {OOOO0O0OO0O0O0O00} has no type specified.")#line:1200
                OO0OO000O0O000O00 =False #line:1201
                return OO0OO000O0O000O00 #line:1202
            if not ((O000000OOOOO00O0O .get ('type'))in (['con','dis'])):#line:1203
                print (f"Error: cedent {OOOO0O0OO0O0O0O00} has invalid type. Allowed values are 'con' and 'dis'.")#line:1204
                OO0OO000O0O000O00 =False #line:1205
                return OO0OO000O0O000O00 #line:1206
            if (O000000OOOOO00O0O .get ('attributes'),None )==None :#line:1207
                print (f"Error: cedent {OOOO0O0OO0O0O0O00} has no attributes specified.")#line:1208
                OO0OO000O0O000O00 =False #line:1209
                return OO0OO000O0O000O00 #line:1210
            for O00OO0O0000OO0000 in O000000OOOOO00O0O .get ('attributes'):#line:1211
                if (O00OO0O0000OO0000 .get ('name'),None )==None :#line:1212
                    print (f"Error: cedent {OOOO0O0OO0O0O0O00} / attribute {O00OO0O0000OO0000} has no 'name' attribute specified.")#line:1213
                    OO0OO000O0O000O00 =False #line:1214
                    return OO0OO000O0O000O00 #line:1215
                if not ((O00OO0O0000OO0000 .get ('name'))in O0OO000OO00000O00 .data ["varname"]):#line:1216
                    print (f"Error: cedent {OOOO0O0OO0O0O0O00} / attribute {O00OO0O0000OO0000.get('name')} not in variable list. Please check spelling.")#line:1217
                    OO0OO000O0O000O00 =False #line:1218
                    return OO0OO000O0O000O00 #line:1219
                if (O00OO0O0000OO0000 .get ('type'),None )==None :#line:1220
                    print (f"Error: cedent {OOOO0O0OO0O0O0O00} / attribute {O00OO0O0000OO0000.get('name')} has no 'type' attribute specified.")#line:1221
                    OO0OO000O0O000O00 =False #line:1222
                    return OO0OO000O0O000O00 #line:1223
                if not ((O00OO0O0000OO0000 .get ('type'))in (['rcut','lcut','seq','subset','one','list'])):#line:1224
                    print (f"Error: cedent {OOOO0O0OO0O0O0O00} / attribute {O00OO0O0000OO0000.get('name')} has unsupported type {O00OO0O0000OO0000.get('type')}. Supported types are 'subset','seq','lcut','rcut','one','list'.")#line:1225
                    OO0OO000O0O000O00 =False #line:1226
                    return OO0OO000O0O000O00 #line:1227
                if (O00OO0O0000OO0000 .get ('minlen'),None )==None :#line:1228
                    print (f"Error: cedent {OOOO0O0OO0O0O0O00} / attribute {O00OO0O0000OO0000.get('name')} has no minimal length specified.")#line:1229
                    OO0OO000O0O000O00 =False #line:1230
                    return OO0OO000O0O000O00 #line:1231
                if not (type (O00OO0O0000OO0000 .get ('minlen'))is int ):#line:1232
                    if not (O00OO0O0000OO0000 .get ('type')=='one'or O00OO0O0000OO0000 .get ('type')=='list'):#line:1233
                        print (f"Error: cedent {OOOO0O0OO0O0O0O00} / attribute {O00OO0O0000OO0000.get('name')} has invalid type of minimal length.")#line:1234
                        OO0OO000O0O000O00 =False #line:1235
                        return OO0OO000O0O000O00 #line:1236
                if (O00OO0O0000OO0000 .get ('maxlen'),None )==None :#line:1237
                    print (f"Error: cedent {OOOO0O0OO0O0O0O00} / attribute {O00OO0O0000OO0000.get('name')} has no maximal length specified.")#line:1238
                    OO0OO000O0O000O00 =False #line:1239
                    return OO0OO000O0O000O00 #line:1240
                if not (type (O00OO0O0000OO0000 .get ('maxlen'))is int ):#line:1241
                    if not (O00OO0O0000OO0000 .get ('type')=='one'or O00OO0O0000OO0000 .get ('type')=='list'):#line:1242
                        print (f"Error: cedent {OOOO0O0OO0O0O0O00} / attribute {O00OO0O0000OO0000.get('name')} has invalid type of maximal length.")#line:1243
                        OO0OO000O0O000O00 =False #line:1244
                        return OO0OO000O0O000O00 #line:1245
        return OO0OO000O0O000O00 #line:1246

    def _calculate (OO0O0000OO0O0O000 ,**OOOOO000000OOO0OO ):#line:2
        if OO0O0000OO0O0O000 .data ["data_prepared"]==0 :#line:3
            print ("Error: data not prepared")#line:4
            return #line:5
        OO0O0000OO0O0O000 .kwargs =OOOOO000000OOO0OO #line:6
        OO0O0000OO0O0O000 .proc =OOOOO000000OOO0OO .get ('proc')#line:7
        OO0O0000OO0O0O000 .quantifiers =OOOOO000000OOO0OO .get ('quantifiers')#line:8
        OO0O0000OO0O0O000 ._init_task ()#line:10
        OO0O0000OO0O0O000 .stats ['start_proc_time']=time .time ()#line:11
        OO0O0000OO0O0O000 .task_actinfo ['cedents_to_do']=[]#line:12
        OO0O0000OO0O0O000 .task_actinfo ['cedents']=[]#line:13
        if OOOOO000000OOO0OO .get ("proc")=='UICMiner':#line:16
            if not (OO0O0000OO0O0O000 ._check_cedents (['ante'],**OOOOO000000OOO0OO )):#line:17
                return #line:18
            _OO000O0OO0OO00OOO =OOOOO000000OOO0OO .get ("cond")#line:20
            if _OO000O0OO0OO00OOO !=None :#line:21
                OO0O0000OO0O0O000 .task_actinfo ['cedents_to_do'].append ('cond')#line:22
            else :#line:23
                O00OOO0O00O00O0O0 =OO0O0000OO0O0O000 .cedent #line:24
                O00OOO0O00O00O0O0 ['cedent_type']='cond'#line:25
                O00OOO0O00O00O0O0 ['filter_value']=(1 <<OO0O0000OO0O0O000 .data ["rows_count"])-1 #line:26
                O00OOO0O00O00O0O0 ['generated_string']='---'#line:27
                if OO0O0000OO0O0O000 .verbosity ['debug']:#line:28
                    print (O00OOO0O00O00O0O0 ['filter_value'])#line:29
                OO0O0000OO0O0O000 .task_actinfo ['cedents_to_do'].append ('cond')#line:30
                OO0O0000OO0O0O000 .task_actinfo ['cedents'].append (O00OOO0O00O00O0O0 )#line:31
            OO0O0000OO0O0O000 .task_actinfo ['cedents_to_do'].append ('ante')#line:32
            if OOOOO000000OOO0OO .get ('target',None )==None :#line:33
                print ("ERROR: no succedent/target variable defined for UIC Miner")#line:34
                return #line:35
            if not (OOOOO000000OOO0OO .get ('target')in OO0O0000OO0O0O000 .data ["varname"]):#line:36
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:37
                return #line:38
            if ("aad_score"in OO0O0000OO0O0O000 .quantifiers ):#line:39
                if not ("aad_weights"in OO0O0000OO0O0O000 .quantifiers ):#line:40
                    print ("ERROR: for aad quantifier you need to specify aad weights.")#line:41
                    return #line:42
                if not (len (OO0O0000OO0O0O000 .quantifiers .get ("aad_weights"))==len (OO0O0000OO0O0O000 .data ["dm"][OO0O0000OO0O0O000 .data ["varname"].index (OO0O0000OO0O0O000 .kwargs .get ('target'))])):#line:43
                    print ("ERROR: aad weights has different number of weights than classes of target variable.")#line:44
                    return #line:45
        elif OOOOO000000OOO0OO .get ("proc")=='CFMiner':#line:46
            OO0O0000OO0O0O000 .task_actinfo ['cedents_to_do']=['cond']#line:47
            if OOOOO000000OOO0OO .get ('target',None )==None :#line:48
                print ("ERROR: no target variable defined for CF Miner")#line:49
                return #line:50
            O0OOOOO00O0OOO00O =OOOOO000000OOO0OO .get ('target',None )#line:51
            OO0O0000OO0O0O000 .profiles ['hist_target_entire_dataset_labels']=OO0O0000OO0O0O000 .data ["catnames"][OO0O0000OO0O0O000 .data ["varname"].index (OO0O0000OO0O0O000 .kwargs .get ('target'))]#line:52
            OOOO000OO000OOOO0 =OO0O0000OO0O0O000 .data ["dm"][OO0O0000OO0O0O000 .data ["varname"].index (OO0O0000OO0O0O000 .kwargs .get ('target'))]#line:53
            OO00OO0OOO00OO0OO =[]#line:55
            for OO00OOOOOOO0000O0 in range (len (OOOO000OO000OOOO0 )):#line:56
                O0OOOO00O0OO0O0OO =OO0O0000OO0O0O000 ._bitcount (OOOO000OO000OOOO0 [OO00OOOOOOO0000O0 ])#line:57
                OO00OO0OOO00OO0OO .append (O0OOOO00O0OO0O0OO )#line:58
            OO0O0000OO0O0O000 .profiles ['hist_target_entire_dataset_values']=OO00OO0OOO00OO0OO #line:59
            if not (OO0O0000OO0O0O000 ._check_cedents (['cond'],**OOOOO000000OOO0OO )):#line:60
                return #line:61
            if not (OOOOO000000OOO0OO .get ('target')in OO0O0000OO0O0O000 .data ["varname"]):#line:62
                print ("ERROR: target parameter is not variable. Please check spelling of variable name in parameter 'target'.")#line:63
                return #line:64
            if ("aad"in OO0O0000OO0O0O000 .quantifiers ):#line:65
                if not ("aad_weights"in OO0O0000OO0O0O000 .quantifiers ):#line:66
                    print ("ERROR: for aad quantifier you need to specify aad weights.")#line:67
                    return #line:68
                if not (len (OO0O0000OO0O0O000 .quantifiers .get ("aad_weights"))==len (OO0O0000OO0O0O000 .data ["dm"][OO0O0000OO0O0O000 .data ["varname"].index (OO0O0000OO0O0O000 .kwargs .get ('target'))])):#line:69
                    print ("ERROR: aad weights has different number of weights than classes of target variable.")#line:70
                    return #line:71
        elif OOOOO000000OOO0OO .get ("proc")=='4ftMiner':#line:74
            if not (OO0O0000OO0O0O000 ._check_cedents (['ante','succ'],**OOOOO000000OOO0OO )):#line:75
                return #line:76
            _OO000O0OO0OO00OOO =OOOOO000000OOO0OO .get ("cond")#line:78
            if _OO000O0OO0OO00OOO !=None :#line:79
                OO0O0000OO0O0O000 .task_actinfo ['cedents_to_do'].append ('cond')#line:80
            else :#line:81
                O00OOO0O00O00O0O0 =OO0O0000OO0O0O000 .cedent #line:82
                O00OOO0O00O00O0O0 ['cedent_type']='cond'#line:83
                O00OOO0O00O00O0O0 ['filter_value']=(1 <<OO0O0000OO0O0O000 .data ["rows_count"])-1 #line:84
                O00OOO0O00O00O0O0 ['generated_string']='---'#line:85
                OO0O0000OO0O0O000 .task_actinfo ['cedents_to_do'].append ('cond')#line:86
                OO0O0000OO0O0O000 .task_actinfo ['cedents'].append (O00OOO0O00O00O0O0 )#line:87
            OO0O0000OO0O0O000 .task_actinfo ['cedents_to_do'].append ('ante')#line:88
            OO0O0000OO0O0O000 .task_actinfo ['cedents_to_do'].append ('succ')#line:89
        elif OOOOO000000OOO0OO .get ("proc")=='SD4ftMiner':#line:90
            if not (OO0O0000OO0O0O000 ._check_cedents (['ante','succ','frst','scnd'],**OOOOO000000OOO0OO )):#line:93
                return #line:94
            _OO000O0OO0OO00OOO =OOOOO000000OOO0OO .get ("cond")#line:95
            if _OO000O0OO0OO00OOO !=None :#line:96
                OO0O0000OO0O0O000 .task_actinfo ['cedents_to_do'].append ('cond')#line:97
            else :#line:98
                O00OOO0O00O00O0O0 =OO0O0000OO0O0O000 .cedent #line:99
                O00OOO0O00O00O0O0 ['cedent_type']='cond'#line:100
                O00OOO0O00O00O0O0 ['filter_value']=(1 <<OO0O0000OO0O0O000 .data ["rows_count"])-1 #line:101
                O00OOO0O00O00O0O0 ['generated_string']='---'#line:102
                OO0O0000OO0O0O000 .task_actinfo ['cedents_to_do'].append ('cond')#line:103
                OO0O0000OO0O0O000 .task_actinfo ['cedents'].append (O00OOO0O00O00O0O0 )#line:104
            OO0O0000OO0O0O000 .task_actinfo ['cedents_to_do'].append ('frst')#line:105
            OO0O0000OO0O0O000 .task_actinfo ['cedents_to_do'].append ('scnd')#line:106
            OO0O0000OO0O0O000 .task_actinfo ['cedents_to_do'].append ('ante')#line:107
            OO0O0000OO0O0O000 .task_actinfo ['cedents_to_do'].append ('succ')#line:108
        else :#line:109
            print ("Unsupported procedure")#line:110
            return #line:111
        print ("Will go for ",OOOOO000000OOO0OO .get ("proc"))#line:112
        OO0O0000OO0O0O000 .task_actinfo ['optim']={}#line:115
        O0O000O0O0O000000 =True #line:116
        for OO0OOOO0OO00O0O00 in OO0O0000OO0O0O000 .task_actinfo ['cedents_to_do']:#line:117
            try :#line:118
                OO0O00OO00O00OO00 =OO0O0000OO0O0O000 .kwargs .get (OO0OOOO0OO00O0O00 )#line:119
                if OO0O0000OO0O0O000 .verbosity ['debug']:#line:120
                    print (OO0O00OO00O00OO00 )#line:121
                    print (f"...cedent {OO0OOOO0OO00O0O00} is type {OO0O00OO00O00OO00.get('type')}")#line:122
                    print (f"Will check cedent type {OO0OOOO0OO00O0O00} : {OO0O00OO00O00OO00.get('type')}")#line:123
                if OO0O00OO00O00OO00 .get ('type')!='con':#line:124
                    O0O000O0O0O000000 =False #line:125
                    if OO0O0000OO0O0O000 .verbosity ['debug']:#line:126
                        print (f"Cannot optim due to cedent type {OO0OOOO0OO00O0O00} : {OO0O00OO00O00OO00.get('type')}")#line:127
            except :#line:128
                OOOOOO0OOO0000O00 =1 <2 #line:129
        if OO0O0000OO0O0O000 .options ['optimizations']==False :#line:131
            O0O000O0O0O000000 =False #line:132
        O000000O0OOOO0O00 ={}#line:133
        O000000O0OOOO0O00 ['only_con']=O0O000O0O0O000000 #line:134
        OO0O0000OO0O0O000 .task_actinfo ['optim']=O000000O0OOOO0O00 #line:135
        if OO0O0000OO0O0O000 .verbosity ['debug']:#line:139
            print ("Starting to prepare data.")#line:140
            OO0O0000OO0O0O000 ._prep_data (OO0O0000OO0O0O000 .data .df )#line:141
            OO0O0000OO0O0O000 .stats ['mid1_time']=time .time ()#line:142
            OO0O0000OO0O0O000 .quantifiers =OOOOO000000OOO0OO .get ('self.quantifiers')#line:143
        print ("Starting to mine rules.")#line:144
        sys .stdout .flush ()#line:145
        time .sleep (0.01 )#line:146
        if OO0O0000OO0O0O000 .options ['progressbar']:#line:147
            O0OO000000O000O0O =[progressbar .Percentage (),progressbar .Bar (),progressbar .Timer ()]#line:148
            OO0O0000OO0O0O000 .bar =progressbar .ProgressBar (widgets =O0OO000000O000O0O ,max_value =100 ,fd =sys .stdout ).start ()#line:149
            OO0O0000OO0O0O000 .bar .update (0 )#line:150
        OO0O0000OO0O0O000 .progress_lower =0 #line:151
        OO0O0000OO0O0O000 .progress_upper =100 #line:152
        OO0O0000OO0O0O000 ._start_cedent (OO0O0000OO0O0O000 .task_actinfo ,OO0O0000OO0O0O000 .progress_lower ,OO0O0000OO0O0O000 .progress_upper )#line:153
        if OO0O0000OO0O0O000 .options ['progressbar']:#line:154
            OO0O0000OO0O0O000 .bar .update (100 )#line:155
            OO0O0000OO0O0O000 .bar .finish ()#line:156
        OO0O0000OO0O0O000 .stats ['end_proc_time']=time .time ()#line:157
        print ("Done. Total verifications : "+str (OO0O0000OO0O0O000 .stats ['total_cnt'])+", rules "+str (OO0O0000OO0O0O000 .stats ['total_valid'])+", times: prep "+"{:.2f}".format (OO0O0000OO0O0O000 .stats ['end_prep_time']-OO0O0000OO0O0O000 .stats ['start_prep_time'])+"sec, processing "+"{:.2f}".format (OO0O0000OO0O0O000 .stats ['end_proc_time']-OO0O0000OO0O0O000 .stats ['start_proc_time'])+"sec")#line:160
        O0OO0OOOOO00OO0OO ={}#line:161
        O0OO0OOOO00OOOOO0 ={}#line:162
        O0OO0OOOO00OOOOO0 ["task_type"]=OOOOO000000OOO0OO .get ('proc')#line:163
        O0OO0OOOO00OOOOO0 ["target"]=OOOOO000000OOO0OO .get ('target')#line:164
        O0OO0OOOO00OOOOO0 ["self.quantifiers"]=OO0O0000OO0O0O000 .quantifiers #line:165
        if OOOOO000000OOO0OO .get ('cond')!=None :#line:166
            O0OO0OOOO00OOOOO0 ['cond']=OOOOO000000OOO0OO .get ('cond')#line:167
        if OOOOO000000OOO0OO .get ('ante')!=None :#line:168
            O0OO0OOOO00OOOOO0 ['ante']=OOOOO000000OOO0OO .get ('ante')#line:169
        if OOOOO000000OOO0OO .get ('succ')!=None :#line:170
            O0OO0OOOO00OOOOO0 ['succ']=OOOOO000000OOO0OO .get ('succ')#line:171
        if OOOOO000000OOO0OO .get ('opts')!=None :#line:172
            O0OO0OOOO00OOOOO0 ['opts']=OOOOO000000OOO0OO .get ('opts')#line:173
        if OO0O0000OO0O0O000 .df is None :#line:174
            O0OO0OOOO00OOOOO0 ['rowcount']=OO0O0000OO0O0O000 .data ["rows_count"]#line:175
        else :#line:177
            O0OO0OOOO00OOOOO0 ['rowcount']=len (OO0O0000OO0O0O000 .df .index )#line:178
        O0OO0OOOOO00OO0OO ["taskinfo"]=O0OO0OOOO00OOOOO0 #line:179
        OOO000O00OO0OOOO0 ={}#line:180
        OOO000O00OO0OOOO0 ["total_verifications"]=OO0O0000OO0O0O000 .stats ['total_cnt']#line:181
        OOO000O00OO0OOOO0 ["valid_rules"]=OO0O0000OO0O0O000 .stats ['total_valid']#line:182
        OOO000O00OO0OOOO0 ["total_verifications_with_opt"]=OO0O0000OO0O0O000 .stats ['total_ver']#line:183
        OOO000O00OO0OOOO0 ["time_prep"]=OO0O0000OO0O0O000 .stats ['end_prep_time']-OO0O0000OO0O0O000 .stats ['start_prep_time']#line:184
        OOO000O00OO0OOOO0 ["time_processing"]=OO0O0000OO0O0O000 .stats ['end_proc_time']-OO0O0000OO0O0O000 .stats ['start_proc_time']#line:185
        OOO000O00OO0OOOO0 ["time_total"]=OO0O0000OO0O0O000 .stats ['end_prep_time']-OO0O0000OO0O0O000 .stats ['start_prep_time']+OO0O0000OO0O0O000 .stats ['end_proc_time']-OO0O0000OO0O0O000 .stats ['start_proc_time']#line:186
        O0OO0OOOOO00OO0OO ["summary_statistics"]=OOO000O00OO0OOOO0 #line:187
        O0OO0OOOOO00OO0OO ["rules"]=OO0O0000OO0O0O000 .rulelist #line:188
        O000O00O0O00O00OO ={}#line:189
        O000O00O0O00O00OO ["varname"]=OO0O0000OO0O0O000 .data ["varname"]#line:190
        O000O00O0O00O00OO ["catnames"]=OO0O0000OO0O0O000 .data ["catnames"]#line:191
        O0OO0OOOOO00OO0OO ["datalabels"]=O000O00O0O00O00OO #line:192
        OO0O0000OO0O0O000 .result =O0OO0OOOOO00OO0OO #line:193
    def print_summary (OOOOO00OO00O0OOOO ):#line:195
        ""#line:198
        if not (OOOOO00OO00O0OOOO ._is_calculated ()):#line:199
            print ("ERROR: Task has not been calculated.")#line:200
            return #line:201
        print ("")#line:202
        print ("CleverMiner task processing summary:")#line:203
        print ("")#line:204
        print (f"Task type : {OOOOO00OO00O0OOOO.result['taskinfo']['task_type']}")#line:205
        print (f"Number of verifications : {OOOOO00OO00O0OOOO.result['summary_statistics']['total_verifications']}")#line:206
        print (f"Number of rules : {OOOOO00OO00O0OOOO.result['summary_statistics']['valid_rules']}")#line:207
        print (f"Total time needed : {strftime('%Hh %Mm %Ss', gmtime(OOOOO00OO00O0OOOO.result['summary_statistics']['time_total']))}")#line:208
        if OOOOO00OO00O0OOOO .verbosity ['debug']:#line:209
            print (f"Total time needed : {OOOOO00OO00O0OOOO.result['summary_statistics']['time_total']}")#line:210
        print (f"Time of data preparation : {strftime('%Hh %Mm %Ss', gmtime(OOOOO00OO00O0OOOO.result['summary_statistics']['time_prep']))}")#line:211
        print (f"Time of rule mining : {strftime('%Hh %Mm %Ss', gmtime(OOOOO00OO00O0OOOO.result['summary_statistics']['time_processing']))}")#line:212
        print ("")#line:213
    def print_hypolist (O00OO0OOOOO0O000O ):#line:215
        ""#line:218
        O00OO0OOOOO0O000O .print_rulelist ();#line:219
    def print_rulelist (OO0O0O00O00O0O00O ,sortby =None ,storesorted =False ):#line:221
        ""#line:226
        if not (OO0O0O00O00O0O00O ._is_calculated ()):#line:227
            print ("ERROR: Task has not been calculated.")#line:228
            return #line:229
        def O000OO0O000OO0O0O (O0O0OOO000O0O000O ):#line:231
            O00O0000O0O0O00OO =O0O0OOO000O0O000O ["params"]#line:232
            return O00O0000O0O0O00OO .get (sortby ,0 )#line:233
        print ("")#line:235
        print ("List of rules:")#line:236
        if OO0O0O00O00O0O00O .result ['taskinfo']['task_type']=="4ftMiner":#line:237
            print ("RULEID BASE  CONF  AAD    Rule")#line:238
        elif OO0O0O00O00O0O00O .result ['taskinfo']['task_type']=="UICMiner":#line:239
            print ("RULEID BASE  AAD_SCORE  Rule")#line:240
        elif OO0O0O00O00O0O00O .result ['taskinfo']['task_type']=="CFMiner":#line:241
            print ("RULEID BASE  S_UP  S_DOWN Condition")#line:242
        elif OO0O0O00O00O0O00O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:243
            print ("RULEID BASE1 BASE2 RatioConf DeltaConf Rule")#line:244
        else :#line:245
            print ("Unsupported task type for rulelist")#line:246
            return #line:247
        O000O000OO0O000O0 =OO0O0O00O00O0O00O .result ["rules"]#line:248
        if sortby is not None :#line:249
            O000O000OO0O000O0 =sorted (O000O000OO0O000O0 ,key =O000OO0O000OO0O0O ,reverse =True )#line:250
            if storesorted :#line:251
                OO0O0O00O00O0O00O .result ["rules"]=O000O000OO0O000O0 #line:252
        for OOO00OO0O00O0OO0O in O000O000OO0O000O0 :#line:254
            O0OO000OO0OO0OO00 ="{:6d}".format (OOO00OO0O00O0OO0O ["rule_id"])#line:255
            if OO0O0O00O00O0O00O .result ['taskinfo']['task_type']=="4ftMiner":#line:256
                if OO0O0O00O00O0O00O .verbosity ['debug']:#line:257
                   print (f"{OOO00OO0O00O0OO0O['params']}")#line:258
                O0OO000OO0OO0OO00 =O0OO000OO0OO0OO00 +" "+"{:5d}".format (OOO00OO0O00O0OO0O ["params"]["base"])+" "+"{:.3f}".format (OOO00OO0O00O0OO0O ["params"]["conf"])+" "+"{:+.3f}".format (OOO00OO0O00O0OO0O ["params"]["aad"])#line:259
                O0OO000OO0OO0OO00 =O0OO000OO0OO0OO00 +" "+OOO00OO0O00O0OO0O ["cedents_str"]["ante"]+" => "+OOO00OO0O00O0OO0O ["cedents_str"]["succ"]+" | "+OOO00OO0O00O0OO0O ["cedents_str"]["cond"]#line:260
            elif OO0O0O00O00O0O00O .result ['taskinfo']['task_type']=="UICMiner":#line:261
                O0OO000OO0OO0OO00 =O0OO000OO0OO0OO00 +" "+"{:5d}".format (OOO00OO0O00O0OO0O ["params"]["base"])+" "+"{:.3f}".format (OOO00OO0O00O0OO0O ["params"]["aad_score"])#line:262
                O0OO000OO0OO0OO00 =O0OO000OO0OO0OO00 +"     "+OOO00OO0O00O0OO0O ["cedents_str"]["ante"]+" => "+OO0O0O00O00O0O00O .result ['taskinfo']['target']+"(*) | "+OOO00OO0O00O0OO0O ["cedents_str"]["cond"]#line:263
            elif OO0O0O00O00O0O00O .result ['taskinfo']['task_type']=="CFMiner":#line:264
                O0OO000OO0OO0OO00 =O0OO000OO0OO0OO00 +" "+"{:5d}".format (OOO00OO0O00O0OO0O ["params"]["base"])+" "+"{:5d}".format (OOO00OO0O00O0OO0O ["params"]["s_up"])+" "+"{:5d}".format (OOO00OO0O00O0OO0O ["params"]["s_down"])#line:265
                O0OO000OO0OO0OO00 =O0OO000OO0OO0OO00 +" "+OOO00OO0O00O0OO0O ["cedents_str"]["cond"]#line:266
            elif OO0O0O00O00O0O00O .result ['taskinfo']['task_type']=="SD4ftMiner":#line:267
                O0OO000OO0OO0OO00 =O0OO000OO0OO0OO00 +" "+"{:5d}".format (OOO00OO0O00O0OO0O ["params"]["base1"])+" "+"{:5d}".format (OOO00OO0O00O0OO0O ["params"]["base2"])+"    "+"{:.3f}".format (OOO00OO0O00O0OO0O ["params"]["ratioconf"])+"    "+"{:+.3f}".format (OOO00OO0O00O0OO0O ["params"]["deltaconf"])#line:268
                O0OO000OO0OO0OO00 =O0OO000OO0OO0OO00 +"  "+OOO00OO0O00O0OO0O ["cedents_str"]["ante"]+" => "+OOO00OO0O00O0OO0O ["cedents_str"]["succ"]+" | "+OOO00OO0O00O0OO0O ["cedents_str"]["cond"]+" : "+OOO00OO0O00O0OO0O ["cedents_str"]["frst"]+" x "+OOO00OO0O00O0OO0O ["cedents_str"]["scnd"]#line:269
            print (O0OO000OO0OO0OO00 )#line:271
        print ("")#line:272
    def print_hypo (OO0O0O00O0OOO0O00 ,O0OO0O0000OO000O0 ):#line:274
        ""#line:278
        OO0O0O00O0OOO0O00 .print_rule (O0OO0O0000OO000O0 )#line:279
    def print_rule (OO00OO000OOOOOO00 ,OOO00O0O0OO0OO00O ):#line:282
        ""#line:286
        if not (OO00OO000OOOOOO00 ._is_calculated ()):#line:287
            print ("ERROR: Task has not been calculated.")#line:288
            return #line:289
        print ("")#line:290
        if (OOO00O0O0OO0OO00O <=len (OO00OO000OOOOOO00 .result ["rules"])):#line:291
            if OO00OO000OOOOOO00 .result ['taskinfo']['task_type']=="4ftMiner":#line:292
                print ("")#line:293
                OOOOOOO00OOO00000 =OO00OO000OOOOOO00 .result ["rules"][OOO00O0O0OO0OO00O -1 ]#line:294
                print (f"Rule id : {OOOOOOO00OOO00000['rule_id']}")#line:295
                print ("")#line:296
                print (f"Base : {'{:5d}'.format(OOOOOOO00OOO00000['params']['base'])}  Relative base : {'{:.3f}'.format(OOOOOOO00OOO00000['params']['rel_base'])}  CONF : {'{:.3f}'.format(OOOOOOO00OOO00000['params']['conf'])}  AAD : {'{:+.3f}'.format(OOOOOOO00OOO00000['params']['aad'])}  BAD : {'{:+.3f}'.format(OOOOOOO00OOO00000['params']['bad'])}")#line:297
                print ("")#line:298
                print ("Cedents:")#line:299
                print (f"  antecedent : {OOOOOOO00OOO00000['cedents_str']['ante']}")#line:300
                print (f"  succcedent : {OOOOOOO00OOO00000['cedents_str']['succ']}")#line:301
                print (f"  condition  : {OOOOOOO00OOO00000['cedents_str']['cond']}")#line:302
                print ("")#line:303
                print ("Fourfold table")#line:304
                print (f"    |  S  |  ¬S |")#line:305
                print (f"----|-----|-----|")#line:306
                print (f" A  |{'{:5d}'.format(OOOOOOO00OOO00000['params']['fourfold'][0])}|{'{:5d}'.format(OOOOOOO00OOO00000['params']['fourfold'][1])}|")#line:307
                print (f"----|-----|-----|")#line:308
                print (f"¬A  |{'{:5d}'.format(OOOOOOO00OOO00000['params']['fourfold'][2])}|{'{:5d}'.format(OOOOOOO00OOO00000['params']['fourfold'][3])}|")#line:309
                print (f"----|-----|-----|")#line:310
            elif OO00OO000OOOOOO00 .result ['taskinfo']['task_type']=="CFMiner":#line:311
                print ("")#line:312
                OOOOOOO00OOO00000 =OO00OO000OOOOOO00 .result ["rules"][OOO00O0O0OO0OO00O -1 ]#line:313
                print (f"Rule id : {OOOOOOO00OOO00000['rule_id']}")#line:314
                print ("")#line:315
                OO0000O000OO000O0 =""#line:316
                if ('aad'in OOOOOOO00OOO00000 ['params']):#line:317
                    OO0000O000OO000O0 ="aad : "+str (OOOOOOO00OOO00000 ['params']['aad'])#line:318
                print (f"Base : {'{:5d}'.format(OOOOOOO00OOO00000['params']['base'])}  Relative base : {'{:.3f}'.format(OOOOOOO00OOO00000['params']['rel_base'])}  Steps UP (consecutive) : {'{:5d}'.format(OOOOOOO00OOO00000['params']['s_up'])}  Steps DOWN (consecutive) : {'{:5d}'.format(OOOOOOO00OOO00000['params']['s_down'])}  Steps UP (any) : {'{:5d}'.format(OOOOOOO00OOO00000['params']['s_any_up'])}  Steps DOWN (any) : {'{:5d}'.format(OOOOOOO00OOO00000['params']['s_any_down'])}  Histogram maximum : {'{:5d}'.format(OOOOOOO00OOO00000['params']['max'])}  Histogram minimum : {'{:5d}'.format(OOOOOOO00OOO00000['params']['min'])}  Histogram relative maximum : {'{:.3f}'.format(OOOOOOO00OOO00000['params']['rel_max'])} Histogram relative minimum : {'{:.3f}'.format(OOOOOOO00OOO00000['params']['rel_min'])} {OO0000O000OO000O0}")#line:320
                print ("")#line:321
                print (f"Condition  : {OOOOOOO00OOO00000['cedents_str']['cond']}")#line:322
                print ("")#line:323
                O00O0OOO000000000 =OO00OO000OOOOOO00 .get_category_names (OO00OO000OOOOOO00 .result ["taskinfo"]["target"])#line:324
                print (f"Categories in target variable  {O00O0OOO000000000}")#line:325
                print (f"Histogram                      {OOOOOOO00OOO00000['params']['hist']}")#line:326
                if ('aad'in OOOOOOO00OOO00000 ['params']):#line:327
                    print (f"Histogram on full set          {OOOOOOO00OOO00000['params']['hist_full']}")#line:328
                    print (f"Relative histogram             {OOOOOOO00OOO00000['params']['rel_hist']}")#line:329
                    print (f"Relative histogram on full set {OOOOOOO00OOO00000['params']['rel_hist_full']}")#line:330
            elif OO00OO000OOOOOO00 .result ['taskinfo']['task_type']=="UICMiner":#line:331
                print ("")#line:332
                OOOOOOO00OOO00000 =OO00OO000OOOOOO00 .result ["rules"][OOO00O0O0OO0OO00O -1 ]#line:333
                print (f"Rule id : {OOOOOOO00OOO00000['rule_id']}")#line:334
                print ("")#line:335
                OO0000O000OO000O0 =""#line:336
                if ('aad_score'in OOOOOOO00OOO00000 ['params']):#line:337
                    OO0000O000OO000O0 ="aad score : "+str (OOOOOOO00OOO00000 ['params']['aad_score'])#line:338
                print (f"Base : {'{:5d}'.format(OOOOOOO00OOO00000['params']['base'])}  Relative base : {'{:.3f}'.format(OOOOOOO00OOO00000['params']['rel_base'])}   {OO0000O000OO000O0}")#line:340
                print ("")#line:341
                print (f"Condition  : {OOOOOOO00OOO00000['cedents_str']['cond']}")#line:342
                print (f"Antecedent : {OOOOOOO00OOO00000['cedents_str']['ante']}")#line:343
                print ("")#line:344
                print (f"Histogram                                        {OOOOOOO00OOO00000['params']['hist']}")#line:345
                if ('aad_score'in OOOOOOO00OOO00000 ['params']):#line:346
                    print (f"Histogram on full set with condition             {OOOOOOO00OOO00000['params']['hist_cond']}")#line:347
                    print (f"Relative histogram                               {OOOOOOO00OOO00000['params']['rel_hist']}")#line:348
                    print (f"Relative histogram on full set with condition    {OOOOOOO00OOO00000['params']['rel_hist_cond']}")#line:349
                O00O0O00OO00000O0 =OO00OO000OOOOOO00 .result ['datalabels']['catnames'][OO00OO000OOOOOO00 .result ['datalabels']['varname'].index (OO00OO000OOOOOO00 .result ['taskinfo']['target'])]#line:350
                print (" ")#line:351
                print ("Interpretation:")#line:352
                for OO000000O0O000O00 in range (len (O00O0O00OO00000O0 )):#line:353
                  OOO0OO0OO00OOOO0O =0 #line:354
                  if OOOOOOO00OOO00000 ['params']['rel_hist'][OO000000O0O000O00 ]>0 :#line:355
                      OOO0OO0OO00OOOO0O =OOOOOOO00OOO00000 ['params']['rel_hist'][OO000000O0O000O00 ]/OOOOOOO00OOO00000 ['params']['rel_hist_cond'][OO000000O0O000O00 ]#line:356
                  O0O0OOO000OOO0OOO =''#line:357
                  if not (OOOOOOO00OOO00000 ['cedents_str']['cond']=='---'):#line:358
                      O0O0OOO000OOO0OOO ="For "+OOOOOOO00OOO00000 ['cedents_str']['cond']+": "#line:359
                  print (f"    {O0O0OOO000OOO0OOO}{OO00OO000OOOOOO00.result['taskinfo']['target']}({O00O0O00OO00000O0[OO000000O0O000O00]}) has occurence {'{:.1%}'.format(OOOOOOO00OOO00000['params']['rel_hist_cond'][OO000000O0O000O00])}, with antecedent it has occurence {'{:.1%}'.format(OOOOOOO00OOO00000['params']['rel_hist'][OO000000O0O000O00])}, that is {'{:.3f}'.format(OOO0OO0OO00OOOO0O)} times more.")#line:361
            elif OO00OO000OOOOOO00 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:362
                print ("")#line:363
                OOOOOOO00OOO00000 =OO00OO000OOOOOO00 .result ["rules"][OOO00O0O0OO0OO00O -1 ]#line:364
                print (f"Rule id : {OOOOOOO00OOO00000['rule_id']}")#line:365
                print ("")#line:366
                print (f"Base1 : {'{:5d}'.format(OOOOOOO00OOO00000['params']['base1'])} Base2 : {'{:5d}'.format(OOOOOOO00OOO00000['params']['base2'])}  Relative base 1 : {'{:.3f}'.format(OOOOOOO00OOO00000['params']['rel_base1'])} Relative base 2 : {'{:.3f}'.format(OOOOOOO00OOO00000['params']['rel_base2'])} CONF1 : {'{:.3f}'.format(OOOOOOO00OOO00000['params']['conf1'])}  CONF2 : {'{:+.3f}'.format(OOOOOOO00OOO00000['params']['conf2'])}  Delta Conf : {'{:+.3f}'.format(OOOOOOO00OOO00000['params']['deltaconf'])} Ratio Conf : {'{:+.3f}'.format(OOOOOOO00OOO00000['params']['ratioconf'])}")#line:367
                print ("")#line:368
                print ("Cedents:")#line:369
                print (f"  antecedent : {OOOOOOO00OOO00000['cedents_str']['ante']}")#line:370
                print (f"  succcedent : {OOOOOOO00OOO00000['cedents_str']['succ']}")#line:371
                print (f"  condition  : {OOOOOOO00OOO00000['cedents_str']['cond']}")#line:372
                print (f"  first set  : {OOOOOOO00OOO00000['cedents_str']['frst']}")#line:373
                print (f"  second set : {OOOOOOO00OOO00000['cedents_str']['scnd']}")#line:374
                print ("")#line:375
                print ("Fourfold tables:")#line:376
                print (f"FRST|  S  |  ¬S |  SCND|  S  |  ¬S |");#line:377
                print (f"----|-----|-----|  ----|-----|-----| ")#line:378
                print (f" A  |{'{:5d}'.format(OOOOOOO00OOO00000['params']['fourfold1'][0])}|{'{:5d}'.format(OOOOOOO00OOO00000['params']['fourfold1'][1])}|   A  |{'{:5d}'.format(OOOOOOO00OOO00000['params']['fourfold2'][0])}|{'{:5d}'.format(OOOOOOO00OOO00000['params']['fourfold2'][1])}|")#line:379
                print (f"----|-----|-----|  ----|-----|-----|")#line:380
                print (f"¬A  |{'{:5d}'.format(OOOOOOO00OOO00000['params']['fourfold1'][2])}|{'{:5d}'.format(OOOOOOO00OOO00000['params']['fourfold1'][3])}|  ¬A  |{'{:5d}'.format(OOOOOOO00OOO00000['params']['fourfold2'][2])}|{'{:5d}'.format(OOOOOOO00OOO00000['params']['fourfold2'][3])}|")#line:381
                print (f"----|-----|-----|  ----|-----|-----|")#line:382
            else :#line:383
                print ("Unsupported task type for rule details")#line:384
            print ("")#line:388
        else :#line:389
            print ("No such rule.")#line:390
    def get_ruletext (OO0O0O0O00OOOO0OO ,OO000O000OO00O00O ):#line:392
        ""#line:398
        if not (OO0O0O0O00OOOO0OO ._is_calculated ()):#line:399
            print ("ERROR: Task has not been calculated.")#line:400
            return #line:401
        if OO000O000OO00O00O <=0 or OO000O000OO00O00O >OO0O0O0O00OOOO0OO .get_rulecount ():#line:402
            if OO0O0O0O00OOOO0OO .get_rulecount ()==0 :#line:403
                print ("No such rule. There are no rules in result.")#line:404
            else :#line:405
                print (f"No such rule ({OO000O000OO00O00O}). Available rules are 1 to {OO0O0O0O00OOOO0OO.get_rulecount()}")#line:406
            return None #line:407
        OO0O0O00O00O0O0O0 =""#line:408
        OOOO0O00OOOO0000O =OO0O0O0O00OOOO0OO .result ["rules"][OO000O000OO00O00O -1 ]#line:409
        if OO0O0O0O00OOOO0OO .result ['taskinfo']['task_type']=="4ftMiner":#line:410
            OO0O0O00O00O0O0O0 =OO0O0O00O00O0O0O0 +" "+OOOO0O00OOOO0000O ["cedents_str"]["ante"]+" => "+OOOO0O00OOOO0000O ["cedents_str"]["succ"]+" | "+OOOO0O00OOOO0000O ["cedents_str"]["cond"]#line:412
        elif OO0O0O0O00OOOO0OO .result ['taskinfo']['task_type']=="UICMiner":#line:413
            OO0O0O00O00O0O0O0 =OO0O0O00O00O0O0O0 +"     "+OOOO0O00OOOO0000O ["cedents_str"]["ante"]+" => "+OO0O0O0O00OOOO0OO .result ['taskinfo']['target']+"(*) | "+OOOO0O00OOOO0000O ["cedents_str"]["cond"]#line:415
        elif OO0O0O0O00OOOO0OO .result ['taskinfo']['task_type']=="CFMiner":#line:416
            OO0O0O00O00O0O0O0 =OO0O0O00O00O0O0O0 +" "+OOOO0O00OOOO0000O ["cedents_str"]["cond"]#line:417
        elif OO0O0O0O00OOOO0OO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:418
            OO0O0O00O00O0O0O0 =OO0O0O00O00O0O0O0 +"  "+OOOO0O00OOOO0000O ["cedents_str"]["ante"]+" => "+OOOO0O00OOOO0000O ["cedents_str"]["succ"]+" | "+OOOO0O00OOOO0000O ["cedents_str"]["cond"]+" : "+OOOO0O00OOOO0000O ["cedents_str"]["frst"]+" x "+OOOO0O00OOOO0000O ["cedents_str"]["scnd"]#line:420
        return OO0O0O00O00O0O0O0 #line:421
    def _annotate_chart (OOOO000O0O000OO0O ,O0000OO0O0O00OO0O ,OO0O0O00000000O00 ,cnt =2 ):#line:423
        ""#line:430
        OOO0O0OOOOOOOOO00 =O0000OO0O0O00OO0O .axes .get_ylim ()#line:431
        for O000OO00O0O0OOOO0 in O0000OO0O0O00OO0O .patches :#line:433
            O00OOO000O0OOOO0O ='{:.1f}%'.format (100 *O000OO00O0O0OOOO0 .get_height ()/OO0O0O00000000O00 )#line:434
            O0O0000O0OOO00O00 =O000OO00O0O0OOOO0 .get_x ()+O000OO00O0O0OOOO0 .get_width ()/4 #line:435
            OOOO0O0OO000O0O00 =O000OO00O0O0OOOO0 .get_y ()+O000OO00O0O0OOOO0 .get_height ()-OOO0O0OOOOOOOOO00 [1 ]/8 #line:436
            if O000OO00O0O0OOOO0 .get_height ()<OOO0O0OOOOOOOOO00 [1 ]/8 :#line:437
                OOOO0O0OO000O0O00 =O000OO00O0O0OOOO0 .get_y ()+O000OO00O0O0OOOO0 .get_height ()+OOO0O0OOOOOOOOO00 [1 ]*0.02 #line:438
            O0000OO0O0O00OO0O .annotate (O00OOO000O0OOOO0O ,(O0O0000O0OOO00O00 ,OOOO0O0OO000O0O00 ),size =23 /cnt )#line:439
    def draw_rule (O0O000OO000OO0OOO ,O0O000O0OOOOO00OO ,show =True ,filename =None ):#line:441
        ""#line:447
        if not (O0O000OO000OO0OOO ._is_calculated ()):#line:448
            print ("ERROR: Task has not been calculated.")#line:449
            return #line:450
        print ("")#line:451
        if (O0O000O0OOOOO00OO <=len (O0O000OO000OO0OOO .result ["rules"])):#line:452
            if O0O000OO000OO0OOO .result ['taskinfo']['task_type']=="4ftMiner":#line:453
                OOO00OO0000O0O00O ,O0O00O0O00OO0O0O0 =plt .subplots (2 ,2 )#line:455
                OOO000O00O0OO0O00 =['S','not S']#line:456
                OO00OO0000O0O0OO0 =['A','not A']#line:457
                O0000OOO0000O0O00 =O0O000OO000OO0OOO .get_fourfold (O0O000O0OOOOO00OO )#line:458
                O000OOO0OOO00000O =[O0000OOO0000O0O00 [0 ],O0000OOO0000O0O00 [1 ]]#line:460
                OO00OO0OOO00O0O00 =[O0000OOO0000O0O00 [2 ],O0000OOO0000O0O00 [3 ]]#line:461
                O000O0O00O0O00OO0 =[O0000OOO0000O0O00 [0 ]+O0000OOO0000O0O00 [2 ],O0000OOO0000O0O00 [1 ]+O0000OOO0000O0O00 [3 ]]#line:462
                O0O00O0O00OO0O0O0 [0 ,0 ]=sns .barplot (ax =O0O00O0O00OO0O0O0 [0 ,0 ],x =OOO000O00O0OO0O00 ,y =O000OOO0OOO00000O ,color ='lightsteelblue')#line:463
                O0O000OO000OO0OOO ._annotate_chart (O0O00O0O00OO0O0O0 [0 ,0 ],O0000OOO0000O0O00 [0 ]+O0000OOO0000O0O00 [1 ])#line:465
                O0O00O0O00OO0O0O0 [0 ,1 ]=sns .barplot (ax =O0O00O0O00OO0O0O0 [0 ,1 ],x =OOO000O00O0OO0O00 ,y =O000O0O00O0O00OO0 ,color ="gray",edgecolor ="black")#line:467
                O0O000OO000OO0OOO ._annotate_chart (O0O00O0O00OO0O0O0 [0 ,1 ],sum (O0000OOO0000O0O00 ))#line:469
                O0O00O0O00OO0O0O0 [0 ,0 ].set (xlabel =None ,ylabel ='Count')#line:471
                O0O00O0O00OO0O0O0 [0 ,1 ].set (xlabel =None ,ylabel ='Count')#line:472
                OOOOOO0000000OOO0 =sns .color_palette ("Blues",as_cmap =True )#line:474
                OOOOOO00OOO0O0O0O =sns .color_palette ("Greys",as_cmap =True )#line:475
                O0O00O0O00OO0O0O0 [1 ,0 ]=sns .heatmap (ax =O0O00O0O00OO0O0O0 [1 ,0 ],data =[O000OOO0OOO00000O ,OO00OO0OOO00O0O00 ],xticklabels =OOO000O00O0OO0O00 ,yticklabels =OO00OO0000O0O0OO0 ,annot =True ,cbar =False ,fmt =".0f",cmap =OOOOOO0000000OOO0 )#line:479
                O0O00O0O00OO0O0O0 [1 ,0 ].set (xlabel =None ,ylabel ='Count')#line:481
                O0O00O0O00OO0O0O0 [1 ,1 ]=sns .heatmap (ax =O0O00O0O00OO0O0O0 [1 ,1 ],data =np .asarray ([O000O0O00O0O00OO0 ]),xticklabels =OOO000O00O0OO0O00 ,yticklabels =False ,annot =True ,cbar =False ,fmt =".0f",cmap =OOOOOO00OOO0O0O0O )#line:485
                O0O00O0O00OO0O0O0 [1 ,1 ].set (xlabel =None ,ylabel ='Count')#line:487
                OO0OOO000000O00O0 =O0O000OO000OO0OOO .result ["rules"][O0O000O0OOOOO00OO -1 ]['cedents_str']['ante']#line:489
                O0O00O0O00OO0O0O0 [0 ,0 ].set (title ="\n".join (wrap (OO0OOO000000O00O0 ,30 )))#line:490
                O0O00O0O00OO0O0O0 [0 ,1 ].set (title ='Entire dataset')#line:491
                OOO0O0O000OO00OOO =O0O000OO000OO0OOO .result ["rules"][O0O000O0OOOOO00OO -1 ]['cedents_str']#line:493
                OOO00OO0000O0O00O .suptitle ("Antecedent : "+OOO0O0O000OO00OOO ['ante']+"\nSuccedent : "+OOO0O0O000OO00OOO ['succ']+"\nCondition : "+OOO0O0O000OO00OOO ['cond'],x =0 ,ha ='left',size ='small')#line:497
                OOO00OO0000O0O00O .tight_layout ()#line:498
            elif O0O000OO000OO0OOO .result ['taskinfo']['task_type']=="SD4ftMiner":#line:500
                OOO00OO0000O0O00O ,O0O00O0O00OO0O0O0 =plt .subplots (2 ,2 )#line:502
                OOO000O00O0OO0O00 =['S','not S']#line:503
                OO00OO0000O0O0OO0 =['A','not A']#line:504
                O00OOO0OOOO0OO0O0 =O0O000OO000OO0OOO .get_fourfold (O0O000O0OOOOO00OO ,order =1 )#line:506
                O000000OOOO00OOOO =O0O000OO000OO0OOO .get_fourfold (O0O000O0OOOOO00OO ,order =2 )#line:507
                O000000OOO0O00000 =[O00OOO0OOOO0OO0O0 [0 ],O00OOO0OOOO0OO0O0 [1 ]]#line:509
                OO0OO00OOOOO0OOOO =[O00OOO0OOOO0OO0O0 [2 ],O00OOO0OOOO0OO0O0 [3 ]]#line:510
                O0O0000OOOO0O0O0O =[O00OOO0OOOO0OO0O0 [0 ]+O00OOO0OOOO0OO0O0 [2 ],O00OOO0OOOO0OO0O0 [1 ]+O00OOO0OOOO0OO0O0 [3 ]]#line:511
                O0O0O000OO0OO00OO =[O000000OOOO00OOOO [0 ],O000000OOOO00OOOO [1 ]]#line:512
                OO0O0OO00000O00OO =[O000000OOOO00OOOO [2 ],O000000OOOO00OOOO [3 ]]#line:513
                OO0O0O000OO00OO00 =[O000000OOOO00OOOO [0 ]+O000000OOOO00OOOO [2 ],O000000OOOO00OOOO [1 ]+O000000OOOO00OOOO [3 ]]#line:514
                O0O00O0O00OO0O0O0 [0 ,0 ]=sns .barplot (ax =O0O00O0O00OO0O0O0 [0 ,0 ],x =OOO000O00O0OO0O00 ,y =O000000OOO0O00000 ,color ='orange')#line:515
                O0O000OO000OO0OOO ._annotate_chart (O0O00O0O00OO0O0O0 [0 ,0 ],O00OOO0OOOO0OO0O0 [0 ]+O00OOO0OOOO0OO0O0 [1 ])#line:517
                O0O00O0O00OO0O0O0 [0 ,1 ]=sns .barplot (ax =O0O00O0O00OO0O0O0 [0 ,1 ],x =OOO000O00O0OO0O00 ,y =O0O0O000OO0OO00OO ,color ="green")#line:519
                O0O000OO000OO0OOO ._annotate_chart (O0O00O0O00OO0O0O0 [0 ,1 ],O000000OOOO00OOOO [0 ]+O000000OOOO00OOOO [1 ])#line:521
                O0O00O0O00OO0O0O0 [0 ,0 ].set (xlabel =None ,ylabel ='Count')#line:523
                O0O00O0O00OO0O0O0 [0 ,1 ].set (xlabel =None ,ylabel ='Count')#line:524
                OOOOOO0000000OOO0 =sns .color_palette ("Oranges",as_cmap =True )#line:526
                OOOOOO00OOO0O0O0O =sns .color_palette ("Greens",as_cmap =True )#line:527
                O0O00O0O00OO0O0O0 [1 ,0 ]=sns .heatmap (ax =O0O00O0O00OO0O0O0 [1 ,0 ],data =[O000000OOO0O00000 ,OO0OO00OOOOO0OOOO ],xticklabels =OOO000O00O0OO0O00 ,yticklabels =OO00OO0000O0O0OO0 ,annot =True ,cbar =False ,fmt =".0f",cmap =OOOOOO0000000OOO0 )#line:530
                O0O00O0O00OO0O0O0 [1 ,0 ].set (xlabel =None ,ylabel ='Count')#line:532
                O0O00O0O00OO0O0O0 [1 ,1 ]=sns .heatmap (ax =O0O00O0O00OO0O0O0 [1 ,1 ],data =[O0O0O000OO0OO00OO ,OO0O0OO00000O00OO ],xticklabels =OOO000O00O0OO0O00 ,yticklabels =False ,annot =True ,cbar =False ,fmt =".0f",cmap =OOOOOO00OOO0O0O0O )#line:536
                O0O00O0O00OO0O0O0 [1 ,1 ].set (xlabel =None ,ylabel ='Count')#line:538
                OO0OOO000000O00O0 =O0O000OO000OO0OOO .result ["rules"][O0O000O0OOOOO00OO -1 ]['cedents_str']['frst']#line:540
                O0O00O0O00OO0O0O0 [0 ,0 ].set (title ="\n".join (wrap (OO0OOO000000O00O0 ,30 )))#line:541
                O0O0OO00O00OOO00O =O0O000OO000OO0OOO .result ["rules"][O0O000O0OOOOO00OO -1 ]['cedents_str']['scnd']#line:542
                O0O00O0O00OO0O0O0 [0 ,1 ].set (title ="\n".join (wrap (O0O0OO00O00OOO00O ,30 )))#line:543
                OOO0O0O000OO00OOO =O0O000OO000OO0OOO .result ["rules"][O0O000O0OOOOO00OO -1 ]['cedents_str']#line:545
                OOO00OO0000O0O00O .suptitle ("Antecedent : "+OOO0O0O000OO00OOO ['ante']+"\nSuccedent : "+OOO0O0O000OO00OOO ['succ']+"\nCondition : "+OOO0O0O000OO00OOO ['cond']+"\nFirst : "+OOO0O0O000OO00OOO ['frst']+"\nSecond : "+OOO0O0O000OO00OOO ['scnd'],x =0 ,ha ='left',size ='small')#line:550
                OOO00OO0000O0O00O .tight_layout ()#line:552
            elif (O0O000OO000OO0OOO .result ['taskinfo']['task_type']=="CFMiner")or (O0O000OO000OO0OOO .result ['taskinfo']['task_type']=="UICMiner"):#line:555
                OOO0O0O0OO0O0000O =O0O000OO000OO0OOO .result ['taskinfo']['task_type']=="UICMiner"#line:556
                OOO00OO0000O0O00O ,O0O00O0O00OO0O0O0 =plt .subplots (2 ,2 ,gridspec_kw ={'height_ratios':[3 ,1 ]})#line:557
                OOO00OOO0OO0OO00O =O0O000OO000OO0OOO .result ['taskinfo']['target']#line:558
                OOO000O00O0OO0O00 =O0O000OO000OO0OOO .result ['datalabels']['catnames'][O0O000OO000OO0OOO .result ['datalabels']['varname'].index (O0O000OO000OO0OOO .result ['taskinfo']['target'])]#line:560
                O000O0O00OO0OOO0O =O0O000OO000OO0OOO .result ["rules"][O0O000O0OOOOO00OO -1 ]#line:561
                O0OOO00O0OO0OOOO0 =O0O000OO000OO0OOO .get_hist (O0O000O0OOOOO00OO )#line:562
                if OOO0O0O0OO0O0000O :#line:563
                    O0OOO00O0OO0OOOO0 =O000O0O00OO0OOO0O ['params']['hist']#line:564
                else :#line:565
                    O0OOO00O0OO0OOOO0 =O0O000OO000OO0OOO .get_hist (O0O000O0OOOOO00OO )#line:566
                O0O00O0O00OO0O0O0 [0 ,0 ]=sns .barplot (ax =O0O00O0O00OO0O0O0 [0 ,0 ],x =OOO000O00O0OO0O00 ,y =O0OOO00O0OO0OOOO0 ,color ='lightsteelblue')#line:567
                OO000OO0000O00O0O =[]#line:569
                OOO00OOOO000O0OO0 =[]#line:570
                if OOO0O0O0OO0O0000O :#line:571
                    OO000OO0000O00O0O =OOO000O00O0OO0O00 #line:572
                    OOO00OOOO000O0OO0 =O0O000OO000OO0OOO .get_hist (O0O000O0OOOOO00OO ,fullCond =True )#line:573
                else :#line:574
                    OO000OO0000O00O0O =O0O000OO000OO0OOO .profiles ['hist_target_entire_dataset_labels']#line:575
                    OOO00OOOO000O0OO0 =O0O000OO000OO0OOO .profiles ['hist_target_entire_dataset_values']#line:576
                O0O00O0O00OO0O0O0 [0 ,1 ]=sns .barplot (ax =O0O00O0O00OO0O0O0 [0 ,1 ],x =OO000OO0000O00O0O ,y =OOO00OOOO000O0OO0 ,color ="gray",edgecolor ="black")#line:577
                O0O000OO000OO0OOO ._annotate_chart (O0O00O0O00OO0O0O0 [0 ,0 ],sum (O0OOO00O0OO0OOOO0 ),len (O0OOO00O0OO0OOOO0 ))#line:579
                O0O000OO000OO0OOO ._annotate_chart (O0O00O0O00OO0O0O0 [0 ,1 ],sum (OOO00OOOO000O0OO0 ),len (OOO00OOOO000O0OO0 ))#line:580
                O0O00O0O00OO0O0O0 [0 ,0 ].set (xlabel =None ,ylabel ='Count')#line:582
                O0O00O0O00OO0O0O0 [0 ,1 ].set (xlabel =None ,ylabel ='Count')#line:583
                OO0OOOOO00OOOO0O0 =[OOO000O00O0OO0O00 ,O0OOO00O0OO0OOOO0 ]#line:585
                OO0000OO00O00OO0O =pd .DataFrame (OO0OOOOO00OOOO0O0 ).transpose ()#line:586
                OO0000OO00O00OO0O .columns =[OOO00OOO0OO0OO00O ,'No of observatios']#line:587
                OOOOOO0000000OOO0 =sns .color_palette ("Blues",as_cmap =True )#line:589
                OOOOOO00OOO0O0O0O =sns .color_palette ("Greys",as_cmap =True )#line:590
                O0O00O0O00OO0O0O0 [1 ,0 ]=sns .heatmap (ax =O0O00O0O00OO0O0O0 [1 ,0 ],data =np .asarray ([O0OOO00O0OO0OOOO0 ]),xticklabels =OOO000O00O0OO0O00 ,yticklabels =False ,annot =True ,cbar =False ,fmt =".0f",cmap =OOOOOO0000000OOO0 )#line:594
                O0O00O0O00OO0O0O0 [1 ,0 ].set (xlabel =OOO00OOO0OO0OO00O ,ylabel ='Count')#line:596
                O0O00O0O00OO0O0O0 [1 ,1 ]=sns .heatmap (ax =O0O00O0O00OO0O0O0 [1 ,1 ],data =np .asarray ([OOO00OOOO000O0OO0 ]),xticklabels =OO000OO0000O00O0O ,yticklabels =False ,annot =True ,cbar =False ,fmt =".0f",cmap =OOOOOO00OOO0O0O0O )#line:600
                O0O00O0O00OO0O0O0 [1 ,1 ].set (xlabel =OOO00OOO0OO0OO00O ,ylabel ='Count')#line:602
                O00OOOO00OO000O0O =""#line:603
                O0O000000OOO00O00 ='Entire dataset'#line:604
                if OOO0O0O0OO0O0000O :#line:605
                    if len (O000O0O00OO0OOO0O ['cedents_struct']['cond'])>0 :#line:606
                        O0O000000OOO00O00 =O000O0O00OO0OOO0O ['cedents_str']['cond']#line:607
                        O00OOOO00OO000O0O =" & "+O000O0O00OO0OOO0O ['cedents_str']['cond']#line:608
                O0O00O0O00OO0O0O0 [0 ,1 ].set (title =O0O000000OOO00O00 )#line:609
                if OOO0O0O0OO0O0000O :#line:610
                    OO0OOO000000O00O0 =O0O000OO000OO0OOO .result ["rules"][O0O000O0OOOOO00OO -1 ]['cedents_str']['ante']+O00OOOO00OO000O0O #line:611
                else :#line:612
                    OO0OOO000000O00O0 =O0O000OO000OO0OOO .result ["rules"][O0O000O0OOOOO00OO -1 ]['cedents_str']['cond']#line:613
                O0O00O0O00OO0O0O0 [0 ,0 ].set (title ="\n".join (wrap (OO0OOO000000O00O0 ,30 )))#line:614
                OOO0O0O000OO00OOO =O0O000OO000OO0OOO .result ["rules"][O0O000O0OOOOO00OO -1 ]['cedents_str']#line:616
                O0O000000OOO00O00 ="Condition : "+OOO0O0O000OO00OOO ['cond']#line:617
                if OOO0O0O0OO0O0000O :#line:618
                    O0O000000OOO00O00 =O0O000000OOO00O00 +"\nAntecedent : "+OOO0O0O000OO00OOO ['ante']#line:619
                OOO00OO0000O0O00O .suptitle (O0O000000OOO00O00 ,x =0 ,ha ='left',size ='small')#line:620
                OOO00OO0000O0O00O .tight_layout ()#line:622
            else :#line:623
                print ("Unsupported task type for rule details")#line:624
                return #line:625
            if filename is not None :#line:626
                plt .savefig (filename =filename )#line:627
            if show :#line:628
                plt .show ()#line:629
            print ("")#line:631
        else :#line:632
            print ("No such rule.")#line:633
    def get_rulecount (O000OO00O00OO0000 ):#line:635
        ""#line:640
        if not (O000OO00O00OO0000 ._is_calculated ()):#line:641
            print ("ERROR: Task has not been calculated.")#line:642
            return #line:643
        return len (O000OO00O00OO0000 .result ["rules"])#line:644
    def get_fourfold (O00OOO0O0O00OO0O0 ,O0O00OOO0OOO00000 ,order =0 ):#line:646
        ""#line:653
        if not (O00OOO0O0O00OO0O0 ._is_calculated ()):#line:654
            print ("ERROR: Task has not been calculated.")#line:655
            return #line:656
        if (O0O00OOO0OOO00000 <=len (O00OOO0O0O00OO0O0 .result ["rules"])):#line:657
            if O00OOO0O0O00OO0O0 .result ['taskinfo']['task_type']=="4ftMiner":#line:658
                O00OO0OOOO00O0000 =O00OOO0O0O00OO0O0 .result ["rules"][O0O00OOO0OOO00000 -1 ]#line:659
                return O00OO0OOOO00O0000 ['params']['fourfold']#line:660
            elif O00OOO0O0O00OO0O0 .result ['taskinfo']['task_type']=="CFMiner":#line:661
                print ("Error: fourfold for CFMiner is not defined")#line:662
                return None #line:663
            elif O00OOO0O0O00OO0O0 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:664
                O00OO0OOOO00O0000 =O00OOO0O0O00OO0O0 .result ["rules"][O0O00OOO0OOO00000 -1 ]#line:665
                if order ==1 :#line:666
                    return O00OO0OOOO00O0000 ['params']['fourfold1']#line:667
                if order ==2 :#line:668
                    return O00OO0OOOO00O0000 ['params']['fourfold2']#line:669
                print ("Error: for SD4ft-Miner, you need to provide order of fourfold table in order= parameter (valid values are 1,2).")#line:670
                return None #line:671
            else :#line:672
                print ("Unsupported task type for rule details")#line:673
        else :#line:674
            print ("No such rule.")#line:675
    def get_hist (O0OO000O00O0OO0O0 ,O0O00OO0O0OO0OO00 ,fullCond =True ):#line:677
        ""#line:684
        if not (O0OO000O00O0OO0O0 ._is_calculated ()):#line:685
            print ("ERROR: Task has not been calculated.")#line:686
            return #line:687
        if (O0O00OO0O0OO0OO00 <=len (O0OO000O00O0OO0O0 .result ["rules"])):#line:688
            if O0OO000O00O0OO0O0 .result ['taskinfo']['task_type']=="CFMiner":#line:689
                OOOO00O0000OOOO00 =O0OO000O00O0OO0O0 .result ["rules"][O0O00OO0O0OO0OO00 -1 ]#line:690
                return OOOO00O0000OOOO00 ['params']['hist']#line:691
            elif O0OO000O00O0OO0O0 .result ['taskinfo']['task_type']=="UICMiner":#line:692
                OOOO00O0000OOOO00 =O0OO000O00O0OO0O0 .result ["rules"][O0O00OO0O0OO0OO00 -1 ]#line:693
                OOO000OO0OOOO00OO =None #line:694
                if fullCond :#line:695
                    OOO000OO0OOOO00OO =OOOO00O0000OOOO00 ['params']['hist_cond']#line:696
                else :#line:697
                    OOO000OO0OOOO00OO =OOOO00O0000OOOO00 ['params']['hist']#line:698
                return OOO000OO0OOOO00OO #line:699
            elif O0OO000O00O0OO0O0 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:700
                print ("Error: SD4ft-Miner has no histogram")#line:701
                return None #line:702
            elif O0OO000O00O0OO0O0 .result ['taskinfo']['task_type']=="4ftMiner":#line:703
                print ("Error: 4ft-Miner has no histogram")#line:704
                return None #line:705
            else :#line:706
                print ("Unsupported task type for rule details")#line:707
        else :#line:708
            print ("No such rule.")#line:709
    def get_hist_cond (O0O00000OOO00OOO0 ,O0OO0O0O00OOOOOOO ):#line:712
        ""#line:718
        if not (O0O00000OOO00OOO0 ._is_calculated ()):#line:719
            print ("ERROR: Task has not been calculated.")#line:720
            return #line:721
        if (O0OO0O0O00OOOOOOO <=len (O0O00000OOO00OOO0 .result ["rules"])):#line:723
            if O0O00000OOO00OOO0 .result ['taskinfo']['task_type']=="UICMiner":#line:724
                O00OO0OOOO00OO0O0 =O0O00000OOO00OOO0 .result ["rules"][O0OO0O0O00OOOOOOO -1 ]#line:725
                return O00OO0OOOO00OO0O0 ['params']['hist_cond']#line:726
            elif O0O00000OOO00OOO0 .result ['taskinfo']['task_type']=="CFMiner":#line:727
                O00OO0OOOO00OO0O0 =O0O00000OOO00OOO0 .result ["rules"][O0OO0O0O00OOOOOOO -1 ]#line:728
                return O00OO0OOOO00OO0O0 ['params']['hist']#line:729
            elif O0O00000OOO00OOO0 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:730
                print ("Error: SD4ft-Miner has no histogram")#line:731
                return None #line:732
            elif O0O00000OOO00OOO0 .result ['taskinfo']['task_type']=="4ftMiner":#line:733
                print ("Error: 4ft-Miner has no histogram")#line:734
                return None #line:735
            else :#line:736
                print ("Unsupported task type for rule details")#line:737
        else :#line:738
            print ("No such rule.")#line:739
    def get_quantifiers (OO0O000OO0O0O0OO0 ,OO00O000O00OOOO00 ,order =0 ):#line:741
        ""#line:750
        if not (OO0O000OO0O0O0OO0 ._is_calculated ()):#line:751
            print ("ERROR: Task has not been calculated.")#line:752
            return None #line:753
        if (OO00O000O00OOOO00 <=len (OO0O000OO0O0O0OO0 .result ["rules"])):#line:755
            OOO00O00OO0OO00O0 =OO0O000OO0O0O0OO0 .result ["rules"][OO00O000O00OOOO00 -1 ]#line:756
            if OO0O000OO0O0O0OO0 .result ['taskinfo']['task_type']=="4ftMiner":#line:757
                return OOO00O00OO0OO00O0 ['params']#line:758
            elif OO0O000OO0O0O0OO0 .result ['taskinfo']['task_type']=="CFMiner":#line:759
                return OOO00O00OO0OO00O0 ['params']#line:760
            elif OO0O000OO0O0O0OO0 .result ['taskinfo']['task_type']=="SD4ftMiner":#line:761
                return OOO00O00OO0OO00O0 ['params']#line:762
            else :#line:763
                print ("Unsupported task type for rule details")#line:764
        else :#line:765
            print ("No such rule.")#line:766
    def get_varlist (O00O0OOO00OO0OOOO ):#line:768
        ""#line:772
        return O00O0OOO00OO0OOOO .result ["datalabels"]["varname"]#line:774
    def get_category_names (OO00OOO0O00OOO0O0 ,varname =None ,varindex =None ):#line:776
        ""#line:783
        O00OO0OO0OOO0O00O =0 #line:784
        if varindex is not None :#line:785
            if O00OO0OO0OOO0O00O >=0 &O00OO0OO0OOO0O00O <len (OO00OOO0O00OOO0O0 .get_varlist ()):#line:786
                O00OO0OO0OOO0O00O =varindex #line:787
            else :#line:788
                print ("Error: no such variable.")#line:789
                return #line:790
        if (varname is not None ):#line:791
            O0OO000OOO0O0O00O =OO00OOO0O00OOO0O0 .get_varlist ()#line:792
            O00OO0OO0OOO0O00O =O0OO000OOO0O0O00O .index (varname )#line:793
            if O00OO0OO0OOO0O00O ==-1 |O00OO0OO0OOO0O00O <0 |O00OO0OO0OOO0O00O >=len (OO00OOO0O00OOO0O0 .get_varlist ()):#line:794
                print ("Error: no such variable.")#line:795
                return #line:796
        return OO00OOO0O00OOO0O0 .result ["datalabels"]["catnames"][O00OO0OO0OOO0O00O ]#line:797
    def print_data_definition (OOO0O0O00000O0OOO ):#line:799
        ""#line:802
        O0O00O0000OO000OO =OOO0O0O00000O0OOO .get_varlist ()#line:803
        print (f"Dataset has {len(O0O00O0000OO000OO)} variables.")#line:804
        for OO0OOO0O00OOO000O in O0O00O0000OO000OO :#line:805
            OO0OOOOO000OOOOO0 =OOO0O0O00000O0OOO .get_category_names (OO0OOO0O00OOO000O )#line:806
            O00O0OO00OO0O0OOO =""#line:807
            for O00OOO00O0OO00OO0 in OO0OOOOO000OOOOO0 :#line:808
                O00O0OO00OO0O0OOO =O00O0OO00OO0O0OOO +str (O00OOO00O0OO00OO0 )+" "#line:809
            O00O0OO00OO0O0OOO =O00O0OO00OO0O0OOO [:-1 ]#line:810
            print (f"Variable {OO0OOO0O00OOO000O} has {len(OO0OOOOO000OOOOO0)} categories: {O00O0OO00OO0O0OOO}")#line:811
    def _is_calculated (O0OOOO0OO000OOO0O ):#line:813
        ""#line:818
        OO0OOO00O000O0OOO =False #line:819
        if 'taskinfo'in O0OOOO0OO000OOO0O .result :#line:820
            OO0OOO00O000O0OOO =True #line:821
        return OO0OOO00O000O0OOO #line:822
    def get_version_string (O000O000OO0OOOO0O ):#line:825
        ""#line:830
        return O000O000OO0OOOO0O .version_string #line:831
    def get_rule_cedent_list (O0OO0O000000OOOO0 ,OOO0O00OOOO0OO000 ):#line:833
        ""#line:839
        if not (O0OO0O000000OOOO0 ._is_calculated ()):#line:840
            print ("ERROR: Task has not been calculated.")#line:841
            return #line:842
        if OOO0O00OOOO0OO000 <=0 or OOO0O00OOOO0OO000 >O0OO0O000000OOOO0 .get_rulecount ():#line:843
            if O0OO0O000000OOOO0 .get_rulecount ()==0 :#line:844
                print ("No such rule. There are no rules in result.")#line:845
            else :#line:846
                print (f"No such rule ({OOO0O00OOOO0OO000}). Available rules are 1 to {O0OO0O000000OOOO0.get_rulecount()}")#line:847
            return None #line:848
        O0O000O000OO00000 =[]#line:849
        O0OO000OOOOO00OOO =O0OO0O000000OOOO0 .result ["rules"][OOO0O00OOOO0OO000 -1 ]#line:850
        O0O000O000OO00000 =list (O0OO000OOOOO00OOO ['trace_cedent_dataorder'].keys ())#line:851
        return O0O000O000OO00000 #line:853
    def get_rule_variables (O00OO0000O0O0OO0O ,OO00OO00000OO00O0 ,O000OO0OO0O0OOO00 ,get_names =True ):#line:856
        ""#line:864
        if not (O00OO0000O0O0OO0O ._is_calculated ()):#line:865
            print ("ERROR: Task has not been calculated.")#line:866
            return #line:867
        if OO00OO00000OO00O0 <=0 or OO00OO00000OO00O0 >O00OO0000O0O0OO0O .get_rulecount ():#line:868
            if O00OO0000O0O0OO0O .get_rulecount ()==0 :#line:869
                print ("No such rule. There are no rules in result.")#line:870
            else :#line:871
                print (f"No such rule ({OO00OO00000OO00O0}). Available rules are 1 to {O00OO0000O0O0OO0O.get_rulecount()}")#line:872
            return None #line:873
        OO0O0OO0OO0000OO0 =[]#line:874
        O0OOO0O0O00O00O00 =O00OO0000O0O0OO0O .result ["rules"][OO00OO00000OO00O0 -1 ]#line:875
        O00OOOO00OOOOOOOO =O00OO0000O0O0OO0O .result ["datalabels"]['varname']#line:876
        if not (O000OO0OO0O0OOO00 in O0OOO0O0O00O00O00 ['trace_cedent_dataorder']):#line:877
            print (f"ERROR: cedent {O000OO0OO0O0OOO00} not in result.")#line:878
            exit (1 )#line:879
        for OOO00OO00OOOO00OO in O0OOO0O0O00O00O00 ['trace_cedent_dataorder'][O000OO0OO0O0OOO00 ]:#line:880
            if get_names :#line:881
                OO0O0OO0OO0000OO0 .append (O00OOOO00OOOOOOOO [OOO00OO00OOOO00OO ])#line:882
            else :#line:883
                OO0O0OO0OO0000OO0 .append (OOO00OO00OOOO00OO )#line:884
        return OO0O0OO0OO0000OO0 #line:886
    def get_rule_categories (OO0OO000OOO000OOO ,O000O0O0OOO000OOO ,OO0O000O0OO00OO00 ,O00OO0000OOO0O0OO ,get_names =True ):#line:889
        ""#line:898
        if not (OO0OO000OOO000OOO ._is_calculated ()):#line:899
            print ("ERROR: Task has not been calculated.")#line:900
            return #line:901
        if O000O0O0OOO000OOO <=0 or O000O0O0OOO000OOO >OO0OO000OOO000OOO .get_rulecount ():#line:902
            if OO0OO000OOO000OOO .get_rulecount ()==0 :#line:903
                print ("No such rule. There are no rules in result.")#line:904
            else :#line:905
                print (f"No such rule ({O000O0O0OOO000OOO}). Available rules are 1 to {OO0OO000OOO000OOO.get_rulecount()}")#line:906
            return None #line:907
        OOOOOO0O0O0OO0OO0 =[]#line:908
        OOO0000OOOO0O000O =OO0OO000OOO000OOO .result ["rules"][O000O0O0OOO000OOO -1 ]#line:909
        OO0O0O0OOO000OOOO =OO0OO000OOO000OOO .result ["datalabels"]['varname']#line:910
        if O00OO0000OOO0O0OO in OO0O0O0OOO000OOOO :#line:911
            OO000O0O0O0OO0OOO =OO0O0O0OOO000OOOO .index (O00OO0000OOO0O0OO )#line:912
            OO0000O00000OO0O0 =OO0OO000OOO000OOO .result ['datalabels']['catnames'][OO000O0O0O0OO0OOO ]#line:913
            if not (OO0O000O0OO00OO00 in OOO0000OOOO0O000O ['trace_cedent_dataorder']):#line:914
                print (f"ERROR: cedent {OO0O000O0OO00OO00} not in result.")#line:915
                exit (1 )#line:916
            O0O00O0OOO00O0000 =OOO0000OOOO0O000O ['trace_cedent_dataorder'][OO0O000O0OO00OO00 ].index (OO000O0O0O0OO0OOO )#line:917
            for OOO0OO0OOO0000OO0 in OOO0000OOOO0O000O ['traces'][OO0O000O0OO00OO00 ][O0O00O0OOO00O0000 ]:#line:918
                if get_names :#line:919
                    OOOOOO0O0O0OO0OO0 .append (OO0000O00000OO0O0 [OOO0OO0OOO0000OO0 ])#line:920
                else :#line:921
                    OOOOOO0O0O0OO0OO0 .append (OOO0OO0OOO0000OO0 )#line:922
        else :#line:923
            print (f"ERROR: variable not found: {OO0O000O0OO00OO00},{O00OO0000OOO0O0OO}. Possible variables are {OO0O0O0OOO000OOOO}")#line:924
            exit (1 )#line:925
        return OOOOOO0O0O0OO0OO0 #line:926
    def get_dataset_variable_count (OOO000O00OO0O0OO0 ):#line:929
        ""#line:934
        if not (OOO000O00OO0O0OO0 ._is_calculated ()):#line:935
            print ("ERROR: Task has not been calculated.")#line:936
            return #line:937
        OOO0OO000O00O00O0 =OOO000O00OO0O0OO0 .result ["datalabels"]['varname']#line:938
        return len (OOO0OO000O00O00O0 )#line:939
    def get_dataset_variable_list (O0O0O0OOO0OOO00O0 ):#line:942
        ""#line:947
        if not (O0O0O0OOO0OOO00O0 ._is_calculated ()):#line:948
            print ("ERROR: Task has not been calculated.")#line:949
            return #line:950
        OO0OO00000OO0OO0O =O0O0O0OOO0OOO00O0 .result ["datalabels"]['varname']#line:951
        return OO0OO00000OO0OO0O #line:952
    def get_dataset_variable_name (O00OO0O00000O0OO0 ,O0O00O0O00OOO0OO0 ):#line:955
        ""#line:961
        if not (O00OO0O00000O0OO0 ._is_calculated ()):#line:962
            print ("ERROR: Task has not been calculated.")#line:963
            return #line:964
        O0OOOO0OOOO00O0OO =O00OO0O00000O0OO0 .get_dataset_variable_list ()#line:965
        if O0O00O0O00OOO0OO0 >=0 and O0O00O0O00OOO0OO0 <len (O0OOOO0OOOO00O0OO ):#line:966
            return O0OOOO0OOOO00O0OO [O0O00O0O00OOO0OO0 ]#line:967
        else :#line:968
            print (f"ERROR: dataset has only {len(O0OOOO0OOOO00O0OO)} variables, required index is {O0O00O0O00OOO0OO0}, but available values are 0-{len(O0OOOO0OOOO00O0OO)-1}.")#line:969
            exit (1 )#line:970
    def get_dataset_variable_index (OOO00000O0OOOO0O0 ,OO0OOO00O0O00O0O0 ):#line:972
        ""#line:978
        if not (OOO00000O0OOOO0O0 ._is_calculated ()):#line:979
            print ("ERROR: Task has not been calculated.")#line:980
            return #line:981
        O00O0000O0OOO0OO0 =OOO00000O0OOOO0O0 .get_dataset_variable_list ()#line:982
        if OO0OOO00O0O00O0O0 in O00O0000O0OOO0OO0 :#line:983
            return O00O0000O0OOO0OO0 .index (OO0OOO00O0O00O0O0 )#line:984
        else :#line:985
            print (f"ERROR: attribute {OO0OOO00O0O00O0O0} is not in dataset. The list of attribute names is  {O00O0000O0OOO0OO0}.")#line:986
            exit (1 )#line:987
    def get_dataset_category_list (O000OO000OOO00O00 ,O0O00OOOOO0O0OO00 ):#line:990
        ""#line:996
        if not (O000OO000OOO00O00 ._is_calculated ()):#line:997
            print ("ERROR: Task has not been calculated.")#line:998
            return #line:999
        OOO0000O0O0O00O0O =O000OO000OOO00O00 .result ["datalabels"]['catnames']#line:1000
        O0OO00OO0O000O0O0 =None #line:1001
        if isinstance (O0O00OOOOO0O0OO00 ,int ):#line:1002
            O0OO00OO0O000O0O0 =O0O00OOOOO0O0OO00 #line:1003
        else :#line:1004
            O0OO00OO0O000O0O0 =O000OO000OOO00O00 .get_dataset_variable_index (O0O00OOOOO0O0OO00 )#line:1005
        if O0OO00OO0O000O0O0 >=0 and O0OO00OO0O000O0O0 <len (OOO0000O0O0O00O0O ):#line:1007
            return OOO0000O0O0O00O0O [O0OO00OO0O000O0O0 ]#line:1008
        else :#line:1009
            print (f"ERROR: dataset has only {len(OOO0000O0O0O00O0O)} variables, required index is {O0OO00OO0O000O0O0}, but available values are 0-{len(OOO0000O0O0O00O0O)-1}.")#line:1010
            exit (1 )#line:1011
    def get_dataset_category_count (O0O0O00000OO0OO0O ,O000OOO00O000O0OO ):#line:1013
        ""#line:1019
        if not (O0O0O00000OO0OO0O ._is_calculated ()):#line:1020
            print ("ERROR: Task has not been calculated.")#line:1021
            return #line:1022
        O00OO0OO00O0O00OO =None #line:1023
        if isinstance (O000OOO00O000O0OO ,int ):#line:1024
            O00OO0OO00O0O00OO =O000OOO00O000O0OO #line:1025
        else :#line:1026
            O00OO0OO00O0O00OO =O0O0O00000OO0OO0O .get_dataset_variable_index (O000OOO00O000O0OO )#line:1027
        OOOO0OO00OOOO0OOO =O0O0O00000OO0OO0O .get_dataset_category_list (O00OO0OO00O0O00OO )#line:1028
        return len (OOOO0OO00OOOO0OOO )#line:1029
    def get_dataset_category_name (O0OOO0O0OOOO00000 ,OO0OO000000OO0OO0 ,O000O0O0O00O0000O ):#line:1032
        ""#line:1039
        if not (O0OOO0O0OOOO00000 ._is_calculated ()):#line:1040
            print ("ERROR: Task has not been calculated.")#line:1041
            return #line:1042
        OOOO00O000OO0OOOO =None #line:1043
        if isinstance (OO0OO000000OO0OO0 ,int ):#line:1044
            OOOO00O000OO0OOOO =OO0OO000000OO0OO0 #line:1045
        else :#line:1046
            OOOO00O000OO0OOOO =O0OOO0O0OOOO00000 .get_dataset_variable_index (OO0OO000000OO0OO0 )#line:1047
        OOO0OOO0O000OOOOO =O0OOO0O0OOOO00000 .get_dataset_category_list (OOOO00O000OO0OOOO )#line:1049
        if O000O0O0O00O0000O >=0 and O000O0O0O00O0000O <len (OOO0OOO0O000OOOOO ):#line:1050
            return OOO0OOO0O000OOOOO [O000O0O0O00O0000O ]#line:1051
        else :#line:1052
            print (f"ERROR: variable has only {len(OOO0OOO0O000OOOOO)} categories, required index is {O000O0O0O00O0000O}, but available values are 0-{len(OOO0OOO0O000OOOOO)-1}.")#line:1053
            exit (1 )#line:1054
    def get_dataset_category_index (O0000O00O0O0O00OO ,O000000OO0O0O000O ,OO0OO0OOO000O0O00 ):#line:1057
        ""#line:1064
        if not (O0000O00O0O0O00OO ._is_calculated ()):#line:1065
            print ("ERROR: Task has not been calculated.")#line:1066
            return #line:1067
        O000OO0OO000OOO0O =None #line:1068
        if isinstance (O000000OO0O0O000O ,int ):#line:1069
            O000OO0OO000OOO0O =O000000OO0O0O000O #line:1070
        else :#line:1071
            O000OO0OO000OOO0O =O0000O00O0O0O00OO .get_dataset_variable_index (O000000OO0O0O000O )#line:1072
        O0O0O0OOO0O0O00O0 =O0000O00O0O0O00OO .get_dataset_category_list (O000OO0OO000OOO0O )#line:1073
        if OO0OO0OOO000O0O00 in O0O0O0OOO0O0O00O0 :#line:1074
            return O0O0O0OOO0O0O00O0 .index (OO0OO0OOO000O0O00 )#line:1075
        else :#line:1076
            print (f"ERROR: value {OO0OO0OOO000O0O00} is invalid for the variable {O0000O00O0O0O00OO.get_dataset_variable_name(O000OO0OO000OOO0O)}. Available category names are {O0O0O0OOO0O0O00O0}.")#line:1077
            exit (1 )#line:1078
