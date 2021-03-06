#!/usr/bin/env python
#
# Tests the Diversions TopoFlow component.
#
# site_prefix = 'Treynor'
# case_prefix = 'June_20_67'
#
# Required input files:
# - June_20_67_diversions_fraction_method.cfg  # note filename
# - Treynor.rti

from shutil import rmtree
from os import makedirs, listdir
from os.path import join, dirname, exists
from nose.tools import assert_is_instance, assert_is_not_none
from numpy.testing import assert_almost_equal
from topoflow.components.diversions_base import diversions_component as Model
from . import input_dir, output_dir, time_factor


cfg_file = join(input_dir, 'June_20_67_diversions_fraction_method.cfg')


def setup_module():
    global comp
    comp = Model()
    if not exists(output_dir):
        makedirs(output_dir)


def teardown_module():
    parent_dir = dirname(output_dir)
    if exists(parent_dir):
        rmtree(parent_dir)


def test_is_instance():
    assert_is_instance(comp, Model)


def test_irf():
    comp.initialize(cfg_file)
    comp.update()
    comp.finalize()


def test_has_output():
    assert_is_not_none(listdir(output_dir))


def test_update_frac():
    time_step = comp.get_time_step()
    frac_time = 1.0 / time_factor

    comp.initialize(cfg_file)
    comp.update_frac(frac_time)
    end_time = comp.get_current_time()
    comp.finalize()
    assert_almost_equal(end_time, frac_time*time_step)


def test_update_until():
    time_step = comp.get_time_step()
    until_time = time_step*time_factor + time_step/time_factor

    comp.initialize(cfg_file)
    comp.update_until(until_time)
    end_time = comp.get_current_time()
    comp.finalize()
    assert_almost_equal(end_time, until_time)
