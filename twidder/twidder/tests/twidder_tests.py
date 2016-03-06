#!/usr/bin/env python

from TwidderTester import TwidderTester
import os
import subprocess

twidder_host = "localhost"
twidder_port = "5000"
twidder_path = "/"

user1 = ["test1@test1.com",
    "123",
    "John",
    "Doe",
    "Linkoping",
    "Sweden",
    "Male"
    ]

user2 = ["test2@test2.com",
    "123",
    "Ewa",
    "Goldman",
    "Stockholm",
    "Sweden",
    "Female"
    ]

# ---------------------

if __name__ == "__main__":
    # Fetch site
    tester = TwidderTester(twidder_host, twidder_port, twidder_path)

    # Sign up
    tester.sign_up(user1[0], user1[1], user1[2], user1[3], user1[4], user1[5], user1[6])
    tester.sign_up(user2[0], user2[1], user2[2], user2[3], user2[4], user2[5], user2[6])

    # Sign in
    tester.sign_in(user1[0], user1[1])
