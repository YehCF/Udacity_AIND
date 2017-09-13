import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states: object) -> object:
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ select the model with value self.n_constant

    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Bayesian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """

    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # implement model selection based on BIC scores

        final_BIC_score = float("inf")
        final_model = None

        for n_components in range(self.min_n_components, self.max_n_components+1, 1):
            # train HMM model
            model = self.base_model(num_states=n_components)

            if model:
                try:
                    # score the model
                    loglikelihood_score = model.score(self.X, self.lengths)

                    # calculate p
                    p = n_components^2 + 2*n_components*model.n_features - 1
                    # calculate BIC score
                    BIC_score = -2 * loglikelihood_score + p * math.log(len(self.X))

                    if BIC_score < final_BIC_score:
                        #print(n_components, loglikelihood_score, BIC_score)
                        final_BIC_score = BIC_score
                        final_model = model
                except ValueError:
                    pass

        return final_model


class SelectorDIC(ModelSelector):
    ''' select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # implement model selection based on DIC scores

        # Set variables
        final_score = float("-inf")
        final_model = None

        # Iterate through possible n_components
        for n_components in range(self.min_n_components, self.max_n_components+1, 1):

            # train the model with n_components
            model = self.base_model(num_states=n_components)

            if model:
                # calculate DIC score
                try:
                    # log likelihood of this class
                    loglikelihood = model.score(self.X, self.lengths)
                    # anti-likelihood of other classes
                    average_anti_likelihood = np.mean([model.score(*self.hwords[word]) for word in self.words.keys() if word != self.this_word])

                    # calculate DIC score
                    score = loglikelihood - average_anti_likelihood

                    if score > final_score:
                        #print(n_components, loglikelihood, score)
                        final_score = score
                        final_model = model
                except ValueError:
                    pass

        return final_model


class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''

    def select(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # implement model selection using CV

        # Creates K-folds
        k = 3 if len(self.words[self.this_word]) >= 3 else len(self.words[self.this_word])

        final_model = None
        final_average_score = float("-inf")
        # iterate through each n_components to create different models
        for n_components in range(self.min_n_components, self.max_n_components+1, 1):
            scores = [] # for a model trained with a fold of dataset

            # Check whether the data can be splitted into K-folds
            if k > 2:
                # default in sklearn.model_selection.KFold
                KFold_splitter = KFold(n_splits=k)

                for train_idx, validation_idx in KFold_splitter.split(self.words[self.this_word]):
                    # combine train & validation sets
                    self.X, self.lengths = combine_sequences(train_idx, self.words[self.this_word])
                    validation_X, validation_lengths = combine_sequences(validation_idx, self.words[self.this_word])
                    model = self.base_model(num_states=n_components)
                    if model:
                        #print(validation_X, validation_lengths)
                        try:
                            score = model.score(validation_X, validation_lengths)
                            scores.append(score)
                        except ValueError:
                            pass

                average_score = sum(scores) / len(scores) if len(scores) > 0 else float("-inf")
            else:
                # if the data sets can't be splitted, just iterate through all possible n_components

                model = self.base_model(num_states=n_components)

                if model:
                    try:
                        average_score = model.score(self.X, self.lengths)
                    except:
                        average_score = float("-inf")

            if average_score > final_average_score:
                final_average_score = average_score
                #print(n_components, final_average_score)
                self.X, self.lengths = self.hwords[self.this_word]
                best_num_components = n_components
                final_model = self.base_model(num_states=best_num_components)

        return final_model
