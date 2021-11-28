def get_name_phone(tracker):
    name = tracker.get_slot('name')
    phone = tracker.get_slot('phone')
    return name, phone


def _yes_no_buttons():
    return [
        ("Yes", "Yes"),
        ("No", "No"),
    ]


def _feel_better_buttons():
    return [
        ("I feel better", "I feel better"),
        ("I feel worse", "I feel worse"),
    ]
