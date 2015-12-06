from __future__ import absolute_import
from .. import parse_demographics

import os
import csv


def prepare_for_tests():
    with open('demographics.csv', 'w') as csvfile:
        file_writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        file_writer.writerow(['id', 'gender', 'age', 'forrest_seen_count'])
        file_writer.writerow(['1', 'm', '30-35', '5'])
        file_writer.writerow(['2', 'm', '30-35', '1'])
    test_object = parse_demographics.parse_csv('demographics.csv')
    return test_object


def test_seen_most_times():
	test_subjects = prepare_for_tests()
	seen_count = parse_demographics.seen_most_times(test_subjects)
	assert seen_count[0] == 5 
	assert seen_count[1] == 1
	delete_file()


def test_seen_least_times():
	test_subjects = prepare_for_tests()
	seen_count = parse_demographics.seen_least_times(test_subjects)
	assert seen_count[0] == 1
	assert seen_count[1] == 2
	delete_file()


def test_find_id_by_gender():
	test_subjects = prepare_for_tests()
	id_list = parse_demographics.find_id_by_gender(test_subjects, 'm')
	assert len(id_list) == 2
	assert id_list[0] == 'm'
	assert id_list[1] == 'm'
	delete_file()


def test_find_count_by_id():
	test_subjects = prepare_for_tests()
	count = parse_demographics.find_count_by_id(test_subjects, 1)
	assert count == 5
	delete_file()


def delete_file():
	os.remove('demographics.csv')
