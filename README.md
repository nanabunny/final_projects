# final_projects
# Topic
Monte Carlo simulation for different Random Number Generators (RNG) algorithms in gaming, with user interaction
Random Number Generators (RNGs) are a set of algorithms that generates numbers by random chance, and plays an important role in game development. A simple case for RNG can be a coinflip to determine hit or miss for certain skill. For some specific gaming genres, RNG is playing an extremely important role, as it is involved in the core gameplay and directly affect user’s gaming experience.
RNG has to be chose very carefully for gaming. However, an RNG that provide good randomness may not guarantee a good user experience. Most pseudorandom number generator (pseudo-RNG) can generate usable random number sequences, but results in bad user experience.
In this project, I am proposing a simplified RNG-based gaming model with user interaction involved,  and illustrate how different RNGs will affect the user experience and users retention rate.
# Hypothesis
Different RNG algorithms will affect users’ gaming experience, thus having influence on users retention rate. Pseudo random is better.
# Assumption
1. Game: The game is relatively easy. I model the game as an RNG that produces sequence of 0s and 1s. Different RNG will be used for the game. 
2. Player: The players are modeled as a connected graph. Each node represents a player, and edge between nodes means the 2 players knows each other. Connected nodes can share the generated sequence, so each player knows the sequence generated for itself and players connected as well.
3. Hit or not?: In my project, the PRD sequence is generated according to the method used in DOTA2. Given the nominal chance, we can get a C value. The probability of an effect to occur on the Nth test since the last successful occur is given by P(N) = C × N. 
4. Value: Given the nominal rate and the number of trails that we try, the program will generate a sequence recording at what times we get a hit. The value of a player is defined as the length of this generated sequence for the player, that is, the number of hits we get, from specific number of trails at specific rate.
5. Satisfying factor: The satisfying factor is defined as the sum of difference of sequence lengths between player x and all its connected players divided by the number of connected players.
6. Uniformity factor: The sum of satisfying factors of all players in one graph. Smaller uniformity factor means a more general gaming experience.
Leaving game: Player with satisfactory lower than a certain threshold for certain rounds of gameplay will leave the game, with the sequence stop to generate, but the node, value and edges will still keep in the graph. By doing so, we can get users retention rate under two kinds of algorithms.
# Conclusion
The conclusion is that under pseudo random algorithm, the quality of game experience will be more stable, and game players will have higher satisfaction degrees. Under pseudo random, in certain rounds of games, the retention rate will be higher than true random.
# Reference
The C value is referenced from DOTA2. https://dota2.gamepedia.com/Random_distribution
