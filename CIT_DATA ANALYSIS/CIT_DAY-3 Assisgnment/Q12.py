"""Unique Visitors: A website stores visitor IDs i a list.
Find:
Total unique visitors between two days
common visitors between two days
Visitors who visited only one day 1 using sets."""

visitors_d1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
visitors_d2 = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

day1_set = set(visitors_d1)
day2_set = set(visitors_d2)

total_unique_visitors = day1_set | day2_set
print("Total unique visitors between two days:", total_unique_visitors)
common_visitors = day1_set & day2_set
print("Common visitors between two days:", common_visitors)
visitors_only_day1 = day1_set - day2_set
print("Visitors who visited only day 1:", visitors_only_day1)
