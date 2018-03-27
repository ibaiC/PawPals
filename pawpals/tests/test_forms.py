from django.test import TestCase

from pawpals.forms import *

# All form validations are made by Django and we had no special model attributes
# to test due to this.
# The only exception being DateTimeField fields which were instantly populated
# with the date and time of the creation of the object instance therefore, no
# impossible value could be passed to it.
