#!/bin/bash
# Start server on port 8000 (avoiding AirPlay on 5000)
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
