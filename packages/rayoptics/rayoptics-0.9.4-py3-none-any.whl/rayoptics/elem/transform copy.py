#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright © 2018 Michael J. Hayford
""" Useful transforms for processing sequential models

.. Created on Fri Feb  9 10:09:58 2018

.. codeauthor: Michael J. Hayford
"""

import numpy as np
import itertools


def compute_global_coords(sm, glo=1, origin=None):
    """ Return global surface coordinates (rot, t) wrt surface glo. 
    
    If origin isn't None, it should be a tuple (r, t) being the transform
      from the desired global origin to the specified global surface.
    """
    def accumulate_transforms(seq, b4_seg, transform_calc, 
                              tfrm_prev, glo_z_dir):
        b4_ifc, b4_gap, b4_z_dir = b4_seg
        r_prev, t_prev = tfrm_prev
        for (ifc, gap, z_dir) in seq:
            zdist = b4_gap.thi
            r, t = transform_calc(b4_ifc, zdist, b4_z_dir, glo_z_dir, ifc)

            t_new = np.matmul(r_prev, t) + t_prev
            r_new = np.matmul(r_prev, r)

            tfrms.append((r_new, t_new))
            r_prev, t_prev = r_new, t_new
            b4_ifc, b4_gap, b4_z_dir = ifc, gap, z_dir

    # Initialize origin of global coordinate system.
    tfrms = []
    if origin is None:
        r_origin, t_origin = np.identity(3), np.array([0., 0., 0.])
    else:
        r_origin, t_origin = origin
    tfrm_origin = r_origin, t_origin
    tfrms.append(tfrm_origin)

    # Compute transforms from global surface to object surface
    if glo > 0:
        # iterate in reverse over the segments before the
        #  global reference surface
        step = -1
        seq = itertools.zip_longest(sm.ifcs[glo::step],
                                    sm.gaps[glo-1::step],
                                    sm.z_dir[glo-1::step])
        ifc, gap, z_dir = b4_seg = next(seq)
        glo_b4_z_dir = -z_dir
        # loop of remaining surfaces in path
        accumulate_transforms(seq, b4_seg, reverse_transform, 
                              tfrm_origin, glo_b4_z_dir)
        tfrms.reverse()

    # Compute transforms from global surface to image surface
    seq = itertools.zip_longest(sm.ifcs[glo:], sm.gaps[glo:], sm.z_dir[glo:])
    b4_ifc, b4_gap, b4_z_dir = b4_seg = next(seq)
    glo_z_dir = b4_z_dir
 
    accumulate_transforms(seq, b4_seg, forward_transform, 
                          tfrm_origin, glo_z_dir)

    return tfrms


def compute_global_coords_prev(sm, glo=1, origin=None):
    """ Return global surface coordinates (rot, t) wrt surface glo. 
    
    If origin isn't None, it should be a tuple (r, t) being the transform
      from the desired global origin to the specified global surface.
    """
    tfrms = []
    if origin is None:
        r_prev, t_prev = np.identity(3), np.array([0., 0., 0.])
    else:
        r_prev, t_prev = origin
    tfrms.append((r_prev, t_prev))

    if glo > 0:
        # iterate in reverse over the segments before the
        #  global reference surface
        step = -1
        seq = itertools.zip_longest(sm.ifcs[glo::step],
                                    sm.gaps[glo-1::step],
                                    sm.z_dir[glo-1::step])
        ifc, gap, z_dir = next(seq)
        glo_b4_z_dir = -z_dir
        # loop of remaining surfaces in path
        while True:
            try:
                b4_ifc, b4_gap, b4_z_dir = next(seq)
                zdist = gap.thi
                r, t = reverse_transform(ifc, zdist, z_dir, 
                                         glo_b4_z_dir, b4_ifc)

                t_new = np.matmul(r_prev, t) + t_prev
                r_new = np.matmul(r_prev, r)

                tfrms.append((r_new, t_new))
                r_prev, t_prev = r_new, t_new
                ifc, gap, z_dir = b4_ifc, b4_gap, b4_z_dir
            except StopIteration:
                break
        tfrms.reverse()

    seq = itertools.zip_longest(sm.ifcs[glo:], sm.gaps[glo:], sm.z_dir[glo:])
    b4_ifc, b4_gap, b4_z_dir = next(seq)
    glo_z_dir = b4_z_dir
    if origin is None:
        r_prev, t_prev = np.identity(3), np.array([0., 0., 0.])
    else:
        r_prev, t_prev = origin
        if r_prev is None:
            r_prev = np.identity(3)

    # loop forward over the remaining surfaces in path
    while True:
        try:
            ifc, gap, z_dir = next(seq)
            zdist = b4_gap.thi
            r, t = forward_transform(b4_ifc, zdist, b4_z_dir, glo_z_dir, ifc)

            t_new = np.matmul(r_prev, t) + t_prev
            r_new = np.matmul(r_prev, r)

            tfrms.append((r_new, t_new))
            r_prev, t_prev = r_new, t_new
            b4_ifc, b4_gap, b4_z_dir = ifc, gap, z_dir
        except StopIteration:
            break

    return tfrms


def forward_transform(s1, zdist, zdir, glo_zdir, s2):
    """ generate transform rotation and translation from
        s1 coords to s2 coords """

    t_orig = glo_zdir * np.array([0., 0., zdist])
    r_after_s1 = r_before_s2 = None
    if s1.decenter:
        r_after_s1, t_after_s1 = s1.decenter.tform_after_surf()
        t_orig += t_after_s1

    if s2.decenter:
        r_before_s2, t_before_s2 = s2.decenter.tform_before_surf()
        t_orig += t_before_s2

    r_cascade = np.identity(3)
    if r_after_s1 is not None:
        t_orig = np.matmul(r_after_s1, t_orig)
        r_cascade = r_after_s1
        if r_before_s2 is not None:
            r_cascade = np.matmul(r_after_s1, r_before_s2)
    elif r_before_s2 is not None:
        r_cascade = r_before_s2

    return r_cascade, t_orig


def reverse_transform(s1, zdist, zdir, glo_zdir, s2):
    """ generate transform rotation and translation from
        s1 coords to s2 coords, applying transforms in the reverse order """
    t_orig = glo_zdir * np.array([0., 0., zdist])
    r_before_s1 = r_after_s2 = None
    if s1.decenter:
        r_before_s1, t_before_s1 = s1.decenter.tform_before_surf()
        t_orig += t_before_s1

    if s2.decenter:
        r_after_s2, t_after_s2 = s2.decenter.tform_after_surf()
        t_orig += t_after_s2

    r_cascade = np.identity(3)
    if r_before_s1 is not None:
        r_cascade = r_before_s1.transpose()
        t_orig = np.matmul(r_cascade, t_orig)
        if r_after_s2 is not None:
            r_cascade = np.matmul(r_cascade, r_after_s2.transpose())
    elif r_after_s2 is not None:
        r_cascade = r_after_s2.transpose()

    return r_cascade, t_orig


def forward_transform_orig(s1, zdist, s2):
    """ generate transform rotation and translation from
        s1 coords to s2 coords """

    # calculate origin of s2 wrt to s1
    t_orig = np.array([0., 0., zdist])
    r_after_s1 = r_before_s2 = None
    if s1.decenter:
        # get transformation info after s1
        r_after_s1, t_after_s1 = s1.decenter.tform_after_surf()
        t_orig += t_after_s1

    if s2.decenter:
        # get transformation info before s2
        r_before_s2, t_before_s2 = s2.decenter.tform_before_surf()
        t_orig += t_before_s2

    r_cascade = np.identity(3)
    if r_after_s1 is not None:
        # rotate the origin of s2 around s1 "after" transformation
        t_orig = r_after_s1.dot(t_orig)
        r_cascade = r_after_s1
        if r_before_s2 is not None:
            r_cascade = r_after_s1.dot(r_before_s2)
    elif r_before_s2 is not None:
        r_cascade = r_before_s2

    return r_cascade, t_orig


def reverse_transform_orig(s1, zdist, s2):
    """ generate transform rotation and translation from
        s2 coords to s1 coords """

    # calculate origin of s2 wrt to s1
    t_orig = np.array([0., 0., zdist])
    r_after_s1 = r_before_s2 = None
    if s1.decenter:
        # get transformation info after s1
        r_after_s1, t_after_s1 = s1.decenter.tform_before_surf()
        t_orig += t_after_s1

    if s2.decenter:
        # get transformation info before s2
        r_before_s2, t_after_s2 = s2.decenter.tform_after_surf()
        t_orig += t_after_s2

    # going in reverse direction so negate translation
    t_orig = -t_orig

    r_cascade = np.identity(3)
    if r_before_s2 is not None:
        # rotate the origin of s1 around s2 "before" transformation
        r_cascade = r_before_s2.transpose()
        t_orig = r_cascade.dot(t_orig)
        if r_after_s1 is not None:
            r_cascade = r_cascade.dot(r_after_s1.transpose())
    elif r_after_s1 is not None:
        r_cascade = r_after_s1.transpose()

    return r_cascade, t_orig


def cascade_transform(r_prev, t_prev, r_seg, t_seg):
    """ take the seg transform and cascade it with the prev transform """
    return r_prev.dot(r_seg), r_prev.dot(t_seg) + t_prev


def transfer_coords(r_seg, t_seg, pt_s1, dir_s1):
    """ take p and d in s1 coords of seg and transfer them to s2 coords """
    rt = r_seg.transpose()
    return rt.dot(pt_s1 - t_seg), rt.dot(dir_s1)


def transform_before_surface(interface, ray_seg):
    """Transform ray_seg from interface to previous seg.

    Args:
        interface: the :class:'~seq.interface.Interface' for the path sequence
        ray_seg: ray segment exiting from **interface**

    Returns:
        (**b4_pt**, **b4_dir**)

        - **b4_pt** - ray intersection pt wrt following seg
        - **b4_dir** - ray direction cosine wrt following seg
    """
    if interface.decenter:
        # get transformation info after surf
        r, t = interface.decenter.tform_before_surf()
        if r is None:
            b4_pt, b4_dir = (ray_seg[0] - t), ray_seg[1]
        else:
            rt = r.transpose()
            b4_pt, b4_dir = rt.dot(ray_seg[0] - t), rt.dot(ray_seg[1])
    else:
        b4_pt, b4_dir = ray_seg[0], ray_seg[1]

    return b4_pt, b4_dir


def transform_after_surface(interface, ray_seg):
    """Transform ray_seg from interface to following seg.

    Args:
        interface: the :class:'~seq.interface.Interface' for the path sequence
        ray_seg: ray segment exiting from **interface**

    Returns:
        (**b4_pt**, **b4_dir**)

        - **b4_pt** - ray intersection pt wrt following seg
        - **b4_dir** - ray direction cosine wrt following seg
    """
    if interface.decenter:
        # get transformation info after surf
        r, t = interface.decenter.tform_after_surf()
        if r is None:
            b4_pt, b4_dir = (ray_seg[0] - t), ray_seg[1]
        else:
            rt = r.transpose()
            b4_pt, b4_dir = rt.dot(ray_seg[0] - t), rt.dot(ray_seg[1])
    else:
        b4_pt, b4_dir = ray_seg[0], ray_seg[1]

    return b4_pt, b4_dir
