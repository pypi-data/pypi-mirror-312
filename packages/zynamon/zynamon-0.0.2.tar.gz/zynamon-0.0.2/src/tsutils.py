"""
Utility functions for 'TimeSeries' objects.
This module provides various helper functions to be used w/ 'TimeSeries' objects or collections
of them. Besides the required import functions ("CVS reading") and read/write functions for
larger storage files (JSON, HDF5, PK formats), routines for the following tasks are contained:
    + perform regression analysis
    + predict future threshold violations
    + create coherent versions of two arbitrary time-series (i.e. align to common time base)
    + perform sample-wise numerical operations on two arbitrary time-series
    - ...todo...
"""
__version__ = 2.0
__author__ = 'Dr. Marcus Zeller (marcus.zeller@siemens-energy.com)'
__date__ = '2022-2024 @ Erlangen, Germany (Siemens Energy Global GmbH & Co. KG)'

import os
import csv
import json
import h5py
import time
import numpy as np
import pickle as pk

from zynamon.tscore import TimeSeries, ts_convert_time, is_timeseries, TS_SAVE_FORMATS
from zdev.core import fileparts
from zdev.parallel import duration_str
from zdev.validio import text_clear_strings, valid_encoding, valid_str_name


# EXPORTED DATA
TS_KEYWORDS_TIME = ( 'time', 'stamp' )
TS_KEYWORDS_VALUE = ( 'data', 'val', 'value', 'meas', 'measured', 'measurement', 'sample' )
TS_NAME_REPLACE = {
    '>=': 'gte',
    '<=': 'lte',
    '>': 'gt',
    '<': 'lt',
    '°': 'deg'
    }
TS_OPERATIONS = {
    '+': 'added',
    '-': 'subtracted',
    '*': 'muliplied',
    '/': 'divided'
 }

# INTERNAL PARAMETERS & DEFAULTS
# n/a


def ts_infos(collection, time_iso=True, print_summary=True, print_onto=None,
             show_series=True, show_meta=True):
    """ Gathers information on the 'collection' of 'TimeSeries' objects and prints (if desired).

    Args:
        collection (list or dict): Collection of 'TimeSeries' objects (either dict or list) for
            which to gather general information.
        time_iso (bool, optional): Switch to convert [start,end] times for all objects to
            readable string representation (i.e. ISO 8061 string). Defaults to 'True'.
        print_summary (bool, optional): Switch to print found information. Defaults to 'True'.
        print_onto (:obj:, optional): Text-file opened for writing (i.e. active instance of
            '_io.TextIOWrapper'). Defaults to 'None' (i.e. printing on REPL console).
        show_series (bool, optional): Switch to list all individual time-series by name and
            respective length [samples]. Defaults to 'True'.
        show_meta (bool, optional): Switch to indicate if all keys of "meta" information
            present in the time-series data should also be listed. Defaults to 'True'.

    Returns:
        infos (list of 2-tuples): List of (ts_name, ts_length) tuples.
        tags (list): List of all 'tags' strings (i.e. keys).
        totals (2-tuple): Two Tuples containing infos on time extent for whole collection, i.e.
            (i) num_samples     -> minimum & maximum number of samples (across *all* objects)
            (ii) joint interval -> overlapping interval (covered by *all* objects)
    """
    infos = []
    tags = []

    # parse collection (depending on type)
    if (type(collection) is dict):
        for name in collection.keys():
            infos.append([name, len(collection[name]), [collection[name][0].t, collection[name][-1].t]])
            for tag in collection[name].meta.keys():
                if (tag not in tags):
                    tags.append(tag)
    elif (type(collection) is list):
        for ts in collection:
            infos.append([ts.name, len(ts), [ts[0].t, ts[-1].t]])
            for tag in ts.meta.keys():
                if (tag not in tags):
                    tags.append(tag)
    elif (is_timeseries(collection)):
        ts = collection
        infos.append([ts.name, len(ts), [ts[0].t, ts[-1].t]])
        for tag in ts.meta.keys():
            if (tag not in tags):
                tags.append(tag)

    infos.sort(key=lambda x: x[0]) # sort acc. to time-series name

    # derive infos on whole collection
    if (len(infos)):
        get_samples = lambda x: [item[1] for item in x]
        get_start = lambda x: [item[2][0] for item in x]
        get_end = lambda x: [item[2][1] for item in x]
        all_samples = get_samples(infos)
        num_samples = [min(all_samples), max(all_samples)]
        time_start = max(get_start(infos))
        time_end = min(get_end(infos))
        if (time_start > time_end):
            interval = ['!! NOT', 'OVERLAPPING !!']
        else:
            interval = ts_convert_time([time_start, time_end], '%Y-%m-%d %H:%M:%S')
    else:
        num_samples = [0, 0]
        time_start = 0.0
        time_end = 0.0
        interval = ['empty', 'collection']

    # use readable time in infos?
    if (time_iso):
        for item in infos:
            item[2] =  ts_convert_time(item[2], '%Y-%m-%d %H:%M:%S')

    # display summary (either on REPL using 'print' or in file opened for using '.write()')
    if (print_summary):
        if (print_onto is None):
            out = 'print'
            newline = ''
            skipline = 'print("")'
        else:
            out = 'print_onto.write'
            newline = r'print_onto.write("\n")'
            skipline = newline

        if (print_onto is None): # only to structure output on REPL
            print("="*128)

        eval(f'{out}("TOTAL COLLECTION:")'+','+newline)
        eval(f'{out}(f"Number of time-series: {len(infos)}")'+','+newline)
        eval(f'{out}(f"Minimum length: {num_samples[0]:9d} samples")'+','+newline)
        eval(f'{out}(f"Maximum length: {num_samples[1]:9d} samples")'+','+newline)
        eval(f'{out}(f"Joint interval: [ {interval[0]} <=> {interval[1]} ]")'+','+newline)
        eval(skipline)

        if (show_series):
            eval(f'{out}("TIME-SERIES:")'+','+newline)
            eval(f'{out}("Index  Name                                                          # Samples  Duration (interval)        ")'+','+newline)
            eval(f'{out}("-"*128)'+','+newline)
            for n, ts in enumerate(infos):
                eval(f'{out}(f"{n+1: 5}  {ts[0]:60}  {ts[1]: 9}  [ {ts[2][0]} <-> {ts[2][1]} ]")'+','+newline)
            eval(f'{out}("-"*128)'+','+newline)
            eval(skipline)

        if (show_meta):
            eval(f'{out}(f"META INFORMATION:")'+','+newline)
            eval(f'{out}(f"Number of tags: {len(tags)}")'+','+newline)
            eval(f'{out}("Tags/keys:")'+','+newline)
            for key in tags:
                eval(f'{out}(f"  o {key}")'+','+newline)
            eval(skipline)
            eval(f'{out}(f"Note: Not all tags may have been used by all time-series! (i.e. this is the union set)")'+','+newline)
            eval(skipline)

        if (print_onto is None): # only to structure output on REPL
            print("="*128)

    return infos, tags, (num_samples, interval)


def ts_read_file(the_file, target='dict', read_limit=None, verbose=False):
    """ Reads 'TimeSeries' objects collected in 'the_file' and return as desired 'target'.

    This routine works for all supported files acc. to 'TS_SAVE_FORMATS' that have been saved
    e.g. during previous imports from CSV-files. Contained objects may either be placed in a
    list or a dictionary structure. Since 'TimeSeries' objects cannot be used directly (except
    for Python's "pickle", PK), an intermediate step is to convert their information to a 'dict'
    item and then recreate all contained 'TimeSeries' objects in the given 'target' structure
    by this function.

    Args:
        the_file (str): Name of storage file to read from in either format of 'TS_SAVE_FORMATS'.
        target (str, optional): Target structure if several objects have been combined in one
            single file, options are 'list' or dict'. Defaults to 'dict'.
        read_limit (int, optional): Maximum number of objects to read from file. Defaults to
            'None' (i.e. extract all).
        verbose (bool, optional): Switch to show basic infos & time required to load contents.
            Defaults to 'False'.

    Returns:
        collection (list or dict): Collection of all 'TimeSeries' objects found in the file
            w/ type acc. to 'target'. These are created from the all entries in the JSON-file.
    """
    from zynamon.tscore import _ts_from_dict, _ts_from_h5group

    # determine format of storage file & init
    fpath, fbase, fext = fileparts(the_file)
    if (target == 'dict'):
        collection = {}
    elif (target == 'list'):
        collection = []
    else:
        raise ValueError(f"Unknown target structure '{target}' specified")

    if (read_limit is not None):
        limit = read_limit
    else:
        limit = int(1e9)

    # load or re-create 'TimeSeries' objects & arrange collection (dep. on source/target type)
    t0 = time.process_time()
    if (fext == 'pk'):
        with open(the_file, mode='rb') as pf:
            objects = pk.load(pf)

        # single 'TimeSeries' object...
        if (is_timeseries(objects)):
            if (target == 'dict'):
                collection = { objects.name: objects }
            else:
                collection.append(objects)

        # ...or actual collection?
        elif (type(objects) is dict):
            if (target == 'dict'):
                for n, name in enumerate(objects.keys(), start=1):
                    collection[name] = objects[name]
                    if (n == limit):
                        break
            else:
                for n, name in enumerate(objects.keys(), start=1):
                    collection.append(objects[name])
                    if (n == limit):
                        break
        elif (type(objects) is list):
            if (target == 'dict'):
                for n, ts_item in enumerate(objects, start=1):
                    collection[ts_item.name] = ts_item
                    if (n == limit):
                        break
            else:
                collection = objects[:limit]

        else:
            print(f"Error: Unknown contents in '{the_file}'! (aborting)")

    elif (fext == 'json'):
        with open(the_file, mode='r') as jf:
            objects = json.load(jf)

        if (type(objects) is dict):
            # pre-processing (only required for single "export_to_json()" files)...
            tmp = list(objects.keys())
            single_item = all((item in tmp) for item in ('name','arr_t','arr_x','meta','time'))
            if (single_item):
                objects = {objects['name']: objects}
            # assign dict items to target structure
            for n, name in enumerate(objects.keys(), start=1):
                ts = _ts_from_dict(objects[name])
                if (target == 'dict'):
                    collection[name] = ts
                else:
                    collection.append(ts)
                if (n == limit):
                    break

        elif (type(objects) is list):
            for n, ts_item in enumerate(objects, start=1):
                ts = _ts_from_dict(ts_item)
                if (target == 'dict'):
                    collection[ts.name] = ts
                else:
                    collection.append(ts)
                if (n == limit):
                    break

        else:
            print(f"Error: Unknown contents in '{the_file}'! (aborting)")

    elif (fext in ('h5','hdf5')):
        with h5py.File(the_file, mode='r') as hf:
            for n, name in enumerate(hf.keys(), start=1):
                ts = _ts_from_h5group(hf[name])
                if (target == 'dict'):
                    collection[name] = ts
                else:
                    collection.append(ts)
                if (n == limit):
                    break
    else:
        raise NotImplementedError(f"Unknown format '{fext}' found")
    t1 = time.process_time()

    # display basic infos
    if (verbose):
        if (target == 'dict'):
            coll_size = len(collection.keys())
        else:
            coll_size = len(collection)
        print(f"(loaded {coll_size} items in {duration_str(t1-t0)})")

    return collection


def ts_write_file(the_file, collection, overwrite=False, save_fmt='h5', target='dict',
                  verbose=False):
    """ Exports all 'TimeSeries' objects in 'collection' to 'the_file'.

    Args:
        the_file (str): Filename to write to (proper extension will be enforced).
        collection (list or dict): All 'TimeSeries' objects to be written to the file.
        overwrite (bool, optional): Switch to overwrite existing files. Defaults to 'False'.
        save_fmt (str, optional): Output format to write w/ available options as in
            'zynamon.tscore.TS_SAVE_FORMATS'. Defaults to 'h5'.
        target (str, optional): File structure to be used w/ options 'list'|'dict'. Note that
            this setting has *no effect* on HDF5-files, since these always adhere to a dict-like
            structure! Defaults to 'dict'.
        verbose (bool, optional): Switch to show basic infos & time required to write contents.
            Defaults to 'False'.

    Returns:
        --
    """
    from zynamon.tscore import _ts_to_dict, _ts_to_h5group

    # ensure proper extension & check for existence
    fpath, fbase, fext = fileparts(the_file)
    the_file = os.path.join(fpath, fbase+'.'+save_fmt)
    if (os.path.isfile(the_file)):
        if (overwrite):
            print(f"Warning: Overwriting time-series collection '{the_file}'!")
        else:
            raise FileExistsError(f"Time-series collection '{the_file}' exists")

    # init file objects
    if (target == 'dict'):
        objects = {}
    elif (target == 'list'):
        objects = []
    else:
        raise NotImplementedError(f"Unknown target file structure '{target}' specified")

    # arrange collection (acc. to source & target structures) & store to file ("in one go")
    t0 = time.process_time()
    if (save_fmt == 'pk'):
        if (type(collection) is dict):
            if (target == 'dict'):
                objects = collection
            else:
                for name, ts in collection.items():
                    objects.append(ts)
        else: # type(collection) is list
            if (target == 'dict'):
                for ts in collection:
                    objects[ts.name] = ts
            else:
                objects = collection
        with open(the_file, mode='wb') as pf:
            pk.dump(objects, pf)

    elif (save_fmt == 'json'):
        # convert objects to dict items
        if (type(collection) is dict):
            for name, ts in collection.items():
                if (target == 'dict'):
                    objects[name] = _ts_to_dict(ts)
                else:
                    objects.append(_ts_to_dict(ts))
        else: # type(collection) is list
            for ts in collection:
                if (target == 'dict'):
                    objects[ts.name] = _ts_to_dict(ts)
                else:
                    objects.append(_ts_to_dict(ts))
        with open(the_file, mode='w') as jf:
            if (target == 'dict'):
                json.dump(objects, jf, indent=4, sort_keys=True)
            else:
                json.dump(objects, jf, indent=4)

    elif (save_fmt in ('h5','hdf5')):
        if (type(collection) is dict):
            for name, ts in collection.items():
                if (target == 'dict'):
                    objects[name] = _ts_to_dict(ts)
                else:
                    objects.append(_ts_to_dict(ts))
        else: # type(collection) is list
            for ts in collection:
                objects[ts.name] = _ts_to_dict(ts)
        with h5py.File(the_file, mode='w') as hf:
            for (k, ts_item) in objects.items():
                _ts_to_h5group(hf, ts_item)

    else:
        raise NotImplementedError(f"Unknown save format '{save_fmt}' specified")
    t1 = time.process_time()

    # display basic infos
    if (verbose):
        if (type(collection) == 'dict'):
            coll_size = len(collection.keys())
        else:
            coll_size = len(collection)
        print(f"(saved {coll_size} items in {duration_str(t1-t0)})")

    return


def ts_import_csv(csv_file, col_time=None, col_data=None, col_meta=None,
                  headers=None, encoding=None, enforce=None, new_name=None,
                  keep_meta=True, ensure_causal=True, save_file=True, save_fmt='json',
                  max_ts=99, max_lines=1e9, verbose=0):
    """ Import samples of one (or more) time-series from a CSV-file w/ a common time reference.

    The files are assumed to contain samples from one (or more) time-series in a "line-by-line"
    manner, i.e. each line contains ONE NEW SAMPLE of the SAME COMMON TIME REFERENCE. This
    sequence of samples is defined by a common time reference and at least one more column
    carrying some time-series values. However, multiple different measurement points (up to
    'max_ts') may be contained in the file in separate columns and will be imported altogether.
    For efficient processing, all samples of the same series are collected first in a buffered
    manner before finally adding them in a single batch.

    If desired, any other columns are considered as "meta" information and may be kept as well.
    Since these are assumed to have repeating contents, a compression of the resulting
    'TimeSeries' object is likely, as these tags are extracted acc. to the first line of
    occurrence and will be stored only once (per time-series).

    For all of the columns, information on the contents of the CSV-file may also be detected
    *automagically* based on a keyword approach. In total, the operational precedence is as
    follows:
        1. map 'time' reference (as specified / auto-detect otherwise)
        2a. map 'data' columns (as specified)
        2b. map 'meta' columns (as specified)
        3. map any remaining columns by auto-detection

    Notes an the "auto-detection" feature:
        (i) 'time' will only consider the 1st matching column!
        (ii) 'data' may also map limit values (e.g. 'max_val')
              --> use explicit 'meta' configurations to avoid this!

    Args:
        csv_file (str): Absolute filename to "CSV-like" file (w/ or w/o headers).
        col_time (str, optional): Header of column containing the time reference. Defaults to
            'None' (i.e. auto-detect).
        col_data (list of str, optional): Header of one or more columns containing data.
            Defaults to 'None' (i.e. auto-detect).
        col_meta (list of str, optional): Header of one or more columns containing meta data.
            Defaults to 'None' (i.e. after auto-detection any remaining columns will be mapped).
            Note: Use 'xtools' as SPECIAL CASE to indicate that first two lines in CSV-files
            carry additional meta information and have to be treated separately!
        headers (list, optional): Headers of all columns if not in the file. Defaults to 'None'.
        encoding (str, optional): Encoding of CSV-file. Defaults to 'None' (i.e. auto mode).
        enforce (list, optional): Enforce conversions while extracting data. If the types in the
            CSV-source are known, this may be particularly required for 'datetime' formats. If
            multiple time-series are contained, each one requires an "enforce" item of its own.
            Defaults to 'None' (i.e. plain data is copied).
        new_name (str, optional): Joint label for all data found in the file. Defaults to 'None'
            (i.e. basename of CSV-file will be used).
        keep_meta (bool, optional: Switch for storing the meta information in the 'TimeSeries',
            otherwise it will be discarded. Defaults to 'None'.
        ensure_causal (bool, optional): Switch for ensuring that all samples of a time-series
            are sorted in ascending time and computing some statistics. Defaults to 'True'.
        save_file (bool, optional): Switch to save all imported 'TimeSeries' to file. Otherwise,
            conversion results will only be available in memory. Defaults to 'True'.
        save_fmt (str, optional): File format in which converted data is saved (options
            'json' and 'pk'). Defaults to 'json'.
        max_ts (int, optional): Maximum number of time-series to consider. Defaults to '99'.
        max_lines (int, optional): Maximum number of lines to scan for. Defaults to '1e9'.
        verbose (int, optional): Verbosity level of function. Defaults to '0' (= silent).
            Level 1 -> shows only a short summary (at the end)
            Level 2 -> shows a detailed summary (at the end)
            Level 3 -> generates a "heartbeat" (after each 50000 lines)

    Returns:
        objects (list): List of all 'TimeSeries' objects imported from the CSV-file.

    Example:
        SIGNAL_NAME,    SIGNAL_DESCRIPTION,   SIG_CLASS, UNIT, VALUE, TIME_STAMP
        =10/Idc_SPR,    SPR Current-DC,       MES,       A,    0.010, 2020-04-16 20:59:42.5
        =10/Idc_SPR,    SPR Current-DC,       MES,       A,    0.017, 2020-04-16 20:59:45.5
        ...
        =10/Idc_SPR,    SPR Current-DC,       MES,       A,    0.038, 2020-04-18 13:48:07.2

        --> Optimise output by 'meta=['SIGNAL_NAME','SIGNAL_DESCRIPTION','SIG_CLASS','UNIT']',
            such that these information will only be stored once!
    """

    # configure file
    fpath, fname, fext = fileparts(csv_file)
    text_clear_strings(csv_file, '"', verbose=False) # Note: This will remove unnessary quotes
    if (encoding is None):
        enc = valid_encoding(csv_file)
    else:
        enc = encoding
    if (new_name is None):
        basename = fname
    else:
        basename = new_name

    # check consistency
    if (col_time is not None):
        if (type(col_time) != str):
            print(f"(warning: unknown time column format '{col_time}' specified, setting to auto)")
            col_time = None
    if ((col_data is None) and (col_meta is None)):
        print("(warning: meta data cannot be differentiated, may be mapped to time-series?)")
    if (save_fmt not in TS_SAVE_FORMATS):
        raise NotImplementedError(f"Unknown save format '{save_fmt}' specified")

    # read CSV-file in proper encoding
    with open(csv_file, mode='r', encoding=enc) as tf:

        # init format parsing (Note: First line will always be checked)
        meta_info = {}
        meta_is_init = False
        first_line = tf.readline()
        tf_format = csv.Sniffer().sniff( first_line )

        # parse format & columns configuration
        if (col_meta == 'xtools'): # SPECIAL case
            # Note: Special case for "CMS X-Tools" file exports, as these carry additional
            # "meta information" already in their first two lines. Hence, the column format will
            # be changing afterwards, i.e. starting with the third line.

            # get meta info from first two lines
            second_line = tf.readline()
            if (keep_meta):
                k_meta = first_line.split(tf_format.delimiter)
                v_meta = second_line.split(tf_format.delimiter)
                for n, key in enumerate(k_meta):
                    k_meta[n] = key.strip() # clean whitespaces (incl. newline)
                    meta_info.update({k_meta[n]: v_meta[n].strip()})
            meta_is_init = True

            # get regular time reference & data column(s) from third line
            third_line = tf.readline()
            fields = third_line.split( tf_format.delimiter )
            for n, item in enumerate(fields):
                fields[n] = item.strip() # clean whitespaces (incl. newline)
            k_time = fields[0] # 1st column = time reference (assigned directly)
            k_data = []
            for n, item in enumerate(fields[1:], start=1):
                k_data.append( fields[n] ) # later columns = values (also works for several!)

        else: # NORMAL case
            # Note: For the "normal" case, the column headers are parsed and the mapping as
            # specified is done OR an auto-detection (based on typical keywords) is carried out.

            if (headers is None):
                fields = first_line.split( tf_format.delimiter )
                for n, item in enumerate(fields):
                    fields[n] = item.strip() # clean whitespaces (incl. newline)
            else:
                fields = headers
                tf.seek(0)

            # (1) get time reference (as specified or via auto-detection)
            k_time = ''
            if (col_time is not None):
                k_time = col_time
            else:
                for item in fields:
                    if (item.lower().endswith(TS_KEYWORDS_TIME)):
                        k_time = item
                        break

            # (2a) get data columns (as specified)
            k_data = []
            if (col_data is not None):
                if (type(col_data) == str):
                    k_data.append(col_data)
                else: # list of columns
                    for item in col_data:
                        k_data.append(item)

            # (2b) get meta columns (as specified)
            k_meta = []
            if (col_meta is not None):
                if (type(col_meta) == str):
                    k_meta.append(col_meta)
                else: # list of columns
                    for item in col_meta:
                        k_meta.append(item)

            # (3) auto-detection: map all remaining columns based on keywords (if not specified)
            for item in fields:
                # -> data was specified, map any other to meta
                if ((col_data is not None) and (col_meta is None)):
                    if (item not in (k_data+[k_time])):
                        k_meta.append(item)
                # -> meta was specified, map any other to data
                elif ((col_data is None) and (col_meta is not None)):
                    if (item not in (k_meta+[k_time])):
                        k_data.append(item)
                # -> neither data nor meta were specified, map matching to data, rest to meta
                elif ((col_data is None) and (col_meta is None)):
                    if (item.lower().endswith(TS_KEYWORDS_VALUE)):
                        k_data.append(item)
                    elif (item not in (k_data+[k_time])):
                        k_meta.append(item)

            # init extraction of meta information (if desired)
            if (keep_meta):
                for item in k_meta:
                    meta_info.update({item: ''})
                meta_is_init = False
            else:
                meta_is_init = True

        # check limitations
        if (len(k_data) > max_ts):
            print(f"(warning: found max # of time-series (={max_ts}) -> ignoring rest)")
            k_data[max_ts:] = []

        # init time-series collection
        buffers = []
        objects = []
        for n, item in enumerate(k_data):
            if (col_meta == 'xtools'):
                ts_name = meta_info['Data Name']+'_'+item
            else:
                ts_name = basename+'_'+item
            buffers.append([])
            objects.append( TimeSeries(ts_name, tags=meta_info) )

        # line-wise processing
        stream = csv.DictReader(tf, fieldnames=fields, dialect=tf_format)
        m = 0
        while (True):
            try: # Note: Safe approach in case NULL is found in files!
                m += 1
                line = stream.__next__()
                if (m == max_lines):
                    print(f"(warning: reached max # of lines (={int(max_lines)}) -> skipping)")
                    break
                elif ((verbose >= 3) and (not m%50000)):
                    print(f"(read {m} lines)")

                # extract meta information (only for first line!)
                if (not meta_is_init):
                    for n, item in enumerate(k_data):
                        for key in objects[n].meta.keys():
                            objects[n].tags_register({key: line[key]}, overwrite=True)
                    meta_is_init = True

                # copy time-series data
                for n, item in enumerate(k_data):
                    if (enforce is None): # use plain data...
                        sample = [line[k_time], line[item]]
                    else: # ... or enforce type conversion
                        # time
                        if (enforce[0] is not None):
                            the_time = ts_convert_time(line[k_time], target=enforce[0])
                        else:
                            the_time = line[k_time]
                        # data
                        if (len(enforce) > 1+n): # 1st entry == always time!
                            if (enforce[1+n] is float):
                                try:
                                    the_data = float(line[item])
                                except:
                                    the_data = 0.0
                            elif (enforce[1+n] is int):
                                try:
                                    the_data = int(line[item])
                                except:
                                    the_data = 0
                            elif (enforce[1+n] is str):
                                try:
                                    the_data = str(line[item])
                                except:
                                    the_data = ''
                        else:
                            the_data = line[item]
                        sample = [the_time, the_data]
                    buffers[n].append(sample)

            except: # reached EOF or NUll
                break

    # add batch of samples to time-series & ensure causality (if desired)
    for n, ts in enumerate(objects):
        ts.samples_add(buffers[n], analyse=(not ensure_causal))
        if (ensure_causal):
            ts.time_causalise()
            ts.time_analyse()

    # save time-series to file(s)
    if (save_file):
        the_file = os.path.abspath(os.path.join(fpath,basename+'.'+save_fmt))
        if (os.path.isfile(the_file)):
            os.remove(the_file)
        for ts in objects:
            ts.export_to_file(the_file, combine=True, fmt=save_fmt)

    # display summary
    if (verbose):
        print(f"(registered {len(objects)} individual time-series:)")
        if (verbose >= 2):
            for ts in objects:
                print(f"( - '{ts.name}' w/ {len(ts)} samples )")
        if (save_file):
            print(f"(stored all data in '{basename}.{save_fmt}')")

    return objects


def ts_import_csv_mixed(csv_file, col_name, col_time, col_data,
                        headers=None, encoding=None, enforce=None, new_name=None,
                        keep_meta=True, ensure_causal=True, save_file=True, save_fmt='json',
                        max_ts=1e5, max_lines=1e9, verbose=0):
    """ Imports a "mixed sequence" of time-series data samples from a CSV-file.

    The files are assumed to contain samples from many different time-series that are generated
    in an asynchronous manner such that NO COMMON TIME REFERENCE is available. In particular,
    EACH LINE CONTAINS ONE NEW SAMPLE OF A (NEW or EXISTING) TIME-SERIES, THAT IS RELATED TO A
    SPECIFIC TIME INSTANT / EVENT. For efficient processing, all samples of the same series are
    collected first in a buffered manner before finally adding them in a single batch.

    In order to determine the structure of the file, the first line is expected to contain the
    required column headers. Otherwise, 'headers' needs to provide the respective fields and the
    1st line in the file is then assumed to start w/ data.

    Each time-series is defined by information from the following columns:
        (1) col_name = unique name of time-series (may also be created from several parts)
        (2) col_time = time information of time-series
        (3) col_data = sample values of time-series
    Any other columns not covered by the above will be considered as "meta" information, but may
    be kept as well. Since these information are assumed to have repeating contents, the
    resulting 'TimeSeries' data structures will exhibit a significant compression in size, since
    these tags are extracted acc. to the first line of occurrence and will be stored only once
    (per time-series).

    Args:
        csv_file (str): Absolute filename to "CSV-like" file (w/ headers in first line).
        col_name (str or list): Column referring to the time-series names. If several columns
            are required to create unique identifiers, this is expected to be a list (of str)
            and the name parts will be concatenated by '_'.
        col_time (str): Column containing times of time-series (e.g. 'meas_time').
        col_data (str): Column containing the samples values of time-series (e.g. 'value').
        headers (list, optional): Headers of all columns if not in the file. Defaults to 'None'.
        encoding (str, optional): Encoding of CSV-file. Defaults to 'None' (i.e. auto mode).
        enforce (list, optional): 2-tuple specifying conversions that should be enforced on
            'time' and 'data' entries. Defaults to 'None' (i.e. plain data is copied).
        new_name (str, optional): Joint label for all data found in the file. Defaults to 'None'
            (i.e. basename of CSV-file will be used).
        keep_meta (bool, optional): Switch for storing all "static" meta information only once.
            Defaults to 'True'.
        ensure_causal (bool, optional): Switch for ensuring that all samples of a time-series
            are sorted in ascending time and computing some statistics. Defaults to 'True'.
        save_file (bool, optional): Switch to save all imported 'TimeSeries' to file. Otherwise,
            conversion results will only be available in memory. Defaults to 'True'.
        save_fmt (str, optional): File format in which converted data is saved w/ options
            'TS_SAVE_FORMATS'. Defaults to 'json'.
        max_ts (int, optional): Maximum number of time-series to consider. Defaults to '1e5'.
        max_lines (int, optional): Maximum number of lines to scan for. Defaults to '1e9'.
        verbose (int, optional): Verbosity level of function. Defaults to '0' (= silent).
            Level 1 -> shows only a short summary (at the end)
            Level 2 -> shows a detailed summary (at the end)
            Level 3 -> generates a "heartbeat" (after each 50000 lines)
            Level 4 -> generates infos on each NEW time-series that is found
            Note: Level 4 may produce *many* lines, depending on the contents of the file!

    Returns:
        objects (list): List of all 'TimeSeries' ojects imported from the CSV-file.

    Example:
        SIGNAL_NAME,      SIGNAL_DESCRIPTION,   SIG_CLASS, UNIT, VALUE, INSERT_TIME
        =10QA12/CB_STAT,  Stat 1 CB open/close, STAT,      NULL, 0,     2020-04-16 20:59:42.5
        =My_own_signal,   Anything else,        MES,       NULL, 14.75, 2020-04-16 21:02:19.2
        ...
        =21UF44/PAC_EST,  Not enough AC power!, WARN,      NULL, 1,     2020-05-03 08:40:17.3
        ...
        =My_own_signal,   Anything else,        MES,       NULL, 12.33, 2020-06-07 09:48:08.6
    """

    # configure file & check consistency
    fpath, fname, fext = fileparts(csv_file)
    text_clear_strings(csv_file, '"', verbose=False) # Note: This will remove unnessary quotes
    if (encoding is None):
        enc = valid_encoding(csv_file)
    else:
        enc = encoding
    if (new_name is None):
        basename = fname
    else:
        basename = new_name
    if (save_fmt not in TS_SAVE_FORMATS):
        raise NotImplementedError(f"Unknown save format '{save_fmt}' specified")

    # read CSV-file in proper encoding
    with open(csv_file, mode='r', encoding=enc) as tf:

        # parse format & configuration
        first_line = tf.readline()
        tf_format = csv.Sniffer().sniff(first_line)
        if (headers is None):
            fields = first_line.split(tf_format.delimiter)
            for n, item in enumerate(fields):
                fields[n] = item.strip() # clean whitespaces (incl. newline)
        else:
            fields = headers
            tf.seek(0)

        # check consistency (proper columns available?)
        if (type(col_name) is list):
            name_combo = True
            for name_part in col_name:
                if (name_part not in fields):
                    raise ValueError(f"Column '{name_part}' for labels not found")
        else:
            name_combo = False
            if (col_name not in fields):
                raise ValueError(f"Column '{col_name}' for labels not found")
        if (col_data not in fields):
            raise ValueError(f"Column '{col_data}' for time-series values not found")
        if (col_time not in fields):
            raise ValueError(f"Column '{col_time}' for time-series time-stamps not found!")

        # get columns of meta information (if desired)
        k_meta = []
        if (keep_meta):
            for item in fields:
                if (item not in (col_name, col_data, col_time)):
                    k_meta.append(item)

        # init time-series collection
        buffers = {}
        objects = []

        # copy data of all time-series from file...
        stream = csv.DictReader(tf, fieldnames=fields, dialect=tf_format)
        m = 0
        while (True):
            try:
                m += 1
                line = stream.__next__() # Note: Safe approach in case NULL is found in files!
                if (m >= max_lines):
                    print(f"(warning: reached max # of lines (={int(max_lines)}) -> skipping)")
                    break
                elif ((verbose >= 3) and (not m%50000)):
                    print(f"(read {m} lines)")

                # get/create time-series name & ensure "safe" usage (i.e. remove special chars)
                if (name_combo):
                    tmp = ''
                    for name_part in col_name:
                        tmp += line[name_part]+'_'
                    ts_name = tmp[:-1]
                else:
                    ts_name = line[col_name]
                ts_name = valid_str_name(ts_name, repl_str='_', repl_dict=TS_NAME_REPLACE)

                # create new time-series & buffer?
                if (ts_name not in buffers.keys()):
                    if (len(objects) >= max_ts):
                        print(f"(warning: found max # of time-series (={int(max_ts)}) -> ignoring rest)")
                        continue
                    elif (verbose >= 4):
                        print(f"(line #{m}: found time-series '{ts_name}')")
                    ts = TimeSeries(ts_name)
                    if (keep_meta):
                        meta_info = {}
                        for item in k_meta:
                            meta_info.update({item: line[item]})
                        ts.tags_register(meta_info)
                    buffers[ts_name] = []
                    objects.append(ts)

                # add sample to proper buffer
                if (enforce is None): # use plain data...
                    sample = [line[col_time], line[col_data]]
                else: # ... or enforce type conversion
                    # time
                    if (enforce[0] is not None):
                        the_time = ts_convert_time(line[col_time], enforce[0])
                    else:
                        the_time = line[col_time]
                    # data
                    if (enforce[1] is float):
                        try:
                            the_data = float(line[col_data])
                        except:
                            the_data = 0.0
                    elif (enforce[1] is int):
                        try:
                            the_data = int(line[col_data])
                        except:
                            the_data = 0
                    elif (enforce[1] is str):
                        try:
                            the_data = str(line[col_data])
                        except:
                            the_data = ''
                    else:
                        the_data = line[col_data]
                    sample = [the_time, the_data]
                buffers[ts_name].append(sample)

            except: # reached EOF or NUll
                break

    # add batch of samples to time-series & ensure causality (if desired)
    for ts in objects:
        ts.samples_add(buffers[ts.name], analyse=(not ensure_causal))
        if (ensure_causal):
            ts.time_causalise()
            ts.time_analyse()

    # save imported time-series to file?
    if (save_file):
        the_file = os.path.join(fpath,basename+'.'+save_fmt)
        if (os.path.isfile(the_file)):
            os.remove(the_file)
        for ts in objects:
            ts.export_to_file(the_file, combine=True, fmt=save_fmt)

    # display summary
    if (verbose):
        print(f"(registered {len(objects)} individual time-series)")
        if (verbose >= 2):
            for ts in objects:
                print(f"( - '{ts.name}' w/ {len(ts)} samples )")
        if (save_file):
            print(f"(stored all data in '{basename}.{save_fmt}')")

    return objects


def ts_get_by_name(collection, name):
    """ Returns 'TimeSeries' object from 'collection' whose name matches 'name'.

    Note: This is a convenience function to manage list or dict collections in the same way!

    Args:
        collection (dict or list): Collection of 'TimeSeries' objects as either 'dict'|'list'.
        name (str): Name of object that shall be found.

    Returns:
        ts (:obj:): TimeSeries object as retrieved from 'collection'.
    """
    ts = None
    if (type(collection) is dict):
        if (name in collection.keys()):
            ts = collection[name]
    elif (type(collection) is list):
        idx = ts_get_list_index(collection, name)
        if (idx is not None):
            ts = collection[idx]
    else:
        raise NotImplementedError(f"Unknown type '{type(collection)}' for collection")
    return ts


def ts_get_list_index(collection, name):
    """ Returns index of 'TimeSeries' object in list 'collection' w/ matching 'name'.

    Args:
        collection (list): Collection list of 'TimeSeries' objects.
        name (str): Name of object that shall be found.

    Returns:
        idx (int): Index of list object matching 'name'.
    """
    idx = next((n for n, ts in enumerate(collection) if (ts.name == name)), None)
    return idx


def ts_find_in_history(ts, operation):
    """ Checks whether 'operation' has been applied in the past of 'ts' and returns entries.

    Note that not all time-series operations are stored to the history, but only the ones
    "actually modifying". For more info on the individual operations see "zynamon.tscore".

    Args:
        ts (:obj:): TimeSeries object to investigate.
        operation (str): Operation to be checked for in the history. Available options:
            'samples_'  +   'add'| 'crop' | 'pack' | 'unique'
            'time_'     +   'align' | 'causalise' | 'convert' | 'reset'
            'values_'   +   'filter' | 'purge' | 'set'
            'tags_'     +   'register' | 'delete'

    Returns:
        res (bool): Confirmation if 'operation' had been applied in the past.
        idx (list): List containing the indices of all matching operations (if any, else []).
    """
    chk = []
    for n, item in enumerate(ts.history):
        if (item[0] == f'@{operation}'):
            chk.append((n, item[1]))
    return any(chk), chk


# #TODO: Use the following as easy-to-read abbreviations for common operations?!?!?

# def is_filtered(ts):
#     return ts_find_in_history(ts, 'values_filter')[0]

# def is_modified(ts):
#     return (ts_find_in_history(ts, 'values_filter')[0]
#             or ts_find_in_history(ts, 'values_pugre')[0]
#             or ts_find_in_history(ts, 'values_set')[0])

# def is_time_altered(ts):
#     return (ts_find_in_history(ts, 'time_align')[0]
#             or ts_find_in_history(ts, 'time_causalise')[0])

# # def ts_has_string_data(ts):
# #     return ts.is_type_x(str, check_array=True)


def ts_list_segments(ts, seg_def):
    """ Creates a list of consistent 'segments' for block-wise processing functions.

    This is a robust convenience function, ensuring that all segments based on 'seg_def' are
    wrapped in a valid list for consumption by 'TimeSeries.samples_crop()'. Hence, it will
    typically be used to prepare calculations operating on several different blocks of time.
    Segments can be defined in any format supported by 'tscore.ts_timespec()' as follows:
        scalar              -> single limit, i.e. interval "from the end"
        2-tuple             -> interval limits [A,B] within the time-series
        list of segments    -> list of limits (i.e. scalars / intervals may be mixed)

    Args:
        ts (:obj:): TimeSeries object from which segments are to be used.
        seg_def (various): Definition of segments to be extracted from 'ts'.

    Returns:
        seg_list (list): Consistent list of segments (for cropping).

    Examples: Segment definition vs. final interpretation by 'TimeSeries.samples_crop()'
              (Note: First two cases employ "direct indexing"!)

        'seg_def':                                  | Resolved intervals:
        ---------------------------------------------------------------------------------------
        1000                                        | [*now*-1000, *now*]
        [200, 300, 500]                             | [*now*-200,*now*], [*now*-300,*now*],
                                                      [*now*-500,*now*]
        ['2022-04-07 12:10','2022-04-07 12:30']     | ['2022-04-07 12:10', *now*],
                                                      ['2022-04-07 12:30', *now*]
        [['2022-04-07 12:10','2022-04-07 12:30']]   | ['2022-04-07 12:10', '2022-04-07 12:30']
        [datetime.datetime(2022, 4, 7, 12, 21, 24), | ['2022-04-07 12:21:24', *now*],
         ['2022-04-07 12:10', 1649334600.0]]          ['2022-04-07 12:10','2022-04-07 12:30']
        ----------------------------------------------------------------------------------------
    """
    from zynamon.tscore import _TIME_TYPE

    # (single) scalar limit
    if (type(seg_def) not in (list,tuple)):
        if (type(seg_def) not in _TIME_TYPE.keys()):
            raise ValueError("Wrong definition of scalar limit! {seg_def}")
        else:
            seg_list = [seg_def]

    # (single) interval limit
    elif ((len(seg_def) == 2) and
          (type(seg_def[0]) not in (list,tuple)) and (type(seg_def[1]) not in (list,tuple))):
        if ((type(seg_def[0]) not in _TIME_TYPE.keys()) or (type(seg_def[1]) not in _TIME_TYPE.keys())):
            raise ValueError(f"Wrong definition of interval limits! {seg_def}")
        else:
            seg_list = seg_def

    # list of scalar or interval limits (Note: Entries may be mixed!)
    else:
        for s, seg in enumerate(seg_def):
            if (type(seg) not in (list,tuple)):
                if (type(seg) not in _TIME_TYPE.keys()):
                    raise ValueError("Wrong definition of segments!")
            elif (len(seg) != 2):
                raise ValueError(f"Wrong definition of segments! {seg}")
            elif ((type(seg[0]) not in _TIME_TYPE.keys()) or (type(seg[1]) not in _TIME_TYPE.keys())):
                raise ValueError(f"Wrong definition of segments! {seg}")
        seg_list = seg_def

    return seg_list


def ts_calc_regression(ts, segments=None, accuracy=False, orig_spec=True, model='linear'):
    """ Estimates a regression 'model' for 'ts' based on the samples in the 'segments'.

    In the simplest case, the best parameters for the linear model "y = b1*x+ b0" for any given
    segment are computed acc. to [ https://de.wikipedia.org/wiki/Lineare_Einfachregression ]

                SUM_i=0^i=N-1  (x_i - x_avg) * (y_i - y_avg)
        b1  =  ----------------------------------------------
                SUM_i=0^i=N-1  (x_i - x_avg)**2

        b0  =  y_avg - b1 * x_avg

    Note: The center of these piecewise-linear curves is located at the origin (0,0), whereas
    timestamps are based on "Linux epoch", i.e. '1970-01-01 00:00:00'. Thus, the shift
    parameters (b0) are often numerically quite large so as to "reach" the values in typical
    today's time ranges (i.e. years of 2020+).

    Args:
        ts (:obj:): 'TimeSeries' object for which to perform regression analysis.
        segments (various, optional): Definition of intervals of 'ts' which should be analysed.
            See 'ts_list_segments()' for details. Defaults to 'None' (i.e. full range is used).
        accuracy (bool, optional): Switch to key 'accuracy' to 'section' to provide measures
            (MAE, MSE) to judge the estimation quality. Defaults to 'False'.
        orig_spec (bool, optional): Switch to enforce same "timespec" for the time instants in
            key 'points' of 'sections' as in object 'ts'. Defaults to 'True'.
        model (str, optional): Estimation model. Defaults to 'linear'.

    Returns:
        sections (list of dict): List of dicts for all sections acc. to regression analysis.
            The number of entries corresponds to the defined 'segments' whereas the number of
            parameters depends on the used 'model'. Each dict item is given by:
                {
                    'params':   [b1,b0],            # if model = 'linear'
                    'points':   [[xA,xB],[yA,yB]],  # point coordinates (start "A" / end "B")
                    'accuracy': { 'MAE': <float>,   # MAE = mean absolute error
                                  'MSE': <float> }  # MSE = mean squared error
                }
            Note: The 'points' can be used for a simple comparative plotting!
    """

    # gather all segments
    if (segments is None): # default mode (use whole signal)
        segments_list = [ [0, len(ts)], ]
    else:
        segments_list = ts_list_segments(ts, segments)

    # linear regression analysis
    sections = []
    for s, seg in enumerate(segments_list):
        sec_item = { 'params': [], 'points': [], 'accuracy': {'MAE': 0.0, 'MSE': 0.0} }

        # get respective frame of data
        ts_seg = ts.samples_crop(seg, inplace=False)
        ts_seg.time_convert('stamp') # Note: Ensure "usable" format

        if (model == 'linear'):

            # compute mean values
            t_avg = ts_seg.df.t.mean()
            x_avg = ts_seg.df.x.mean()

            # compute parameters (i.e. slope (b1) & shift (b0))
            num, den = 0.0, 0.0
            for n in range(len(ts_seg)):
                num += (ts_seg[n].t - t_avg) * (ts_seg[n].x - x_avg)
                den += (ts_seg[n].t - t_avg)**2

            b1 = num / den
            b0 = x_avg - (b1*t_avg)
            sec_item['params'] = [b1,b0]

            # compute start/end points
            yA = b1*ts_seg[0].t + b0
            yB = b1*ts_seg[-1].t + b0
            if (orig_spec):
                t_range = ts_convert_time([ts_seg[0].t, ts_seg[-1].t], ts.get_timespec_str())
            else:
                t_range = [ts_seg[0].t, ts_seg[-1].t]
            sec_item['points'] = [t_range, [yA,yB]]

            # compute accuracy measures?
            if (accuracy):
                tmp_ae, tmp_se = 0.0, 0.0
                for n in range(len(ts_seg)):
                    error = (b1*ts_seg[n].t + b0) - ts_seg[n].x
                    tmp_ae += abs(error)
                    tmp_se += error**2
                sec_item['accuracy']['MAE'] = tmp_ae/len(ts_seg)
                sec_item['accuracy']['MSE'] = tmp_se/len(ts_seg)
            else:
                sec_item['accuracy'] = None

        else:
            raise NotImplementedError(f"Unknown regression '{model}' specified")
            # TODO: have more sophisticated regressions?

        sections.append( sec_item )

    return sections


def ts_predict(ts, thresholds, segments=None, warn_readable=False):
    """ Predicts future violation of 'ts' against 'thresholds' (for all desired 'segments').

    This function uses a linear regression model on the TimeSeries 'ts' in order to compare the
    trending against one or more 'thresholds'. As result, estimates for the remaining times
    (durations) until thresholds are exceeded are provided.

    Args:
        ts (:obj:): 'TimeSeries' object for which predition is to be performed.
        thresholds (list): List of thresholds against which violation is to be compared.
        segments (various, optional): Definition of intervals of 'ts' which should be analysed.
            See 'ts_list_segments()' for details. Defaults to 'None' (i.e. full range is used).
        warn_readable (bool, optional): Switch to use an easy-to-read string representation for
            the pre-warning time. Defaults to 'False' (i.e. float in [s]).

    Returns:
        pre_warn (list): "Pre-warning" time defined as minimum (= most critical!) distance of
            upcoming violation (per threshold) for the various segments.
        ttt (list): Predicted "time-to-threshold" as seen from most recent sample of 'ts'.
            The number of entries corresponds to 'len(sections) x len(thresholds)'.
    """

    # init
    ttt = []
    pre_warn = []
    time_base = ts_convert_time([ts[0].t, ts[-1].t], 'stamp')

    # compute linear regression model
    sections = ts_calc_regression(ts, segments, model='linear')

    # check all sections
    for s, sec in enumerate(sections):
        ttt.append([])

        # compute time of & distance to all thresholds (from last sample)
        for t, th in enumerate(thresholds):
            time_thresh = (th - sec['params'][1]) / sec['params'][0]
            time_dist = time_thresh - time_base[1]
            ttt[s].append(time_dist)
            if (time_dist < 0):
                raise RuntimeError(f"Estimated distance is *NOT* in future! ({time_dist})")

    # determine "pre-warning" time (i.e. minimum distance over all considered sections)
    for t in range(len(thresholds)):
        dist_min = 1e9
        for s in range(len(sections)):
            dist_min = min([dist_min, ttt[s][t]]) # compared w.r.t. unit [s]
        if (warn_readable):
            pre_warn.append(duration_str(dist_min, max_unit='days'))
        else:
            pre_warn.append(dist_min)

    return pre_warn, ttt


def ts_cohere(ts1, ts2, res=None, mode='avg'):
    """ Cohere 'ts1' and 'ts2', i.e. determine & pack to a common time basis.

    This function brings two different time-series to a common, equidistant time reference. As
    such, it is used as an inherent pre-processing step for most arithmetic operations, since
    arbitrary time-series may generally exhibit different time-scales and/or gaps of samples.

    Args:
        ts1 (:obj:): First time-series.
        ts2 (:obj:): Second time-series.
        res (float, optional): Desired common resolution (if any). Note that this will only be
            applied if the sampling intervals of both 'ts1' and 'ts2' are below that value.
            Otherwise the (integer) maximum of the sampling intervals is used as resolution
            which is also the default setting (for 'None').
        mode (str, optional): Desired aggregation mode for the time-series w/ options 'avg'|
            'max'|'min'|'median' (see 'zynamon.tscore.samples_pack' for details). Defaults to
            'avg'.

    Returns:
        ts1_coherent (:obj:): Packed version of 'ts1' w/ time reference matching 'ts2_coherent'.
        ts2_coherent (:obj:): Packed version of 'ts2' w/ time reference matching 'ts1_coherent'.
    """

    # determine common ("coherent") sampling basis
    if ((res is not None) and ((res >= ts1.time['Ts']) and (res >= ts2.time['Ts']))):
        Ts_max = None
        Ts_res = res
    else: # (res is None)
        ts1.time_analyse()
        ts2.time_analyse()
        Ts_max = max(ts1.time.Ts, ts2.time.Ts)
        Ts_res = int(Ts_max)+1 # round to next integer [s]

    # check if already coherent w/ desired rate (if specified)
    if ((ts1.time.stat['quality'] == ts2.time.stat['quality'] == 'equidistant') and
        ((res is not None) and (ts1.time['Ts'] == ts2.time['Ts'] == res))):
        ts1_coherent = ts1.clone()
        ts2_coherent = ts2.clone()
    else:
        # pack / resample time-series
        ts1_coherent = ts1.samples_pack(Ts_res, mode, inplace=False)
        ts2_coherent = ts2.samples_pack(Ts_res, mode, inplace=False)

    return ts1_coherent, ts2_coherent


def ts_relate(ts1, ts2, op, res=None, mode='avg'):
    """ Apply sample-wise 'operation' (e.g. '+'|'-'|'*'|'/') onto time-series 'ts1' and 'ts2'.

    Args:
        ts1 (:obj:): First time-series operand, will be made coherent with 2nd one.
        ts2 (:obj:): Second time-series operand, will be made coherent with 1st one.
        op (str): Operation to be applied sample-wise for each matching time instant of coherent
            versions of 'ts1' and 'ts2' w/ available options '+'|'-'|'*'|'/'.
        res (float, optional): Desired common resolution (if any). Note that this will only be
             applied if the sampling intervals of both 'ts1' and 'ts2' are below that value.
             Otherwise the (integer) maximum of the sampling intervals is used as resolution
             which is also the default setting (for 'None').
        mode (str, optional): Desired aggregation mode for the time-series w/ options 'avg'|
            'max'|'min'|'median' (see 'zynamon.tscore.samples_pack' for details). Defaults to 
            'avg'.

    Returns:
        ts_op (:obj:):
    """

    # check consistency
    if (op not in TS_OPERATIONS.keys()):
        raise NotImplementedError("Unknown time-series operation {op}")

    # prepare inputs (i.e. ensure coherence & extract processing arrays)
    ts1c, ts2c = ts_cohere(ts1, ts2, res, mode)
    at1, ax1, _ = ts1c.to_numpy()
    at2, ax2, _ = ts2c.to_numpy()

    # prepare output
    ts_op = ts1c.clone(ts1.name+TS_OPERATIONS[op]+ts2.name, keep_history=False)

    # apply (sample-wise) operation
    new_values = []
    for n1, instant in enumerate(at1):
        try:
            n2 = int( np.where(at2 == instant)[0] )
            val = eval(f"ax1[n1] {op} ax2[n2]")
            new_values.append( val )
        except:
            new_values.append( np.nan )

    # write operation's result to output & smooth NaN values ;)
    ts_op.values_set(new_values)
    ts_op.df.interpolate('linear', inplace=True)

    return ts_op


# def ts_calc_GENERAL_slope(self):
#     """ todo

#     have same segment-wise decomposition (as "helper" in tsutils???)
#       --> then grow into a general analysis framwork with:
#         - max/min/mean statistics
#         - sigma / variance
#         - RMS values? (where reasonable)
#         - histograms w/ 10 - 50 bin levels, squeezed into |max-min| range
#         - slope (general and also due to sections / time intervals?)

#     general restriction to an "extracetd frame"?
#         (e.g. defaults = last x samples / y seconds?)

#       ...

#     # FIXME: compute different lin regs

#     # create a linear regression (for comparison)
#     inc = slope * dt/len(self)
#     linreg_hit = np.arange(self.x[0], self.x[-1]+(inc/2), inc) # +(inc/2) only to ensure!
#     # Note: This will NOT hit the end-point but be a better approx
#     # End-point including is obtained by "inc = slope * (dt/(len(self)-1)"

#     inc2 = slope * dt/(len(self)-1)
#     linreg_ext = np.arange(self.x[0], self.x[-1]+(inc/2), inc2)

#     avg = np.average(self.x)
#     linreg_avg = np.arange(avg-(dx/2), avg+(dx/2), inc)



#===============================================================================================
#===============================================================================================
#===============================================================================================

#%% MAIN
if __name__ == "__main__":
    print("This is the 'zynamon.tsutils' module.")
    print("See 'help(zynamon.tsutils)' for proper usage.")



################################################################################################
# Explanation:
#
#   What is the DIFFERENCE between 'ts_import_csv()' and 'ts_import_csv_mixed()'...
#   ..or: WHEN TO USE WHICH ONE?
#
#   1. 'ts_import_csv()' can import data that...
#       ...represents continuous time-series (probably w/ much redundant meta information)
#
#   (1a) = single time-series:
#   NAME,               DESCRIPTION,          CLASS,    UNIT,   VALUE,  INSERT_TIME
#   =10QA12/CB_STAT,    Stat 1 CB open/close, STAT,     NULL,   0,      2020-04-16 20:59:42.5
#   =10QA12/CB_STAT,    Stat 1 CB open/close, STAT,     NULL,   0,      2020-04-19 04:33:27.1
#   ...
#   =10QA12/CB_STAT,    Stat 1 CB open/close, STAT,     NULL,   1,      2020-05-03 08:40:17.3
#
#   (1b) = several time-series, in multiple columns:
#   TIMESTAMP,              LOCATION_TAG,   VALUE_1,    VALUE_2,    ...     VALUE_N
#   2020-04-16 20:59:42.5,  GER: Erlangen,  14.7,       60,         ...     134683.3
#   2020-04-16 20:59:45.3,  GER: Erlangen,  14.8        59,         ...     136584.45
#   ...
#   2020-04-16 21:06:13.7,  GER: Erlangen,  12.9        64,         ...     140432.8
#
#
#   2. 'ts_import_csv_mixed()' can import...
#       ...non-continuous lists of data, contributing to many time-series (i.e. event sequence)
#
#   NAME,               DESCRIPTION,            CLASS,  UNIT,   VALUE,  INSERT_TIME
#   =10QA12/CB_STAT,    Stat 1 CB open/close,   STAT,   NULL,   0,      2020-04-16 20:59:42.5
#   =20QA11/CB_STAT,    Stat 2 CB open/close,   STAT,   NULL,   1,      2020-04-19 04:33:27.1
#   ...
#   =10/GEN_FLT,        Stat 1 General FAULT!,  ALR,    NULL,   1,      2020-05-03 08:40:17.3
#   ...
#   =20QA11/CB_STAT,    Stat 2 CB open/close,   STAT,   NULL,   0,      2020-05-08 16:03:39.4
#   ...
#
################################################################################################