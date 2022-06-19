# Guessing with Noise
 
This simulates a guess-the-number game, where answers can be randomly flipped.

The guessing game picks a secret number.
For each incorrect guess, it tells you if it's higher or lower,
but the catch is that it provides bad information a small percentage of the time.
Each number may be guessed only once, or in other words,
guessing the same number multiple times will produce the same response, right or wrong.

The game is played using a strategy that keeps track of each interval between guesses
along with the probability that the secret number is in that interval.

Dependencies:

* python >= 3.10.5
