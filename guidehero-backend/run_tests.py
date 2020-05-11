import sys
import unittest


if __name__ == '__main__':
    pattern = '*.*'
    if len(sys.argv) > 1:
        pattern = sys.argv[1]
    print(pattern)
    from tests.environment import create_test_environment
    create_test_environment()
    suite = unittest.TestLoader().discover('tests', pattern=pattern)
    unittest.TextTestRunner(verbosity=2).run(suite)
