#!/bin/zsh
time ./pipeline_test.py 1 19.594083 8.669111 53992.3861186 8 0  > /tmp/test00.done &
time ./pipeline_test.py 1 19.594083 8.669111 53992.3861186 8 1  > /tmp/test01.done &
time ./pipeline_test.py 1 19.594083 8.669111 53992.3861186 8 2  > /tmp/test02.done &
time ./pipeline_test.py 1 19.594083 8.669111 53992.3861186 8 3  > /tmp/test03.done &
time ./pipeline_test.py 1 19.594083 8.669111 53992.3861186 8 4  > /tmp/test04.done &
time ./pipeline_test.py 1 19.594083 8.669111 53992.3861186 8 5  > /tmp/test05.done &
time ./pipeline_test.py 1 19.594083 8.669111 53992.3861186 8 6  > /tmp/test06.done &
time ./pipeline_test.py 1 19.594083 8.669111 53992.3861186 8 7  > /tmp/test07.done &

