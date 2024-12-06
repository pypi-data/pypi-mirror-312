# -*- coding: utf-8 -*-
"""
Helper functions for the import, conversion & aggregation of (many) CSV-files.
This module contains helpers in the context of working with dump files from CBM projects. Since
these are often available as simple, but quite "bulky" CSV-files (e.g. exported from LCG or AWS
cloud services), it is reasonable to bring the contained information to a more "manageable"
format (see 'cbm.tscore').

Note: The functions here are designed to work on the subfolder structure as implied by the
      script 'CBM_import_data'!
"""
__version__ = 2.0
__author__ = 'Dr. Marcus Zeller (marcus.zeller@siemens-energy.com)'
__date__ = '2022-2024 @ Erlangen, Germany (Siemens Energy Global GmbH & Co. KG)'

import re
import os
import time
import shutil

from zynamon.tsutils import *
from zdev.core import anyfile


# EXPORTED DATA
IMPORT_FORMATS = ('csv','txt')

# INTERNAL PARAMETERS & DEFAULTS
_DEBUG_BACKUP = True # switch [bool] to use a "_BACKUP" folder for original files in each path
_DEBUG_LOW = 0  # verbosity for "low-level" functions (see 'cbm.tsutils.import_xxx' for details)
                # 0 = off | 1 = short summary | 2 = detailed summary | 3 = heartbeat | 4 = full)


def batch_convert_data(path, sub_folders, csv_type, col_name, col_time, col_value,
                       enforce=None, causal=True, save_files=False, save_series=False,
                       save_fmt=('json','pk'), fname_out='_all',
                       allow_reimport=True,  allow_transcode=True, verbose=0):
    """ Converts time-series data from all CSV-files in all 'sub_folders' below 'path'.

    This helper will go into 'path', check for all CSV-like files in all 'sub_folders', extract
    all time-series data that are found and convert/store them acc. to the given settings. Since
    data in different files may also refer to the same time-series (i.e. identical in name) the
    converted data has to be combined. Therefore, causality may have to be enforced at every
    "save stage" (in order to present time-series w/ monotonously increasing time instants).

    Regarding the 'csv_type', there are three general types of structure that may be found:

        'mixed':    Each line contains a new sample for a specific time-series such that
                    contributing samples may appear in "mixed order" and associated time-stamps
                    could be completely aysnchronous & sporadic. In addition, "meta information"
                    will be collected from columns not referred to by the 'col...' arguments in
                    the form of "key=value" pairs. A typical example for this type are
                    event-driven recordings (e.g. status, warnings, alarms).

        'stream':  Each line contains a new sample for one or more time-series whose names are
                   identified by the headers of the 'col_data' columns (on the other hand, the
                   'col_name' setting will be ignored). However, in contrast to the "mixed"
                   type, the common time reference in 'col_time' is valid for all listed data,
                   usually referring to equidistantly sampled measurement signals.

        'stream_meta': Related to the above; however, this constellation reflects the special
                       case in which only 1 signal stream is present but only after two lines
                       indicating meta information (as well as the signal name). In this case,
                       these lines have to be extracted/stripped first, before actual import
                       can proceed.
                       A typical example is CSV-files exported from "CMS X-Tools" software.

    Differences for time-series naming:

        'mixed':    Names are taken from column 'col_name' entries (per line). If 'col_name'
                    is a list, names will be concatenated by '_'.

        'stream':   Names are taken from column(s) in 'col_value' (header from 1st line).

        'stream_meta': Names are taken from filename.

    Args:
        path (str): Parent location of all data locations listed in 'sub_folders'.
        sub_folders (list of str): List of sub-folders to check for CSV-files containing more
            time-series data. If empty, i.e. [], the parent folder in 'path' will be searched.
        csv_type (str): Structure of CSV-files, either 'mixed'|'stream'|'stream_meta'.
        col_name (str or list): Column(s) indicating datapoint name. If more than one columns
            are required to create a unique identifier, the items are concatenated by '_'.
            Note: This setting is only used if 'csv_type' is 'mixed'!
        col_time (str): Column indicating the timestamps of the datapoint samples.
        col_value (str): Column indicating the values of the datapoint samples.
            Note: This setting defines the signal names if 'csv_type' is 'stream'!
        enforce (list, optional): 2-tuple specifying conversions that should be enforced on
            'time' and 'data' entries. Defaults to 'None' (i.e. plain data is copied).
        causal (bool, optional): Ensure that a "causal" timeline is present which may be
            required if samples have a non-monotonous ordering. Defaults to 'True'.
        save_files (bool, optional): Switch to save each file after import, resulting in a
            "1-to-1"" conversion of all CSV-files. Otherwise, all contents imported from each
            subfolder are stored in a single file (as for the parent). Defaults to 'False'.
        save_series (bool, optional): Switch to save each single time-series found in its
            separate file. This can only be applied as final step since samples of (the same)
            time-series *might* be distributed over several subfolders. Defaults to 'False'.
        save_fmt (list, optional): 2-tuple of file formats [str] to which converted data shall
            be stored to w/ options 'TS_SAVE_FORMATS'. Defaults to ('json', 'pk').
            Note: The two different levels are applied as follows:
                item [0]    -> single time-series and/or files ("1-to-1" conversion)
                item [1]    -> sub-folders & main path & collections (e.g. time periods, assets)            Defaults to ('json', 'pk').
        fname_out (str, optional): Filename for storing the full collection at parent level w/o
            file extension. Defaults to '_all'.
        allow_reimport (bool, optional): Switch to allow re-importing files w/ 'IMPORT_FORMATS'.
            If disabled, such files will be ignored if a storage file of type 'TS_SAVE_FORMATS'
            already exists. Otherwise, any (new?) files found in the sub-folder will (again?) be
            imported and added to the collection file. Defaults to 'True'.
        allow_transcode (bool, optional): Switch to allow a "trans-coding" of storage files,
            i.e. if such file exist in the sub-folders but do not match the currently desired
            setting in 'save_fmt[1]', they will still be loaded an the collection will be saved
            to the desired (new) format. Defaults to 'True'.
            Note: This avoids a complete re-import of data from original files!
        verbose (int, optional): Verbosity level of function. Defaults to '0'.
            Level 0 which will only display basic information on all steps & traversed folders.
            Level 1 will additionally produce information on all files encountered, and
            Level 2 will finally add details on each time-series found (new or existing).

    Returns:
        collected (dict): Dict of collected & combined 'TimeSeries' objects from all files
            in all 'sub_folders' of 'path'.
    """
    back = os.getcwd()
    os.chdir(path)

    # check for special meta format
    if (csv_type == 'stream_meta'):
        col_meta = 'xtools'
    else:
        col_meta = None

    # init & sub-folder checks (which are actually existing)
    collected = {}
    the_folders = sub_folders.copy()
    for chk in sub_folders:
        path_chk = os.path.join(path, chk)
        if (not os.path.isdir(path_chk)):
            the_folders.remove(chk)
    if (the_folders == []):
        return collected

    # init backup folder (to keep original files)
    if (_DEBUG_BACKUP):
        folder_backup = os.path.join(path, '_BACKUP')
        if (not os.path.isdir(folder_backup)):
            os.mkdir(folder_backup)

    # parse ALL SUB-FOLDERS...
    for sub in the_folders:
        print(f"o SUB-FOLDER '{sub}'")
        path_sub = os.path.join(path, sub)
        collected[sub] = []

        # check for existing (sub-folder) store file
        file_store, fext_store = None, None
        chk = os.path.join(path_sub, f'_{sub}.{save_fmt[1]}')
        if (os.path.isfile(chk)):
            file_store = chk
        elif (allow_transcode):
            file_store = anyfile(path_sub, f'_{sub}', TS_SAVE_FORMATS)
            if (file_store):
                _, __, fext_store = fileparts(file_store)

        # retrieve stored (sub-folder) data (if any)
        if (file_store):
            print(f"  Loading storage <{file_store}>") #'{os.path.basename(file_store)}'")
            loaded = ts_read_file(file_store, target='list', verbose=True)
            for ts in loaded:
                collected[sub].append(ts)

        # parse & import data from sub-folder files
        if (not file_store or allow_reimport):
            print("  Importing files... ")

            for fname in os.listdir(sub):
                _, fbase, fext = fileparts(fname)
                if (fext not in IMPORT_FORMATS):
                    continue # skip any other file formats

                # ensure backup folder (if any)
                if (_DEBUG_BACKUP):
                    path_bkp = os.path.join(folder_backup, sub)
                    if (not os.path.isdir(path_bkp)):
                        os.mkdir(path_bkp)

                # data import & conversion
                if (verbose):
                    print(f"  + Converting <{fname}>")

                if (csv_type == 'mixed'):
                    objects = ts_import_csv_mixed(os.path.join(path_sub, fname),
                        col_name, col_time, col_value,
                        enforce=enforce, keep_meta=True, ensure_causal=False,
                        save_file=save_files, save_fmt=save_fmt[0], verbose=_DEBUG_LOW)

                else: # (csv_type == 'stream'|'stream_meta'):
                    objects = ts_import_csv(os.path.join(path_sub, fname),
                        col_time, col_value, col_meta,
                        enforce=enforce, ensure_causal=False,
                        save_file=save_files, save_fmt=save_fmt[0], verbose=_DEBUG_LOW)

                # move file to backup folder (if any)
                if (_DEBUG_BACKUP):
                    try:
                        shutil.move(os.path.join(path_sub, fname), os.path.join(path_bkp, fname))
                    except:
                        print("    (file backup failed, check if existing)")

                # determine if new or existing time-series (within same sub-folder)
                for ts in objects:
                    idx = ts_get_list_index(collected[sub], ts.name)
                    if (idx is None):
                        if (verbose >= 2):
                            print(f"    - (new) '{ts.name}'")
                        collected[sub].append(ts)
                    else:
                        if (verbose >= 2):
                            print(f"    - (existing) -> add samples to '{ts.name}'")
                        collected[sub][idx].samples_add(ts, analyse=False)
                        collected[sub][idx].samples_unique()

        # save sub-folder collection
        if (collected[sub] != []):
            if (causal):
                print("  Ensuring causality of all time-series")
                for ts in collected[sub]:
                    ts.time_causalise()
            fname_sub = os.path.join(path_sub, f'_{sub}.'+save_fmt[1])
            if (allow_transcode and (fext_store is not None) and (save_fmt[1] != fext_store)):
                print(f"  Transcoding sub-folder to <{fname_sub}>")
            else:
                print(f"  Saving sub-folder to <{fname_sub}>")
            ts_write_file(fname_sub, collected[sub], True, save_fmt[1], target='dict')

        print("")

    # combine collections @ parent folder (i.e. from all existing sub-folders)
    print(f"o PARENT folder")
    collected_all = []
    collected_names = []

    # ensure uniqueness
    print("  Ensuring uniqueness of all time-series (possible *merge* of objects)")
    for sub in the_folders:
        for ts in collected[sub]:
            if (ts.name not in collected_names): # first appearance...
                collected_all.append(ts)
                collected_names.append(ts.name)
            else: # ...existing -> append samples
                idx = ts_get_list_index(collected_all, ts.name)
                obj = collected_all[idx]
                obj.samples_add(ts, analyse=True)
                collected_all.pop(idx)
                collected_all.append(obj)

    # ensure causality
    if (causal):
        print("  Ensuring causality of all time-series")
        for n in range(len(collected_all)):
            if (verbose >= 1):
                print(f"  - '{collected_all[n].name}'")
            collected_all[n].time_causalise()

    # save whole collection
    if (collected_all != []):
        file_all = os.path.join(path, fname_out+'.'+save_fmt[1])
        print(f"  Saving WHOLE COLLECTION to <{file_all}>")
        ts_write_file(file_all, collected_all, True, save_fmt[1], target='dict')

    # save all time-series to individual files
    if (save_series):
        print(f"  Saving ALL COLLECTED TIME-SERIES (w/ individual filenames)")
        path_series = os.path.join(path, '_all_ts_'+save_fmt[0])
        if (not os.path.isdir(path_series)):
            os.mkdir(path_series)
        for idx in range(len(collected_all)):
            ts = collected_all[idx]
            fname_ts = os.path.join(path_series, ts.name+'.'+save_fmt[0])
            ts.export_to_file(fname_ts, True, fmt=save_fmt[0])

    print("")

    os.chdir(back)
    return collected


def batch_compress_data(the_file, agg_params=[(5*60, 'avg')], save_fmt='hdf5',
                        overwrite=False, verbose=0):
    """ Compresses all time-series of collection stored in 'the_file'.

    Args:
        the_file (str): Location of input file w/ collection of (uncompressed) time-series.
        agg_params (list, optional): List of 2-tuples as (agg_time, agg_mode) acc. to
            'cbm.tscore.TimeSeries.samples_pack()'. Defaults to [(300, 'avg')].
            Note: Applying a several different compression options at once avoids re-loading the
            original storage file several times!
        save_fmt (str, optional): Output format w/ options from 'cbm.tsutils.SAVE_FORMATS'.
            Defaults to HDF5 ('h5').
        overwrite (bool, optional): Switch to allow overwrite of existing files, i.e.
            compression process will be repeated. Defaults to 'False'.
        verbose (int, optional): Verbosity level of function. Defaults to '0'.
            Level 0 which will only display basic information on all steps.
            Level 1 will additionally produce information on all time-series encountered.

    Returns:
        objects (dict): Dictionary containing all compressed 'TimeSeries' from 'the_file'.
    """

    # load collection & perform desired aggregation (in-place)
    if (verbose):
        print(f"Loading '{os.path.basename(the_file)}'")
    objects = ts_read_file(the_file, target='dict', verbose=(verbose>=1))

    # init output filename
    fpath, fname, _ = fileparts(the_file)

    # apply all different compression settings
    for (agg_time, agg_mode) in agg_params:
        fname_out = fname+'_'+duration_str(agg_time, sep='')+'_'+f'{agg_mode}'

        # check for existence (Note: Necessary to avoid work if overwrite is *not* desired!)
        file_out = os.path.join(fpath, fname_out+'.'+save_fmt)
        if (not overwrite):
            existing_file = anyfile(fpath, fname_out, TS_SAVE_FORMATS)
            if (existing_file is not None):
                print(f"Compressed file '{fname_out}' already exists! (enforce 'overwrite')")
                return None

        print(f"+ Compressing w/ {agg_time} sec in mode '{agg_mode}'")
        comp = {}
        for n, ts_name in enumerate(objects):
            if (verbose):
                print(f"  - Aggregating '{ts_name}'")
            comp[ts_name] = objects[ts_name].samples_pack(agg_time, agg_mode, inplace='False')

        # save compressed collection
        if (verbose):
            print(f"Saving '{fname_out+'.'+save_fmt}'")
        ts_write_file(file_out, objects, overwrite, save_fmt, target='dict', verbose=(verbose>=1))

    return objects


def batch_merge_data(path, sub_folders, base, causal=True, save_fmt='pk', fname_out='',
                     overwrite=False, verbose=False):
    """ Merges data from storage files in 'sub_folders' below 'path'.

    This helper will go into 'path', check for all storage files (e.g. 'pk'|'json') and combine
    their collections on a 'TimeSeries' basis. In a typical usage, 'sub_folders' should refer
    to different periods of time (e.g. months), such that the resulting output storage files
    will then contain data of a longer (contiguous) interval.

    Args:
        path (str): Parent location of all data locations listed in 'sub_folders'.
        sub_folders (list of str): List of sub-folders to check for storage files ('pk'|'json').
        base (str): Basic filename of storage file on which to performing the merging operation
            w/o file extension (e.g. '_all_real_5min_avg').
        causal (bool, optional): Ensure that a monotonously increasing timeline is present.
            This may not be required if the 'base' files have already been sorted and the
            ordering of all 'sub_folders' is too. Defaults to 'True'.
        save_fmt (str, optional): File format for merged storage file w/ options 'pk'|'json'.
            Defaults to 'pk'.
        fname_out (str, optional): Filename w/o file extension for merged storage file at
            parent level. Defaults to '' (i.e. filename is constructed from 'base' + all items
            from 'sub_folders').
        overwrite (bool, optional): Switch to allow overwriting of existing files, i.e. merging
            process will be repeated. Defaults to 'False'.
        verbose (bool optional): Switch to print detailed progress information in case of
            'causal'. Defaults to 'False'.

        verbose (int, optional): Verbosity level of function. Defaults to '0'.
            Level 0 which will only display basic information on all steps & traversed folders.
            Level 1 will additionally produce information on all files encountered, and
            Level 2 will finally add details on each time-series found (new or existing).

    Returns:
        collected_all (dict): Dict of collected & combined 'TimeSeries' objects from all 'base'
            storage files in all 'sub_folders'.
    """
    back = os.getcwd()
    os.chdir(path)

    # init output filename
    if (fname_out == ''):
        fname_out = base
        for item in sub_folders:
            fname_out += '_'+item

    # check for existence (Note: Necessary to avoid work if overwrite is *not* desired!)
    if (not overwrite):
        existing_file = anyfile(path, fname_out, TS_SAVE_FORMATS)
        if (existing_file is not None):
            print(f"Merged file '{fname_out}' already exists! (enforce 'overwrite')")
            return None
    file_out = os.path.join(path, fname_out+'.'+save_fmt)

    # parse all sub-folders
    collected = {}
    for sub in sub_folders:
        print(f"o Sub-folder '{sub}'")
        collected[sub] = []
        path_per = os.path.join(path, sub)
        fname_per = os.path.join(path_per, base+'.'+save_fmt)

        # retrieve stored data (in any format)
        file_existing = anyfile(path_per, base, TS_SAVE_FORMATS)
        if (file_existing is not None):
            print(f"  Loading '{os.path.basename(file_existing)}'")
            collected[sub] = ts_read_file(file_existing, target='list')
        else:
            print(f"  No '{base}' file found (skipping sub-folder)")
        print("")

    # combine full collection @ parent folder (i.e. asset level)
    collected_all = []
    collected_names = []

    # ensure uniqueness
    print("Ensuring uniqueness of all time-series...")
    for sub in sub_folders:
        for ts in collected[sub]:
            if (ts.name not in collected_names): # first appearance...
                collected_all.append(ts)
                collected_names.append(ts.name)
            else: # ...existing -> append samples
                idx = ts_get_list_index(collected_all, ts.name)
                obj = collected_all[idx]
                obj.samples_add(ts, analyse=True)
                collected_all.pop(idx)
                collected_all.append(obj)

    # ensure causality
    if (causal):
        print("Ensuring causality of all time-series...")
        for n in range(len(collected_all)):
            if (verbose):
                print(f"  - Sorting '{collected_all[n].name}'")
            collected_all[n].time_causalise()

    # save whole collection
    print(f"Saving MERGED COLLECTION as '{file_out}'")
    ts_write_file(file_out, collected_all, overwrite=True, save_fmt=save_fmt, target='dict')

    print("")

    os.chdir(back)
    return collected_all


def save_summary(info_file, collection, folder_details=[None,None],
                 show_series=True, show_meta=True):
    """ Determine & save summary information about the imported time-series in 'collection'.

    Args:

        info_file (str): Filename of info file to store. Typically ending as '.txt' or '.info'.
        collection (dict or list): Collection of all 'TimeSeries' as either dict or list.
        folder_details (2-tuple, optional): Root-folder path [str] and number of subfolders
            [int] from which 'collection' was imported. Defaults to '[None, None]'.
        show_series (bool, optional): Switch to list all individual time-series by name and
            respective length [samples]. Defaults to 'True'.
        show_meta (bool, optional): Switch to indicate if all keys of "meta" information
            present in the time-series data should also be listed. Defaults to 'True'.

    Returns:
        --
    """
    with open(info_file, mode='wt') as iif:
        iif.write("="*128+"\n")

        # store infos on import folders
        iif.write(f"SUMMARY for 'TimeSeries' IMPORT from FOLDER:\n")
        if (folder_details[0] is None):
            iif.write(f"??? unknown ???\n")
        else:
            iif.write(f"<{folder_details[0]}>\n")
        iif.write("\n")
        if (folder_details[1] is not None):
            iif.write(f"Number of visited sub-folders: {folder_details[1]}\n")
        else:
            iif.write(f"Number of visited sub-folders: ??? unknown ???\n")
        iif.write("\n")

        # get infos about collection
        infos, tags, (num_samples, interval) = ts_infos(collection,
                                                        print_summary=True, print_onto=iif,
                                                        show_series=True, show_meta=True)

        iif.write("="*128+"\n")

    return


def csv_splitter(path, sub_folders=None, split_lines=int(1e6), delete_orig=True, verbose=True):
    """ Parses all 'sub_folders' in 'path' for CSV-files and creates single files (if required).

    This helper may be used in order to make CSV-files created as database dumps more "usable",
    since text editors usually have a size limit for working w/ large files.

    Args:
        path (str): Location of main folder, i.e. where to start the search for CSV-files.
        sub_folders (list of str): Names of all sub-folders to search for CSV-files. Defaults to
            'None', i.e. all subfolders will be traversed.
        split_lines (int, optional): Number of lines after which the CSV-files will be split
            into "parts" , i.e. separate CSV-files with endings "_ptN.csv" (where N indicates a
            running index). Defaults to 1000000.
        delete_orig (bool, optional): Switch to remove original (large) CSV-file after
            successful spliting. Defaults to 'True'.
        verbose (bool optional): Switch to show progress information on traversed folders/files.
            Defaults to 'True'.

    Returns:
        --
    """
    back = os.getcwd()
    os.chdir(path)

    # collect available subfolders
    if (sub_folders is None):
        sub_folders = []
        for item in os.listdir(os.getcwd()):
            if (os.path.isdir(item)):
                sub_folders.append(item)

    print(sub_folders)
    print(path)

    # parse all folders
    for sub in sub_folders:
        path_sub = os.path.join(path, sub)
        print(path_sub)
        if (not os.path.isdir(path_sub)):
            continue # skip non-existing folders
        elif (verbose):
            print(f"o Sub-folder '{sub}'")

        # parse all files
        for fname in os.listdir(path_sub):
            if ((not fname.endswith('csv')) or (re.search('_pt[0-9]*.csv', fname) is not None)):
                continue # skip non-CSV files or files that have already been split
            else:
                if (verbose):
                    print(f"  - File: '{fname}'")
                csv_file = os.path.join(path_sub, fname)
                enc = valid_encoding(csv_file)

                # read CSV-file in proper encoding
                with open(csv_file, mode='r', encoding=enc) as tf:

                    # parse format & configuration
                    first_line = tf.readline()
                    tf_format = csv.Sniffer().sniff(first_line)
                    fields = first_line.split(tf_format.delimiter)
                    for n, item in enumerate(fields):
                        fields[n] = item.strip() # clean whitespaces (incl. newline)

                    # if (num_header_lines > 2): # TODO: have this as another argument?
                    #     #
                    #     # TODO: get also "second_line = tf.readline()"
                    #     #         --> see "ts_import_csv" with "meta = xtools"

                    # create header line
                    line_header = ''
                    for item in fields:
                        line_header += f'{item}{tf_format.delimiter}'
                    line_header = line_header[:-1]+'\n'

                    # copy data of all time-series from file...
                    lines_for_next_split = []
                    num_lines, num_splits = 0, 0
                    m = 1
                    while (True):
                        try:
                            line = tf.readline()
                            if (line == ''): # regular break condition
                                raise

                            # export split file?
                            lines_for_next_split.append(line)
                            if (m == split_lines):
                                num_lines += m
                                num_splits += 1
                                with open(os.path.abspath(csv_file[:-4]+f'_pt{num_splits}.csv'), mode='wt') as sf:
                                    sf.write(line_header)
                                    sf.writelines(lines_for_next_split)
                                # reset
                                lines_for_next_split = []
                                m = 1
                            else:
                                m += 1
                        except:
                            break

                    # write last file (w/ remaining lines)
                    if (num_splits):
                        num_splits += 1
                        with open(os.path.abspath(csv_file[:-4]+f'_pt{num_splits}.csv'), mode='wt') as sf:
                            sf.write(line_header)
                            sf.writelines(lines_for_next_split)
                        if (verbose):
                            print(f"    (split into {num_splits} files)")
                    else:
                        if (verbose):
                            print(f"    (no split necessary, only {m} lines)")

                # remove original file? (only in case of splitting!)
                if ((num_splits >= 1) and delete_orig):
                     os.remove(csv_file)

    return



#===============================================================================================
#===============================================================================================
#===============================================================================================

#%% MAIN
if __name__ == "__main__":
    print("This is the 'cbm.batchimport' module.")
    print("See 'help(cbm.batchimport)' for proper usage.")