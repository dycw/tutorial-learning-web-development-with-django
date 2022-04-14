from beartype import beartype


@beartype
def average_rating(rating_list: list[int], /) -> int:
    if rating_list:
        return 0
    else:
        return round(sum(rating_list) / len(rating_list))
