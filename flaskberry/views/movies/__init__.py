# -*- coding: utf-8 -*-
from flask import Blueprint

mod = Blueprint('movies', __name__)

import routes, events
