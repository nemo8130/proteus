# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 17:35:53 2015

@author: fredrik
"""

import numpy as np


def make_features(names, window_size):

    all_features = np.zeros((1, window_size * 20 + 42))

    for name in names:

        score_features = get_score_features(name, window_size)               # 300
        aa_features_extra = get_aa_features_extra(name, window_size)         #  20 + 9
        disorder_features = get_disorder_features(name, window_size)         #   4
        order_features = get_order_features(name)                            #   3
        structure_features = get_structure_features(name, window_size)       #   3
        topography_features = get_topography_features(name)                  #   2
        conservation_features = get_conservation_features(name, window_size) #   1
                                                                             # 342 features in total
        # Split the old and new aa features
        aa_features_comp = aa_features_extra[:, :20]
        aa_features_extra = aa_features_extra[:, 20:]

        features = np.hstack((score_features,         # 300 [:300]
                              aa_features_comp,       #  20 [300:320]
                              disorder_features,      #   4 [320:324]
                              order_features,         #   3 [324:327]
                              structure_features,     #   3 [327:330]
                              aa_features_extra,      #   9 [330:339]
                              topography_features,    #   2 [339:341]
                              conservation_features)) #   1 [341:342]

        all_features = np.vstack((all_features, features))

    all_features = all_features[1:,:]

    return all_features


def get_score_features(name, window_size):

    window_residues = range(-window_size/2 + 1, window_size/2 + 1)

    filename = name + ".mtx"
    columns = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11,
               12, 13, 14, 15, 16, 17, 18, 19, 21, 22]

    with open(filename) as f:
        lines = f.readlines()

    row_list = []
    for line in lines[14:]:
        col_list = []
        words = line.split()
        for idx in columns:
            col_list.append(int(words[idx].strip()))
        row_list.append(col_list)

    scoring_matrix = np.array(row_list)

    score_features = []
    for residue in range(scoring_matrix.shape[0]):
        row_scores = []
        for window_residue in window_residues:
            row = residue + window_residue
            if not 0 <= row <= scoring_matrix.shape[0] - 1:
                row_scores.extend([0] * 20)
            else:
                row_scores.extend(scoring_matrix[row,:])
        score_features.append(row_scores)

    score_features = np.array(score_features)

    return score_features


def get_aa_features_extra(name, window_size):

    filename = name + ".mtx"
    aa_data={"A": {"polar": 0,
                 "nonpolar": 1,
                 "a_polar": 0,
                 "b_polar": 0,
                 "neutral": 1,
                 "positive": 0,
                 "negative": 0,
                 "hydropathy": 1.8,
                 "weight": 89},
           "C": {"polar": 0,
                 "nonpolar": 1,
                 "a_polar": 0,
                 "b_polar": 0,
                 "neutral": 1,
                 "positive": 0,
                 "negative": 0,
                 "hydropathy": 2.5,
                 "weight": 121},
           "D": {"polar": 0,
                 "nonpolar": 0,
                 "a_polar": 1,
                 "b_polar": 0,
                 "neutral": 0,
                 "positive": 0,
                 "negative": 1,
                 "hydropathy": -3.5,
                 "weight": 133},
           "E": {"polar": 0,
                 "nonpolar": 0,
                 "a_polar": 1,
                 "b_polar": 0,
                 "neutral": 0,
                 "positive": 0,
                 "negative": 1,
                 "hydropathy": -3.5,
                 "weight": 147},
           "F": {"polar": 0,
                 "nonpolar": 1,
                 "a_polar": 0,
                 "b_polar": 0,
                 "neutral": 1,
                 "positive": 0,
                 "negative": 0,
                 "hydropathy": 2.8,
                 "weight": 165},
           "G": {"polar": 0,
                 "nonpolar": 1,
                 "a_polar": 0,
                 "b_polar": 0,
                 "neutral": 1,
                 "positive": 0,
                 "negative": 0,
                 "hydropathy": -0.4,
                 "weight": 75},
           "H": {"polar": 0,
                 "nonpolar": 0,
                 "a_polar": 0,
                 "b_polar": 1,
                 "neutral": 0.9,
                 "positive": 0.1,
                 "negative": 0,
                 "hydropathy": -3.2,
                 "weight": 155},
           "I": {"polar": 0,
                 "nonpolar": 1,
                 "a_polar": 0,
                 "b_polar": 0,
                 "neutral": 1,
                 "positive": 0,
                 "negative": 0,
                 "hydropathy": 4.5,
                 "weight": 131},
           "K": {"polar": 0,
                 "nonpolar": 0,
                 "a_polar": 0,
                 "b_polar": 1,
                 "neutral": 0,
                 "positive": 1,
                 "negative": 0,
                 "hydropathy": -3.9,
                 "weight": 146},
           "L": {"polar": 0,
                 "nonpolar": 1,
                 "a_polar": 0,
                 "b_polar": 0,
                 "neutral": 1,
                 "positive": 0,
                 "negative": 0,
                 "hydropathy": 3.8,
                 "weight": 131},
           "M": {"polar": 0,
                 "nonpolar": 1,
                 "a_polar": 0,
                 "b_polar": 0,
                 "neutral": 1,
                 "positive": 0,
                 "negative": 0,
                 "hydropathy": 1.9,
                 "weight": 149},
           "N": {"polar": 1,
                 "nonpolar": 0,
                 "a_polar": 0,
                 "b_polar": 0,
                 "neutral": 1,
                 "positive": 0,
                 "negative": 0,
                 "hydropathy": -3.5,
                 "weight": 132},
           "P": {"polar": 0,
                 "nonpolar": 1,
                 "a_polar": 0,
                 "b_polar": 0,
                 "neutral": 1,
                 "positive": 0,
                 "negative": 0,
                 "hydropathy": -1.6,
                 "weight": 115},
           "Q": {"polar": 1,
                 "nonpolar": 0,
                 "a_polar": 0,
                 "b_polar": 0,
                 "neutral": 1,
                 "positive": 0,
                 "negative": 0,
                 "hydropathy": -3.5,
                 "weight": 146},
           "R": {"polar": 0,
                 "nonpolar": 0,
                 "a_polar": 0,
                 "b_polar": 1,
                 "neutral": 0,
                 "positive": 1,
                 "negative": 0,
                 "hydropathy": -4.5,
                 "weight": 174},
           "S": {"polar": 1,
                 "nonpolar": 0,
                 "a_polar": 0,
                 "b_polar": 0,
                 "neutral": 1,
                 "positive": 0,
                 "negative": 0,
                 "hydropathy": -0.8,
                 "weight": 105},
           "T": {"polar": 1,
                 "nonpolar": 0,
                 "a_polar": 0,
                 "b_polar": 0,
                 "neutral": 1,
                 "positive": 0,
                 "negative": 0,
                 "hydropathy": -0.7,
                 "weight": 119},
           "V": {"polar": 0,
                 "nonpolar": 1,
                 "a_polar": 0,
                 "b_polar": 0,
                 "neutral": 1,
                 "positive": 0,
                 "negative": 0,
                 "hydropathy": 4.2,
                 "weight": 117},
           "W": {"polar": 0,
                 "nonpolar": 1,
                 "a_polar": 0,
                 "b_polar": 0,
                 "neutral": 1,
                 "positive": 0,
                 "negative": 0,
                 "hydropathy": -0.9,
                 "weight": 204},
           "Y": {"polar": 1,
                 "nonpolar": 0,
                 "a_polar": 0,
                 "b_polar": 0,
                 "neutral": 1,
                 "positive": 0,
                 "negative": 0,
                 "hydropathy": -1.3,
                 "weight": 181}
           }

    
#    aa_dict = "../../aa_data.dict"
    aaList = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L',
              'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

    with open(filename) as f:
        lines = f.readlines()
    seq = lines[1].strip()

#    with open(aa_dict) as f:
#        line = f.read()
#    aa_data = eval(line)

    aa_features = []
    for residue in range(len(seq)):
        window_residues = range(-window_size/2, window_size/2 + 1)
        current_window = []
        row_shares = []
        polar = 0
        nonpolar = 0
        a_polar = 0
        b_polar = 0
        neutral = 0
        positive = 0
        negative = 0
        hydropathy = 0
        weight = 0
        for window_residue in window_residues:
            idx = residue + window_residue
            if not 0 <= idx <= len(seq) - 1:
                pass
            else:
                current_window.extend(seq[idx])

        for aa in aaList:
            count = current_window.count(aa)
            row_shares.append(round(float(count)/float(len(current_window)), 5))
            polar += aa_data[aa]["polar"] * count
            nonpolar += aa_data[aa]["nonpolar"] * count
            a_polar += aa_data[aa]["a_polar"] * count
            b_polar += aa_data[aa]["b_polar"] * count
            neutral += aa_data[aa]["neutral"] * count
            positive += aa_data[aa]["positive"] * count
            negative += aa_data[aa]["negative"] * count
            hydropathy += aa_data[aa]["hydropathy"] * count
            weight += aa_data[aa]["weight"] * count

            residue_features = row_shares + [polar, nonpolar, a_polar, b_polar,
                                             neutral, positive, negative,
                                             hydropathy, weight]

        aa_features.append(residue_features)

    aa_features = np.array(aa_features)

    return aa_features


def get_disorder_features(name, window_size):

    window_residues = range(-window_size/2 + 1, window_size/2 + 1)

    filename = name + ".diso"
    disorder_cutoff = 0.5

    with open(filename) as f:
        lines = f.readlines()[3:]
    scores = []
    for line in lines:
        words = line.split()
        scores.append(float(words[3].strip()))

    disorder_features = []
    for residue in range(len(scores)):
        if scores[residue] < disorder_cutoff:
            length = 0
            start = 0
            stop = 0

        else:
            start_idx = residue
            found_start = False
            at_end = False
            while not found_start and not at_end:
                if scores[start_idx] >= disorder_cutoff:
                    if start_idx == 0:
                        at_end = True
                    else:
                        start_idx -= 1    # Move to next residue and try again
                else:
                    found_start = True
                    start_idx += 1    # The region actually stopped last round
            start = round(float(start_idx) / len(scores), 5)

            stop_idx = residue
            found_stop = False
            at_end = False
            while not found_stop and not at_end:
                if scores[stop_idx] >= disorder_cutoff:
                    if stop_idx == len(scores) - 1:
                        at_end = True
                    else:
                        stop_idx += 1    # Move to next residue and try again
                else:
                    found_stop = True
                    stop_idx -= 1    # The region actually stopped last round
            stop = round(float(stop_idx + 1) / len(scores), 5)

            length = stop_idx - start_idx + 1

        current_window = []
        for window_residue in window_residues:
            idx = residue + window_residue
            if not 0 <= idx <= len(scores) - 1:
                pass
            else:
                current_window.append(scores[idx])

        score = np.array(current_window).mean()

        row_features = [score, length, start, stop]

        disorder_features.append(row_features)

    disorder_features = np.array(disorder_features)

    return disorder_features


def get_order_features(name):

    filename = name + ".diso"
    disorder_cutoff = 0.5

    with open(filename) as f:
        lines = f.readlines()[3:]
    scores = []
    for line in lines:
        words = line.split()
        scores.append(float(words[3].strip()))

    order_features = []
    for residue in range(len(scores)):

        if scores[residue] < disorder_cutoff:

            start_idx = residue
            found_start = False
            at_end = False
            while not found_start and not at_end:
                if scores[start_idx] < disorder_cutoff:
                    if start_idx == 0:
                        at_end = True
                    else:
                        start_idx -= 1    # Move to next residue and try again
                else:
                    found_start = True
                    start_idx += 1    # The region actually stopped last round
            start = round(float(start_idx) / len(scores), 5)

            stop_idx = residue
            found_stop = False
            at_end = False
            while not found_stop and not at_end:
                if scores[stop_idx] < disorder_cutoff:
                    if stop_idx == len(scores) - 1:
                        at_end = True
                    else:
                        stop_idx += 1    # Move to next residue and try again
                else:
                    found_stop = True
                    stop_idx -= 1    # The region actually stopped last round
            stop = round(float(stop_idx + 1) / len(scores), 5)

            length = stop_idx - start_idx + 1

        else:
            length = 0
            start = 0
            stop = 0

        #score = scores[residue] # Used in disorder instead

        row_features = [length, start, stop]

        order_features.append(row_features)

    order_features = np.array(order_features)

    return order_features


def get_structure_features(name, window_size):

    window_residues = range(-window_size/2 + 1, window_size/2 + 1)

    filename = name + ".ss"
    with open(filename) as f:
        lines = f.readlines()

    scores_coil = []
    scores_helix = []
    scores_extended = []
    scores = []

    for line in lines:
        words = line.split()
        scores_coil.append(float(words[3]))
        scores_helix.append(float(words[4]))
        scores_extended.append(float(words[5]))

    for residue in range(len(scores_helix)):
        current_window_coil = []
        current_window_helix = []
        current_window_extended = []
        for window_residue in window_residues:
            idx = residue + window_residue
            if not 0 <= idx <= len(scores_helix) - 1:
                pass
            else:
                current_window_coil.append(scores_coil[idx])
                current_window_helix.append(scores_helix[idx])
                current_window_extended.append(scores_extended[idx])

        scores.append([np.array(current_window_coil).mean(),
                       np.array(current_window_helix).mean(),
                       np.array(current_window_extended).mean()])

    structure_features = np.array(scores)

    return structure_features


def get_topography_features(name):

    filename = name + ".diso"

    with open(filename) as f:
        lines = f.readlines()[3:]
    scores = []
    for line in lines:
        words = line.split()
        scores.append(float(words[3].strip()))

    top_features = []
    for residue in range(len(scores)):
        start_idx = residue
        start_score = scores[start_idx]
        found_extreme_left = False
        at_end = False

        while not found_extreme_left and not at_end:
            if not ((scores[start_idx] < start_score - 0.1) or (scores[start_idx] > start_score + 0.1)):
                if start_idx == 0:
                    at_end = True
                else:
                    start_idx -= 1    # Move to next residue and try again
            else:
                found_extreme_left = True
        extreme_score_left = scores[start_idx]

        stop_idx = residue
        found_extreme_right = False
        at_end = False
        while not found_extreme_right and not at_end:
            if not ((scores[stop_idx] < start_score - 0.1) or (scores[stop_idx] > start_score + 0.1)):
                if stop_idx == len(scores) - 1:
                    at_end = True
                else:
                    stop_idx += 1    # Move to next residue and try again
            else:
                found_extreme_right = True
        extreme_score_right = scores[stop_idx]

        top_length = stop_idx - start_idx + 1

        if extreme_score_left < start_score - 0.1 and extreme_score_right < start_score - 0.1:
            top_feature = 1
        elif extreme_score_left > start_score + 0.1 and extreme_score_right > start_score + 0.1:
            top_feature = -1
        else:
            top_feature = 0

        top_features.append([top_feature, top_length])

    top_features = np.array(top_features)

    return top_features


def get_conservation_features(name, window_size):

    window_residues = range(-window_size/2 + 1, window_size/2 + 1)

    filename = name + ".psi"
    with open(filename) as f:
        lines = f.readlines()[3:-6]

    con_scores = []
    for line in lines:
        words = line.split()
        con_scores.append([float(words[42].strip())])

    con_features = []
    for residue in range(len(con_scores)):
        current_window_scores = []
        for window_residue in window_residues:
            idx = residue + window_residue
            if not 0 <= idx <= len(con_scores) - 1:
                pass
            else:
                current_window_scores.extend(con_scores[idx])
        con_features.append(np.array(current_window_scores).mean())

    con_features = np.array(con_features)

    return con_features.reshape((len(con_features), 1))
