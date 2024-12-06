import asyncio
from typing import List, Dict, Tuple, Optional
import random
from tqdm import tqdm
from tqdm.asyncio import tqdm_asyncio
from openai import OpenAI, AsyncOpenAI
from .base import BaseModel, convert_numpy

COMPARISON_PROMPT = """Which of the following options would you prefer?:

Option A:
{option_A}

Option B:
{option_B}

Please respond with only "A" or "B"."""

class OpenAIModel(BaseModel):
    def __init__(
        self,
        model_name: str,
        api_key: str,
        base_url: Optional[str] = None,
        max_tokens: int = 10,
        concurrency_limit: int = 50,
    ):
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.concurrency_limit = concurrency_limit
        
        # Initialize both sync and async clients
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.async_client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        
        # Track statistics
        self.stats = {'longer_than_4': 0, 'unparseable': 0}
        
    def _parse_response(self, response: str) -> str:
        """Parse model response into 'A' or 'B'."""
        response = response.strip()
        
        if len(response) > 4:
            self.stats['longer_than_4'] += 1
            return random.choice(['A', 'B'])
        elif 'A' in response:
            return 'A'
        elif 'B' in response:
            return 'B'
        else:
            self.stats['unparseable'] += 1
            return random.choice(['A', 'B'])

    def _format_messages(self, option_a: str, option_b: str) -> List[Dict[str, str]]:
        """Format messages for API call."""
        prompt = COMPARISON_PROMPT.format(option_A=option_a, option_B=option_b)
        if 'o1' in self.model_name:
            return [{'role': 'user', 'content': prompt}]
        else:
            return [
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt}
            ]

    def compare_pair(self, option_a: str, option_b: str) -> Tuple[str, str]:
        """Synchronously compare a single pair.
        Returns:
            Tuple[str, str]: (raw_response, parsed_response)
        """
        messages = self._format_messages(option_a, option_b)
        
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=self.max_tokens
        )
        raw_response = completion.choices[0].message.content
        parsed = self._parse_response(raw_response)
        return raw_response, parsed

    def batch_compare_pairs(
        self, 
        pairs: List[Tuple[str, str]], 
        n_trials: int = 1
    ) -> List[Tuple[Tuple[str, str], Dict[str, int], List[Dict[str, str]]]]:
        """Synchronously compare multiple pairs."""
        results = []
        
        with tqdm(total=len(pairs), desc="Comparing pairs", unit="pair") as pbar:
            for pair_idx, pair in enumerate(pairs):
                option_a, option_b = pair
                counts = {'A': 0, 'B': 0}
                responses = []
                
                for trial in range(n_trials):
                    raw_response, parsed = self.compare_pair(option_a, option_b)
                    responses.append({
                        'raw': raw_response,
                        'parsed': parsed
                    })
                    counts[parsed] += 1
                    
                results.append((pair, counts, responses))
                pbar.update(1)
                
        return results

    async def compare_pair_async(self, option_a: str, option_b: str) -> Tuple[str, str]:
        """Asynchronously compare a single pair.
        Returns:
            Tuple[str, str]: (raw_response, parsed_response)
        """
        messages = self._format_messages(option_a, option_b)
        
        if 'o1' in self.model_name:
            completion = await self.async_client.chat.completions.create(
                model=self.model_name,
                messages=messages
            )
        else:
            completion = await self.async_client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=self.max_tokens
            )
        
        raw_response = completion.choices[0].message.content
        parsed = self._parse_response(raw_response)
        return raw_response, parsed

    async def batch_compare_pairs_async(
        self, 
        pairs: List[Tuple[str, str]], 
        n_trials: int = 1
    ) -> List[Tuple[Tuple[str, str], Dict[str, int], List[Dict[str, str]]]]:
        """Asynchronously compare multiple pairs with batching."""
        semaphore = asyncio.Semaphore(self.concurrency_limit)
        results = {}
        
        async def process_pair(pair_idx: int):
            if pair_idx not in results:
                results[pair_idx] = []
            
            option_a, option_b = pairs[pair_idx]
            retry_delay = 5
            max_retries = 5
            
            for trial in range(n_trials):
                for attempt in range(max_retries):
                    try:
                        async with semaphore:
                            raw_response, parsed = await self.compare_pair_async(option_a, option_b)
                            results[pair_idx].append({
                                'raw': raw_response,
                                'parsed': parsed
                            })
                            break
                    except Exception as e:
                        if attempt == max_retries - 1:
                            print(f"Max retries exceeded for pair {pair_idx}, trial {trial}")
                            print(f"Error: {str(e)}")
                        else:
                            print(f"Retry {attempt + 1}/{max_retries} for pair {pair_idx}, trial {trial}")
                            await asyncio.sleep(retry_delay)
                            retry_delay *= 2

        print("\nStarting API calls...")
        tasks = [process_pair(pair_idx) for pair_idx in range(len(pairs))]
        
        for f in tqdm_asyncio.as_completed(tasks, total=len(tasks), desc="Processing pairs", unit="pair"):
            await f

        final_results = []
        for pair_idx, pair in enumerate(pairs):
            responses = results.get(pair_idx, [])
            if not responses:
                print(f"\nWarning: No responses received for pair {pair_idx}")
                counts = {'A': 0, 'B': 0, 'failed': n_trials}
            else:
                counts = {
                    'A': sum(1 for r in responses if r['parsed'] == 'A'),
                    'B': sum(1 for r in responses if r['parsed'] == 'B'),
                    'failed': n_trials - len(responses)
                }
            final_results.append((pair, counts, responses))

        return final_results