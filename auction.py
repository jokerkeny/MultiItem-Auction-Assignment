'''
@Author: jokerkeny
@Date: 2020-07-21 00:13:33
@LastEditors: jokerkeny
@LastEditTime: 2020-07-21 22:25:41
@Description:
for interactive version, see 'auction.ipynb'
'''
import pandas as pd
import itertools
import numpy as np

# User Input

USE_people_names = True  # If set False, it'll be automatically generated
people_names = [
    "Derick",
    "Elaine",
    "Fred",
]
USE_item_names = True  # If set False, item_names would be item_1, item_2, ...
item_names = [
    "Guest room",
    "Bedroom",
    "Master Bedroom",
]
bid_matrix = [
    [1500, 2000, 2500],  # sounds he cares more about room type
    [1700, 2000, 2300],  # room type doesn't matter that much
    [1600, 2100, 2300],  # he has a low budget and care less about room
]

# The excess payment would be equally returned to all people
adj_method = "equal_return"

# The final payment would be normalized to original total amount
# better for large payment difference
# adj_method = "normalize"

# Program
if not USE_people_names:
    people_names = ["person_" + i for i in range(1, len(bid_matrix)+1)]
if not USE_item_names:
    item_names = ["item_" + i for i in range(1, len(bid_matrix)+1)]


def check(bid_matrix, people_names, item_names):
    # dimension check
    n = len(bid_matrix)

    if n != len(people_names):
        print("People_names length not equal to bid_matrix number of rows")
        raise Exception

    if n != len(item_names):
        print("item_names length not equal to bid_matrix number of rows")
        raise Exception

    for row in bid_matrix:
        if n != len(row):
            print("bid_matrix rows' lengths \
                are not all equal to its number of rows")
            raise Exception
    # total amount check
    total_amount = sum(bid_matrix[0])
    for irow in range(1, n):
        if total_amount != sum(bid_matrix[irow]):
            print(
                f"total_amount of f{people_names[irow]}'s bids \
                    differs from others'")
            raise Exception

    # positive check (don't need)


def print_bidmatrix(bid_matrix, people_names, item_names):
    df = pd.DataFrame(bid_matrix, index=people_names, columns=item_names)
    print("The bid prices of all people for all items:")
    print("============================================================")
    print(df)
    print("============================================================")
    print("The total price of all items: ", sum(bid_matrix[0]))


def assignment(bid_matrix, people_names):
    # algorithm 1: check all permutation O(n!)
    n = len(bid_matrix)
    people_indices = list(range(n))
    max_bidsum = 0
    for perm in itertools.permutations(people_indices):
        bidsum = 0
        for i_item, i_ppl in enumerate(perm):
            bidsum += bid_matrix[i_ppl][i_item]
        if max_bidsum < bidsum:
            max_bidsum = bidsum
            best_perm = perm
    print("The highest sum of bids among all possible assignments is:",
          max_bidsum)

    original_bids = []
    ppl_assigned = []
    for i_item, i_ppl in enumerate(best_perm):
        original_bids.append(bid_matrix[i_ppl][i_item])
        ppl_assigned.append(people_names[i_ppl])
    return max_bidsum, original_bids, ppl_assigned
    # algorithm 2: Hungarian algorithm O(n3)


def adjust_payment(max_bidsum, bid_matrix, adj_method):
    total_amount = sum(bid_matrix[0])
    if adj_method == "equal_return":
        eachret = (max_bidsum-total_amount)/len(bid_matrix)
        adj_payment = np.array(original_bids)-eachret
    elif adj_method == "normalize":
        adj_payment = np.array(original_bids)*total_amount/max_bidsum
    else:
        print("adj_method not defined")
        raise Exception
    return adj_payment


def print_result(ppl_assigned, original_bids, adj_payment, item_names):
    df = pd.DataFrame({'Assignment': ppl_assigned, 'orig_bid': original_bids,
                       'Final_payment': adj_payment}, index=item_names)
    print("Items assignment and payment needed:")
    print("============================================================")
    print(df)
    print("============================================================")


check(bid_matrix, people_names, item_names)
print_bidmatrix(bid_matrix, people_names, item_names)
max_bidsum, original_bids, ppl_assigned = assignment(bid_matrix, people_names)
adj_payment = adjust_payment(max_bidsum, bid_matrix, adj_method)
print_result(ppl_assigned, original_bids, adj_payment, item_names)
