import pandas as pd
import numpy.ma as ma
import numpy as np

class Relation:
    @staticmethod
    def equals(value, target):
        return value == target

    @staticmethod
    def gt(value, target):
        return value > target

    @staticmethod
    def lt(value, target):
        return value < target

class Question:
    def __init__(self, attribute, target, relation):
        self.attribute = attribute
        self.target = target
        self.relation = relation

    # Test the question over a power's attributes
    def test(self, n, t):
        print(self)
        if self.attribute == 't':
            return self.relation(t, self.target)

        if self.attribute == 'n':
            return self.relation(n, self.target)

        raise ValueError("Invalid attribute {}, supported attributes are 't', 'n'".format(self.attribute))

    # Return labels matching the question
    def ask(self):
        pass

    def __str__(self):
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
    def __init__(self, power_size, label_size, budget):
        # Pairing table is a power_size x label_size array
        # pairing_table[pi][li] = (s, n)
        # pi is the power, (probably use cluster #)
        # li is the label, (probably use index #)
        # where s is the cummulative score
        # and n is the number of questions contributing to that score
        self.pairing_table = np.zeros((power_size, label_size, 2))
        self.budget = budget

    # Return the individual appliance powers from the result
    def compute_appliance_power(self, gsp_result):
        pass

    # Return the base labels to query from, at most 5
    def query_labels(self):
        pass

    # Return a tuple (n, t) where n is number of times on and t is avg. on time
    def compute_attributes(self, appliance_power):
        pass

    # Returns a question to apply to the current frame
    def select_question(self, attributes):
        pass

    # Run over each frame to query user and update model
    def process_frame(self, frame_num, frame_size, gsp_result):
        powers = self.compute_appliance_power(gsp_result)
        label_candidates = self.query_labels()
        attributes = [self.compute_attributes(power) for power in powers]

        # Ask budgets when budget available
        for i in range(self.budget):
            question = select_question(attributes)

            # Get powers for question
            candidate_powers = []
            for (power, attr) in zip(powers, attributes):
                answer = question.test(**attr)

                if answer:
                    candidate_powers.append(power)

            # Get labels for question
            candidate_labels = question.ask()

            # Compute weight of the question for each pairing
            # Lower with more candidates
            weight = 1.0 / len(candidate_labels) / len(candidate_powers)

            # Update pairing_table's weights and questions
            for power in candidate_powers:
                for label in candidate_labels:
                    self.pairing_table[power, label, 0] += weight
                    self.pairing_table[power, label, 1] += 1
