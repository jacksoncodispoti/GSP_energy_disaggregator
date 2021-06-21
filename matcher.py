from math import log2
from typing import Callable, Sequence, Tuple
import pandas as pd
import numpy.ma as ma
import numpy as np
from pandas.core.frame import DataFrame
from pandas.core.generic import NDFrame

class Relation:
    @staticmethod
    def equals(value: float, target: float) -> bool:
        return value == target

    @staticmethod
    def gt(value: float, target: float) -> bool:
        return value > target

    @staticmethod
    def lt(value: float, target: float) -> bool:
        return value < target

class Question:
    def __init__(self, attribute: str, target: float, relation: Callable[[float, float], bool]):
        self.attribute = attribute
        self.target = target
        self.relation = relation

    # Test the question over a power's attributes
    def test(self, n: int, t: float) -> bool:
        if self.attribute == 't':
            return self.relation(t, self.target)

        if self.attribute == 'n':
            return self.relation(n, self.target)

        raise ValueError("Invalid attribute {}, supported attributes are 't', 'n'".format(self.attribute))

    # Return labels matching the question
    def ask(self):
        pass

    def __str__(self) -> str:
        relation = ' '

        if self.relation == Relation.gt:
            relation = ' more than '

        elif self.relation == Relation.lt:
            relation = ' less than '

        if self.attribute == 't':
            return 'Which appliances did you use for{}{} minutes'.format(relation, self.target)

        if self.attribute == 'n':
            return 'Which appliances did you use{}{} times'.format(relation, self.target)

        return ''

class Matcher:
    def __init__(self, power_size: int, labels: Sequence[str], always_on: Sequence[str], budget: int):
        # Pairing table is a power_size x label_size array
        # pairing_table[pi][li] = (s, n)
        # pi is the power, (probably use cluster #)
        # li is the label, (probably use index #)
        # where s is the cummulative score
        # and n is the number of questions contributing to that score
        self.labels = list(set(labels) - set(always_on))
        self.always_on = always_on
        self.pairing_table = np.zeros((power_size, len(labels) - len(always_on)))
        self.budget = budget

    @staticmethod
    def compute_entropy(row: Sequence[float]) -> float:
        entropy = 0.0
        row_sum = np.sum(row)

        for vote in row:
            if vote != 0:
                entropy += -vote / row_sum * log2(vote / row_sum)

        return entropy

    @staticmethod
    def compute_consensus(row) -> float:
        return np.sum(row) / Matcher.compute_entropy(row)

    # Return the individual appliance powers from the result
    def compute_appliance_power(self, gsp_result: NDFrame) -> Sequence[np.ndarray]:
        return [a for a in gsp_result.transpose().values]

    # Return the base labels to query from, at most 5
    def query_labels(self) -> Sequence[str]:
        return self.labels

    # Return a tuple (n, t) where n is number of times on and t is avg. on time
    def compute_attributes(self, appliance_power: np.ndarray) -> Tuple[int, float]:
        threshold = 20

        # Do threshold over whole thing, TTTTT streams is on, count number of for minutes (T)
        # Count number of streams for N
        threshed = np.greater(appliance_power, threshold)

        n = 0
        t = 0
        last = False

        for b in threshed:
            if b:
                t += 1

            if last != b:
                if last == False:
                    n += 1
                last = b

        if n != 0:
            t /= n

        return (n, t)

    def question_consensus(self, q: Question) -> float:
        rows = [r for r in self.pairing_table if q.test(*self.compute_attributes(r))]
        return np.mean([Matcher.compute_consensus(r) for r in rows])

    # Returns a question to apply to the current frame
    def select_question(self, attributes: Sequence[Tuple[int, float]]) -> Question:
        # Initially, questions will be about preset times, < 5, < 15, > 15 min
        # 1 time, 2 times, 3 or more times
        questions = [Question('t', 5, Relation.lt),
            Question('t', 15, Relation.lt),
            Question('t', 15, Relation.gt),
            Question('n', 1, Relation.equals),
            Question('n', 2, Relation.equals),
            Question('n', 2, Relation.gt)
        ]

        questions = [(q, self.question_consensus(q)) for q in questions]
        questions.sort(key=lambda x: x[1])

        return questions[0][0]

    def final_matching(self):
        colors = ['blue', 'orange', 'green', 'red', 'purple']
        for (i, label) in enumerate(self.labels):
            match = np.argmax(np.transpose(self.pairing_table)[i])
            color = colors[match]
            print('{} matches with {}'.format(label, color))

    # Run over each frame to query user and update model
    def process_frame(self, current_time: int, frame_size: int, gsp_result: DataFrame, gsp_truth: DataFrame) -> None:
        frame_disag = gsp_result[current_time:]
        frame_truth = gsp_truth[current_time:]

        powers = self.compute_appliance_power(frame_disag)
        label_candidates = self.query_labels()
        attributes = [self.compute_attributes(power) for power in powers]

        # Ask budgets when budget available
        for i in range(self.budget):
            question = self.select_question(attributes)
            print('Asking question: {}'.format(question))

            # Get powers for question
            candidate_powers = []
            for (i, (power, attr)) in enumerate(zip(powers, attributes)):
                answer = question.test(*attr)

                if answer:
                    candidate_powers.append((i, power))

            # Get labels for question
            candidate_labels = label_candidates
            powers_truth = self.compute_appliance_power(frame_truth)
            attributes_truth = [self.compute_attributes(power) for power in powers_truth]
            candidate_labels = [i for (i, a) in enumerate(attributes_truth) if question.test(*a)]
            candidate_labels = [frame_truth.columns[i] for i in candidate_labels]

            # Compute weight of the question for each pairing
            # Lower with more candidates
            weight = 1.0 / len(candidate_labels) / len(candidate_powers)

            print('{} {}'.format(question, weight))

            # Update pairing_table's weights and questions
            for (pi, power) in candidate_powers:
                for label in candidate_labels:
                    self.pairing_table[pi, self.labels.index(label)] += weight

        print(frame_truth)
        print(self.pairing_table)
