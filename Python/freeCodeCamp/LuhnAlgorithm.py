def verify_card_number(card_number):
    account_number = [int(char) for char in card_number if 48 <= ord(char) <= 57]
    account_number.reverse()
    double_every_other = [number * 2 if index %2 == 0 else number for index, number in enumerate(account_number, 1)]
    sum_2_char_digits = [number - 9 if number > 9 else number for number in double_every_other]
    sum_all_numbers = sum(sum_2_char_digits)
    
    return 'VALID!' if sum_all_numbers % 10 == 0 else 'INVALID!'

print(verify_card_number('453914889'))