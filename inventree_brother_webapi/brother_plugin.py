"""Brother label printing via web API plugin for InvenTree.

Supports printing of labels via brother_ql_web API
"""


# translation
from django.utils.translation import ugettext_lazy as _

from plugins.inventree_brother_webapi.version import BROTHER_PLUGIN_VERSION

from brother_ql.labels import ALL_LABELS
import requests
import io

# InvenTree plugin libs
from plugin import InvenTreePlugin
from plugin.mixins import LabelPrintingMixin, SettingsMixin


def get_label_choices():
    """
    Return a list of available label types
    """

    return [(label.identifier, label.name) for label in ALL_LABELS]


def get_rotation_choices():
    """
    Return a list of available rotation angles
    """

    return [("standard", "Standard"), ("rotated", "Rotated")]


class BrotherLabelPlugin(LabelPrintingMixin, SettingsMixin, InvenTreePlugin):

    AUTHOR = "Jan Krajdl"
    DESCRIPTION = "Label printing plugin for Brother printers via web API"
    VERSION = BROTHER_PLUGIN_VERSION

    NAME = "Brother Web API printer"
    SLUG = "brotherwebapi"
    TITLE = "Brother Label Printer via API"

    SETTINGS = {
        'LABEL': {
            'name': _('Label Media'),
            'description': _('Select label media type'),
            'choices': get_label_choices,
            'default': '12',
        },
        'API_URL': {
            'name': _('API URL address'),
            'description': _('Complete URL address where is running brother_ql_web application'),
            'default': 'http://'
        },
        'AUTO_CUT': {
            'name': _('Auto Cut'),
            'description': _('Cut each label after printing'),
            'validator': bool,
            'default': True,
        },
        'ROTATION': {
            'name': _('Rotation'),
            'description': _('Rotation of the image on the label'),
            'choices': get_rotation_choices,
            'default': 'rotated',
        },
    }

    def print_label(self, **kwargs):
        """
        Send the label to the api
        """


        # Extract width (x) and height (y) information
        # width = kwargs['width']
        # height = kwargs['height']

        # Extract image from the provided kwargs
        label_image = kwargs['png_file']
        img_bytes = io.BytesIO()
        label_image.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()

        # Read settings
        api_url = self.get_setting('API_URL') + '/labeldesigner/api/print'

        # Generate instructions for printing
        params = {
            'print_type': 'image',
            'print_count': 1,
            'orientation': self.get_setting('ROTATION'),
            'cut_once': int(not self.get_setting('AUTO_CUT')),
            'label_size': self.get_setting('LABEL')
        }

        requests.post(api_url, data=params, files={'image': ('label.png', img_bytes)})
