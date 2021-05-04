# Spirit Island

This project was born from the intersection of two of my deepest passions: analytics and strategy games. I'll be looking at my favorite cooperative anti-colonial strategy game, Spirit Island, to answer the following questions:

1. How does design of game mechanics affect player experience?
2. How optimal are common strategies in the community?
3. Is there an "optimal" strategy to play out each turn?

## Why Spirit Island?

As a slight board game enthusiast, Spirit Island is a breath of fresh air among other competitive games (often with colonial overtones). Playing *with* and not *against* other players is in itself a rewarding social experience that supports intricately crafted game mechanics that make for a surprisingly cohesive playing experience. The game is fundamentally about achieving a team goal under resource constraints. Additionally it is a largely asymmetrical game where players are subject to different constraints and have access to different information. In theory, information asymmetry can be overcome through effective communication but in practice, this is seldom practical due to the large volume of information each player has to independently process before collaboration.

In every turn, Spirit Island offers a large volume of information to players. For an experienced player, this helps with finding near optimal solutions under tight constraints. However, for newer players, this can easily be overwhelming to the point that it's hard to begin to understand what to do. Ideally, at the end of this project, I would also like to achieve a personal goal of deploying a decision support system to help new players. The ideal result should have the following features:

1. Accessible statistics to help understand complex board states at a glance.
2. Forecast the short term (1-2 turns) effects of player actions under game variance.
3. Live strategy suggestions for optimal/near-optimal plays.

## Roadmap

### Stage 1: Descriptive Analysis of game components

Here, I hope to better understand how different aspects of the game design may affect player exerience. In particular,
- Network analysis of game boards to identify if any lands are more important.
- Examine bias arising from interactions between the distribution of lands in different boards and the invader deck.
- Correlation analysis between powers and their elemental value/cost.

Hopefully, I can load up a significant portion of the game information into a database and get up a simple dashboard that provides analytics for a static game state in this stage.

### Stage 2: Short run game dynamics

### Stage 3: Long run game dynamics