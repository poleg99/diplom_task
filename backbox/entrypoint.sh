#!/bin/bash
flask db migrate
flask db upgrade
python back_api.py
