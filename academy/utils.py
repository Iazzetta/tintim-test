def get_grade_letter(grade_number: int) -> str:
    if grade_number >= 97 and grade_number <= 100:
        return 'A+'
    elif grade_number >= 93 and grade_number <= 96:
        return 'A'
    elif grade_number >= 90 and grade_number <= 92:
        return 'A-'
    elif grade_number >= 87 and grade_number <= 89:
        return 'B+'
    elif grade_number >= 83 and grade_number <= 86:
        return 'B'
    elif grade_number >= 80 and grade_number <= 82:
        return 'B-'
    elif grade_number >= 77 and grade_number <= 79:
        return 'C+'
    elif grade_number >= 73 and grade_number <= 76:
        return 'C'
    elif grade_number >= 70 and grade_number <= 72:
        return 'C-'
    elif grade_number >= 60 and grade_number <= 69:
        return 'D'
    return 'F'

def get_grade_number(grade_letter: str) -> int:
    if grade_letter == 'A+':
        return 100
    elif grade_letter == 'A':
        return 96
    elif grade_letter == 'A-':
        return 92
    elif grade_letter == 'B+':
        return 89
    elif grade_letter == 'B':
        return 86
    elif grade_letter == 'B-':
        return 82
    elif grade_letter == 'C+':
        return 79
    elif grade_letter == 'C':
        return 76
    elif grade_letter == 'C-':
        return 72
    elif grade_letter == 'D':
        return 69
    return 59