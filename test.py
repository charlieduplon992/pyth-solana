#!/usr/bin/python3
import pyth
import sys

# The idea here is to test each type as input to each function.
# num, float, str, list, tuple, set, dict

test_cases = [
    # Ideally, we want to have tests for every possible token. Please don't
    # move the tests around, they should be in the same order as in doc.txt

    # 0
    ('01', '0\n1\n'),
    ('0.1', '0\n0.1\n'),
    ('007', '0\n0\n7\n'),
    # 0123456789
    ('-1023 5123', '-4100'),
    # \n
    ('1\n1', '1\n1'),
    ('\np1', '11'),
    ('+1\n2', '2\n3'),
    #
    ('1 1', '1'),
    ('1  1', '1'),
    # !
    ('!0', 'True'),
    ('!.0', 'True'),
    ('!"', 'True'),
    ('![', 'True'),
    ('!(', 'True'),
    ('!.{', 'True'),
    ('!.d[', 'True'),
    ('!q1 0', 'True'),
    ('!>2 1', 'False'),
    ('!]0', 'False'),
    ('!.5', 'False'),
    ('!(1', 'False'),
    ('!"Hallo', 'False'),
    ('!.{"Hallo', 'False'),
    ('!.d[,1 2', 'False'),
    # "
    ('"a', 'a\n'),
    ('"a"', 'a\n'),
    ('"\\', '\\\n'),
    ('"\\"', '"\n'),
    ('"\\""', '"\n'),
    ('"\\\\', '\\\n'),
    ('"\\\\\\"', '\\"\n'),
    ('"\n', '\n\n'),
    ('"\\\n', ''),
    ('"\0', '\0'),
    # #
    ('#1B1', '1\n1'),
    ('#1/1 0 2)2', '1\n2'),
    ('#/2-2Z=+Z1', '1\n2'),
    ('.A#[Y]0]1,1 0,4 5\\a', "[[], [1], [4, 5], 'a']"),
    ('%#2[3 4 5 1 0', '[3, 5, 1]'),
    ('_I#["aba""dasd""kewek', "['aba', 'kewek']"),
    # $
    ("\n$'\\0121'", '\n1'),
    ('+$1$2', '3'),
    # %
    ('%5 2', '1'),
    ('%6 3', '0'),
    ('%3U8', '[0, 3, 6]'),
    ('%2"YNeos', 'Yes'),
    ('%2(1 2 3 4', '(1, 3)'),
    ('%"i=%d"1', 'i=1'),
    ('%"%s=%d",\\i1', 'i=1'),
    ('%"%0.2f".12345', '0.12'),
    ('%U5 2', '[0, 1, 0, 1, 0]'),
    # &
    ('&1 0', '0'),
    ('&!0!0', 'True'),
    ('&!1!0', 'False'),
    ('&0/1Z', '0'),
    ('&2 3', '3'),
    # '
    # (
    ('(', '()'),
    ('()', '()'),
    ('(1', '(1,)'),
    ('(1 2', '(1, 2)'),
    ('(1"abc"3)', "(1, 'abc', 3)"),
    # )
    ('(1)2', '(1,)\n2'),
    ('V3N)0', '0\n1\n2\n0'),
    ('FN"abc"N)0', 'a\nb\nc\n0'),
    ('#/1Z)1', '1'),
    ('c"a b")1', "['a', 'b']\n1"),
    # *
    ('*3 2', '6'),
    ('*3 .5', '1.5'),
    ('.R*.1.2 5', '0.02'),
    (r'*\x5', 'xxxxx'),
    ('*2"ab', 'abab'),
    ('*3]0', '[0, 0, 0]'),
    ('*[1 2 3)2', '[1, 2, 3, 1, 2, 3]'),
    ('*2,Z1', '[0, 1, 0, 1]'),
    ('*U3U2', '[[0, 0], [0, 1], [1, 0], [1, 1], [2, 0], [2, 1]]'),
    ('*"abc"U2',
     "[['a', 0], ['a', 1], ['b', 0], ['b', 1], ['c', 0], ['c', 1]]"),
    ('*"abc",0 1',
     "[['a', 0], ['a', 1], ['b', 0], ['b', 1], ['c', 0], ['c', 1]]"),
    ('*"ab""cd', "['ac', 'ad', 'bc', 'bd']"),
    ('*.5,4T', '[2.0, 5.0]'),
    ('*_5"hi"', ''),
    ('*"blah"_2', 'halbhalb'),
    # +
    ('+4U3', '[4, 0, 1, 2]'),
    ('+U3U3', '[0, 1, 2, 0, 1, 2]'),
    ('+,1 0 3', '[1, 0, 3]'),
    ('+1 10', '11'),
    ('+1.2 3', '4.2'),
    ('+,1 2,3 4', '[1, 2, 3, 4]'),
    ('+"12""41"', '1241'),
    ('+.{2 3', '{2, 3}'),
    ('+.{2]1', '{1, 2}'),
    ('+FY', '0'),
    # ,
    (',"a"1', "['a', 1]"),
    # -
    ('-5 2', '3'),
    ('-["a""b""a")"a"', '[\'b\']'),
    ('-3U5', '[]'),
    ('-1"1001', ''),
    ('-1.{"1001', '{1}'),
    ('-1,01', '[]'),
    ('-"1001"1', '00'),
    ('-md"1001"1', "['1', '0', '0', '1']"),
    ('-.{1"1001', '{1}'),
    ('-.{1 1', 'set()'),
    ('-,01 1', '[0]'),
    # .
    ('1.', '1.0'),
    ('.1', '0.1'),
    ('2.1', '2.1'),
    # /
    ('/3.1 .7', '4'),
    ('/312 105', '2'),
    ('/[1 2 1 3 1)1', '3'),
    ('/UT_1', '0'),
    ('/"abcda""a"', '2'),
    ('/2,1 2', '[2, 1]'),
    # :
    (':G12 15', 'mno'),
    (':"abc"\\b0', 'True'),
    (':"abc"\\b"abc', 'aabcc'),
    (':"abcde",0 3]"lol"', 'lolbclole'),
    (':"####$$$$"%2U8\\x', 'x#x#x$x$'),
    (':U10r4 7 8', '[0, 1, 2, 3, 8, 8, 8, 7, 8, 9]'),
    (':,01]1 12', '[0, 12]'),
    (':15 22 3', '[15, 18, 21]'),
    (':1 2 .25', '[1, 1.25, 1.5, 1.75]'),
    (':10 _5 6', '[10, 4, -2]'),
    (':1.3 0 _.5', '[1.0, 0.5, 0]'),
    (':_5 5 _3', '[-4, -1, 2, 5]'),
    (':"hi 11:26.""\d\d?:\d\d(:\d\d)?"1', "['11:26']"),
    (':"hi blah ajsd adsad qe""([a-e]) "2', 'hi blah ajsdadsadqe'),
    (':"23{42}{4323""{|}"3', "['23', '42', '', '4323']"),
    (':"abcdef""b(c)d"4', "[['bcd', 'c']]"),
    # ;
    ('chc"4 5";', '[\'4\']'),
    ('V2V2INN;3', '1\n1\n3'),
    ('jL;c2<G6', "['a b c', 'd e f']"),
    ('m*dC;U4', '[0, 32, 64, 96]'),
    ('-R;["a b""def"" ', "['ab', 'def', '']"),
    ('.u+N;2k', '[\'\', \'"\', \'""\']'),
    ('m,;m,;m;1 1 1', "[[' ', [['', ['\\n']]]]]"),
    ('.W}H*G!;C+h;CZ\\a', '{'),
    # <
    ('<.{1U2', 'True'),
    ('<G6', 'abcdef'),
    ('<1 2', 'True'),
    ('<"a""B"', 'False'),
    ('<[1 1 1)[0 2)', 'False'),
    ('<2"abcde', 'abc'),
    ('<0"abcde', 'abcde'),
    ('<7"abcde', ''),
    ('<5[2 3 4)', '[]'),
    ('<\\m[\\a\\z\\g\\t', '[False, True, False, True]'),
    # =
    ('=Z=Y2YZ', '2\n2'),
    ('*4=G3', '12'),
    ('=hZZ', '1'),
    ('=/T3T', '3'),
    ('JU2=XZJ3ZJ', '[3, 1]\n[3, 1]'),
    ('=,GHU2GH', '0\n1'),
    ('=.aTT', '10'),
    ('=^2TT', '1024'),
    ('J]]3=s.TJJ', '[3]'),
    # >
    ('>.{1U2', 'False'),
    ('>G20', 'uvwxyz'),
    ('>1 2', 'False'),
    ('>"a""B"', 'True'),
    ('>[1 1 1)[0 2)', 'True'),
    ('>2U5', '[3, 4]'),
    ('>0U5', '[]'),
    ('>4"xyz', 'xyz'),
    ('>.5,01', '[True, False]'),
    # ?
    ('?1 2 1', '2'),
    ('?0 2 1', '1'),
    ('?1 2 /1 0', '2'),
    ('m?Jd*J50-50J2', '[50, 50]'),
    # @
    ('@4 2', '2.0'),
    (' XH,01 2@HU2', '2'),
    ('@U3T', '1'),
    ('@[1 2 5)U4', '[1, 2]'),
    ('@"abc"[\\a 1 2', 'a'),
    ('@,01[1 2', '[1]'),
    ('@.{U3[4 1 3 6', '{1}'),
    ('@16,2 4', '[4.0, 2.0]'),
    # A
    ('A,1 2', ''),
    ('A,1 2GH', '1\n2'),
    ('A,1 2HG', '2\n1'),
    ('A"ab"GH', 'a\nb'),
    # B
    ('V4BN', '0'),
    ('#12B1', '12\n1'),
    ('_B4', '[4, -4]'),
    ('+BT2', '[10, 12]'),
    ('_B"Hi', "['Hi', 'iH']"),
    # C
    ('C100', 'd'),
    ('C"d', '100'),
    ('C"abcd', '1633837924'),
    ('C,"ab""cd', "['ac', 'bd']"),
    ('C[U4r1 5r2 6', '[[0, 1, 2], [1, 2, 3], [2, 3, 4], [3, 4, 5]]'),
    ('C1633837924', 'abcd'),
    ('Cc150 2', 'K'),
    # D
    ('D.QR3.Q', '3'),
    ('DhdR*2dh7', '14'),
    ('Dw;w', ''),
    ('lD["acasd""cas""casd""ds', "['ds', 'cas', 'casd', 'acasd']"),
    ('/D5[5 1 7 8 4 2 3', '[1, 4, 2, 3, 5, 7, 8]'),
    # E
    ('+EE', '9', '4\n5'),
    # F
    ('Fk3k', '0\n1\n2'),
    ('Fd<G3d', 'a\nb\nc'),
    ('rF,1 5', '[1, 2, 3, 4]'),
    ('^F[4 3 2 1', '4096'),
    ('.!F3 2', '720'),
    (']Fd4', "[[[[' ']]]]"),
    ('*FY', "1"),
    # G
    ('G', 'abcdefghijklmnopqrstuvwxyz'),
    ('lG', '26'),
    # H
    ('H', '{}'),
    # I
    ('I3\n4', '4'),
    ('I0\n4', ''),
    ('Ip3', '3'),
    ('_I[1 2 1)', 'True'),
    ('SI[3 2 1)', 'False'),
    ('tIY', 'True'),
    ('wI1]1', 'blah\n[1]', 'blah'),
    ('-IG2', 'True'),
    ('-IG\\a', 'False'),
    ('{I', 'False', '[1, 1]'),
    ('{IsM.cF', 'True', '[1, 2, 3], 2'),
    # J
    ('J3J', '3'),
    # K
    ('KJ0KJ', '0\n0'),
    # L
    ('Lby5', '5'),
    ('L&b^2ytby3', '4'),
    ('<LG5', "['', 'a', 'ab', 'abc', 'abcd']"),
    ('<LJG5', "['', 'a', 'ab', 'abc', 'abcd']"),
    ('+L2"abcd', "['2a', '2b', '2c', '2d']"),
    ('JUT.(LJ[0 1 0 2', '[0, 2, 1, 5]'),
    ('XL0U2,4 2', '[[4, 1], [2, 1]]'),
    ("LhbLtb'2y2", '1\n3'),
    # M
    ('M+GHg1\\1', '11'),
    ('hMU3', '[1, 2, 3]'),
    ('SM,"ba""31', "['ab', '13']"),
    ('>MC,U5_U5', '[False, False, False, True, True]'),
    ('xMC,U5r4T', '[4, 4, 4, 4, 12]'),
    ('mM[,1 0,1 1,1 2', '[[], [1], [1, 1]]'),
    ('*M[[3 1 2)[8 7 6', '[6, 336]'),
    ('XM[[U3 1 4)[2 U3 _1', '[[0, 4, 2], [0, 1, 1]]'),
    ('_MM[,1 2,3 4', '[[-1, -2], [-3, -4]]'),
    ('/LL3[,1 2,3 4', '[[3, 1], [1, 0]]'),
    ('/RL3[,1 2,3 4', '[[0, 0], [1, 1]]'),
    ('*LLL2[,,1 4,5 2,,3 1,3 6', '[[[2, 8], [10, 4]], [[6, 2], [6, 12]]]'),
    ('++MC,U3U3Z', '[0, 2, 4, 0]'),
    # N
    ('N', '"'),
    # O
    ('O_1OT', '2'),
    ('O_1.ROZ2', '0.13'),
    ('O_1OG', 'e'),
    ('O_1%O^T1000 1000', '884'),
    ('O_1.RO1.0 2', '0.13'),
    ('O_1.RsO.j1 1 2', '0.13'),
    ('O_1O.{U7', '1'),
    # P
    ('PU3', '[0, 1]'),
    ('P"abc"', 'ab'),
    ('P2', '[2]'),
    ('P162', '[2, 3, 3, 3, 3]'),
    ('P1', '[]'),
    ('P_1', 'False'),
    ('P_2', 'True'),
    ('P0', '[]'),
    ('P_13', 'True'),
    ('P_21', 'False'),
    ('P12345', '[3, 5, 823]'),
    # Q
    ('lQ', '2', '[(),()]'),
    # R
    ('D.QR2.Q', '2'),
    ('D.QR2.Q.Q', '2\n2'),
    ('D.QR3Dyb.QRby1', '3\n1'),
    ('%R4[13 14 97', '[1, 2, 1]'),
    (',R1U3', '[[0, 1], [1, 1], [2, 1]]'),
    ('XR01[U2,4 3', '[[1, 1], [1, 3]]'),
    # S
    ('S"bca', 'abc'),
    ('S[3 2 4', '[2, 3, 4]'),
    ('S5', '[1, 2, 3, 4, 5]'),
    ('ScT3', '[1, 2, 3]'),
    # T
    ('T', '10'),
    # U
    ('U"abc', '[0, 1, 2]'),
    ('U3', '[0, 1, 2]'),
    ('U_4', '[-4, -3, -2, -1]'),
    ('U4.21523', '[0, 1, 2, 3]'),
    # V
    ('V4N', '0\n1\n2\n3\n'),
    ('VG ;N', 'z'),
    ('>V[1 5 7)[2 5 6)', '[False, False, True]'),
    ('jV[1 8 0)[2 6 9 5)', '[[1], [1, 2], [0]]'),
    ('_VU3_U3', '[[2, 0], [1, 1], [0, 2]]'),
    ('V2V2+NH', '0\n1\n1\n2'),
    ('V2.5N', '0\n1'),
    # v
    ('v"1', '1'),
    ('+2v"1', '3'),
    ('v"001', '1'),
    ('v"0', '0'),
    ('v"0,3', '(0, 3)'),
    ('v,\\1\\9', '[1, 9]'),
    # W
    ('W0Y', ''),
    ('W<lN10=+NN;N', '""""""""""""""""'),
    ('Wp0', '0'),
    ('V3_WN"abc', 'abc\ncba\ncba'),
    ('V2+W>N0\\f2', 'f\nf2'),
    ('m:Wd<G5 1 3 2', "['abcde', 'bc']"),
    ('|WdZ2', '2'),
    ('_W1J2', '-2'),
    ('_WZJ2', '2'),
    # X
    ('XUT5Z', '[0, 1, 2, 3, 4, 0, 6, 7, 8, 9]'),
    ('=YUT XY5Z', ''),
    ('=YUT XY15ZY', '[0, 1, 2, 3, 4, 0, 6, 7, 8, 9]'),
    ('X5UT5', '[0, 1, 2, 3, 4, 10, 6, 7, 8, 9]'),
    ('X"abc"1"d', 'adc'),
    ('X*2U5]1]2', '[0, 2, 2, 3, 4, 0, 2, 2, 3, 4]'),
    ('X"abcdef""ace""bdf', 'bbddff'),
    ('X"abcdef""abcde""12"', '12121f'),
    ('X"<></\\><>""</\\>', '><>\\/<><'),
    ('XHU3k', "{(0, 1, 2): ''}"),
    ('X(1 2 3)1]2', '(1, [2], 3)'),
    ('X1H3', '{1: 3}'),
    ('X1XH1 3 4', '{1: 7}'),
    ('X]1H1', '{(1,): 1}'),
    ('X1<G4\\w', 'awbcd'),
    ('X1<G4H', 'a{}bcd'),
    ('X0]k1', "['1']"),
    # Y
    ('Y', '[]'),
    # Z
    ('Z', '0'),
    # [
    ('[', '[]'),
    ('[1 ]3 5 9 .{1', '[1, [3], 5, 9, {1}]'),
    # \              (this text is here to prevent backslash line continuation)
    ('\\1', '1'),
    ('\\"', '"'),
    ('\\\\', '\\'),
    # ]
    (']', '[5]', '5'),
    (']1', '[1]'),
    # ^
    ('^3 3', '27'),
    ('^]1 2', '[[1, 1]]'),
    ('^,1 4 2', '[[1, 1], [1, 4], [4, 1], [4, 4]]'),
    ('^.{,1 2 1', '[{1}, {2}]'),
    ('^2,3 4', '[8, 16]'),
    # _
    ('_5', '-5'),
    ('_"abcd', 'dcba'),
    ('_XH3k', "{'': 3}"),
    # `
    ('`2', '2'),
    ('`\\2', "'2'"),
    # a
    ('aY3', '[3]'),
    ('aYU2', '[[0, 1]]'),
    ('J.{)aJ1', '{1}'),
    ('J.{)aJJ', '{()}'),
    ('a1 2', '1'),
    ('a.5_.1', '0.6'),
    ('a1,02', '[1, 1]'),
    # b
    ('b', '\n\n'),
    # c
    ('c1 2', '0.5'),
    ('hcG\\d', 'abc'),
    ('hc"as jdfaj', 'as'),
    ('c"absda"3', "['abs', 'da']"),
    ('c3"absda"', "['ab', 'sd', 'a']"),
    ('c"absda"[2 3', "['ab', 's', 'da']"),
    ('c[,1 \\a]3,1 \\a]5[1 2 3),1 \\a,3 5),1\\a', '[[], [[3]], [[5], [1, 2, 3]], [[3, 5]]]'),
    ('c["abd""""de")k', "[['abd'], ['de']]"),
    # d
    ('d', ' '),
    # e
    ('e1251', '1'),
    ('e[12 41 12)', '12'),
    # f
    ('f>T2U5', '[3, 4]'),
    ('f>T2 0', '3'),
    ('f>T2 .5', '2.5'),
    ('f1', '1'),
    # g
    ('g.{)[1', 'False'),
    ('gU5 3', '[2, 3, 4]'),
    ('g3 3', 'True'),
    ('g\\a,\\a\\b', '[True, False]'),
    # h
    ('h1', '2'),
    ('h[12 3 132', '12'),
    # i
    ('i"4123"5', '538'),
    ('i[12 431)2', '455'),
    ('i[2 4 5)7', '131'),
    ('i[2 4 5)_T', '165'),
    ('i[234 1234 12 341)1', '4'),
    ('i234 1234', '2'),
    ('ik3', '0'),
    ('i6U6', '[6, 1, 2, 3, 2, 1]'),
    # j
    ('j"a"[1 3 "n"', '1a3an'),
    ('j9 2', '[1, 0, 0, 1]'),
    ('j1"anc', 'a1n1c'),
    ('j3 1', '[0, 0, 0]'),
    ('j6_2', '[1, 1, 0, 1, 0]'),
    ('jU4', '0\n1\n2\n3'),
    ('j,1 5 2', '[[1], [1, 0, 1]]'),
    ('j8_3', '[1, 1, 2]'),
    ('j_5 2', '[-2, 1, 1]'),
    # k
    ('k', ''),
    # l
    ('l[123 1234 12)', '3'),
    ('l4', '2.0'),
    ('l_1', '4.532360141827194j'),
    # m
    ('m^d2 4', '[0, 1, 4, 9]'),
    ('m^d2"abc', "[['aa'], ['bb'], ['cc']]"),
    ('mm+d`k2 3', "[['00', '01'], ['10', '11'], ['20', '21']]"),
    ('mdmd4', '[0, 1, 2, 3]'),
    ('md4md3', '[0, 1, 2, 3]\n[0, 1, 2]'),
    ('md@T2', '[0, 1, 2]'),
    ('m', '[0, 1, 2]', '3'),
    ('mm', '[[], [0], [0, 1], [0, 1, 2]]', '4'),
    # n
    ('n1 2', 'True'),
    ('nYk', 'True'),
    # o
    ('o_NU3', '[2, 1, 0]'),
    ('oeCN"DFAFD', 'FFADD'),
    ('o%N2 5', '[0, 2, 4, 1, 3]'),
    # p
    ('p3', '3'),
    ('*2p3', '36'),
    # q
    ('q1 2', 'False'),
    ('qbb', 'True'),
    # r
    ('r4 9', '[4, 5, 6, 7, 8]'),
    ('r9 4', '[9, 8, 7, 6, 5]'),
    ('r"Ab"0', 'ab'),
    ('r"Ab"1', 'AB'),
    ('r"Ab"2', 'aB'),
    ('r"Ab daf"3', 'Ab Daf'),
    ('r"Ab daf"4', 'Ab daf'),
    ('r"Ab daf"5', 'Ab Daf'),
    ('r" asfd  "6', 'asfd'),
    ('r"432 23."7', '[432, 23.0]'),
    ('r"aaabb"8', "[[3, 'a'], [2, 'b']]"),
    ('r"3a2bc"9', 'aaabbc'),
    ('r[1 1 2 2)8', '[[2, 1], [2, 2]]'),
    ('r[[3 1)[2 \\a))9', "[1, 1, 1, 'a', 'a']"),
    ('r[[3 \\1)[2 \\a))9', '111aa'),
    ('sr\\A\\F', 'ABCDE'),
    ('lrk"aa', '24929'),
    ('`sr\\0\\5', "'01234'"),
    ('r\\f\\a', "['f', 'e', 'd', 'c', 'b']"),
    ('r9[,1 2', '[2]'),
    ('r1"bHla"', 'BHLA'),
    ('r2,04', '[[0, 1], [4, 3]]'),
    ('r\\a,\\b\\c', "[['a'], ['a', 'b']]"),
    # s
    ('s[1 2 4 2', '9'),
    ('s[1 2 \\4 2', '342'),
    ('sY', '[]'),
    ('s^123 .5', '11'),
    ('s"0123"', '123'),
    ('qs]M^T3U^T3', 'True'),
    ('s"', '0'),
    # t
    ('t5', '4'),
    ('tU5', '[1, 2, 3, 4]'),
    # u
    ('u*GhH4 1', '24',),
    ('u*GhH[2 4 2)1', '45'),
    ('um/Gd4Y', '[1, 2, 1, 0]'),
    ('u@,/G2h*3GG_40', '-20'),
    ('uXGH1m03', '[1, 1, 1]'),
    # v
    ('v"[1,[]]', '[1, []]'),
    # w
    ('w', '1i12', '1i12'),
    ('w2w', '1\n2\na', '1\na'),
    # x
    ('x1 2', '3'),
    ('x[1 2 3)2', '1'),
    ('xG\\r', '17'),
    ('xG\\1', '-1'),
    ('x0[1 10 0 2 0 4 _1 0', '[2, 4, 7]'),
    ('x"abc"c"nas abc asdf sad ab asdf abcd abc', '[1, 7]'),
    ('x"b1j2iod2de"2', '3'),
    # y
    ('y5', '10'),
    ('yk', "['']"),
    ('y"ab', "['', 'a', 'b', 'ab']"),
    ('yY', '[[]]'),
    ('yU3', '[[], [0], [1], [2], [0, 1], [0, 2], [1, 2], [0, 1, 2]]'),
    ('y{,01', '[[], [0], [1], [0, 1]]'),
    # z
    ('z', '1i12', '1i12'),
    ('z2z', '1\n2\n1', '1\na'),
    # {
    ('{"2341234123', '2341'),
    ('{[1 2 3 2 4 1 2', '[1, 2, 3, 4]'),
    ('{[Y', '[[]]'),
    ('{.{,2 1', '[1, 2]'),
    # |
    ('|3 4', '3'),
    ('|3 k', '3'),
    ('|ZY', '[]'),
    ('|Z4', '4'),
    # }
    ('}4U7', 'True'),
    ('}\\aG', 'True'),
    ('}2 9', '[2, 3, 4, 5, 6, 7, 8, 9]'),
    ('}_3 0', '[-3, -2, -1, 0]'),
    ('}9 4', '[9, 8, 7, 6, 5, 4]'),
    ('}2_2', '[2, 1, 0, -1, -2]'),
    ('}U5 1', '[[0, 1], [1], [2, 1], [3, 2, 1], [4, 3, 2, 1]]'),
    # ~
    ('~Z\\aZ', 'a'),
    ('*2~TNT', '20\n"'),
    ('+l~*N5N', '1"""""'),
    # .a
    ('.a1', '1'),
    ('.a_5', '5'),
    ('.a[1', '1.0'),
    ('.a[3 4', '5.0'),
    ('.R.a[[1_2),07)2', '9.06'),
    ('.aY', '0'),
    # .A
    ('.A[0 0 1', 'False'),
    ('.A[\\a \\b \\c', 'True'),
    ('.b*NY[3 3 2)[8 5 3', '[24, 15, 6]'),
    ('.b/NY4[6 3 2 9', '[0, 0, 1, 0]'),
    ('.b+NY9,4\\a', "[4, '1a']"),
    ('.b+NY,3 4 2', '[3, 5]'),
    ('.b%NY[,5 3,8 2', '[2, 0]'),
    # .B
    ('.B12', '1100'),
    ('.B\\a', '1100001'),
    ('.Bk', '0'),
    # .c
    ('.c0 0', '1'),
    ('.c0 3', '0'),
    ('.c3 0', '1'),
    ('.c5 12', '0'),
    ('.c17 12', '6188'),
    ('.c17 1', '17'),
    ('.c17 17', '1'),
    ('.c"abc"2', "['ab', 'ac', 'bc']"),
    # .C
    ('.C"abc"2', "['aa', 'ab', 'ac', 'bb', 'bc', 'cc']"),
    # .d
    ('.d[,1\\a,2\\r', "{1: 'a', 2: 'r'}"),
    ('.d.001', ''),
    # .D
    ('.D11 3', '[3, 2]'),
    ('.DS4 2', '[1, 2, 4]'),
    ('.DS4,02', '[2, 4]'),
    ('.D"abcde",1 3', 'ace'),
    # .e
    ('.e*bk"abd', "['', 'b', 'dd']"),
    # .E
    ('.E[0 0 1', 'True'),
    ('.E[kkY', 'False'),
    ('.E_12.5', '-12'),
    ('.E.5', '1'),
    # .f
    ('.fq9e^Z2 5 18', '[23, 27, 33, 37, 43]'),
    ('.fq9e^Z2 5', '[3, 7, 13, 17, 23]'),
    ('.f>CZ30000 5\\a', "['ua', 'ub', 'uc', 'ud', 'ue']"),
    ('.f>CZ20000 5\\A', "['NA', 'NB', 'NC', 'ND', 'NE']"),
    ('.fqsZ38 2\\0', "['38', '038']"),
    ('.fZ2\\}', "['}', '~']"),
    ('.f1 2k', "['', 'a']"),
    ('.fT1', '[1]'),
    ('.fT0', '[]'),
    ('.fT1U4', '[0]'),
    ('.fT5U4', '[0, 1, 2, 3]'),
    (' .fJZTZJ', '10'),
    # .F
    ('.F"{},{}",01', '0,1'),
    ('.F"{}"",01', ',01'),
    # .g
    ('.ge*kkT', '[[0], [1, 9], [2, 8], [5], [4, 6], [3, 7]]'),
    ('.g>k\\d"edafrb', "['dab', 'efr']"),
    # .h
    ('%.hq1 1 100', '15'),
    ('%.h1 100', '15'),
    ('%.h\\1 100', '74'),
    ('%.h]1 100', '54'),
    ('%.h.{1 100', '54'),
    ('%.hH100', '73'),
    # .H
    ('.H\\b', '62'),
    # .i
    ('.iU3r4 7', '[0, 4, 1, 5, 2, 6]'),
    ('.i"an""asdfa"', 'aansdfa'),
    ('.i.{U3.{r4 7', '[0, 4, 1, 5, 2, 6]'),
    # .I
    ('.I*GG100', '10.0'),
    ('.I*GG1', '1.0'),
    ('.I*GG16', '4.0'),
    ('.I*G^.n1G1', '0.567143290409784'),
    # .j
    ('.j0', '1j'),
    ('.j', '1j'),
    ('.j1', '(1+1j)'),
    ('.j3_2', '(3-2j)'),
    ('+.j2 1.j0', '(2+2j)'),
    ('-.j4 2.j0', '(4+1j)'),
    ('*.j3_2.j0', '(2+3j)'),
    ('^.j1_1 2', '-2j'),
    ('_.j1_1', '(-1+1j)'),
    ('c.j2_6 2', '(1-3j)'),
    ('%.j5 3 2', '(1+1j)'),
    ('.a.j1 1', '1.4142135623730951'),
    ('C.j0', '-1j'),
    ('P.j0', '1.5707963267948966'),
    ('s.j.5.8', '0.5'),
    ('e.j.5.8', '0.8'),
    ('>.j.5.5.j0', 'False'),
    ('<.j.5.5.j0', 'True'),
    # .l
    ('.l9 3', '2.0'),
    ('.R.l3)2', '1.1'),
    ('.l_1', '3.141592653589793j'),
    # .m
    ('.m_e*bbT', '[3, 7]'),
    ('.meCbG', "['d', 'n', 'x']"),
    # .M
    ('.M_e*ZZT', '[0]'),
    ('.MeCZG', "['c', 'm', 'w']"),
    # .n
    ('.R.n0 2', '3.14'),
    ('.n[]1 2[3]4 5', '[1, 2, 3, 4, 5]'),
    ('.n,1,2,,3 3 2', '[1, 2, 3, 3, 2]'),
    # .N
    ('.N+*NTY:3 2 4', '10'),
    # .O
    ('.O65', '101'),
    ('.O\\a', '141'),
    ('.OY', '0.0'),
    ('.O]1', '1.0'),
    ('.O[1 2 3', '2.0'),
    ('.O,05', '2.5'),
    # .p
    ('.p2', '[[0, 1], [1, 0]]'),
    ('.p"abc', "['abc', 'acb', 'bac', 'bca', 'cab', 'cba']"),
    ('.p_2', '[[-2, -1], [-1, -2]]'),
    # .P
    ('.P0 0', '1'),
    ('.P0 3', '0'),
    ('.P3 0', '1'),
    ('.P5 12', '0'),
    ('.P17 12', '2964061900800'),
    ('.P17 1', '17'),
    ('q.P17 17.!17', 'True'),
    ('.P"abc"2', "['ab', 'ac', 'ba', 'bc', 'ca', 'cb']"),
    ('.P123[\\a\\b\\c\\d\\e\\f\\g\\h)', "['a', 'b', 'd', 'c', 'e', 'g', 'h', 'f']"),
    ('.P40443[\\a\\b\\c\\d\\e\\f\\g\\h)', "['a', 'b', 'd', 'c', 'e', 'g', 'h', 'f']"),
    ('.P_40197[\\a\\b\\c\\d\\e\\f\\g\\h)', "['a', 'b', 'd', 'c', 'e', 'g', 'h', 'f']"),
    ('.P123"abcdefgh"', 'abdceghf'),
    # .q
    ('.q1', ''),
    # .Q
    ('.Q', "[3, 'a']", "3\n'a'"),
    # .r
    ('.r"asdf"G', 'bteg'),
    ('.r[1 2 11)UT', '[2, 3, 11]'),
    ('q.{"1ba".r.{"1az"G', 'True'),
    # .R
    ('.R4.5Z', '4'),
    ('.R3.141 2', '3.14'),
    ('.R3.1415926535 4.33', '3.14'),
    ('.R60.5 60.5', '60.5'),
    # .s
    ('.s"aabbbabada"\\a', 'bbbabad'),
    ('.s[0 1 0 2 0 0)0', '[1, 0, 2]'),
    ('.s[0 1 0 2 0 0)]0', '[1, 0, 2]'),
    ('.s[0 1 0 2 0 0),01', '[2]'),
    ('.sJU3ZJ', '[1, 2]\n[0, 1, 2]'),
    # .S
    ('O_1.Sv"0,3', '[3, 0]'),
    ('O_1.S"abc"', 'bca'),
    ('O_1.S3', '[1, 2, 0]'),
    ('O_1JU3.SJJ', '[1, 2, 0]\n[1, 2, 0]'),
    # .t
    ('.R.t1 0 2', '0.84'),
    ('.R.t1 8 2', '1.18'),
    ('.t,\\a"qwe"d', "['aq', ' w', ' e']"),
    ('.t,,01]4T', '[[0, 4], [1, 10]]'),
    ('.t,"}}}"\p', "['}p', '} ', '} ']"),
    # .T
    ('.TU4', '[[0, 0, 0], [1, 1], [2]]'),
    ('.T[[1 5 4)]2[3 4', '[[1, 2, 3], [5, 4], [4]]'),
    ('.Tc"a sdfa bsdf as', "['asba', 'dss', 'fd', 'af']"),
    ('.TY', '[]'),
    # .u
    ('.u*NhY5 1', '[1, 1, 2, 6, 24, 120]'),
    ('.ue*NN7', '[7, 9, 1]'),
    ('.ueC+`NY"abc"0', '[0, 5, 6, 3]'),
    ('.u@,/N2h*3NN3', '[3, 10, 5, 16, 8, 4, 2, 1]'),
    ('.uXNY1m03', '[[0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 1, 1]]'),
    ('.uaN02Y', '[[], [0], [0, 0]]'),
    # .U
    ('.Uh*bZ7', '1237'),
    ('.U*l`bZ"abcd', 'ddddddd'),
    # .v
    ('.v"+T1', '11'),
    ('.v"blah', '\n'),
    ('.v".v\\"sS4', '10'),
    # .w
    # .W
    ('.W<H5+Z1Z', '5'),
    ('.W0+Z1 3', '3'),
    ('.WteH*ZZ7', '2401'),
    # .x
    ('m.x/8d5T', '[5, 8, 4, 2, 2, 1, 1, 1, 1, 0]'),
    ('.x4 5', '4'),
    # .V
    ('.V1bI>b5B', '1\n2\n3\n4\n5\n6'),
    ('.V\\apbI>b\\fB', 'abcdefg'),
    # .y
    ('.yY', '[[]]'),
    ('.y"ab', "['', 'a', 'b', 'ab', 'ba']"),
    ('.y3', '[[], [0], [1], [2], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [0, 1, 2], \
[0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]]'),
    # .z
    ('l.z', '2', '1 2\n31'),
    # .Z
    ('.Z.Z"Hello World!', 'Hello World!'),
    ('l.Z"aaaaabbbbbcccccdddddeeeeefffff', '24'),
    # ."
    ('."adblah', 'bcacbcdabcabbcca'),
    ('."4T1420', 'I76POS'),
    ('."abc"Q', 'bbaaabb\n3', '3'),
    # .^
    ('.^3 99 10', '7'),
    # .&
    ('.&124 51', '48'),
    # .|
    ('.|124 51', '127'),
    ('S.|U3[1 5 11', '[0, 1, 2, 5, 11]'),
    ('.|,01[1 5', '[0, 1, 5]'),
    ('S.|"abd""def', 'abdef'),
    ('q.{U4.|.{1U4', 'True'),
    # .<
    ('.<U4 7', '[3, 0, 1, 2]'),
    ('.<3 7', '384'),
    ('.<Y4', '[]'),
    # .>
    ('.>U4 7', '[1, 2, 3, 0]'),
    ('.>1234 7', '9'),
    ('.>Y0', '[]'),
    # ./
    ('./"abc"', "[['abc'], ['a', 'bc'], ['ab', 'c'], ['a', 'b', 'c']]"),
    ('./U4', '[[[0, 1, 2, 3]], [[0], [1, 2, 3]], [[0, 1], [2, 3]], '
     '[[0, 1, 2], [3]], [[0], [1], [2, 3]], [[0], [1, 2], [3]], '
     '[[0, 1], [2], [3]], [[0], [1], [2], [3]]]'),
    ('./3', '[[1, 1, 1], [1, 2], [3]]'),
    ('./5', '[[1, 1, 1, 1, 1], [1, 1, 1, 2], [1, 1, 3], [1, 2, 2], '
     '[1, 4], [2, 3], [5]]'),
    # .*
    ('J,1 5r.*J', '[1, 2, 3, 4]'),
    # .+
    ('.+[2 0 3)', '[-2, 3]'),
    # .)
    ('JU3*2.)JJ', '4\n[0, 1]'),
    # .(
    ('JU3*2.(J1J', '2\n[0, 2]'),
    # .-
    ('.-"aabbaabc""aaab', 'babc'),
    ('.-,00]0', '[0]'),
    ('.-UTU5', '[5, 6, 7, 8, 9]'),
    # ._
    ('._4', '1'),
    ('.__3', '-1'),
    ('._.0', '0'),
    ('._U5', '[[0], [0, 1], [0, 1, 2], [0, 1, 2, 3], [0, 1, 2, 3, 4]]'),
    ('._"abc', "['a', 'ab', 'abc']"),
    # .:
    ('.:U4 2', '[[0, 1], [1, 2], [2, 3]]\n'),
    ('.:"dcba"3', "['dcb', 'cba']\n"),
    ('.:4 2', '[[0, 1], [1, 2], [2, 3]]\n'),
    ('.:4 .5', '[[0, 1], [1, 2], [2, 3]]\n'),
    ('.:4 3', '[[0, 1, 2], [1, 2, 3]]\n'),
    ('.:3', '[[0], [1], [2], [0, 1], [1, 2], [0, 1, 2]]\n'),
    ('.:"abc")1', "['a', 'b', 'c', 'ab', 'bc', 'abc']\n1\n"),
    ('.:"abc", 1 2', "['a', 'ab', 'b', 'bc', 'c']"),
    ('.:U3,1 3', '[[0], [0, 1, 2], [1], [2]]'),
    # .{
    ('.{', 'set()'),
    ('.{1', '{1}'),
    ('.{,01', '{0, 1}'),
    ('.{[Y', '{()}'),
    # .!
    ('.!5', '120'),
    ('.!0', '1'),
    ('.R.!.5 3', '0.886'),
    # .[
    ('.["hallo"\.8', 'hallo...'),
    ('.[\.8"hallo"', '...hallo'),
    ('.[8"hallo"\.', '.hallo..'),
    ('.["hallo"\.3', 'hallo.'),
    ('.[\.3"hallo"', '.hallo'),
    ('.[3"hallo"\.', 'hallo.'),
    ('.["hallo""-+"T', 'hallo-+-+-'),
    ('.["-+"T"hallo"', '-+-+-hallo'),
    ('.[T"hallo""-+"', '-+hallo-+-'),
    ('.[U3Z5', '[0, 1, 2, 0, 0]'),
    ('.[Z5U3', '[0, 0, 0, 1, 2]'),
    ('.[5U3Z', '[0, 0, 1, 2, 0]'),
    ('.[6U3Z', '[0, 0, 1, 2, 0, 0]'),
    ('.[U5 05', '[0, 1, 2, 3, 4]'),
    ('.[Y1 3', '[1, 1, 1]'),
    ('.[3Y1', '[1, 1, 1]'),
    ('.[1 3Y', '[1, 1, 1]'),
    ('.[k\+3', '+++'),
    ('.[3k\+', '+++'),
    ('.[\+3k', '+++'),
    # .?
    ('IZ2).?3', '3'),
    ('V4N).?4', '0\n1\n2\n3\n4\n'),
    # Docs
    ('"Hello World!', 'Hello World!'),
    ('FNrZTN', '0\n1\n2\n3\n4\n5\n6\n7\n8\n9'),
    ('K1FNr1hQ=*KN;K', '120', '5'),
    ('L*3by12', '36'),
    ('L?b*bytb1yQ', '120', '5'),
    ('u*GhHQ1', '120', '5'),
    ('J1VQJKZ=ZJ=J+ZK', '1\n1\n2\n3\n5\n8\n13\n21\n34\n55', '10'),
    ('A(Z1)VQHA(H+HG', '1\n1\n2\n3\n5\n8\n13\n21\n34\n55', '10'),
    ('#/100T=T-T1', '10\n11\n12\n14\n16\n20\n25\n33\n50\n100'),
]


def test(pyth_code, expected_output, input_message=''):
    output, error = pyth.run_code(pyth_code, input_message)

    if input_message != '':
        if error:
            sys.exit("Error thrown by %s on input %s\n%s" %
                     (pyth_code, input_message, error))
        if output != expected_output and output != expected_output + '\n':
            sys.exit("Bad output by %s on input %s"
                     "\nExpected: %r.\nReceived: %r" %
                     (pyth_code, input_message, expected_output, output))
    else:
        if error:
            sys.exit("Error thrown by %s\n%s" %
                     (pyth_code, error))
        if output != expected_output and output != expected_output + '\n':
            sys.exit("Bad output by %s"
                     "\nExpected: %r.\nReceived: %r" %
                     (pyth_code, expected_output, output))

if __name__ == '__main__':
    for test_case in test_cases:
        test(*test_case)
    print("All " + str(len(test_cases)) + ' tests passed')
