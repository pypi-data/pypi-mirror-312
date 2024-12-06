Primate AI
==========

Primate AI is a Python package that bridges decision-making and natural language processing, inspired by intelligent behavior.

Features
--------

- **Decision-Making Models**
  - Game-theoretic strategies (e.g., tit-for-tat).
  - Multi-agent simulations.
  - Reinforcement learning agents.

- **Natural Language Processing**
  - Sentiment analysis.
  - Tokenization and text similarity.
  - Language evolution simulation.

Installation
------------

You can install the package via pip::

    pip install primate

Quick Start
-----------

Example usage:

.. code-block:: python

    # Decision Agent
    from primate.decision.agent import DecisionAgent
    agent = DecisionAgent(strategy="tit_for_tat")
    decision = agent.decide(opponent_action="cooperate")
    print(f"Agent decided to: {decision}")

    # Sentiment Analysis
    from primate.nlp.sentiment import SentimentAnalyzer
    analyzer = SentimentAnalyzer()
    print(analyzer.analyze("I love bananas!"))  # Output: "positive"

License
-------

This project is licensed under the MIT License.
