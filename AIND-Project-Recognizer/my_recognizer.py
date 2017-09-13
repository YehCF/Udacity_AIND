import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    probabilities = []
    guesses = []
    # TODO implement the recognizer

    # Iterate through ordered test set word_id
    for idx, word in enumerate(test_set.wordlist):
        # get the trained model of this word
        probabilities_of_models = {}
        current_best_guess = None
        best_loglikelihood = float("-inf")

        # input for hmm
        test_X, test_lengths = test_set.get_item_Xlengths(item=idx)

        for model_word, model in models.items():
            try:
                loglikelihood = model.score(test_X, test_lengths)
            except:
                pass
            probabilities_of_models[model_word] = loglikelihood

            if loglikelihood > best_loglikelihood:
                best_loglikelihood = loglikelihood
                current_best_guess = model_word

        guesses.append(current_best_guess)
        probabilities.append(probabilities_of_models)

    return probabilities, guesses
