import time
import gress

# init params
sheep = 100
sleep = 0.1

# EXAMPLE 1
print("\nEXAMPLE 1")
for i in gress.gress(range(sheep)):
    time.sleep(sleep)

# EXAMPLE 2
print("\nEXAMPLE 2")

# init bar
bar = gress.Bar("Counting: {count} of {maximum} ({percent}%) {bar} {speed}/s | {timer} | ETA {autoeta}", maximum=sheep)
bar.start()

# counting sheep
for i in range(sheep):
    time.sleep(sleep)
    
    # increment progress
    bar += 1
    
    # count slower while sleeping (50 sheep and more)
    if bar.current == sheep / 2:
        bar.write("{time} I should sleep now, so I'm counting slower...")
        sleep *= 2

# finish and make final report
bar.finish("{time} All {count} sheep counted in {autotimer} with the average rate of {speed}/s")
