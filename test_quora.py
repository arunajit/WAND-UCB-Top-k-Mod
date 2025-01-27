import pandas as pd 
from Inv_Index import InvertedIndex
from wand_algorithm import WAND_Algo
from ucb_wand_algorithm import WAND_Algo as mod_wand_algo


jsonObj = pd.read_json(path_or_buf='./quora/corpus.jsonl', lines=True)
documents = jsonObj[ 'text'].to_dict()
query_terms = ["reinforcement", "learning"]
top_k = 3
inverted_index = InvertedIndex(documents).get_inverted_index()
topk_result, full_evaluation_count = WAND_Algo(query_terms, top_k, inverted_index)
print('Top-k result = ', topk_result)

print('Evaluation Count = ', full_evaluation_count)
print(f'Documents:\n{[documents[i[1]] for i in topk_result]}')

query_terms = ["reinforcement", "learning"]
top_k = 3
inverted_index = InvertedIndex(documents).get_inverted_index()
topk_result, full_evaluation_count = mod_wand_algo(query_terms, top_k, inverted_index)
print('Top-k result = ', topk_result)

print('Evaluation Count = ', full_evaluation_count)
print(f'Documents:\n{[documents[i[1]] for i in topk_result]}')