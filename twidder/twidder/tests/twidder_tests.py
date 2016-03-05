#!/usr/bin/env python

from TwidderTester import TwidderTester

twidder_host = "localhost"
twidder_port = "5000"
twidder_path = "/"

# ---------------------

if __name__ == "__main__":
    tester = TwidderTester(twidder_host, twidder_port, twidder_path)
    tester.sign_up()
