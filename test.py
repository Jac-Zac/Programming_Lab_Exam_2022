#!/usr/bin/env python3
#==============================
# Test  
#==============================

import unittest
import tempfile
import warnings

from esame import CSVTimeSeriesFile, compute_avg_monthly_difference, ExamException

score = 0

class TestAndGrade(unittest.TestCase):

    # Roba per il testing
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)


    #===========================================================
    # Test per il 18: tre ore di dati, tutti i dati presenti.
    #===========================================================

    def test_correctness(self):

        with tempfile.NamedTemporaryFile('w+t') as file:

            file.write('date,passengers\n')

            # First year
            file.write('1949-01,112\n')
            file.write('1949-02,118\n')
            file.write('1949-03,132\n')
            file.write('1949-04,129\n')
            file.write('1949-05,121\n')
            file.write('1949-06,135\n')
            file.write('1949-07,148\n')
            file.write('1949-08,148\n')
            file.write('1949-09,136\n')
            file.write('1949-10,119\n')
            file.write('1949-11,104\n')
            file.write('1949-12,118\n')

            # Second year
            file.write('1950-01,115\n')
            file.write('1950-02,126\n')
            file.write('1950-03,141\n')
            file.write('1950-04,135\n')
            file.write('1950-05,125\n')
            file.write('1950-06,149\n')
            file.write('1950-07,170\n')
            file.write('1950-08,170\n')
            file.write('1950-09,158\n')
            file.write('1950-10,133\n')
            file.write('1950-11,114\n')
            file.write('1950-12,140\n')

            # Third year
            file.write('1951-01,145\n')
            file.write('1951-02,150\n')
            file.write('1951-03,178\n')
            file.write('1951-04,163\n')
            file.write('1951-05,172\n')
            file.write('1951-06,178\n')
            file.write('1951-07,199\n')
            file.write('1951-08,199\n')
            file.write('1951-09,184\n')
            file.write('1951-10,162\n')
            file.write('1951-11,146\n')
            file.write('1951-12,166\n')

            # Needed things 
            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
            results = compute_avg_monthly_difference(time_series,"1949","1951")

            self.assertEqual(results[0], 16.5)
            self.assertEqual(results[1], 16)
            self.assertEqual(results[2], 23)

            global score; score += 18 # Increase score

    #===================================================
    #  Test che ci sia la variabile "name" nell'init
    #===================================================
    def test_csv_file_interface(self):

        with tempfile.NamedTemporaryFile('w+t') as file:

            # First year
            file.write('date,passengers\n')
            file.write('1949-01,112\n')
            file.write('1949-02,118\n')
            file.seek(0)

            time_series_file = CSVTimeSeriesFile(name = file.name)
            time_series = time_series_file.get_data()

            # Test su lunghezze
            self.assertTrue(len(time_series) in [1,2])

            global score; score += 0.5 # Increase score

    #===================================================
    #  Test su errori esistenza e tipo del nome del file
    #===================================================
    def test_csv_file_interface_nonexisttent_file(self):

        with self.assertRaises(ExamException):
            time_series_file = CSVTimeSeriesFile(name='file_non_esistente.csv')
            time_series_file.get_data()
        global score; score += 0.5 # Increase score

    def test_csv_file_interface_wrong_type(self):

        with self.assertRaises(ExamException):
            time_series_file = CSVTimeSeriesFile(name=[])
            time_series_file.get_data()

        with self.assertRaises(ExamException):
            time_series_file = CSVTimeSeriesFile(name=None)
            time_series_file.get_data()

        global score; score += 0.5 # Increase score

    def test_csv_file_empty(self):

        with tempfile.NamedTemporaryFile('w+t') as file:

            # Scrivo i contenuti nel file di test
            file.write('date,passengers\n')


            time_series_file = CSVTimeSeriesFile(file.name)

            try:
                time_series = time_series_file.get_data()
            except ExamException:
                pass

            global score; score += 0.5 # Increase score

    # Print the score
    @classmethod
    def tearDownClass(cls):
        global score

        print('\n\n----------------')
        print('| Voto: {}/20 |'.format(score))
        print('----------------\n')

# Run the tests
unittest.main()
