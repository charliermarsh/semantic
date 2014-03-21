import unittest


def run():
    testsuite = unittest.TestLoader().discover('.')
    unittest.TextTestRunner(verbosity=1).run(testsuite)

if __name__ == '__main__':
    run()
