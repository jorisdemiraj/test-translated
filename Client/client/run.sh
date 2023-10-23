#!/bin/bash
python3  start_server.py &
streamlit run gui.py &


wait
