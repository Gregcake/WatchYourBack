python main.py < massacre-sample-1.in > massacre-test-1.out
fc massacre-test-1.out massacre-sample-1.out
pause
python main.py < massacre-sample-2.in > massacre-test-2.out
fc massacre-test-2.out massacre-sample-2.out
pause
python main.py < massacre-sample-3.in > massacre-test-3.out
fc massacre-test-3.out massacre-sample-3.out
pause
python main.py < move-sample-1.in > move-test-1.out
fc move-test-1.out move-sample-1.out
pause
python main.py < move-sample-2.in > move-test-2.out
fc move-test-2.out move-sample-2.out
pause
python main.py < move-sample-3.in > move-test-3.out
fc move-test-3.out move-sample-3.out
pause
del massacre-test-1.out
del massacre-test-2.out
del massacre-test-3.out
del move-test-1.out
del move-test-2.out
del move-test-3.out