import unittest
from unittest.mock import Mock
import util
import constcount as cc
import datetime


class utilTest(unittest.TestCase):
    def test_test(self):
        mock = Mock(return_value="gg11")

        self.assertEqual(1, 1)

    def test_dictMerge(self):
        # g
        firstDict = {"abc": 1, "bcd": 1}
        secDict = {"bcd": 1, "aaa": 1}
        answerDict = {"abc": 1, "bcd": 2, "aaa": 1}
        # w
        resDict = util.dictMerge(firstDict, secDict)
        # t

        self.assertEqual(resDict, answerDict)

    def test_namuDataCreate(self):
        # g
        firstDict = {"a": 100, "b": 2, "c": 5, "d": 20, "e": 10,
                     "f": 11, "g": 21, "h": 42, "i": 22, "j": 23, "k": 19, "l": 8}
        answerArray = ["a", "h", "j", "i", "g", "d", "k", "f", "e", "l"]
        answerArray.append("day")

        # w
        # 2, 48, 336, 1440
        resArray = util.namuDataCreate(
            48-1, firstDict, cc.COUNT, cc.COUNTKIND)
        # t
        self.assertEqual(resArray, answerArray)

    def test_sumRanking(self):
        # g
        firstDataDict = {'na_time': datetime.datetime(2022, 6, 6, 12, 2, 49), 'na_one': 'aa', 'na_two': 'bb',
                         'na_three': 'cc', 'na_four': 'dd', 'na_five': 'ee', 'na_six': 'ff', 'na_seven': 'gg',
                         'na_eight': 'hh', 'na_nine': 'ii', 'na_ten': 'jj', 'id': 1}

        firstAnswerDict = {'aa': 10, 'bb': 9, 'cc': 8, 'dd': 7,
                           'ee': 6, 'ff': 5, 'gg': 4, 'hh': 3, 'ii': 2, 'jj': 1}

        # w
        res = util.sumRanking(firstDataDict)

        # t
        self.assertEqual(res, firstAnswerDict)


if __name__ == '__main__':
    unittest.main()
