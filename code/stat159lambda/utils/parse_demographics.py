import csv


class Subject:
    """
    Subject class in which each instance represents one subject. Each subject
    has attributes:
    1. id : int
    2. gender : string
    3. age_range : string
    4. forrest_seen_count : int

    Parameters
    ----------
    demographics : a row of the demographics.csv file that's being read in by 
    parse_csv
    """
    def __init__(self, demographics):
        self.id = int(demographics["id"])
        self.gender = demographics["gender"]
        self.age_range = demographics["age"]
        if demographics["forrest_seen_count"]:
            self.forrest_seen_count = int(demographics["forrest_seen_count"])
        # Accounting for case of missing data
        else:
            self.forrest_seen_count = -1


def parse_csv(fname):
    """
	Parses the given demographics.csv file and creates instances for each
    subject. Returns subject instances in a list.

	Parameters
	----------
	fname : string

	Returns 
	-------
	subjects : array
	"""
    with open(fname) as csvfile:
        reader = csv.DictReader(csvfile)
        return [Subject(row) for row in reader]


def seen_most_times(subjects):
    """
    Identifies which subject has seen Forrest Gump the most times. Ties are
    broken arbitrarily. If no one has seen Forrest Gump before, returned
    subject ID will be -1.

    Parameters
    ---------
    subjects : array

    Returns
    -------
    subject : tuple
    Tuple contains both the count of how many times watched and subject's ID
    """
    count = 0
    subject_id = -1
    for subject in subjects:
        if subject.forrest_seen_count > count:
            count = subject.forrest_seen_count
            subject_id = subject.id
    return (count, subject_id)


def seen_least_times(subjects):
    """
    Identifies which subject has seen Forrest Gump the least times. Ties are
    broken arbitrarily.

    Parameters
    ----------
    subjects : array

    Returns
    -------
    subject : tuple
    Tuple contains both the count of how many times watched and subject's ID
    """
    min_count = subjects[0].forrest_seen_count
    subject_id = subject[0].id
    for subject in subjects[1:]:
        if subject.forrest_seen_count < min_count:
            min_count = subject.forrest_seen_count
            subject_id = subject.id
    return (min_count, subject_id)


def find_id_by_gender(subjects, gender):
    """
    Identifies the ID's of a given gender

    Parameters
    ----------
    subjects : array
    gender : string

    Returns 
    -------
    ids : int array
    """
    return [s.gender for s in subjects if s.gender == gender]


def find_count_by_id(subjects, sid):
    """
    Finds the number of times a particular subject has seen Forrest Gump given
    his or her ID.

    Parameters
    ----------
    subjects : array
    sid : int

    Returns
    -------
    forrest_seen_count : int
    """
    for subject in subjects:
        if subject.id == sid:
            return subject.forrest_seen_count
