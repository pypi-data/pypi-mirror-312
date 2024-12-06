# Utility-Lens

A Python library for analyzing pairwise preferences of language models. Features utility and transitivity analysis with Bradley-Terry and Thurstonian models.

## Installation

```bash
pip install utility-lens
```

## Demos

Two types of analyses are provided: Utility Analysis and Transitivity Analysis. (Nov-30-2024)

### A. Utility Computation

Uses Bradley-Terry or Thurstonian models to compute the perceived cardinal utilities of items based on pairwise comparisons from an LLM.

```python
from utility_lens import OpenAIModel, UtilityAnalyzer
import numpy as np

# Required: OpenAI API key
openai_api_key = 'api_key'

# Required: List of items to compare
animals = [ "elephant", "human", "chimpanzee", "komodo", "lion", "giraffe", "hippopotamus", "kangaroo", "platypus", "dolphin", "penguin", "octopus", "seahorse", "rhinoceros", "zebra", "gorilla", "koala", "sloth", "panda", "camel", "ostrich", "eagle", "beaver", "otter", "wolf", "bear", "walrus", "seal", "llama", "flamingo", "crocodile", "iguana", "cobra", "tortoise", "salamander", "tuna", "shark", "manta", "jellyfish", "squirrel", "moose", "bison", "orangutan", "peacock", "macaw", "swan", "lemur", "raccoon", "armadillo", "hedgehog"]

###################
# Initialize model#
###################
model = OpenAIModel(
    # Required parameters:
    model_name="gpt-3.5-turbo-0125",  # Required: Name of model to use
    api_key=openai_api_key,           # Required: OpenAI API key

    # Optional parameters (with defaults):
    base_url=None,       # Optional (default=None): Base URL for API 
    max_tokens=10,       # Optional (default=10): Max tokens in response
    concurrency_limit=50,# Optional (default=50): Max concurrent calls
                         #  Doesn't mean much unless using async
)

#########################
# Initialize analyzer   #
#########################
analyzer = UtilityAnalyzer(
    # Required parameters:
    model=model,            # Required: Model instance to use
    items=animals,          # Required: List of items to compare

    # Optional parameters (with defaults):
    n_trial=10,             # Optional (default=10): # samples per pair 
    n_pairs=None,           # Default=200: Use 200 out of all possible  
                            #  pairs. Can also use -1 or None for all 
                            #  pairs or specify a number
    seed=42,                # Optional (default=42): Random seed 
    save_directory="results"# Optional (default=None): Set to save 
                            #  None means don't save results
)

############################################
# Run Bradley-Terry/Thurstonian analysis   #
############################################
bt_results = analyzer.run(
    # All parameters are optional with defaults shown:
    method="bradley-terry", # Optional (default="bradley-terry")
                            #  Model type to use ("bradley-terry" or 
                            #  "thurstonian")
    use_soft_labels=True,   # Optional (default=True): Use ratios vs binary
                            #  True = actual ratios (e.g., 7:3)
                            #  False = binary preferences (e.g., 1 or 0)
    num_epochs=1000,        # Optional (default=1000): Number of training epchs
    learning_rate=0.01,     # Optional (default=0.01): LR for optimization
    use_async=True          # Optional (default=True): Processing mode
                            #  False: Sequential (works everywhere)
                            #  True: Concurrent(faster but needs async support)
)

############################################
# Results dictionary structure explanation #
############################################

# Bradley-Terry results structure:
# {
#    'utilities': Dict,    # Maps item index to utility value
#                          # Example: {0: 1.2, 1: 0.8, 2: -0.5}
#    'rankings': List,     # Sorted (item, utility) pairs
#                          # Example: [("elephant", 1.2), ("human", 0.8)]
#    'accuracy': float,    # Model prediction accuracy (0-1)
#    'log_loss': float,    # Model log loss
#    'raw_data': Dict      # Raw preference data collected from model
# }

# Thurstonian results structure:
# {
#    'utilities': Dict,   # Maps item index to mean and variance
#                         # Example: {0: {'mean': 1.2, 'variance': 0.1}}
#    'rankings': List,    # Sorted by mean utility
#                         # Example: [("..", {'mean': 1, 'variance': 1})]
#    'accuracy': float,   # Model prediction accuracy (0-1)
#    'log_loss': float,   # Model log loss
#    'raw_data': Dict     # Raw preference data collected from model
# }
```

### B. Transitivity Analysis
Analyzes the consistency of an LLM's pairwise preferences by checking for cycles and violations of transitivity principles.

```python
from utility_lens import OpenAIModel, TransitivityAnalyzer

# Required: OpenAI API key
openai_api_key = 'api_key'

# Required: List of items to compare
animals = [ "elephant", "human", "chimpanzee", "komodo", "lion", "giraffe", "hippopotamus", "kangaroo", "platypus", "dolphin", "penguin", "octopus", "seahorse", "rhinoceros", "zebra", "gorilla", "koala", "sloth", "panda", "camel", "ostrich", "eagle", "beaver", "otter", "wolf", "bear", "walrus", "seal", "llama", "flamingo", "crocodile", "iguana", "cobra", "tortoise", "salamander", "tuna", "shark", "manta", "jellyfish", "squirrel", "moose", "bison", "orangutan", "peacock", "macaw", "swan", "lemur", "raccoon", "armadillo", "hedgehog"]

###################
# Initialize model#
###################
model = OpenAIModel(
    # Required parameters:
    model_name="gpt-3.5-turbo-0125",  # Required: Name of model to use
    api_key=openai_api_key,           # Required: OpenAI API key

    # Optional parameters (with defaults):
    base_url=None,        # Optional (default=None): Base URL for API 
    max_tokens=10,        # Optional (default=10): Max tokens in response
    concurrency_limit=50, # Optional (default=50): Max concurrent calls
)

#########################
# Initialize analyzer   #
#########################
analyzer = TransitivityAnalyzer(
    # Required parameters:
    model=model,              # Required: Model instance to use
    items=animals,             # Required: List of items to compare

    # Optional parameters (with defaults):
    n_trial=10,             # Optional (default=10): # samples per pair
    n_triad=10,             # Optional (default=200): Number of triads
                            # Use -1 for all possible triads
    seed=42,                # Optional (default=42): Random seed
    save_directory="results"# Optional (default=None): Dir to save results
                            # None means don't save results
)

############################
# Run transitivity analysis#
############################
results = analyzer.run(
    use_async=True  # Optional (default=True): Processing mode
                    # True = Concurrent processing (faster but needs async support)
                    # False = Sequential processing (works everywhere)
)

#################################
# Print key transitivity metrics#
#################################
print("\nTransitivity Analysis Results:")
print(f"Overall transitivity score: {results['transitivity_score']:.3f}")
print(f"Weak stochastic transitivity: {results['weak_stochastic_transitivity_satisfied']}")
print(f"Strong stochastic transitivity: {results['strong_stochastic_transitivity_satisfied']}")

# Print top cycles (if any)
print("\nTop preference cycles found:")
for cycle in results['possible_cycles'][:3]:  # Show top 3 cycles
    print(f"\nProbability: {cycle['probability']:.3f}")
    print(f"Path: {cycle['cycle_path']}")
    print(f"Items involved: {cycle['triad']}")

############################################
# Results dictionary structure explanation #
############################################

# Results structure:
# {
#    'transitivity_score': float,    # Overall transitivity (0-1)
#                                   # 1 = perfectly transitive
#                                   # 0 = completely cyclic
#
#    'weak_stochastic_transitivity_satisfied': str,  # Format: "X/Y"
#                                   # X = number of triads satisfying WST
#                                   # Y = total triads tested
#
#    'strong_stochastic_transitivity_satisfied': str,  # Format: "X/Y"
#                                   # X = number of triads satisfying SST
#                                   # Y = total triads tested
#
#    'possible_cycles': List[Dict],  # List of detected preference cycles
#                                   # Sorted by probability (highest first)
#                                   # Each dict contains:
#                                   # - 'probability': float
#                                   # - 'cycle_path': str description
#                                   # - 'triad': List[str] items involved
#
#    'triad_results': List[Dict],   # Detailed results for each triad
#                                   # Including preference strengths and
#                                   # transitivity violations
#
#    'raw_data': List[Dict]         # Raw comparison data from model
# }
```