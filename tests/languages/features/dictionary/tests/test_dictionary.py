import pickle

from revscoring.datasources import revision_oriented
from revscoring.dependencies import solve
from revscoring.languages.features.dictionary.dictionary import Dictionary

calvins_words = {"yakka", "foob", "mog", "gurg", "pubbawup", "zink", "watoom",
                 "gazork", "chumble", "spuzz"}


def dictionary_check(word):
    return word.lower() in calvins_words


my_dict = Dictionary("calvin.dictionary", dictionary_check)

r_text = revision_oriented.revision.text
p_text = revision_oriented.revision.parent.text


def test_dictionary():
    cache = {p_text: "This is a mog and a gurg.  Pubbawup gurg 85 apples.",
             r_text: "This is a gurg and a gurg.  Pubbawup gurg 85 zink."}

    assert (solve(my_dict.revision.datasources.dict_words, cache=cache) ==
            ['gurg', 'gurg', 'Pubbawup', 'gurg', 'zink'])

    assert (solve(my_dict.revision.parent.datasources.dict_words, cache=cache) ==
            ['mog', 'gurg', 'Pubbawup', 'gurg'])

    assert (solve(my_dict.revision.datasources.dict_word_frequency, cache=cache) ==
            {'gurg': 3, 'pubbawup': 1, 'zink': 1})

    assert (solve(my_dict.revision.datasources.non_dict_word_frequency,
                  cache=cache) ==
            {'this': 1, 'is': 1, 'a': 2, 'and': 1})

    assert (solve(my_dict.revision.parent.datasources.dict_word_frequency,
                  cache=cache) ==
            {'gurg': 2, 'pubbawup': 1, 'mog': 1})

    assert (solve(my_dict.revision.parent.datasources.non_dict_word_frequency,
                  cache=cache) ==
            {'this': 1, 'is': 1, 'a': 2, 'and': 1, 'apples': 1})

    diff = my_dict.revision.diff
    assert (solve(diff.datasources.dict_word_delta, cache=cache) ==
            {'gurg': 1, 'mog': -1, 'zink': 1})

    pd = solve(diff.datasources.dict_word_prop_delta, cache=cache)
    assert pd.keys() == {'gurg', 'mog', 'zink'}
    assert round(pd['gurg'], 2) == 0.33
    assert round(pd['mog'], 2) == -1
    assert round(pd['zink'], 2) == 1

    pd = solve(diff.datasources.non_dict_word_prop_delta, cache=cache)
    assert pd.keys() == {'apples'}
    assert round(pd['apples'], 2) == -1

    assert solve(my_dict.revision.dict_words, cache=cache) == 5
    assert solve(my_dict.revision.parent.dict_words, cache=cache) == 4
    assert solve(my_dict.revision.non_dict_words, cache=cache) == 5
    assert solve(my_dict.revision.parent.non_dict_words, cache=cache) == 6

    assert solve(diff.dict_word_delta_sum, cache=cache) == 1.0
    assert solve(diff.dict_word_delta_increase, cache=cache) == 2
    assert solve(diff.dict_word_delta_decrease, cache=cache) == -1
    assert solve(diff.non_dict_word_delta_sum, cache=cache) == -1
    assert solve(diff.non_dict_word_delta_increase, cache=cache) == 0
    assert solve(diff.non_dict_word_delta_decrease, cache=cache) == -1

    assert round(solve(diff.dict_word_prop_delta_sum, cache=cache), 2) == 0.33
    assert round(
        solve(
            diff.dict_word_prop_delta_increase,
            cache=cache),
        2) == 1.33
    assert round(
        solve(
            diff.dict_word_prop_delta_decrease,
            cache=cache),
        2) == -1
    assert round(
        solve(
            diff.non_dict_word_prop_delta_sum,
            cache=cache),
        2) == -1
    assert (round(solve(diff.non_dict_word_prop_delta_increase, cache=cache), 2) ==
            0)
    assert (round(solve(diff.non_dict_word_prop_delta_decrease, cache=cache), 2) ==
            -1)


def test_pickling():
    assert (pickle.loads(pickle.dumps(my_dict.revision.dict_words)) ==
            my_dict.revision.dict_words)
    assert (pickle.loads(pickle.dumps(my_dict.revision.parent.dict_words)) ==
            my_dict.revision.parent.dict_words)
    assert (pickle.loads(pickle.dumps(my_dict.revision.non_dict_words)) ==
            my_dict.revision.non_dict_words)
    assert (pickle.loads(pickle.dumps(my_dict.revision.parent.non_dict_words)) ==
            my_dict.revision.parent.non_dict_words)

    diff = my_dict.revision.diff
    assert (pickle.loads(pickle.dumps(diff.dict_word_delta_sum)) ==
            diff.dict_word_delta_sum)
    assert (pickle.loads(pickle.dumps(diff.dict_word_delta_increase)) ==
            diff.dict_word_delta_increase)
    assert (pickle.loads(pickle.dumps(diff.dict_word_delta_decrease)) ==
            diff.dict_word_delta_decrease)
    assert (pickle.loads(pickle.dumps(diff.non_dict_word_delta_sum)) ==
            diff.non_dict_word_delta_sum)
    assert (pickle.loads(pickle.dumps(diff.non_dict_word_delta_increase)) ==
            diff.non_dict_word_delta_increase)
    assert (pickle.loads(pickle.dumps(diff.non_dict_word_delta_decrease)) ==
            diff.non_dict_word_delta_decrease)

    assert (pickle.loads(pickle.dumps(diff.dict_word_prop_delta_sum)) ==
            diff.dict_word_prop_delta_sum)
    assert (pickle.loads(pickle.dumps(diff.dict_word_prop_delta_increase)) ==
            diff.dict_word_prop_delta_increase)
    assert (pickle.loads(pickle.dumps(diff.dict_word_prop_delta_decrease)) ==
            diff.dict_word_prop_delta_decrease)
    assert (pickle.loads(pickle.dumps(diff.non_dict_word_prop_delta_sum)) ==
            diff.non_dict_word_prop_delta_sum)
    assert (pickle.loads(pickle.dumps(diff.non_dict_word_prop_delta_increase)) ==
            diff.non_dict_word_prop_delta_increase)
    assert (pickle.loads(pickle.dumps(diff.non_dict_word_prop_delta_decrease)) ==
            diff.non_dict_word_prop_delta_decrease)
