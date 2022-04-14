from beartype import beartype


@beartype
def average_rating(rating_list: list[int], /) -> int:
    if len(rating_list) >= 1:
        return round(sum(rating_list) / len(rating_list))
    else:
        return 0
