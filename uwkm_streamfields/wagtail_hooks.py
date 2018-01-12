#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018-01-12 michael_yin
#

"""

"""

from django.conf import settings
from wagtail.wagtailcore import hooks


@hooks.register('insert_editor_js')
def editor_js():
    s = """<script type="text/javascript">var collapse = false;</script>"""
    s += """<script src="{0}colorpicker/js/colorpicker.js"></script>"""
    s += """<script src="{0}js/custom-admin.js"></script>"""
    s += """<script src="{0}js/colorPicker.js"></script>"""
    return s.format(settings.STATIC_URL)

@hooks.register('insert_editor_css')
def editor_css():
    s = """<link rel="stylesheet" href="{0}colorpicker/css/colorpicker.css"></link>"""
    s += """<link rel="stylesheet" href="{0}css/custom-admin.css"></link>"""
    return s.format(settings.STATIC_URL)
