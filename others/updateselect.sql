select a.solutionID, a.day, a.count,
floor((a.f1/b.total)*a.count) as f1,
floor((a.f2/b.total)*a.count) as f2,
floor((a.f3/b.total)*a.count) as f3,
floor((a.f4/b.total)*a.count) as f4,
floor((a.f5/b.total)*a.count) as f5,
floor((a.f6/b.total)*a.count) as f6,
floor((a.f7/b.total)*a.count) as f7,
floor((a.f8/b.total)*a.count) as f8,
floor((a.f9/b.total)*a.count) as f9,
floor((a.f10/b.total)*a.count) as f10,
floor((a.f11/b.total)*a.count) as f11,
floor((a.f12/b.total)*a.count) as f12,
floor((a.f13/b.total)*a.count) as f13,
floor((a.f14/b.total)*a.count) as f14,
floor((a.f15/b.total)*a.count) as f15,
floor((a.f16/b.total)*a.count) as f16,
floor((a.f17/b.total)*a.count) as f17,
floor((a.f18/b.total)*a.count) as f18,
floor((a.f19/b.total)*a.count) as f19,
floor((a.f20/b.total)*a.count) as f20,
floor((a.f21/b.total)*a.count) as f21,
floor((a.f22/b.total)*a.count) as f22,
floor((a.f23/b.total)*a.count) as f23,
floor((a.f24/b.total)*a.count) as f24,
floor((a.f25/b.total)*a.count) as f25,
floor((a.f26/b.total)*a.count) as f26,
floor((a.f27/b.total)*a.count) as f27,
floor((a.f28/b.total)*a.count) as f28,
floor((a.f29/b.total)*a.count) as f29,
floor((a.f30/b.total)*a.count) as f30,
floor((a.f31/b.total)*a.count) as f31,
floor((a.f32/b.total)*a.count) as f32,
floor((a.f33/b.total)*a.count) as f33,
floor((a.f34/b.total)*a.count) as f34,
floor((a.f35/b.total)*a.count) as f35,
floor((a.f36/b.total)*a.count) as f36,
floor((a.f37/b.total)*a.count) as f37,
floor((a.f38/b.total)*a.count) as f38,
floor((a.f39/b.total)*a.count) as f39,
floor((a.f40/b.total)*a.count) as f40,
floor((a.f41/b.total)*a.count) as f41,
floor((a.f42/b.total)*a.count) as f42,
floor((a.f43/b.total)*a.count) as f43,
floor((a.f44/b.total)*a.count) as f44,
floor((a.f45/b.total)*a.count) as f45,
floor((a.f46/b.total)*a.count) as f46,
floor((a.f47/b.total)*a.count) as f47,
floor((a.f48/b.total)*a.count) as f48,
floor((a.f49/b.total)*a.count) as f49,
floor((a.f50/b.total)*a.count) as f50

from `solution_day_show` as a join

(SELECT solutionID, day, (
f1 + 2*f2 + 3*f3 + 4*f4 + 5*f5 + 6*f6 + 7*f7 + 8*f8 + 9*f9 + 10*f10 +
11*f11 + 12*f12 + 13*f13 + 14*f14 + 15*f15 + 16*f16 + 17*f17 + 18*f18 + 19*f19 + 20*f20 +
21*f21 + 22*f22 + 23*f23 + 24*f24 + 25*f25 + 26*f26 + 27*f27 + 28*f28 + 29*f29 + 30*f30 +
31*f31 + 32*f32 + 33*f33 + 34*f34 + 35*f35 + 36*f36 + 37*f37 + 38*f38 + 39*f39 + 40*f40 +
41*f41 + 42*f42 + 43*f43 + 44*f44 + 45*f45 + 46*f46 + 47*f47 + 48*f48 + 49*f49 + 50*f50
) AS total
FROM  `solution_day_show` where day = '2016-12-12') as b on a.solutionID=b.solutionID and a.day=b.day




update `solution_day_show`  inner join
(SELECT solutionID, day, (
f1 + 2*f2 + 3*f3 + 4*f4 + 5*f5 + 6*f6 + 7*f7 + 8*f8 + 9*f9 + 10*f10 +
11*f11 + 12*f12 + 13*f13 + 14*f14 + 15*f15 + 16*f16 + 17*f17 + 18*f18 + 19*f19 + 20*f20 +
21*f21 + 22*f22 + 23*f23 + 24*f24 + 25*f25 + 26*f26 + 27*f27 + 28*f28 + 29*f29 + 30*f30 +
31*f31 + 32*f32 + 33*f33 + 34*f34 + 35*f35 + 36*f36 + 37*f37 + 38*f38 + 39*f39 + 40*f40 +
41*f41 + 42*f42 + 43*f43 + 44*f44 + 45*f45 + 46*f46 + 47*f47 + 48*f48 + 49*f49 + 50*f50
) AS total
FROM  `solution_day_show` where day = '2016-12-12') as b on `solution_day_show`.solutionID=b.solutionID and `solution_day_show`.day=b.day 

set
f1 = floor((`solution_day_show`.f1/b.total)*`solution_day_show`.count)






update `solution_day_show` as a inner join
(SELECT solutionID, day, (
f1 + 2*f2 + 3*f3 + 4*f4 + 5*f5 + 6*f6 + 7*f7 + 8*f8 + 9*f9 + 10*f10 +
11*f11 + 12*f12 + 13*f13 + 14*f14 + 15*f15 + 16*f16 + 17*f17 + 18*f18 + 19*f19 + 20*f20 +
21*f21 + 22*f22 + 23*f23 + 24*f24 + 25*f25 + 26*f26 + 27*f27 + 28*f28 + 29*f29 + 30*f30 +
31*f31 + 32*f32 + 33*f33 + 34*f34 + 35*f35 + 36*f36 + 37*f37 + 38*f38 + 39*f39 + 40*f40 +
41*f41 + 42*f42 + 43*f43 + 44*f44 + 45*f45 + 46*f46 + 47*f47 + 48*f48 + 49*f49 + 50*f50
) AS total
FROM  `solution_day_show` where day = '2016-12-12') as b on a.solutionID=b.solutionID and a.day=b.day 

set
f1 = floor((a.f1/b.total)*a.count),
f2 = floor((a.f2/b.total)*a.count),
f3 = floor((a.f3/b.total)*a.count),
f4 = floor((a.f4/b.total)*a.count),
f5 = floor((a.f5/b.total)*a.count),
f6 = floor((a.f6/b.total)*a.count),
f7 = floor((a.f7/b.total)*a.count),
f8 = floor((a.f8/b.total)*a.count),
f9 = floor((a.f9/b.total)*a.count),
f10 = floor((a.f10/b.total)*a.count),
f11 = floor((a.f11/b.total)*a.count),
f12 = floor((a.f12/b.total)*a.count),
f13 = floor((a.f13/b.total)*a.count),
f14 = floor((a.f14/b.total)*a.count),
f15 = floor((a.f15/b.total)*a.count),
f16 = floor((a.f16/b.total)*a.count),
f17 = floor((a.f17/b.total)*a.count),
f18 = floor((a.f18/b.total)*a.count),
f19 = floor((a.f19/b.total)*a.count),
f20 = floor((a.f20/b.total)*a.count),
f21 = floor((a.f21/b.total)*a.count),
f22 = floor((a.f22/b.total)*a.count),
f23 = floor((a.f23/b.total)*a.count),
f24 = floor((a.f24/b.total)*a.count),
f25 = floor((a.f25/b.total)*a.count),
f26 = floor((a.f26/b.total)*a.count),
f27 = floor((a.f27/b.total)*a.count),
f28 = floor((a.f28/b.total)*a.count),
f29 = floor((a.f29/b.total)*a.count),
f30 = floor((a.f30/b.total)*a.count),
f31 = floor((a.f31/b.total)*a.count),
f32 = floor((a.f32/b.total)*a.count),
f33 = floor((a.f33/b.total)*a.count),
f34 = floor((a.f34/b.total)*a.count),
f35 = floor((a.f35/b.total)*a.count),
f36 = floor((a.f36/b.total)*a.count),
f37 = floor((a.f37/b.total)*a.count),
f38 = floor((a.f38/b.total)*a.count),
f39 = floor((a.f39/b.total)*a.count),
f40 = floor((a.f40/b.total)*a.count),
f41 = floor((a.f41/b.total)*a.count),
f42 = floor((a.f42/b.total)*a.count),
f43 = floor((a.f43/b.total)*a.count),
f44 = floor((a.f44/b.total)*a.count),
f45 = floor((a.f45/b.total)*a.count),
f46 = floor((a.f46/b.total)*a.count),
f47 = floor((a.f47/b.total)*a.count),
f48 = floor((a.f48/b.total)*a.count),
f49 = floor((a.f49/b.total)*a.count),
f50 = floor((a.f50/b.total)*a.count)

where a.day='2016-12-12'


