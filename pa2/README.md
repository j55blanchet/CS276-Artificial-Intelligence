## Instructions

To run the full suite of tests, I recommend you install `pytest` with `pip install pytest`. THen simply run `pytest` in the root of this project directory.

To run any invidual test, you can simply add a call to the test function later on in the file and run that file.

For example, to run `test_maze4` individually in `test_mazeworld.py`, you'd add the following line to the end of the file:

    test_maze4()

Then you can execute the file with:

    python3 test_mazeworld.py

To see the output animation, you may want to edit the `animate` parameter in the `run_astar` method.


## Notes

I wrote this program using Python 3.8. If it doesn't run on older versions, it's possible that I used some features only available in 3.8+ versions of python.