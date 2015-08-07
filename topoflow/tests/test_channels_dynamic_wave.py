#!/usr/bin/env python
#
# Tests the ChannelsDynamWave TopoFlow component.
#
# site_prefix = 'Treynor'
# case_prefix = 'June_20_67'
#
# Required input files:
# - June_20_67_channels_dynamic_wave.cfg
# - Treynor.rti
# - Treynor_slope.rtg
# - Treynor_chan-a.rtg
# - Treynor_chan-n.rtg
# - Treynor_chan-w.rtg
# - Treynor_flow.rtg

from os import makedirs, listdir
from os.path import join, dirname, exists
from shutil import rmtree
import numpy as np
from nose.tools import raises, assert_is_instance, assert_is_not_none
from topoflow.components.channels_dynamic_wave import channels_component
from . import input_dir, output_dir


def setup_module():
    global comp
    comp = channels_component()
    if not exists(output_dir):
        makedirs(output_dir)


def teardown_module():
    parent_dir = dirname(output_dir)
    if exists(parent_dir):
        rmtree(parent_dir)


def test_is_instance():
    assert_is_instance(comp, channels_component)


# The variable 'dinv' is undefined in channels_dynamic_wave.py.
@raises(NameError)
def test_irf():
    cfg_file = join(input_dir, 'June_20_67_channels_dynamic_wave.cfg')

    # @mperignon found these attributes are needed but not provided.
    comp.P_rain = 100
    comp.SM = 0
    comp.ET = 0
    comp.GW = 0
    comp.IN = 0
    comp.MR = 0
    comp.rho_H2O = 1000
    comp.S_free = np.zeros((44, 29))  # shape from Treynor.rti

    comp.initialize(cfg_file)
    comp.update()
    comp.finalize()


def test_has_output():
    assert_is_not_none(listdir(output_dir))
