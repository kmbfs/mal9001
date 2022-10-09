import sys

class TestMarry:

    def test_run_marry(self):
        sys.stdin = open("test_inputs.txt")
        import marry
        sys.stdin = sys.__stdin__
