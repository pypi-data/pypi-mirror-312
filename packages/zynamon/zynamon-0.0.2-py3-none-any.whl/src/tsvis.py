"""
'TimeSeriesVisualiser' class for creating well-defined time-series plots.
This class uses the well-known "plotly" framework to present only desired signals out of
(potentially large) 'TimeSeries' collections. Most display settings are thereby configured via
JSON-files (e.g. which signals in which subplots, labeling, optional processing etc). However,
in order to provide a feeling of "playing around", the time interval of the data to be plotted
and additional visual means (slider & selector for the time range) may be included.

Note: This module is quite similar to "dsap.sigvis" (based on the "matplotlib" framework).
"""
__version__ = 2.0
__author__ = 'Dr. Marcus Zeller (marcus.zeller@siemens-energy.com)'
__date__ = '2022-2024 @ Erlangen, Germany (Siemens Energy Global GmbH & Co. KG)'

import os
import json
import plotly.graph_objects as go
import plotly.subplots as sp

from zynamon.tscore import *
from zynamon.tsutils import *
from zdev.colors import *
from zdev.indexing import expand_index_str
from dsap.sigvis import SubPlotConfig, _REQ_KEYS_PAGE, _REQ_KEYS_SUBPLOT


# INTERNAL PARAMETERS & DEFAULTS

# general settings
_FONT_TYPE = 'Arial'    # (default) family of all fonts on page (title, axes, legend)
_FONT_SIZE = 12         # (default) size [pt] of fonts (base, other sizes are derived from this)
_LINE_WIDTH = 1.5       # (default) width [pt] of all plotted curves
_MARKER_SIZE = 4        # (default) size [pt] of markers (if any)

# internal settings for proper layout
_FSD_TITLE_PAGE = +2    # font size delta (increase) for page titles
_FSD_TITLE_SUB = +1     # font size delta (increase) for subplot/axes titles
_FSD_LEGEND = -1        # font size delta (decrease) for legend entries
_FSD_TICKS = -2         # font size delta (decrease) for axes ticks/labels
_SLIDER_SIZE = 0.08     # height of time slider (at bottom of plots, if any)
_SLIDER_COLOR = rgb2hex(cGray03)    # (background) color of time slider


class TimeSeriesVisualiser:
    """ Standardised visualisation of time-series acc. to given configurations.
    Note: This is similar to the 'dsap.sigvis' module, but based on the "plotly" framework. """

    def __init__(self, config_file, plot_params=None): ##, consistency=_CHECKS):
        """ Initialises 'SignalVisualiser' object by parsing the layout 'config_file'. """

        # attributes
        self.config_file = os.path.abspath(config_file)
        self.config_path, fname = os.path.split(self.config_file)
        self.config_name, self.config_ext = fname.split('.')
        self.num_pages = -1
        self.num_subplots = -1
        self.num_signals = -1
        self.max_signals = -1
        self.has_positions = [] # flags indicating that 'pos' properties are used
        # Note: This will be checked for each page of a multi-page report!

        # members
        self.pages = {}
        self.figures = {}

        # ascertain general plot parameters
        if (plot_params is None):
            self.plot_params = {
                'font_type': _FONT_TYPE,
                'font_size': _FONT_SIZE,
                'line_width': _LINE_WIDTH,
                'marker_size': _MARKER_SIZE,
                'time_slider': True,
                'time_selector': False
                }
        else:
            self.plot_params = plot_params

        # initialisation routines
        self.parse_config(config_file)

        return


    def parse_config(self, config_file, consistency=False):
        """ Parses the associated 'config_file' and indicate design flaws (if desired).

        Args:

            config_file (str): Filename of configuration file for "layouts" (JSON).
            consistency (bool, optional): Switch for performing some consistency checks.
                Defaults to 'True'.

        Returns:
            --
        """
        with open(config_file, mode='r') as cf:

            # load page definitions
            self.pages = json.load(cf)
            if (type(self.pages) != dict):
                print(f"Configuration file <{config_file}> is no proper 'json' file!")
                self.pages = {}
                return

            # check on mandatory fields
            for ID in self.pages.keys():
                for key in _REQ_KEYS_PAGE:
                    if (key not in self.pages[ID].keys()):
                        print(f"Error: Mandatory key '{key}' missing! (page '{ID}')")
                        return
                for s, sp_cfg in enumerate(self.pages[ID]['subplot']):
                    for key in _REQ_KEYS_SUBPLOT:
                        if (key not in sp_cfg.keys()):
                            print(f"Error: Mandatory field {key} missing! (page '{ID}', sp_cfg {s})")
                            return
                        else: # ensure 'list' type
                            chk = sp_cfg['signal']
                            if (type(chk) != list):
                                sp_cfg['signal'] = [chk]

            # determine additional information
            self.num_pages = len(self.pages)
            self.num_subplots = []
            self.num_signals = []
            self.max_signals = []
            self.has_positions = [False] * len(self.pages)
            for pg, (ID, pg_cfg) in enumerate(self.pages.items()):
                self.num_subplots.append(pg_cfg['layout'][0]*pg_cfg['layout'][1])
                self.num_signals.append([len(pg_cfg['subplot'][s]['signal'])
                                         for s in range(self.num_subplots[pg])])
                self.max_signals.append( max(self.num_signals[pg]) )
                if ('pos' in pg_cfg['subplot'][0].keys()): # check only 1st subplot definition
                    self.has_positions[pg] = True
                else:
                    self.has_positions[pg] = False

            # # perform consistency checks
            # if (consistency):

            #     if (max(self.num_subplots) >= _MAX_SUBPLOTS):
            #         print(f"Warning: Layouts should not exceed {_MAX_SUBPLOTS} subplots per page!")

            #     if (max(self.max_signals) >= _MAX_SIGNALS):
            #         print(f"Warning: Subplots should not contain more than {_MAX_SIGNALS} curves!")

            #     for pg, ID in enumerate(self.pages.keys()):

            #         if (self.num_subplots[pg] != len(self.pages[ID]['subplot'])):
            #             print(f"Warning: Mismatch in page '{ID}' layout! (deviation from number of specified subplots)")

            #         for s, sp_cfg in enumerate(self.pages[ID]['subplot']):
            #             for key in ('color', 'style', 'legend'):
            #                 if (not ensure_proper_lengths(self.pages[ID]['subplot'][s], key)):
            #                     print(f"Warning: Mismatch in number of '{key}' entries! (page '{ID}', subplot {s})")

        return


    def create_page(self, ID):
        """ Initialises a "plotly" figure for plotting all data acc. to the config of page 'ID'.

        Since plotly interpretes subplot titles as annotations, these need to be set right from
        the start. To this end, the page configs need to be checked whether subplots are simply
        enumerated or if they are provided with 'pos' information. In the latter case, proper
        indexing is calculated internally.

        Args:
            ID (str): Name of page to be plotted, as previously found by 'parse_config()'.

        Returns:
            --
        """

        # check consistency
        if (ID not in self.pages.keys()):
            print(f"Error: Page '{ID}' does not exist in parsed config! (aborting)")
            return
        else:
            pg = list(self.pages.keys()).index(ID)

        # create all subplot titles (if any)
        sp_titles = [''] * self.num_subplots[pg]
        if (not self.has_positions[pg]):
            for s, sp_cfg in enumerate(self.pages[ID]['subplot']):
                if ('title' in sp_cfg.keys()):
                    sp_titles[s] = sp_cfg['title']
        else: # use proper ordering
            for s, sp_cfg in enumerate(self.pages[ID]['subplot']):
                ax = sp_cfg['pos']
                idx = (ax[0]-1)*self.pages[ID]['layout'][1] + ax[1] # Note: (m-1)*cols + n
                if ('title' in sp_cfg.keys()):
                    sp_titles[idx-1] = sp_cfg['title']

        # create page acc. to specification
        if ('caption' in self.pages[ID].keys()):
            title = self.pages[ID]['caption']
        else:
            title = ID

        # create page acc. to specification & add to reference list
        fh = create_fig_plotly(self.pages[ID]['layout'], title, sp_titles,
                               font_type=self.plot_params['font_type'],
                               font_size=self.plot_params['font_size'])
        self.figures[ID] = [fh, self.pages[ID]['layout']]

        return


    def plot_page(self, ID, collection, interval=None, renderer='browser', verbose=False):
        """ Plots all subplots specified for page 'ID' w/ time-series data from 'collection'.

        Args:
            ID (str): Name of page to be plotted, as previously found by 'parse_config()'.
            collection (list or dict): Collection of 'TimeSeries' objects where all signals are
                to be found. This may either be arranged as list or dict.

            interval () : #TODO
            slider (bool, optional): #TODO
            selector (bool, optional): #TODO

            renderer (str, optional): #TODO

        Returns:
            --
        """

        # get page index
        page_list = list(self.pages.keys())
        pg = page_list.index(ID)
        fh = self.figures[ID][0]

        if (verbose):
            print(f"Plotting page '{ID}'")

        # cycle through all subplots
        for s, sp_cfg in enumerate(self.pages[ID]['subplot']):

            # get subplot position (if specified)
            if ('pos' in sp_cfg.keys()):
                ax = sp_cfg['pos']
            else: # (otherwise assume vertical Mx1 layout)
                ax = (s+1,1)

            # draw all traces on subplot
            if (verbose):
                print(f"Drawing {len(sp_cfg['signal'])} curves on subplot #{s}")
            plotly_axes_by_cfg((self.figures[ID][0], ax), sp_cfg, collection, time_seg=interval,
                               line_width=self.plot_params['line_width'],
                               font_size=self.plot_params['font_size'],
                               marker_size=self.plot_params['marker_size'])

        # apply time range slider?
        if (self.plot_params['time_slider']):
            str_slider = f"rangeslider=dict(visible=True, \
                autorange=True, thickness=_SLIDER_SIZE, bgcolor=_SLIDER_COLOR, \
                borderwidth=1, bordercolor='{rgb2hex(cSilver)}', \
                yaxis=dict(range=[-1e9,-1e9+1],rangemode='fixed'))"

            # dynamic creation to place slider at bottom (i.e. only for last "xaxis")
            num_xaxes = self.num_subplots[pg]
            if (num_xaxes == 1):
                str_xaxes = "xaxis=dict(type='date', "+str_slider+")"
            else:
                str_xaxes = "xaxis=dict(type='date',rangeslider=dict(visible=False))"
                for n in range(2, num_xaxes):
                    str_xaxes += f", xaxis{n}=dict(type='date',rangeslider=dict(visible=False))"
                str_xaxes += f", xaxis{num_xaxes}=dict(type='date', "+str_slider+")"
            eval(f"fh.update_layout("+str_xaxes+")")

        # apply time range selector? (pre-defined w.r.t. given interval)
        if (self.plot_params['time_selector']):
            pass

            #     fh.update_layout(
            #         xaxis2=dict(
            #             rangeselector=dict(
            #                 buttons=[
            #                     dict(label="MYTEST", count=1, step="month", stepmode="backward")
            #                     ]
            #                 )))

            #     # if (num_xaxes > 1):
            #     #     xon = f'xaxis{n:d}'
            #     #     eval("fh.update_layout("+xon+"=dict(type='linear',rangeslider=dict(visible=True)))")
            #     #     print(f"ON for {num_xaxes}")
            #     #     for n in range(num_xaxes-1,1,-1):
            #     #         xoff = f'xaxis{n:d}'
            #     #         eval("fh.update_layout("+xoff+"=dict(type='linear',rangeslider=dict(visible=False)))")
            #     #         print(f"OFF for {n}")
            #     #     fh.update_layout(xaxis=dict(type='linear',rangeslider=dict(visible=False)))
            #     #     print(f"OFF for axis (1)")
            #     # else:
            #     #     xon = 'xaxis'
            #     #     eval("fh.update_layout("+xon+"=dict(type='linear',rangeslider=dict(visible=True)))")
            #     #     print(f"ON for axis (1)")


        # finalise figure
        fh.update_traces(mode='lines+markers')
        # fh.update_layout(showlegend=False)
        # fh.update_layout( legend_tracegroupgap = 180 ) # increase distance (if "own_legend?")

        # finalise figure
        fh.show(renderer, width=1600, height=900)

        return


    def plot_report(self, collection, save_folder, save_formats=['html'],
                    pages=None, verbose=False):
        """  Creates a "report", i.e. plots *all* pages that are found in the 'config'.

        Note that as long as "static images" (e.g. PDF, TIFF, PNG or JPEG) or also contained in
        tjhe list of desired format, interactive elements such as time slider & range selectors
        will be automatically but temporarily disabled! That is, if these controls are required
        for HMTL rendering, this should be done in a separate call!

        Args:
            collection (list or dict):
            save_folder (str):
            save_formats (list of str, optional):
            pages (list, optional):
            verbose (bool, optional):

        Returns:
            --
        """

        # determine all pages to be plotted
        if (pages is None): # --> plot all! ;)
            pages_to_plot = self.pages
        else:
            pages_to_plot = expand_index_str(pages)
        num_pages = len(pages_to_plot)

        # ensure sliders & selectors are disabled if plotting to "static images"
        old_settings = None
        if (('pdf' in save_formats) or ('tiff' in save_formats)
            or ('png' in save_formats) or ('jpg' in save_formats)):
            old_settings = (self.plot_params['time_slider'], self.plot_params['time_selector'])
            self.plot_params['time_slider'] = False
            self.plot_params['time_selector'] = False

        # create report by drawing all individual pages
        if (verbose):
            print(f"Creating report w/ {num_pages} pages")
        for ID, pg_cfg in self.pages.items():
            self.create_page(ID)
            self.plot_page(ID, collection, interval=None, renderer=None, verbose=verbose)

        # save report in desired format(s)
        fname_base = os.path.join(save_folder, self.config_name)
        if ('html' in save_formats):
            for pg, ID in enumerate(self.pages.keys()):
                self.figures[ID][0].write_html(f'{fname_base}_{pg}_{ID}.html', auto_open=False)
        elif ('pdf' in save_formats):
            pass # TODO?
        elif ('tiff' in save_formats):
            pass # TODO?
        elif ('png' in save_formats):
            pass # TODO?

        # revert plot settings
        if (old_settings is not None):
            self.plot_params['time_slider'], self.plot_params['time_selector'] = old_settings

        return


#-----------------------------------------------------------------------------------------------


class SubPlotlyConfig(SubPlotConfig):
    """ Specification of a single "plotly" axes (similar to class for "matplotlib" framework) """

    def __init__(self, config):
        """ Initialises a 'SubPlotlyConfig' object by parsing the 'config'.

        Args:
            config (dict): Subplot definition as parsed from layout file (or defined manually).
                See below for format definition.

        Returns:
            --

        Format definition: (Note that only identifiers of signals to be plotted are required!)

            config: {
                'pos':    [m,n],                    --OPTIONAL-- (subplot position in layout)
                'title':  [str],                    --OPTIONAL-- (above axes)
                'label':  [str],                    --OPTIONAL-- (left of axes, rotated 90°)
                'signal': [str1, ..., strN]         => MANDATORY
                'color':  ['col1', ..., 'colN'],    --OPTIONAL--
                'style':  ['sty1', ..., 'styN'],    --OPTIONAL--
                'legend': ['txt1', ..., 'txtN'],    --OPTIONAL--

                'filter': #### TODO ####
                'agg':    #### TODO ####

                }

        Notes:
            If 'styles' are specified, the user has to make sure that these are unique within
            each subplot (i.e. no repetitions)!
        """

        # init acc. to base class
        super().__init__(config, None)

        # # attributes (in addition, as req. for "plotly" / 'TimeSeries' handling)
        self.own_legend = False
        self.is_filtered = [False]      # flags indicating which signals are to be filtered
        self.is_aggregated = [False]    # flags indicating which signals are to be aggregated

        # # members
        # self.num_signals = len(config['signal'])    # number of signals on subplot
        # # self.xrange = [0, None]                     # time range [s] (default: whole signal)
        # # self.xidx = [0, None]                       # time interval [samples]
        # self.legend_entries = []                    # relevant legend entries

        return


    def configure_filter(self):
        """ Checks if filtering is required for (some time-series on) the subplot. """
        self.is_filtered = []
        if ('filter' in self.config.keys()):
            for item in self.config['filter']:
                if (item is not None):
                    self.is_filtered.append(True)
                else:
                    self.is_filtered.append(False)
        else:
            self.is_filtered = [False] * len(self.config['signal'])
        return


    def configure_aggregation(self):
        """ Checks if aggregation is required for (some time-series on) the subplot. """
        self.is_aggregated = []
        if ('agg' in self.config.keys()):
            pass
        else:
            self.is_aggregated = [False] * len(self.config['signal'])
        return


    def line_properties_plotly(self, s):
        """ Returns line properties for subplot signal 's' matching "plotly" conventions.

        Args:
            s (int): Index of current signal in the subplot.

        Returns:
            col (str): Color specification as hex-string (e.g. '#ff0000').
            sty (str): Line style specification (i.e. 'solid', 'dash', 'dashdot' or 'dot').
            mrk (str): Marker style (if any) - NOT USED FOR PLOTLY!

        Note: Any of these properties defaults to 'None' if they are not specified in the layout
        or cannot be converted to "plotly" conventions.
        """
        col, sty, mrk = None, None, None

        # parse properties (based on "matplotlib" conventions)
        col_tmp, sty_tmp, mrk_tmp = self.line_properties(s)

        # convert to "plotly" conventions
        if (col_tmp is not None):
            col = rgb2hex(col_tmp) # Note: Plotly requires HEX format! (but only )
        if (sty_tmp is not None):
            if (sty_tmp in ('-','solid')):
                sty = 'solid'
            elif (sty_tmp in ('--','dashed')):
                sty = 'dash'
            elif (sty_tmp in ('-.','dashdot')):
                sty = 'dashdot'
            elif (sty_tmp in (':','dotted')):
                sty = 'dot'
        # Note: 'mrk' is UNUSED by "plotly"!

        return col, sty, mrk


    def close(self):
        """ Closes subplot specification object. """
        return



#-----------------------------------------------------------------------------------------------
# HELPER FUNCTIONS
#-----------------------------------------------------------------------------------------------

def create_fig_plotly(layout, fig_title=None, sp_titles=None,
                      font_type=_FONT_TYPE, font_size=_FONT_SIZE):
        """ Initialises a "plotly" figure w/ given 'layout' and subplot 'titles'.

        Args:
            layout (2-tuple): Desired subplot layout of the figure (MxN).
            fig_title (str, optional): Overall title of the figure (if any). Defaults to 'None'.
            sp_titles (list of str, optional): Individual headings for all subplots. If desired,
                this list must have M*N items. Defaults to 'None'.
            font_type (str, optional): Font family used for all titles. Defaults to 'Arial'.
            font_size (int, optional): (Base) size of fonts [px]. The actual size of text in the
                titles is derived by internal rules. Defaults to 12.

        Returns:
            fh (:obj:): Handle to a 'go._figure.Figure' object w/ pre-initialised appearance.
        """
        rows, cols = layout

        # create page w/ all subplots acc. to layout
        if (cols == 1):
            fh = sp.make_subplots(rows, cols, subplot_titles=sp_titles,
                                  shared_xaxes=True, vertical_spacing=0.05,     # default: 0.3
                                  shared_yaxes=False, horizontal_spacing=0.1)   # default: 0.2
        else:  # TODO: what is different? bind other axes together?
            # pass
            fh = sp.make_subplots(rows, cols, subplot_titles=sp_titles,
                                  shared_xaxes=True, vertical_spacing=0.05,     # default: 0.3
                                  shared_yaxes=False, horizontal_spacing=0.1)   # default: 0.2

        # finalise figure
        fh.update_layout(title_text=fig_title,
                         title_font_family=font_type, title_font_size=font_size+_FSD_TITLE_PAGE)
        fh.update_annotations(font_family=font_type, font_size=font_size+_FSD_TITLE_SUB)

        # Note: Subplot titles are hard-coded as annotations!
        # [ https://community.plotly.com/t/setting-subplot-title-font-sizes/46612 ]

        return fh


def plotly_axes_by_cfg(ax, config, collection, time_seg=None, iso_format='%Y-%m-%d %H:%M:%S',
                       own_legend=False,
                       line_width=_LINE_WIDTH, font_size=_FONT_SIZE, marker_size=_MARKER_SIZE):
    """ Plots signals given by 'config' and found in 'collection' to the (plotly) subplot 'ax'.

    Note that this routine is placed separately from the other 'tsvis' classes in order to
    allow its use as stand-alone tool (e.g. in context w/ 'zutils..quickplotly()' functions).

    Args:
        ax (2-tuple): Handle to an existing "go.Figure" (plotly) and respective "axes" for the
            subplot, i.e. (fh, (row,col)).
        config (dict): Dictionary defining the appearance of the subplot graphs. For details on
            the format see class 'SubPlotlyConfig'.
        collection (list or dict): Collection of 'TimeSeries' objects where all signals defined
            in the 'config' are to be found. This may either be arranged as list or dict.
        time_seg (2-tuple or scalar, optional): Frame definition by interval or scalars in *any
            form* supported by 'cbm.tscore.ts_timespec()'. Defaults to 'None' (i.e. full).
        iso_format (str, optional): Detailed format of 'iso' time string w/ options acc. to
            'cbm.tscore.ts_timespec'. Defaults to '%Y-%m-%d %H:%M:%S'.
        own_legend (bool, optional): Switch to indicate if the subplot should have a separate
            legend, otherwise the signals will be added to the whole list. Defaults to 'False'.
        line_width (float, optional): Width [pt] of all curves. Defaults to '_LINE_WIDTH'.
        font_size (float, optional): Base size [pt] of all fonts, other sizes are derived from
            this. Defaults to '_FONT_SIZE'.
        marker_size (float, optional): Size [pt] of any markers. Defaults to '_MARKER_SIZE'.

    Returns:
        --
    """

    # init
    fh, (r,c) = ax
    spc = SubPlotlyConfig(config)

    # analyse subplot definition
    # spc.configure_zoom(time) # incompatible: zooming = cropping to 'time_seg' below!
    # spc.configure_stacking() # incompatible: not used for TimeSeries!
    spc.configure_legend()
    spc.configure_filter()
    spc.configure_aggregation()

    # plot all traces in subplot
    for s, sig in enumerate(spc.config['signal']):

        # get original time-series data
        ts_orig = ts_get_by_name(collection, sig)
        if (ts_orig is None):
            print(f"Could not find '{sig}' in collection! (skipping)")
            continue

        # restrict time range to segment?
        if (time_seg is not None):
            ts = collection[sig].samples_crop(time_seg, inplace=False)
            if (not len(ts)):
                print(f"Warning: Could not get full segment of '{sig}'! (setting dummy)")
                fh.add_trace( go.Scatter(y=[0,0], x=ts_convert_time(time_seg, iso_format),
                                         name=f'N/A! ({sig})') )
                continue
        else:
            ts = ts_orig

        # perform filtering on data samples?
        if (spc.is_filtered[s]):
            f_mode = spc.config['filter'][s][0]
            f_params = spc.config['filter'][s][1]
            ts.values_filter(mode=f_mode, params=f_params)
        else:
            f_mode = None

        # convert time (if required)
        ts.time_convert(iso_format)

        # configure legend entries
        if (spc.has_legend):
            if (spc.legend_entries == []):
                ts_name = sig
                if (f_mode is not None):
                    ts_name += f"_filt_{f_mode}"
                    # if (f_params is not None):
                    #     for item in f_params.items():
                    #         ts_name += f'_{item}'
            else:
                ts_name = spc.legend_entries[s]
        else:
            ts_name = ''
            # TODO: how suppress the legend (i.e. all legend entries for this subplot)???

        # build-up Scatter plot call
        str_base = f"x=ts.df.t, y=ts.df.x, name='{ts_name}'"

        # configure line style & marker size
        col, sty, mrk = spc.line_properties_plotly(s)
        str_line = f", line=dict(width={line_width}"
        if ((col is not None) and (sty is not None)):
            str_line += f", color='{col}', dash='{sty}')"
        elif ((col is not None) and (sty is None)):
            str_line += f", color='{col}')"
        elif ((col is None) and (sty is not None)):
            str_line += f", dash='{sty}')"
        else:
            str_line += ")"
        str_line += f", marker=dict(size={marker_size})"
        # Note: Line width & marker size are set always, color & style may be automatic!

        # configure special settings
        str_special = ''
        if (spc.has_legend):
            if (own_legend):
                str_special += f", legendgroup='grp_{r}_{c}', legendgrouptitle_text='Legend:'"
        else:
            pass  # TODO: how suppress the legend (i.e. all legend entries for this subplot)???
        str_special += f", textfont=dict(family='{_FONT_TYPE}', size={_FONT_SIZE+_FSD_TICKS})"

        # plot trace & add to subplot
        fh.add_trace(eval("go.Scatter("+str_base+str_line+str_special+")"), r, c)

    # finalise layout
    fh.update_xaxes(row=r, col=c,
                    tickfont_family=_FONT_TYPE, tickfont_size=font_size+_FSD_TICKS)
    fh.update_yaxes(row=r, col=c,
                    title_text=f"{spc.config['label']}",
                    title_font_family=_FONT_TYPE, title_font_size=font_size+_FSD_TITLE_SUB,
                    tickfont_family=_FONT_TYPE, tickfont_size=font_size+_FSD_TICKS)

    return



################################################################################################
# Page definitons are given by JSON-files and have to meet the following format:
#
#   {
#
#   'PageName_ID':
#   {
#       'note':    [string],                --OPTIONAL--
#       'caption': [string, [more_lines]],  --OPTIONAL--
#       'layout':  [M,N],                   => MANDATORY
#
#       'subplot': [
#           {
#               'pos':    [m,n],                    --OPTIONAL-- (subplot position in layout)
#               'title':  [str],                    --OPTIONAL-- (above axes)
#               'label':  [str],                    --OPTIONAL-- (left of axes, rotated 90°)
#               'signal': [str1, ..., strN]         => MANDATORY
#               'color':  ['col1', ..., 'colN'],    --OPTIONAL--
#               'style':  ['sty1', ..., 'styN']     --OPTIONAL--
#               'legend': ['txt1', ..., 'txtN'],    --OPTIONAL--
#
#               'filter': #### TODO ####            --OPTIONAL--
#               'agg':    #### TODO ####            --OPTIONAL--
#
#           },
#
#           {
#               ... more 'SubPlotlyConfig' definitions (up to M*N) ...
#           }
#       ]
#   },
#
#   ... more page definitions ...
#
#   }
#
# Note: Although the ordering of fields is free, the sequence as shown above is recommended.
#       Moreover, only few fields are required whereas most entries are --OPTIONAL--.
#
#       At minimum, each page definition requires the 'layout' and the 'subplot' fields.
#       The latter has to contain the corresponding number of M*N layout elements. Likewise,
#       for each of the 'subplot' keys, at least the 'signal' field with one or more signal
#       identifiers in format "GroupName.SignalName" is necessary.
#
#       The optional fields 'color' and 'style' can be used for detailing the looks of each
#       individual plot line. If omitted, set to 'null' (= 'None' in Python) or if the
#       respective index falls short of the number of plotted signals, the color' & 'style'
#       specifications are determined from the next element in the default property cycle.
#
#       The 'legend' field is optional as well. If it is omitted or has insufficient entries,
#       the missing descriptors are derived from the signal identifiers. On the other hand,
#       if the 'legend' field is present but set to 'null' (= 'None' in Python), the legend is
#       deactivated.
#
#       ## TODO ## filter & agg!
#
#
#
################################################################################################