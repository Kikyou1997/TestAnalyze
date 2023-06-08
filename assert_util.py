def assert_equals(expect, actual, message=""):
    try:
        assert expect == actual
    except AssertionError as e:
        print('Expect ' + str(expect))
        print('Actual ' + str(actual))
        if len(message) > 0:
            print(message)
        raise e
