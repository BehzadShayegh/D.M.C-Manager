#!/bin/bash
cd code/
python3 CSVReader.py
python3 ScoreBoard.py & python3 RefereeBench.py
python3 CSVWriter.py