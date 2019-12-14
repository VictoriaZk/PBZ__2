from datetime import datetime, date

MIN_WORK_AGE = 18

RETIREMENT_AGE_FEMALE = 55

MAX_RANK = 18

# RU

SEX_CHOICES_RU = [
    ('MALE', 'муж'),
    ('FEMALE', 'жен'),
]

MARTIAL_CHOICES_RU = [
    ('MARRIED', 'женат/замужем'),
    ('UNMARRIED', 'холост/не замужем'),
]

YEARS = [year for year in range(
    1920, datetime.now().year - MIN_WORK_AGE + 1
    )]
