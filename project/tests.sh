#!/bin/bash
echo "Running tests..."
<<<<<<< HEAD
python tests.py
echo "Tests completed. Press any key to continue..."
read -n 1
=======
python3 -m unittest discover -s tests -p "test_*.py"
>>>>>>> 2acda3362eb5b77c1054625adeec2375ac7adbc3
