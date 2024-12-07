"""Core module for grading medical audio cases"""

# pylint: disable=too-many-lines
# pylint: disable=too-many-locals
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments

import re
import string

import jiwer
import nltk
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from num2words import num2words

# Shift into a function
nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)


def hello() -> str:
    """Welcome message for the package"""

    return "Welcome to audio-case-grade!"


def _std_abbrev_substitutions():
    """medical abbreviation conversion"""

    acr_abb = pd.read_csv("Acronyms and Abbreviations.csv", header=0)
    abbrev_map = dict(
        zip(acr_abb["Abbreviation"].str.lower(), acr_abb["Meaning"].str.lower())
    )
    return abbrev_map


def _text_clean(x, abbrev_map):
    """textual cleaning and standardization"""

    clean_text = []
    translator = str.maketrans(string.punctuation, " " * len(string.punctuation))
    for i in x:
        t = jiwer.ExpandCommonEnglishContractions()(i)
        t = jiwer.RemoveEmptyStrings()(t)
        t = jiwer.ToLowerCase()(t)
        t = jiwer.RemoveKaldiNonWords()(t)
        t = t.translate(translator)
        t = jiwer.Strip()(t)
        t = jiwer.SubstituteWords(abbrev_map)(t)
        t = jiwer.SubstituteWords(
            {
                "1+": "one plus",
                "1 +": "one plus",
                "2 d": "2d",
                "o two": "oxygen saturation",
                "o2": "oxygen saturation",
                "mg": "milligrams",
                "hr": "heart rate",
                "rr": "respiratory rate",
                "bp": "blood pressure",
                "x-ray": "xray",
                "x ray": "xray",
                "/": "over",
                "%": "percent",
                "hrs": "hours",
                "wks": "weeks",
                "mths": "months",
                "mos": "months",
                "cr td": "crtd",
                "s 4": "s4",
                "s four": "sfour",
                "s two": "stwo",
                "s 2": "s2",
                "s three": " sthree",
                "s 3": "s3",
                "v one": "vone",
                "v 1": "v1",
                "t 4": "t4",
                "t four": "tfour",
                "t 6": "t6",
                "t six": "tsix",
                "rails": "rales",
                "rail": "rale",
            }
        )(t)
        t = jiwer.RemovePunctuation()(t)
        t = jiwer.RemoveMultipleSpaces()(t)
        clean_text.append(t)
    return clean_text


def _num_text(x):
    """convert numerical numbers in text to word format"""

    t = [re.sub(r"(\d+)", lambda m: num2words(m.group()), sentence) for sentence in x]
    return t


def clean(data):
    """removes stop words from presentations, applies above cleaning functions"""

    stop = stopwords.words("english")
    stop.remove("no")
    stop.remove("not")
    stop.remove("most")
    stop.remove("some")
    stop.remove("out")
    clean_response = _num_text(data["Presentation"])
    abbrev_map = _std_abbrev_substitutions()
    clean_response = _text_clean(clean_response, abbrev_map)
    clean_response = pd.Series(clean_response)
    clean_response = clean_response.apply(
        lambda x: " ".join([word for word in x.split() if word not in (stop)])
    )
    return clean_response


def _keywordcount(response, correct_key):
    """totals the correct keywords from the student responses"""

    count = 0
    position_l = []
    cword_list = []

    for i in correct_key.dropna():
        for j in i:

            if len(str(j)) == 0:
                count = None

            elif str(j) in response and len(str(j)) != 0:
                cword_list.append(j)
                count = count + 1
                a = re.search(str(j), response)
                a = a.start() + 1
                position_l.append([j, a])
            else:
                count = count + 0
                a = 0
                position_l.append([j, a])

    if count is not None:
        # sequenceBool = _pos_sequence(position_l,count)
        percent = round((count / correct_key.str.len().item()), 4) * 100
    else:
        # sequenceBool = None
        percent = None

    # density.append(round((count/len(response)),4)*100) #lexical density
    return (count, percent, cword_list, position_l)


def _keywordcount_wrong(
    response, wrong_key
):  # totals the wrong keywords from the student responses
    count = 0
    wrong_list = []
    position_l = []
    for j in wrong_key:
        if str(j) in response and len(str(j)) != 0:
            wrong_list.append(j)
            count = count + 1
            a = re.search(str(j), response)
            a = a.start() + 1
            position_l.append([j, a])
        else:
            count = count + 0
            a = 0
            position_l.append([j, a])
    return (count, wrong_list, position_l)


def _pos_sequence(position, count):
    """DEPRECATED if the keywords a student has is in order from position least to greatest
    the student recieves TRUE"""

    if count == 0:
        in_order = False
    else:
        in_order = all(position[i] <= position[i + 1] for i in range(len(position) - 1))
    return in_order


def _jaccard(s1, s2):
    """DEPRECATED jaccard similarity for student to physician presentations"""

    s1 = s1.split()
    s2 = s2.split()
    union = list(set(s1 + s2))
    intersection = list(set(s1) - (set(s1) - set(s2)))
    jaccard_coeff = float(len(intersection)) / len(union)
    return jaccard_coeff


def _msk(case, keybank):
    """grab the correct keys for the case a student recieves"""

    keywords = keybank.drop(["Case", "ICD10", "System"], axis=1)
    keyword_bank = pd.Series(
        [keywords[col].str.cat(sep=", ") for col in keywords.columns]
    )
    keyword_bank = pd.Series(
        [list(dict.fromkeys(string_list.split(", "))) for string_list in keyword_bank],
        index=keywords.columns,
    )

    correct_key = keybank[keybank["ICD10"] == case].drop(
        ["Case", "ICD10", "System"], axis=1
    )
    correct_key = pd.Series(
        [correct_key[col].str.split(", ") for col in correct_key.columns]
    )
    wrong_key = []
    for i in range(len(keywords.columns)):
        a = keyword_bank.iloc[i]
        b = list(correct_key.iloc[:, i].item())
        key = list(set(a) ^ set(b))
        wrong_key.append(key)

    physician_pres = None

    return (correct_key, wrong_key, physician_pres)


def _nuero(case, keybank):
    """grab the correct keys for the case a student recieves"""

    keywords = keybank.drop(["Case", "ICD10", "System"], axis=1)
    keyword_bank = pd.Series(
        [keywords[col].str.cat(sep=", ") for col in keywords.columns]
    )
    keyword_bank = pd.Series(
        [list(dict.fromkeys(string_list.split(", "))) for string_list in keyword_bank],
        index=keywords.columns,
    )

    correct_key = keybank[keybank["ICD10"] == case].drop(
        ["Case", "ICD10", "System"], axis=1
    )
    correct_key = pd.Series(
        [correct_key[col].str.split(", ") for col in correct_key.columns]
    )
    wrong_key = []
    for i in range(len(keywords.columns)):
        a = keyword_bank.iloc[i]
        b = list(correct_key.iloc[:, i].item())
        key = list(set(a) ^ set(b))
        wrong_key.append(key)

    physician_pres = None

    return (correct_key, wrong_key, physician_pres)


def _cardiopulm(case, keybank):
    """grab the correct keys for the case a student recieves"""

    keywords = keybank.drop(["Case", "ICD10", "System"], axis=1)
    keyword_bank = pd.Series(
        [keywords[col].str.cat(sep=", ") for col in keywords.columns]
    )
    keyword_bank = pd.Series(
        [list(dict.fromkeys(string_list.split(", "))) for string_list in keyword_bank],
        index=keywords.columns,
    )

    correct_key = keybank[keybank["ICD10"] == case].drop(
        ["Case", "ICD10", "System"], axis=1
    )
    correct_key = pd.Series(
        [correct_key[col].str.split(", ") for col in correct_key.columns]
    )

    wrong_key = []
    for i in range(len(keywords.columns)):
        a = keyword_bank.iloc[i]
        b = list(correct_key.iloc[i].item())
        key = list(set(a) ^ set(b))
        wrong_key.append(key)

    physician_pres = None

    return (correct_key, wrong_key, physician_pres)


def _gi(case, keybank):
    """grab the correct keys for the case a student recieves"""

    keywords = keybank.drop(["Case", "ICD10", "System"], axis=1)
    keyword_bank = pd.Series(
        [keywords[col].str.cat(sep=", ") for col in keywords.columns]
    )
    keyword_bank = pd.Series(
        [list(dict.fromkeys(string_list.split(", "))) for string_list in keyword_bank],
        index=keywords.columns,
    )

    correct_key = keybank[keybank["ICD10"] == case].drop(
        ["Case", "ICD10", "System"], axis=1
    )
    correct_key = pd.Series(
        [correct_key[col].str.split(", ") for col in correct_key.columns]
    )
    wrong_key = []
    for i in range(len(keywords.columns)):
        a = keyword_bank.iloc[i]
        b = list(correct_key.iloc[:, i].item())
        key = list(set(a) ^ set(b))
        wrong_key.append(key)

    physician_pres = None

    return (correct_key, wrong_key, physician_pres)


def _gu(case, keybank):
    """grab the correct keys for the case a student recieves"""

    keywords = keybank.drop(["Case", "ICD10", "System"], axis=1)
    keyword_bank = pd.Series(
        [keywords[col].str.cat(sep=", ") for col in keywords.columns]
    )
    keyword_bank = pd.Series(
        [list(dict.fromkeys(string_list.split(", "))) for string_list in keyword_bank],
        index=keywords.columns,
    )

    correct_key = keybank[keybank["ICD10"] == case].drop(
        ["Case", "ICD10", "System"], axis=1
    )
    correct_key = pd.Series(
        [correct_key[col].str.split(", ") for col in correct_key.columns]
    )
    wrong_key = []
    for i in range(len(keywords.columns)):
        a = keyword_bank.iloc[i]
        b = list(correct_key.iloc[:, i].item())
        key = list(set(a) ^ set(b))
        wrong_key.append(key)

    physician_pres = None

    return (correct_key, wrong_key, physician_pres)


def _keyword_bank(icd10, system, keybank):
    """system look up based on input from user, grabs the correct key and makes
    appropriate replacements"""

    if system == "Musculoskeletal":
        key_filter = keybank[keybank["System"] == "MSK"]
        (correct_key, wrong_key, _physician_pres) = _msk(icd10, key_filter)

    elif system == "Nuerology":
        key_filter = keybank[keybank["System"] == "Neuro"]
        (correct_key, wrong_key, _physician_pres) = _nuero(icd10, key_filter)

    elif system == "Cardiopulmonary":
        key_filter = keybank[keybank["System"] == "Cardiopulm"]
        (correct_key, wrong_key, _physician_pres) = _cardiopulm(icd10, key_filter)

    elif system == "Gastroenterology":
        key_filter = keybank[keybank["System"] == "GI"]
        (correct_key, wrong_key, _physician_pres) = _gi(icd10, key_filter)

    else:  # Genitourinary
        key_filter = keybank[keybank["System"] == "GU"]
        (correct_key, wrong_key, _physician_pres) = _gu(icd10, key_filter)

    return correct_key, wrong_key


def _history(i, list_correct, list_wrong, correct_key, wrong_key):
    """function to calculate metrics for all components of history"""

    # Cardinal Complaint
    cc = correct_key.iloc[0]
    (cc_c_score, cc_c_score_p, cc_cwords_list, cc_sequence_list) = _keywordcount(i, cc)

    cc_wrong = wrong_key[0]
    cc_w_score, cc_w_words_list, cc_wrong_sequence_list = _keywordcount_wrong(
        i, cc_wrong
    )

    # History - Present Illness
    hpi = correct_key.iloc[1]
    (hpi_c_score, hpi_c_score_p, hpi_cwords_list, hpi_sequence_list) = _keywordcount(
        i, hpi
    )

    hpi_wrong = wrong_key[1]
    hpi_w_score, hpi_w_words_list, hpi_wrong_sequence_list = _keywordcount_wrong(
        i, hpi_wrong
    )

    # Review of Systems

    ros = correct_key.iloc[2]
    (ros_c_score, ros_c_score_p, ros_cwords_list, ros_sequence_list) = _keywordcount(
        i, ros
    )

    ros_wrong = wrong_key[2]
    ros_w_score, ros_w_words_list, ros_wrong_sequence_list = _keywordcount_wrong(
        i, ros_wrong
    )

    # Current Medications

    meds = correct_key.iloc[3]
    meds_c_score, meds_c_score_p, meds_cwords_list, meds_sequence_list = _keywordcount(
        i, meds
    )

    meds_wrong = wrong_key[3]
    meds_w_score, meds_w_words_list, meds_wrong_sequence_list = _keywordcount_wrong(
        i, meds_wrong
    )

    history = [
        cc_c_score,
        cc_c_score_p,
        cc_sequence_list,
        cc_cwords_list,
        hpi_c_score,
        hpi_c_score_p,
        hpi_sequence_list,
        hpi_cwords_list,
        ros_c_score,
        ros_c_score_p,
        ros_sequence_list,
        ros_cwords_list,
        meds_c_score,
        meds_c_score_p,
        meds_sequence_list,
        meds_cwords_list,
    ]
    history_wrong = [
        cc_w_score,
        cc_w_words_list,
        cc_wrong_sequence_list,
        hpi_w_score,
        hpi_w_words_list,
        hpi_wrong_sequence_list,
        ros_w_score,
        ros_w_words_list,
        ros_wrong_sequence_list,
        meds_w_score,
        meds_w_words_list,
        meds_wrong_sequence_list,
    ]

    list_correct.append(history)
    list_wrong.append(history_wrong)
    return list_correct, list_wrong


def _objective(i, list_correct, list_wrong, correct_key, wrong_key):
    """function to calculate metrics for all components of objective"""

    # Vital Signs

    vitals = correct_key.iloc[4]
    vitals_c_score, vitals_c_score_p, vitals_cwords_list, vitals_sequence_list = (
        _keywordcount(i, vitals)
    )
    vitals_wrong = wrong_key[4]
    vitals_w_score, vitals_w_words_list, vitals_wrong_sequence_list = (
        _keywordcount_wrong(i, vitals_wrong)
    )
    # General Appearence

    gen = correct_key.iloc[5]
    gen_c_score, gen_c_score_p, gen_cwords_list, gen_sequence_list = _keywordcount(
        i, gen
    )
    gen_wrong = wrong_key[5]
    gen_w_score, gen_w_words_list, gen_wrong_sequence_list = _keywordcount_wrong(
        i, gen_wrong
    )
    # Physical Exam

    pe = correct_key.iloc[6]
    pe_c_score, pe_c_score_p, pe_cwords_list, pe_sequence_list = _keywordcount(i, pe)
    pe_wrong = wrong_key[6]
    pe_w_score, pe_w_words_list, pe_wrong_sequence_list = _keywordcount_wrong(
        i, pe_wrong
    )
    # Diagnostic Labs

    dl = correct_key.iloc[7]
    dl_c_score, dl_c_score_p, dl_cwords_list, dl_sequence_list = _keywordcount(i, dl)
    dl_wrong = wrong_key[7]
    dl_w_score, dl_w_words_list, dl_wrong_sequence_list = _keywordcount_wrong(
        i, dl_wrong
    )
    # Diagnostic Imaging

    di = correct_key.iloc[8]
    di_c_score, di_c_score_p, di_cwords_list, di_sequence_list = _keywordcount(i, di)
    di_wrong = wrong_key[8]
    di_w_score, di_w_words_list, di_wrong_sequence_list = _keywordcount_wrong(
        i, di_wrong
    )

    objective = [
        vitals_c_score,
        vitals_c_score_p,
        vitals_sequence_list,
        vitals_cwords_list,
        gen_c_score,
        gen_c_score_p,
        gen_sequence_list,
        gen_cwords_list,
        pe_c_score,
        pe_c_score_p,
        pe_sequence_list,
        pe_cwords_list,
        dl_c_score,
        dl_c_score_p,
        dl_sequence_list,
        dl_cwords_list,
        di_c_score,
        di_c_score_p,
        di_sequence_list,
        di_cwords_list,
    ]

    objective_wrong = [
        vitals_w_score,
        vitals_w_words_list,
        vitals_wrong_sequence_list,
        gen_w_score,
        gen_w_words_list,
        gen_wrong_sequence_list,
        pe_w_score,
        pe_w_words_list,
        pe_wrong_sequence_list,
        dl_w_score,
        dl_w_words_list,
        dl_wrong_sequence_list,
        di_w_score,
        di_w_words_list,
        di_wrong_sequence_list,
    ]

    list_correct.append(objective)
    list_wrong.append(objective_wrong)
    return list_correct, list_wrong


def _assessment(i, list_correct, list_wrong, correct_key, wrong_key):
    """function to calculate metrics for all components of assessment"""

    # Diagnosis

    dx = correct_key.iloc[9]
    dx_c_score, dx_c_score_p, dx_cwords_list, dx_sequence_list = _keywordcount(i, dx)
    dx_wrong = wrong_key[9]
    dx_w_score, dx_w_words_list, dx_wrong_sequence_list = _keywordcount_wrong(
        i, dx_wrong
    )
    # Differential

    ddx = correct_key.iloc[10]
    ddx_c_score, ddx_c_score_p, ddx_cwords_list, ddx_sequence_list = _keywordcount(
        i, ddx
    )
    ddx_wrong = wrong_key[10]
    ddx_w_score, ddx_w_words_list, ddx_wrong_sequence_list = _keywordcount_wrong(
        i, ddx_wrong
    )

    assessment = [
        dx_c_score,
        dx_c_score_p,
        dx_sequence_list,
        dx_cwords_list,
        ddx_c_score,
        ddx_c_score_p,
        ddx_sequence_list,
        ddx_cwords_list,
    ]

    assessment_wrong = [
        dx_w_score,
        dx_w_words_list,
        dx_wrong_sequence_list,
        ddx_w_score,
        ddx_w_words_list,
        ddx_wrong_sequence_list,
    ]
    list_correct.append(assessment)
    list_wrong.append(assessment_wrong)

    return list_correct, list_wrong


def _plan(i, list_correct, list_wrong, correct_key, wrong_key):
    """function to calculate metrics for all components of plan"""

    # Treatment

    tx = correct_key.iloc[11]
    tx_c_score, tx_c_score_p, tx_cwords_list, tx_sequence_list = _keywordcount(i, tx)
    tx_wrong = wrong_key[11]
    tx_w_score, tx_w_words_list, tx_wrong_sequence_list = _keywordcount_wrong(
        i, tx_wrong
    )
    # Physician Consults

    consult = correct_key.iloc[12]
    consult_c_score, consult_c_score_p, consult_cwords_list, consult_sequence_list = (
        _keywordcount(i, consult)
    )
    consult_wrong = wrong_key[12]
    consult_w_score, consult_w_words_list, consult_wrong_sequence_list = (
        _keywordcount_wrong(i, consult_wrong)
    )
    # Interventions

    inter = correct_key.iloc[13]
    inter_c_score, inter_c_score_p, inter_cwords_list, inter_sequence_list = (
        _keywordcount(i, inter)
    )
    inter_wrong = wrong_key[13]
    inter_w_score, inter_w_words_list, inter_wrong_sequence_list = _keywordcount_wrong(
        i, inter_wrong
    )

    plan = [
        tx_c_score,
        tx_c_score_p,
        tx_sequence_list,
        tx_cwords_list,
        consult_c_score,
        consult_c_score_p,
        consult_sequence_list,
        consult_cwords_list,
        inter_c_score,
        inter_c_score_p,
        inter_sequence_list,
        inter_cwords_list,
    ]
    plan_wrong = [
        tx_w_score,
        tx_w_words_list,
        tx_wrong_sequence_list,
        consult_w_score,
        consult_w_words_list,
        consult_wrong_sequence_list,
        inter_w_score,
        inter_w_words_list,
        inter_wrong_sequence_list,
    ]

    list_correct.append(plan)
    list_wrong.append(plan_wrong)

    return list_correct, list_wrong


def _foundations(i, list_correct, list_wrong, correct_key, wrong_key):
    """function to calculate metrics for all components of foundations"""

    found = correct_key.iloc[14]
    found_c_score, found_c_score_p, found_cwords_list, found_sequence_list = (
        _keywordcount(i, found)
    )
    found_wrong = wrong_key[14]
    found_w_score, found_w_words_list, found_wrong_sequence_list = _keywordcount_wrong(
        i, found_wrong
    )

    foundations = [
        found_c_score,
        found_c_score_p,
        found_sequence_list,
        found_cwords_list,
    ]
    foundations_wrong = [found_w_score, found_w_words_list, found_wrong_sequence_list]

    list_correct.append(foundations)
    list_wrong.append(foundations_wrong)

    return list_correct, list_wrong


def _hist_to_df(hist, hist_wrong):
    """merge all metrics into one data frame"""

    col_names = [
        "History - CC Count",
        "History - CC Percentage",
        "History - CC Sequence",
        "History - CC Word List",
        "History - HPI Count",
        "History - HPI Percentage",
        "History - HPI Sequence",
        "History - HPI Word List",
        "History - ROS Count",
        "History - ROS Percentage",
        "History - ROS Sequence",
        "History - ROS Word List",
        "History - MEDS Count",
        "History - MEDS Percentage",
        "History - MEDS Sequence",
        "History - MEDS Word List",
    ]
    col_names_wrong = [
        "History - CC Wrong Count",
        "History - CC Wrong Word List",
        "History - CC Word Sequence",
        "History - HPI Wrong Count",
        "History - HPI Wrong Word List",
        "History - HPI Word Sequence",
        "History - ROS Wrong Count",
        "History - ROS Wrong Word List",
        "History - ROS Word Sequence",
        "History - MEDS Wrong Count",
        "History - MEDS Wrong Word List",
        "History - MEDS Word Sequence",
    ]

    history_df = pd.DataFrame(
        np.array(hist, dtype=object).reshape(-1, len(hist[0])), columns=col_names
    )
    history_wrong_df = pd.DataFrame(
        np.array(hist_wrong, dtype=object).reshape(-1, len(hist_wrong[0])),
        columns=col_names_wrong,
    )

    return history_df, history_wrong_df


def _obj_to_df(obj, obj_wrong):
    """merge all metrics into one data frame"""

    col_names = [
        "Objective - VITALS Count",
        "Objective - VITALS Percentage",
        "Objective - VITALS Sequence",
        "Objective - VITALS Word List",
        "Objective - GEN Count",
        "Objective - GEN Percentage",
        "Objective - GEN Sequence",
        "Objective - GEN Word List",
        "Objective - PE Count",
        "Objective - PE Percentage",
        "Objective - PE Sequence",
        "Objective - PE Word List",
        "Objective - DL Count",
        "Objective - DL Percentage",
        "Objective - DL Sequence",
        "Objective - DL Word List",
        "Objective - DI Count",
        "Objective - DI Percentage",
        "Objective - DI Sequence",
        "Objective - DI Word List",
    ]
    col_names_wrong = [
        "Objective - VITALS Wrong Count",
        "Objective - VITALS Wrong Word List",
        "Objective - VITALS Word Sequence",
        "Objective - GEN Wrong Count",
        "Objective - GEN Wrong Word List",
        "Objective - GEN Word Sequence",
        "Objective - PE Wrong Count",
        "Objective - PE Wrong Word  List",
        "Objective - PE Word Sequence",
        "Objective - DL Wrong Count",
        "Objective - DL Wrong Word List",
        "Objective - DL Word Sequence",
        "Objective - DI Wrong Count",
        "Objective - DI Wrong Word List",
        "Objective - DI Word Sequence",
    ]

    objective_df = pd.DataFrame(
        np.array(obj, dtype=object).reshape(-1, len(obj[0])), columns=col_names
    )
    objective_wrong_df = pd.DataFrame(
        np.array(obj_wrong, dtype=object).reshape(-1, len(obj_wrong[0])),
        columns=col_names_wrong,
    )

    return objective_df, objective_wrong_df


def _assess_to_df(assess, assess_wrong):
    """merge all metrics into one data frame"""

    col_names = [
        "Assessment - Dx Count",
        "Assessment - Dx Percentage",
        "Assessment - Dx Sequence",
        "Assessment - Dx Word List",
        "Assessment - DDx Count",
        "Assessment - DDx Percentage",
        "Assessment - DDx Sequence",
        "Assessment - DDx Word List",
    ]
    col_names_wrong = [
        "Assessment - Dx Wrong Count",
        "Assessment - Dx Wrong Word List",
        "Assessment - Dx Word Sequence",
        "Assessment - DDx Wrong Count",
        "Assessment - DDx Wrong Word List",
        "Assessment - DDx Word Sequence",
    ]

    assessment_df = pd.DataFrame(
        np.array(assess, dtype=object).reshape(-1, len(assess[0])), columns=col_names
    )
    assessment_wrong_df = pd.DataFrame(
        np.array(assess_wrong, dtype=object).reshape(-1, len(assess_wrong[0])),
        columns=col_names_wrong,
    )
    return assessment_df, assessment_wrong_df


def _plan_to_df(plan, plan_wrong):
    """merge all metrics into one data frame"""

    col_names = [
        "Plan - Tx Count",
        "Plan - Tx Percentage",
        "Plan - Tx Sequence",
        "Plan - Tx Word List",
        "Plan - Consult Count",
        "Plan - Consult Percentage",
        "Plan - Consult Sequence",
        "Plan - Consult Word List",
        "Plan - Interventions Count",
        "Plan - Interventions Percentage",
        "Plan - Interventions Sequence",
        "Plan - Interventions Word List",
    ]
    col_names_wrong = [
        "Plan - Tx Wrong Count",
        "Plan - Tx Wrong Word List",
        "Plan - Tx Word Sequence",
        "Plan - Consult Wrong Count",
        "Plan - Consult Wrong Word List",
        "Plan - Consult Word Sequence",
        "Plan - Interventions Wrong Count",
        "Plan - Interventions Wrong Word List",
        "Plan - Interventions Word Sequence",
    ]

    plan_df = pd.DataFrame(
        np.array(plan, dtype=object).reshape(-1, len(plan[0])), columns=col_names
    )
    plan_wrong_df = pd.DataFrame(
        np.array(plan_wrong, dtype=object).reshape(-1, len(plan_wrong[0])),
        columns=col_names_wrong,
    )

    return plan_df, plan_wrong_df


def _foundations_to_df(foundations, foundations_wrong):
    """merge all metrics into one data frame"""

    col_names = [
        "Foundations -  Count",
        "Foundations -  Percentage",
        "Foundations -  Sequence",
        "Foundations -  Word List",
    ]
    col_names_wrong = [
        "Foundations -  Wrong Count",
        "Foundations -  Wrong Word List",
        "Foundations -  Word Sequence",
    ]

    foundations_df = pd.DataFrame(
        np.array(foundations, dtype=object).reshape(-1, len(foundations[0])),
        columns=col_names,
    )
    foundations_wrong_df = pd.DataFrame(
        np.array(foundations_wrong, dtype=object).reshape(
            -1, len(foundations_wrong[0])
        ),
        columns=col_names_wrong,
    )

    return foundations_df, foundations_wrong_df


def _soap(
    i,
    his,
    obj,
    assess,
    empty_plan,
    foundat,
    his_wrong,
    obj_wrong,
    assess_wrong,
    empty_plan_wrong,
    foundat_wrong,
    correct_key,
    wrong_key,
):
    """calculate all metrics of the SOAP note flow and return the data frames for each section"""

    hist, hist_wrong = _history(i, his, his_wrong, correct_key, wrong_key)
    hist, hist_wrong = _hist_to_df(hist, hist_wrong)

    obj, obj_wrong = _objective(i, obj, obj_wrong, correct_key, wrong_key)
    obj, obj_wrong = _obj_to_df(obj, obj_wrong)

    assess, assess_wrong = _assessment(i, assess, assess_wrong, correct_key, wrong_key)
    assess, assess_wrong = _assess_to_df(assess, assess_wrong)

    plans, plans_wrong = _plan(i, empty_plan, empty_plan_wrong, correct_key, wrong_key)
    plans, plans_wrong = _plan_to_df(plans, plans_wrong)

    found, found_wrong = _foundations(i, foundat, foundat_wrong, correct_key, wrong_key)
    found, found_wrong = _foundations_to_df(found, found_wrong)

    return (
        hist,
        hist_wrong,
        obj,
        obj_wrong,
        assess,
        assess_wrong,
        plans,
        plans_wrong,
        found,
        found_wrong,
    )


def _clean_keybank(keybank):
    """cleans the KeyBank"""

    for i in range(3, len(keybank.columns)):
        k = 0
        for j in keybank.iloc[:, i]:
            if j != "":

                t = jiwer.SubstituteWords({",": ", "})(j)
                t = jiwer.Strip()(t)
                t = jiwer.RemoveMultipleSpaces()(t)
                keybank.loc[k, keybank.columns[i]] = t
                k = k + 1


def _keyword_algorithm(data, icd10, system):
    """main function for keyword algorithm, applies above functions to all student presentations"""

    cln_pres = clean(data)
    history = []
    objective = []
    assessment = []
    plan_list = []
    foundat = []
    history_wrong = []
    objective_wrong = []
    assessment_wrong = []
    plan_list_wrong = []
    foundat_wrong = []
    # sim = [] similarity array save for v2
    c_key = []
    wrong_key = []
    with open("Copy of Case Presentation KeyBank - Transpose.xlsx", "rb") as file:
        keybank = pd.read_excel(
            file,
            sheet_name="KeyBank",
            na_filter=False,
        )

    _clean_keybank(keybank)
    for i, j, k in zip(cln_pres, icd10, system):
        (correct_key, wrong_key) = _keyword_bank(
            j, k, keybank
        )  # physician presentation will be excluded in v1, inclusion in v2
        c_key.append(correct_key)
        wrong_key.append(wrong_key)
        (
            hist,
            hist_wrong,
            obj,
            obj_wrong,
            assess,
            assess_wrong,
            plans,
            plans_wrong,
            found,
            found_wrong,
        ) = _soap(
            i,
            history,
            objective,
            assessment,
            plan_list,
            foundat,
            history_wrong,
            objective_wrong,
            assessment_wrong,
            plan_list_wrong,
            foundat_wrong,
            correct_key,
            wrong_key,
        )

    cor_key = []
    for i, row in enumerate(c_key):
        get_item = []
        for j, (_key, value) in enumerate(row.items()):
            a = value.item()
            get_item.append(a)
        cor_key.append(get_item)

    correct = pd.concat([hist, obj, assess, plans, found], axis=1).reset_index(
        drop=True
    )
    wrong = pd.concat(
        [hist_wrong, obj_wrong, assess_wrong, plans_wrong, found_wrong], axis=1
    ).reset_index(drop=True)
    response_len = cln_pres.str.split(" ").str.len()
    return correct, wrong, cor_key, wrong_key, response_len


def _total(df):
    """get totals for count columns in metric dataframes"""

    return sum(df[e].fillna(0) for e in df.columns if "Count" in e)


def _total_keybank(df):
    """get totals for columns in keyBank"""

    return sum(df[e].fillna(0) for e in df.columns)


def _keybank_count(key, match):  #
    """reports keyword usage on each student"""

    # words they used
    # words they didn't use
    # wrong words they used
    # totals for each section
    counts_cc = []
    if match == "correct":
        for _i, row in enumerate(key):
            a = []
            for _j, cell in enumerate(row):
                if cell[0] != "":
                    a.append(len(cell))
                else:
                    a.append(0)
            counts_cc.append(a)
    else:
        for _i, row in enumerate(key):
            a = []
            for _j, cell in enumerate(row):
                if len(cell) != 0:
                    a.append(len(cell))
                else:
                    a.append(0)
            counts_cc.append(a)

    names = [
        "History - KeyBank CC",
        "History -KeyBank HPI",
        "History - KeyBank ROS",
        "History - KeyBank MEDS",
        "Objective - KeyBank VITALS",
        "Objective - KeyBank GEN",
        "Objective - KeyBank PE",
        "Objective - KeyBank DL",
        "Objective - KeyBank DI",
        "Assessment - KeyBank Dx",
        "Assessment - KeyBank DDx",
        "Plan - KeyBank Tx",
        "Plan - KeyBank Consult",
        "Plan - KeyBank Interventions",
        "Foundation KeyBank",
    ]
    sub_section_counts = pd.DataFrame(counts_cc, columns=names)
    total_count = _total_keybank(sub_section_counts)
    history_total_count = _total_keybank(sub_section_counts.filter(regex="History"))
    obj_total_count = _total_keybank(sub_section_counts.filter(regex="Objective"))
    assess_total_count = _total_keybank(sub_section_counts.filter(regex="Assessment"))
    plans_total_count = _total_keybank(sub_section_counts.filter(regex="Plan"))
    found_total_count = _total_keybank(sub_section_counts.filter(regex="Foundation"))
    section_counts = pd.DataFrame(
        {
            "Total KeyBank Count": total_count,
            "History KeyBank Count": history_total_count,
            "Objective KeyBank Count": obj_total_count,
            "Assessment KeyBank Count": assess_total_count,
            "Plan KeyBank Count": plans_total_count,
            "Foundations KeyBank Count": found_total_count,
        }
    )
    return sub_section_counts, section_counts


def _correct_total(correct):
    """correct key usage to dataframe"""

    total_count = _total(correct)
    history_total_count = _total(correct.filter(regex="History"))
    obj_total_count = _total(correct.filter(regex="Objective"))
    assess_total_count = _total(correct.filter(regex="Assessment"))
    plans_total_count = _total(correct.filter(regex="Plan"))
    found_total_count = _total(correct.filter(regex="Foundations"))

    np.testing.assert_array_equal(
        total_count,
        (
            history_total_count
            + obj_total_count
            + assess_total_count
            + plans_total_count
            + found_total_count
        ),
    )

    total_correct_df = pd.DataFrame(
        {
            "Total Keyword Count": total_count,
            "History Keyword Total": history_total_count,
            "Objective Keyword Total": obj_total_count,
            "Assessment Keyword Total": assess_total_count,
            "Plan Keyword Total": plans_total_count,
            "Foundations keyword Total": found_total_count,
        }
    )
    return total_correct_df


def _wrong_total(wrong):
    """wrong key usage to data frame"""

    total_count = _total(wrong)

    history_total_count = _total(wrong.filter(regex="History"))
    obj_total_count = _total(wrong.filter(regex="Objective"))
    assess_total_count = _total(wrong.filter(regex="Assessment"))
    plans_total_count = _total(wrong.filter(regex="Plan"))
    found_total_count = _total(wrong.filter(regex="Foundations"))

    np.testing.assert_array_equal(
        total_count,
        (
            history_total_count
            + obj_total_count
            + assess_total_count
            + plans_total_count
            + found_total_count
        ),
    )

    total_wrong_df = pd.DataFrame(
        {
            "Total Keyword Count": total_count,
            "History Keyword Total": history_total_count,
            "Objective Keyword Total": obj_total_count,
            "Assessment Keyword Total": assess_total_count,
            "Plan Keyword Total": plans_total_count,
            "Foundations keyword Total": found_total_count,
        }
    )
    return total_wrong_df


def _replace_val(raw_string, value_list):
    """helper function for density calculation"""

    # splices phrases into individual words
    for i in value_list:
        raw_string = raw_string.replace(i, " ")
    t = jiwer.RemoveMultipleSpaces()(raw_string)
    t = jiwer.Strip()(t)
    return t


def _density(correct, res_len):
    """lexical density calculation"""

    val = ["]", "[", "'", ","]
    len_list = []
    list_words = correct.filter(regex="List").apply(
        lambda x: "".join(x.map(str)), axis=1
    )
    for i in list_words:
        t = _replace_val(i, val)
        str_len = len(t.split(" "))
        len_list.append(str_len)
    return round((len_list / res_len), 4) * 100


def lexical_summary(data):
    """main function for entire program takes the data and calculates all metrics
    summarizes, and compiles all information into three data frames"""

    case = data["Case/Scenario Name"]
    organization = data["Organization Unit"]
    icd10 = data["ICD10"]
    system = data["System"]

    correct, wrong, c_key, w_key, res_len = _keyword_algorithm(data, icd10, system)

    total_correct_df = _correct_total(correct)
    total_wrong_df = _wrong_total(wrong)

    correct_sub, correct_section = _keybank_count(c_key, "correct")
    wrong_sub, wrong_section = _keybank_count(w_key, "wrong")

    lex_density = _density(correct, res_len)

    correct_df = pd.concat(
        [total_correct_df, correct, correct_section, correct_sub], axis=1
    )
    wrong_df = pd.concat([total_wrong_df, wrong, wrong_section, wrong_sub], axis=1)

    total_percent = (
        round(
            (
                total_correct_df["Total Keyword Count"]
                / correct_df["Total KeyBank Count"]
            ),
            4,
        )
        * 100
    )
    a = correct_df[
        [
            "History Keyword Total",
            "Objective Keyword Total",
            "Assessment Keyword Total",
            "Plan Keyword Total",
            "Foundations keyword Total",
        ]
    ]
    b = correct_df[
        [
            "History KeyBank Count",
            "Objective KeyBank Count",
            "Assessment KeyBank Count",
            "Plan KeyBank Count",
            "Foundations KeyBank Count",
        ]
    ]
    percentage = round((a / b.values), 4) * 100
    percentage.columns = [
        "History Percentage",
        "Objective Percentage",
        "Assessment Percentage",
        "Plan Percentage",
        "Foundations Percentage",
    ]

    info_df = pd.DataFrame(
        {
            "ID": data["ID"],
            "Student Name": data["Student Name"],
            "Email": data["Email"],
            "Organization Unit": organization,
            "Case/Scenario Name": case,
            "ICD10": icd10,
            "System": system,
            "Presentation": data["Presentation"],
            "Lexical Density Percent": lex_density,
            "Total Percent Correct": total_percent,
            "Response Length": res_len,
        }
    )
    summary_df = pd.concat([info_df, percentage], axis=1)
    # 'Logical Sequence':sequenceBoolList,
    # 'Similarity to Physician Presentation':similarity}) V2
    correct_df = pd.concat(
        [
            info_df[
                [
                    "ID",
                    "Student Name",
                    "Email",
                    "Organization Unit",
                    "Case/Scenario Name",
                    "ICD10",
                    "System",
                ]
            ],
            correct_df,
        ],
        axis=1,
    )
    wrong_df = pd.concat(
        [
            info_df[
                [
                    "ID",
                    "Student Name",
                    "Email",
                    "Organization Unit",
                    "Case/Scenario Name",
                    "ICD10",
                    "System",
                ]
            ],
            wrong_df,
        ],
        axis=1,
    )
    return correct_df, wrong_df, summary_df
