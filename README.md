# Evolutionary Pong AI

**Date:** September 24–26, 2025 (Age 15)  
**Platform:** VS Code  
**Language:** Python 3

## What It Is
A Pong simulation where both paddles are controlled by AIs that learn through evolutionary computation. The paddles start out making random movements and eventually learn to track the ball and rally consistently.

## Why I Built It
I kept seeing videos of AIs learning to play games, and I thought they were fascinating. I wanted to try building my own self-learning AI from scratch instead of using existing ML frameworks.

## How It Works
Each paddle has a set of weighted parameters controlling its movement. After each round, the losing paddle adopts a mutated version of the winner’s weights, with mutation scaled based on how long the winner survived. Over time, this process moves both paddles from randomness toward consistent ball-tracking behavior. The main challenge was balancing the mutation and fitness behavior so the AIs could converge without locking into sloppy solutions.

## How I Built It
I researched evolutionary computation and reinforcement-style learning approaches, then applied the core ideas to a simple Pong environment. I used parameter weights for paddle decisions, mutation for variation, and survival time as a fitness signal. Most of the work went into tuning behavior and figuring out how to prevent degenerate strategies or stagnation.

## How to Run
Requires Python + `pygame`.

```bash
python pong.py
