import time as tt

import collections as cx
import atexit as ae

import pandas  as pd

from .base import utils as ut
from .base import validation_parsing as vp
from .base import core_motif as cm

from typing import Tuple


def motif(
    input_data:str|pd.DataFrame,
    oligo_length_limit:int,
    motif_sequence_constraint:str,
    maximum_repeat_length:int,
    motif_column:str,
    output_file:str|None=None,
    motif_type:int=0,
    left_context_column:str|None=None,
    right_context_column:str|None=None,
    excluded_motifs:list|str|pd.DataFrame|None=None,
    verbose:bool=True) -> Tuple[pd.DataFrame, dict]:
    '''
    Adds a constant or designs constrained motifs free of edge-effects between the given sequence
    contexts. Addition of motifs will not produce excluded motifs unless one was embedded in it.
    Returned DataFrame with added motifs can optionally be saved to a CSV.

    Required Parameters:
        - `input_data` (`str` / `pd.DataFrame`): Path to a CSV file or DataFrame with annotated oligopool variants.
        - `oligo_length_limit` (`int`): Maximum allowed oligo length (≥ 4).
        - `motif_sequence_constraint` (`int`): IUPAC degenerate sequence constraint, or a constant.
        - `maximum_repeat_length` (`int`): Max shared repeat length with oligos (≥ 4).
        - `motif_column` (`str`): Column name for inserting the designed motifs.

    Optional Parameters:
        - `output_file` (`str`): Filename for output DataFrame (default: `None`).
        - `motif_type` (`int`): Motif type to design (0 for non-constant, 1 for constant, default: 0).
        - `left_context_column` (`str`): Column for left DNA context (default: `None`).
        - `right_context_column` (`str`): Column for right DNA context (default: `None`).
        - `excluded_motifs` (`list` / `str` / `pd.DataFrame`): Motifs to exclude;
            can be a CSV path or DataFrame (default: `None`).
        - `verbose` (`bool`): If `True`, logs updates to stdout (default: `True`).

    Returns:
        - A pandas DataFrame of added motifs; saves to `output_file` if specified.
        - A dictionary of stats from the last step in pipeline.

    Notes:
        - `input_data` must contain a unique 'ID' column, all other columns must be non-empty DNA strings.
        - Column names in `input_data` must be unique, and exclude `motif_column`.
        - At least one of `left_context_column` or `right_context_column` must be specified.
        - If `excluded_motifs` is a CSV or DataFrame, it must have 'ID' and 'Exmotif' columns.
        - Constant bases in sequence constraint may lead to `excluded_motifs` and be impossible to solve.
        - Constant barcode anchors must be designed prior to barcode generation.
    '''

    # Argument Aliasing
    indata       = input_data
    oligolimit   = oligo_length_limit
    motifseq     = motif_sequence_constraint
    maxreplen    = maximum_repeat_length
    motifcol     = motif_column
    outfile      = output_file
    motiftype    = motif_type
    leftcontext  = left_context_column
    rightcontext = right_context_column
    exmotifs     = excluded_motifs
    verbose      = verbose

    # Start Liner
    liner = ut.liner_engine(verbose)

    # Motif Verbage Print
    liner.send('\n[Oligopool Calculator: Design Mode - Motif]\n')

    # Required Argument Parsing
    liner.send('\n Required Arguments\n')

    # First Pass indata Parsing and Validation
    (indf,
    indata_valid) = vp.get_parsed_indata_info(
        indata=indata,
        indata_field='    Input Data    ',
        required_fields=('ID',),
        precheck=False,
        liner=liner)

    # Full oligolimit Validation
    oligolimit_valid = vp.get_numeric_validity(
        numeric=oligolimit,
        numeric_field='    Oligo Limit   ',
        numeric_pre_desc=' At most ',
        numeric_post_desc=' Base Pair(s)',
        minval=4,
        maxval=float('inf'),
        precheck=False,
        liner=liner)

    # First Pass motifseq Validation
    motifseq_valid = vp.get_seqconstr_validity(
        seqconstr=motifseq,
        seqconstr_field='    Motif Sequence',
        minlenval=1,
        element='MOTIF',
        liner=liner)

    # Full maxreplen Validation
    maxreplen_valid = vp.get_numeric_validity(
        numeric=maxreplen,
        numeric_field='   Repeat Length  ',
        numeric_pre_desc=' Up to ',
        numeric_post_desc=' Base Pair(s) Oligopool Repeats',
        minval=4,
        maxval=len(motifseq) if motifseq_valid else float('inf'),
        precheck=False,
        liner=liner)

    # Full motifcol Validation
    motifcol_valid = vp.get_parsed_column_info(
        col=motifcol,
        df=indf,
        col_field='    Motif Column  ',
        col_desc='Output in Column',
        col_type=1,
        adjcol=None,
        adjval=None,
        iscontext=False,
        typecontext=None,
        liner=liner)

    # Full outfile Validation
    outfile_valid = vp.get_outdf_validity(
        outdf=outfile,
        outdf_suffix='.oligopool.motif.csv',
        outdf_field='   Output File    ',
        liner=liner)

    # Adjust outfile Suffix
    if not outfile is None:
        outfile = ut.get_adjusted_path(
            path=outfile,
            suffix='.oligopool.motif.csv')

    # Optional Argument Parsing
    liner.send('\n Optional Arguments\n')

    # Full motiftype Validation
    motiftype_valid = vp.get_categorical_validity(
        category=motiftype,
        category_field='    Motif Type    ',
        category_pre_desc=' ',
        category_post_desc=' Motifs',
        category_dict={
            0: 'Non-Constant',
            1: 'Constant'},
        liner=liner)

    # Store Context Names
    leftcontextname  = leftcontext
    rightcontextname = rightcontext

    # Full leftcontext Parsing and Validation
    (leftcontext,
    leftcontext_valid) = vp.get_parsed_column_info(
        col=leftcontext,
        df=indf,
        col_field='     Left Context ',
        col_desc='Input from Column',
        col_type=0,
        adjcol=rightcontextname,
        adjval=+1,
        iscontext=True,
        typecontext=0,
        liner=liner)

    # Full leftcontext Parsing and Validation
    (rightcontext,
    rightcontext_valid) = vp.get_parsed_column_info(
        col=rightcontext,
        df=indf,
        col_field='    Right Context ',
        col_desc='Input from Column',
        col_type=0,
        adjcol=leftcontextname,
        adjval=-1,
        iscontext=True,
        typecontext=1,
        liner=liner)

    # Full exmotifs Parsing and Validation
    (exmotifs,
    exmotifs_valid) = vp.get_parsed_exseqs_info(
        exseqs=exmotifs,
        exseqs_field=' Excluded Motifs  ',
        exseqs_desc='Unique Motif(s)',
        df_field='Exmotif',
        required=False,
        liner=liner)

    # First Pass Validation
    if not all([
        indata_valid,
        oligolimit_valid,
        motifseq_valid,
        maxreplen_valid,
        motifcol_valid,
        outfile_valid,
        motiftype_valid,
        leftcontext_valid,
        rightcontext_valid,
        exmotifs_valid]):
        liner.send('\n')
        raise RuntimeError(
            'Invalid Argument Input(s).')

    # Start Timer
    t0 = tt.time()

    # Adjust Numeric Paramters
    oligolimit = round(oligolimit)

    # Define Edge Effect Length
    edgeeffectlength = None

    # Motif Design Book-keeping
    targetcount = len(indf.index)
    has_context = False
    outdf = None
    stats = None
    warns = {}

    # Parse Oligopool Limit Feasibility
    liner.send('\n[Step 1: Parsing Oligo Limit]\n')

    # Parse oligolimit
    (parsestatus,
    minoligolen,
    maxoligolen,
    minelementlen,
    maxelementlen,
    minspaceavail,
    maxspaceavail) = ut.get_parsed_oligolimit(
        indf=indf,
        variantlens=None,
        oligolimit=oligolimit,
        minelementlen=len(motifseq),
        maxelementlen=len(motifseq),
        element='Motif',
        liner=liner)

    # oligolimit infeasible
    if not parsestatus:

        # Prepare stats
        stats = {
            'status'  : False,
            'basis'   : 'infeasible',
            'step'    : 1,
            'step_name': 'parsing-oligo-limit',
            'vars'    : {
                    'oligo_limit': oligolimit,
                 'limit_overflow': True,
                  'min_oligo_len': minoligolen,
                  'max_oligo_len': maxoligolen,
                'min_element_len': minelementlen,
                'max_element_len': maxelementlen,
                'min_space_avail': minspaceavail,
                'max_space_avail': maxspaceavail},
            'warns'   : warns}

        # Return results
        liner.close()
        return (outdf, stats)

    # Parse Excluded Motifs
    if not exmotifs is None:

        # Show update
        liner.send('\n[Step 2: Parsing Excluded Motifs]\n')

        # Update Step 2 Warning
        warns[2] = {
            'warn_count': 0,
            'step_name' : 'parsing-excluded-motifs',
            'vars': None}

        # Parse exmotifs
        (parsestatus,
        exmotifs,
        problens,
        leftpartition,
        rightpartition) = ut.get_parsed_exmotifs(
            exmotifs=exmotifs,
            typer=tuple,
            element='Motif',
            leftcontext=leftcontext,
            rightcontext=rightcontext,
            warn=warns[2],
            liner=liner)

        # Remove Step 2 Warning
        if not warns[2]['warn_count']:
            warns.pop(2)

        # exmotifs infeasible
        if not parsestatus:

            # Prepare stats
            stats = {
                'status'  : False,
                'basis'   : 'infeasible',
                'step'    : 2,
                'step_name': 'parsing-excluded-motifs',
                'vars'    : {
                     'prob_lens': problens,
                    'prob_count': tuple(list(
                        4**pl for pl in problens))},
                'warns'   : warns}

            # Return results
            liner.close()
            return (outdf, stats)

        # Update Edge-Effect Length
        edgeeffectlength = ut.get_edgeeffectlength(
            maxreplen=maxreplen,
            exmotifs=exmotifs)

    # Parsing Sequence Constraint Feasibility
    liner.send('\n[Step 3: Parsing Motif Sequence]\n')

    # Update Step 2 Warning
    warns[3] = {
        'warn_count': 0,
        'step_name' : 'parsing-motif-sequence',
        'vars': None}

    # Parse primerseq
    (optrequired,
    homology,
    fixedbaseindex,
    exmotifindex) = cm.get_parsed_sequence_constraint(
        motifseq=motifseq,
        exmotifs=exmotifs,
        warn=warns[3],
        liner=liner)

    # Remove Step 3 Warning
    if not warns[3]['warn_count']:
        warns.pop(3)

    # Parse Edge Effects
    if ((not optrequired is False) and \
        (not exmotifs    is None)) and \
       ((not leftcontext  is None) or \
        (not rightcontext is None)):

        # Set Context Flag
        has_context = True

        # Show Update
        liner.send('\n[Step 4: Extracting Context Sequences]\n')

        # Extract Both Contexts
        (leftcontext,
        rightcontext) = ut.get_extracted_context(
            leftcontext=leftcontext,
            rightcontext=rightcontext,
            edgeeffectlength=edgeeffectlength,
            reduce=False,
            liner=liner)

        # Show update
        liner.send('\n[Step 5: Parsing Edge Effects]\n')

        # Update Step 5 Warning
        warns[5] = {
            'warn_count': 0,
            'step_name' : 'parsing-edge-effects',
            'vars': None}

        # Compute Forbidden Prefixes and Suffixes
        (prefixdict,
        suffixdict) = cm.get_parsed_edgeeffects(
            motifseq=motifseq,
            motiftype=motiftype,
            leftcontext=leftcontext,
            rightcontext=rightcontext,
            leftpartition=leftpartition,
            rightpartition=rightpartition,
            exmotifs=exmotifs,
            element='Motif',
            warn=warns[5],
            liner=liner)

        # Remove Step 5 Warning
        if not warns[5]['warn_count']:
            warns.pop(5)

    # Finalize Context
    if not has_context:
        (leftcontext,
        rightcontext,
        prefixdict,
        suffixdict) = (None, None, None, None)

    # Parse Oligopool Repeats
    liner.send('\n[Step 6: Parsing Oligopool Repeats]\n')

    # Parse Repeats from indf
    (parsestatus,
    sourcecontext,
    kmerspace,
    fillcount,
    freecount,
    oligorepeats) = ut.get_parsed_oligopool_repeats(
        df=indf,
        maxreplen=maxreplen,
        element='Motif',
        merge=motiftype == 1,
        liner=liner)

    # Repeat Length infeasible
    if not parsestatus:

        # Prepare stats
        stats = {
            'status': False,
            'basis' : 'infeasible',
            'step'  : 6,
            'step_name': 'parsing-oligopool-repeats',
            'vars'  : {
                'source_context': sourcecontext,
                'kmer_space'    : kmerspace,
                'fill_count'    : fillcount,
                'free_count'    : freecount},
            'warns' : warns}

        # Return results
        liner.close()
        return (outdf, stats)

    # Launching Motif Design
    liner.send('\n[Step 7: Computing Motifs]\n')

    # Define Motif Design Stats
    stats = {
        'status'  : False,
        'basis'   : 'unsolved',
        'step'    : 7,
        'step_name': 'computing-motifs',
        'vars'    : {
               'target_count': targetcount,   # Required Number of Motifs
                'motif_count': 0,             # Motif Design Count
               'orphan_oligo': None,          # Orphan Oligo Indexes
                'repeat_fail': 0,             # Repeat Fail Count
               'exmotif_fail': 0,             # Exmotif Elimination Fail Count
                  'edge_fail': 0,             # Edge Effect Fail Count
            'exmotif_counter': cx.Counter()}, # Exmotif Encounter Counter
        'warns'   : warns}

    # Schedule outfile deletion
    ofdeletion = ae.register(
        ut.remove_file,
        outfile)

    # Design Motifs
    (motifs,
    stats) = cm.motif_engine(
        motifseq=motifseq,
        motiftype=motiftype,
        homology=homology,
        optrequired=optrequired,
        fixedbaseindex=fixedbaseindex,
        maxreplen=maxreplen,
        oligorepeats=oligorepeats,
        leftcontext=leftcontext,
        rightcontext=rightcontext,
        exmotifs=exmotifs,
        exmotifindex=exmotifindex,
        edgeeffectlength=edgeeffectlength,
        prefixdict=prefixdict,
        suffixdict=suffixdict,
        targetcount=targetcount,
        stats=stats,
        liner=liner)

    # Motif Status
    if stats['status']:
        motifstatus = 'Successful'
    else:
        motifstatus = 'Failed'

    # Insert motif into indf
    if stats['status']:

        # Update indf
        ut.update_df(
            indf=indf,
            lcname=leftcontextname,
            rcname=rightcontextname,
            out=motifs,
            outcol=motifcol)

        # Prepare outdf
        outdf = indf

        # Write outdf to file
        if not outfile is None:
            outdf.to_csv(
                path_or_buf=outfile,
                sep=',')

    # Motif Design Statistics
    liner.send('\n[Motif Design Statistics]\n')

    plen = ut.get_printlen(
        value=max(stats['vars'][field] for field in (
            'target_count',
            'motif_count')))

    liner.send(
        '  Design Status   : {}\n'.format(
            motifstatus))
    liner.send(
        '  Target Count    : {:{},d} Motif(s)\n'.format(
            stats['vars']['target_count'],
            plen))
    liner.send(
        '   Motif Count    : {:{},d} Motif(s) ({:6.2f} %)\n'.format(
            stats['vars']['motif_count'],
            plen,
            ut.safediv(
                A=stats['vars']['motif_count'] * 100.,
                B=targetcount)))
    liner.send(
        '  Orphan Oligo    : {:{},d} Entries\n'.format(
            len(stats['vars']['orphan_oligo']),
            plen))

    # Failure Relavant Stats
    if not stats['status']:
        maxval = max(stats['vars'][field] for field in (
            'repeat_fail',
            'exmotif_fail',
            'edge_fail'))

        sntn, plen = ut.get_notelen(
            printlen=ut.get_printlen(
                value=maxval))

        total_conflicts = stats['vars']['repeat_fail']  + \
                          stats['vars']['exmotif_fail'] + \
                          stats['vars']['edge_fail']

        liner.send(
            '  Repeat Conflicts: {:{},{}} Event(s) ({:6.2f} %)\n'.format(
                stats['vars']['repeat_fail'],
                plen,
                sntn,
                ut.safediv(
                    A=stats['vars']['repeat_fail'] * 100.,
                    B=total_conflicts)))
        liner.send(
            ' Exmotif Conflicts: {:{},{}} Event(s) ({:6.2f} %)\n'.format(
                stats['vars']['exmotif_fail'],
                plen,
                sntn,
                ut.safediv(
                    A=stats['vars']['exmotif_fail'] * 100.,
                    B=total_conflicts)))
        liner.send(
            '    Edge Conflicts: {:{},{}} Event(s) ({:6.2f} %)\n'.format(
                stats['vars']['edge_fail'],
                plen,
                sntn,
                ut.safediv(
                    A=stats['vars']['edge_fail'] * 100.,
                    B=total_conflicts)))

        # Enumerate Motif-wise Fail Counts
        if stats['vars']['exmotif_counter']:

            qlen = max(len(motif) \
                for motif in stats['vars']['exmotif_counter'].keys()) + 2

            sntn, vlen = ut.get_notelen(
                printlen=ut.get_printlen(
                    value=max(
                        stats['vars']['exmotif_counter'].values())))

            liner.send('   Exmotif-wise Conflict Distribution\n')

            for exmotif,count in stats['vars']['exmotif_counter'].most_common():
                exmotif = '\'{}\''.format(exmotif)
                liner.send(
                    '     - Motif {:>{}} Triggered {:{},{}} Event(s)\n'.format(
                        exmotif, qlen, count, vlen, sntn))

    # Show Time Elapsed
    liner.send(
        ' Time Elapsed: {:.2f} sec\n'.format(
            tt.time()-t0))

    # Unschedule outfile deletion
    if motifstatus == 'Successful':
        ae.unregister(ofdeletion)

    # Close Liner
    liner.close()

    # Return Solution and Statistics
    return (outdf, stats)
