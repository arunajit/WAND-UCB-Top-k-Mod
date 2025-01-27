'''
    Modified WAND Algorithm with UCB-based adaptive threshold adjustment 
'''
import math
import bisect

iterators = {}

class Iterator:
    def __init__(self, postings, term, term_string):
        self.postings = postings
        self.docs, _ = zip(*self.postings)
        self.cursor = 0
        self.term = term
        self.term_string = term_string

    def current(self):
        return self.postings[self.cursor]

    def next(self):
        if self.last():
            return False
        else:
            self.cursor += 1
            return True

    def gallop_to(self, doc):
        if doc == self.postings[self.cursor][0]:
            return True
        if doc < self.postings[self.cursor][0]:
            return False
        elif doc > self.postings[-1][0]:
            self.cursor = len(self.postings) - 1
            return False
        else:
            i = bisect.bisect_left(self.docs, doc, self.cursor)
            self.cursor = i
            return True

    def last(self):
        if self.cursor == len(self.postings) - 1:
            return True
        else:
            return False

    def __str__(self):
        return "IT:: t:{}, cursor: {}\n postings: {}\nAt last element: {}\n".format(self.term, self.cursor, self.postings, self.last())


def first_posting(postings, t, term_string):
    it = Iterator(postings, t, term_string)
    iterators[term_string] = it
    return it.current()

def next_posting(term_string):
    it = iterators[term_string]
    if it.next():
        return it.current()
    else:
        return None

def seek_to_document(term_string, doc):
    it = iterators[term_string]
    if it.gallop_to(doc):
        return it.current()
    else:
        return None

def select_arm(arm_rewards, arm_counts, exploration_param):
    '''
        Modify Theta Adjustment with UCB
    '''    
    total_pulls = sum(arm_counts)
    if total_pulls < len(arm_counts):
        return total_pulls  # Ensure all arms are tried
    ucb_values = [
        (arm_rewards[i] / (arm_counts[i] + 1e-9)) + exploration_param * math.sqrt(math.log(total_pulls + 1) / (arm_counts[i] + 1e-9))
        for i in range(len(arm_rewards))
    ]
    return ucb_values.index(max(ucb_values))

def WAND_Algo(query_terms, top_k, inverted_index):
    max_weights = {}
    candidates = []
    '''
        Initialize UCB for Threshold Adjustment
            arms - Threshold adjustment actions
            arm_counts - Track arm pulls
            arm_rewards - Track arm rewards
            exploration_param - Exploration weight for UCB
    '''
    arms = [-0.1, 0.0, 0.1]
    arm_counts = [0] * len(arms)
    arm_rewards = [0.0] * len(arms)
    exploration_param = 1.0

    theta = float("-inf")
    ans = []
    fully_evaluated = 0

    for t in range(0, len(query_terms)):
        qterm = query_terms[t]
        if not inverted_index[qterm]:
            continue

        max_weights[qterm] = max(inverted_index[qterm], key=lambda x: x[1])[1]
        c_did, c_w = first_posting(inverted_index[qterm], t, query_terms[t])
        candidates.append((c_did, c_w, query_terms[t]))

    while candidates:
        candidates = sorted(candidates, key=lambda c: c[0])
        score_limit = 0
        pivot = 0
        pivot_found = False

        while pivot < len(candidates):
            tmp_s_lim = score_limit + max_weights[candidates[pivot][2]]
            if tmp_s_lim > theta:
                pivot_found = True
                break
            score_limit = tmp_s_lim
            pivot += 1

        if not pivot_found:
            break

        pivot_doc = candidates[pivot][0]

        if candidates[0][0] == pivot_doc:
            fully_evaluated += 1
            s = 0
            t = 0
            cand_len = len(candidates)
            removed_candidates = []

            while t < cand_len:
                if candidates[t][0] == pivot_doc:
                    s += candidates[t][1]
                    next_candidate = next_posting(candidates[t][2])
                    if not next_candidate:
                        removed_candidates.append(candidates[t])
                    else:
                        candidates[t] = next_candidate + (candidates[t][2],)
                    t += 1
                else:
                    break

            for r in removed_candidates:
                candidates.remove(r)

            if s > theta:
                ans.append((s, pivot_doc))

                if len(ans) > top_k:
                    ans.remove(min(ans, key=lambda x: (x[0], -x[1])))
                    theta = min(ans, key=lambda x: x[0])[0]

            chosen_arm = select_arm(arm_rewards, arm_counts, exploration_param)
            adjustment = arms[chosen_arm]
            theta *= (1 + adjustment)  # Update Rewards After Evaluation
            reward = fully_evaluated / len(candidates) if candidates else 0
            arm_counts[chosen_arm] += 1
            arm_rewards[chosen_arm] += reward
        else:
            removed_candidates = []
            for t in range(0, pivot):
                seeked_candidate = seek_to_document(candidates[t][2], pivot_doc)
                if not seeked_candidate:
                    removed_candidates.append(candidates[t])
                else:
                    candidates[t] = seeked_candidate + (candidates[t][2],)

            for r in removed_candidates:
                candidates.remove(r)

    ans = sorted(ans, key=lambda x: (-x[0], x[1]))
    return ans, fully_evaluated
