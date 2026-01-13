#!/usr/bin/env python
"""
Script para correr Flask sin debug mode
"""
import os
os.environ['FLASK_ENV'] = 'production'

from app import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
