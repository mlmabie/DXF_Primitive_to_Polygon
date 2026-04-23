# HATCH Boundary Inspection

Input: `Airport Doors_MEZZ.dxf`

## Companion Layer Counts

- Total HATCH entities on companion layers: `1404`
- `A-EXTERNAL WALL HATCH`: `24`
- `A-MEZZANINE WALL FULL HATCH`: `1276`
- `A-WALL 1 HATCH`: `11`
- `A-WALL 2 HATCH`: `93`

## Boundary Path Shape

- Boundary path count distribution: `{1: 1325, 2: 44, 3: 15, 4: 9, 5: 4, 6: 2, 7: 1, 9: 1, 10: 1, 41: 1, 42: 1}`
- Path flag distribution:
  - `1` (external): `108` paths
  - `5` (external, derived): `19` paths
  - `6` (polyline, derived): `17` paths
  - `7` (external, polyline, derived): `1149` paths
  - `16` (outermost): `4` paths
  - `17` (external, outermost): `2` paths
  - `21` (external, derived, outermost): `8` paths
  - `22` (polyline, derived, outermost): `102` paths
  - `23` (external, polyline, derived, outermost): `226` paths
- Polyline vertex count distribution:
  - `3` vertices: `4` paths
  - `4` vertices: `759` paths
  - `5` vertices: `57` paths
  - `6` vertices: `163` paths
  - `7` vertices: `36` paths
  - `8` vertices: `155` paths
  - `9` vertices: `28` paths
  - `10` vertices: `62` paths
  - `11` vertices: `8` paths
  - `12` vertices: `31` paths
  - `13` vertices: `18` paths
  - `14` vertices: `20` paths
  - `15` vertices: `15` paths
  - `16` vertices: `27` paths
  - `17` vertices: `17` paths
  - `18` vertices: `10` paths
  - `20` vertices: `13` paths
  - `21` vertices: `3` paths
  - `22` vertices: `4` paths
  - `23` vertices: `2` paths
  - `24` vertices: `8` paths
  - `25` vertices: `4` paths
  - `26` vertices: `4` paths
  - `27` vertices: `2` paths
  - `28` vertices: `4` paths
  - `29` vertices: `4` paths
  - `30` vertices: `2` paths
  - `31` vertices: `1` paths
  - `32` vertices: `1` paths
  - `33` vertices: `1` paths
  - `36` vertices: `3` paths
  - `39` vertices: `2` paths
  - `40` vertices: `2` paths
  - `41` vertices: `1` paths
  - `44` vertices: `4` paths
  - `48` vertices: `4` paths
  - `51` vertices: `2` paths
  - `58` vertices: `2` paths
  - `60` vertices: `1` paths
  - `61` vertices: `2` paths
  - `66` vertices: `2` paths
  - `72` vertices: `1` paths
  - `78` vertices: `1` paths
  - `96` vertices: `2` paths
  - `120` vertices: `1` paths
  - `136` vertices: `1` paths
- Edge path edge count distribution:
  - `3` edges: `3` paths
  - `4` edges: `73` paths
  - `5` edges: `18` paths
  - `6` edges: `10` paths
  - `7` edges: `4` paths
  - `8` edges: `5` paths
  - `9` edges: `7` paths
  - `10` edges: `2` paths
  - `11` edges: `4` paths
  - `12` edges: `3` paths
  - `13` edges: `5` paths
  - `16` edges: `1` paths
  - `17` edges: `1` paths
  - `23` edges: `1` paths
  - `28` edges: `1` paths
  - `30` edges: `1` paths
  - `38` edges: `1` paths
  - `136` edges: `1` paths
- Edge type codes inside edge paths:
  - `1` (line): `952`
  - `2` (circular_arc): `51`
  - `3` (elliptic_arc): `32`

## Nested Paths / Holes

- HATCH entities with more than one boundary path: `79`
  - `A-WALL 2 HATCH` entity #12: flags `[7, 22]` (external+polyline+derived; polyline+derived+outermost)
  - `A-WALL 2 HATCH` entity #38: flags `[7, 22]` (external+polyline+derived; polyline+derived+outermost)
  - `A-WALL 2 HATCH` entity #41: flags `[7, 22]` (external+polyline+derived; polyline+derived+outermost)
  - `A-WALL 2 HATCH` entity #43: flags `[7, 22, 22, 22, 22, 22]` (external+polyline+derived; polyline+derived+outermost; polyline+derived+outermost; polyline+derived+outermost; polyline+derived+outermost; polyline+derived+outermost)
  - `A-WALL 2 HATCH` entity #44: flags `[7, 22, 22, 22]` (external+polyline+derived; polyline+derived+outermost; polyline+derived+outermost; polyline+derived+outermost)
  - `A-WALL 2 HATCH` entity #46: flags `[22, 7, 6]` (polyline+derived+outermost; external+polyline+derived; polyline+derived)
  - `A-WALL 2 HATCH` entity #49: flags `[7, 22]` (external+polyline+derived; polyline+derived+outermost)
  - `A-WALL 2 HATCH` entity #54: flags `[7, 22, 6]` (external+polyline+derived; polyline+derived+outermost; polyline+derived)
  - `A-WALL 2 HATCH` entity #57: flags `[7, 22, 22, 22]` (external+polyline+derived; polyline+derived+outermost; polyline+derived+outermost; polyline+derived+outermost)
  - `A-WALL 2 HATCH` entity #59: flags `[7, 22, 22]` (external+polyline+derived; polyline+derived+outermost; polyline+derived+outermost)
  - `A-WALL 2 HATCH` entity #61: flags `[7, 22, 22, 22]` (external+polyline+derived; polyline+derived+outermost; polyline+derived+outermost; polyline+derived+outermost)
  - `A-WALL 2 HATCH` entity #64: flags `[7, 22, 6]` (external+polyline+derived; polyline+derived+outermost; polyline+derived)
  - `A-WALL 2 HATCH` entity #66: flags `[7, 22, 22, 22]` (external+polyline+derived; polyline+derived+outermost; polyline+derived+outermost; polyline+derived+outermost)
  - `A-WALL 2 HATCH` entity #71: flags `[7, 22]` (external+polyline+derived; polyline+derived+outermost)
  - `A-WALL 2 HATCH` entity #73: flags `[7, 22]` (external+polyline+derived; polyline+derived+outermost)
  - `A-WALL 2 HATCH` entity #81: flags `[23, 22]` (external+polyline+derived+outermost; polyline+derived+outermost)
  - `A-WALL 2 HATCH` entity #86: flags `[7, 22, 22, 22, 22]` (external+polyline+derived; polyline+derived+outermost; polyline+derived+outermost; polyline+derived+outermost; polyline+derived+outermost)
  - `A-MEZZANINE WALL FULL HATCH` entity #124: flags `[7, 22, 22]` (external+polyline+derived; polyline+derived+outermost; polyline+derived+outermost)
  - `A-MEZZANINE WALL FULL HATCH` entity #140: flags `[7, 22]` (external+polyline+derived; polyline+derived+outermost)
  - `A-MEZZANINE WALL FULL HATCH` entity #141: flags `[22, 7, 22, 22, 6]` (polyline+derived+outermost; external+polyline+derived; polyline+derived+outermost; polyline+derived+outermost; polyline+derived)
  - ... 59 more

## Verbatim Samples

### Sample 1: `A-WALL 1 HATCH`

- Parsed paths: `[{'flags': 17, 'labels': ['external', 'outermost'], 'polyline': False, 'edge_types': [1, 1, 1, 1], 'vertices': 0, 'edges': 4}]`

```dxf
  0
HATCH
  5
20883
330
70
100
AcDbEntity
  8
A-WALL 1 HATCH
100
AcDbHatch
 10
0.0
 20
0.0
 30
0.0
210
0.0
220
0.0
230
1.0
  2
ANGLE
 70
     0
 71
     1
 91
        1
 92
       17
 93
        4
 72
     1
 10
21579.39338239805
 20
14917.94584618567
 11
21513.86230023844
 21
15183.90217880055
 72
     1
 10
21513.86230023844
 20
15183.90217880055
 11
21513.86230023844
 21
15183.90217880055
 72
     1
 10
21513.86230023844
 20
15183.90217880055
 11
21579.39338239805
 21
14917.94584618567
 72
     1
 10
21579.39338239805
 20
14917.94584618567
 11
21579.39338239805
 21
14917.94584618567
 97
        1
330
108B3
 75
     1
 76
     1
 52
0.0
 41
1.0
 77
     0
 78
     2
 53
0.0
 43
0.0
 44
0.0
 45
0.0
 46
6.985
 79
     2
 49
5.08
 49
-1.905
 53
90.0
 43
0.0
 44
0.0
 45
-6.985
 46
0.0000000000000004
 79
     2
 49
5.08
 49
-1.905
 98
        1
 10
0.0
 20
0.0
1001
GradientColor1ACI
1070
     5
1001
GradientColor2ACI
1070
     2
1001
ACAD
1010
0.0
1020
0.0
1030
0.0
```

### Sample 2: `A-WALL 1 HATCH`

- Parsed paths: `[{'flags': 1, 'labels': ['external'], 'polyline': False, 'edge_types': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 'vertices': 0, 'edges': 38}]`

```dxf
  0
HATCH
  5
20884
330
70
100
AcDbEntity
  8
A-WALL 1 HATCH
100
AcDbHatch
 10
0.0
 20
0.0
 30
0.0
210
0.0
220
0.0
230
1.0
  2
ANGLE
 70
     0
 71
     1
 91
        1
 92
        1
 93
       38
 72
     1
 10
20658.28261538675
 20
15839.56305185257
 11
20668.17964739596
 21
15829.66109460106
 72
     1
 10
20668.17964739596
 20
15829.66109460106
 11
20675.25247400427
 21
15836.73040317898
 72
     1
 10
20675.25247400427
 20
15836.73040317898
 11
20658.28613341726
 21
15853.70518703872
 72
     1
 10
20658.28613341726
 20
15853.70518703872
 11
20600.99623789067
 21
15796.44378755748
 72
     1
 10
20600.99623789067
 20
15796.44378755745
 11
20674.51704710104
 21
15722.88639083199
 72
     1
 10
20674.51704710104
 20
15722.88639083199
 11
20731.80694262764
 21
15780.14779031323
 72
     1
 10
20731.80694262764
 20
15780.14779031323
 11
20714.84060204063
 21
15797.12257417297
 72
     1
 10
20714.84060204063
 20
15797.12257417297
 11
20707.76777543254
 21
15790.05326559505
 72
     1
 10
20707.76777543254
 20
15790.05326559505
 11
20717.66480744151
 21
15780.15130834351
 72
     1
 10
20717.66480744151
 20
15780.15130834351
 11
20674.52056513132
 21
15737.02852601811
 72
     1
 10
20674.52056513132
 20
15737.02852601811
 11
20615.13837307679
 21
15796.44026952717
 72
     1
 10
20615.13837307679
 20
15796.44026952717
 11
20658.28261538675
 21
15839.56305185257
 72
     1
 10
20658.28261538675
 20
15839.56305185257
 11
20668.17964739596
 21
15829.66109460106
 72
     1
 10
20668.17964739596
 20
15829.66109460106
 11
20675.25247400427
 21
15836.73040317898
 72
     1
 10
20675.25247400427
 20
15836.73040317898
 11
20658.28613341726
 21
15853.70518703872
 72
     1
 10
20658.28613341726
 20
15853.70518703872
 11
20600.99623789067
 21
15796.44378755748
 72
     1
 10
20600.99623789067
 20
15796.44378755745
 11
20674.51704710104
 21
15722.88639083199
 72
     1
 10
20674.51704710104
 20
15722.88639083199
 11
20731.80694262764
 21
15780.14779031323
 72
     1
 10
20731.80694262764
 20
15780.14779031323
 11
20714.84060204063
 21
15797.12257417297
 72
     1
 10
20714.84060204063
 20
15797.12257417297
 11
20707.76777543254
 21
15790.05326559505
 72
     1
 10
20707.76777543254
 20
15790.05326559505
 11
20717.66480744151
 21
15780.15130834351
 72
     1
 10
20717.66480744151
 20
15780.15130834351
 11
20674.52056513132
 21
15737.02852601811
 72
     1
 10
20674.52056513132
 20
15737.02852601811
 11
20615.13837307679
 21
15796.44026952717
 72
     1
 10
20615.13837307679
 20
15796.44026952717
 11
20658.28261538675
 21
15839.56305185257
 72
     1
 10
20658.28261538675
 20
15839.56305185257
 11
20668.17964739596
 21
15829.66109460106
 72
     1
 10
20668.17964739596
 20
15829.66109460106
 11
20675.25247400427
 21
15836.73040317898
 72
     1
 10
20675.25247400427
 20
15836.73040317898
 11
20658.28613341726
 21
15853.70518703872
 72
     1
 10
20658.28613341726
 20
15853.70518703872
 11
20600.99623789067
 21
15796.44378755748
 72
     1
 10
20600.99623789067
 20
15796.44378755745
 11
20674.51704710104
 21
15722.88639083199
 72
     1
 10
20674.51704710104
 20
15722.88639083199
 11
20731.80694262764
 21
15780.14779031323
 72
     1
 10
20731.80694262764
 20
15780.14779031323
 11
20714.84060204063
 21
15797.12257417297
 72
     1
 10
20714.84060204063
 20
15797.12257417297
 11
20707.76777543254
 21
15790.05326559505
 72
     1
 10
20707.76777543254
 20
15790.05326559505
 11
20717.66480744151
 21
15780.15130834351
 72
     1
 10
20717.66480744151
 20
15780.15130834351
 11
20674.52056513132
 21
15737.02852601811
 72
     1
 10
20674.52056513132
 20
15737.02852601811
 11
20615.13837307679
 21
15796.44026952717
 72
     1
 10
20615.13837307679
 20
15796.44026952717
 11
20658.28261538675
 21
15839.56305185257
 72
     1
 10
21579.39338239805
 20
14917.94584618564
 11
21513.86230023844
 21
15183.90217880055
 72
     1
 10
21582.30626196355
 20
14918.66357359698
 11
21516.77517980394
 21
15184.61990621183
 97
       38
330
1085E
330
1085D
330
1085C
330
1085B
330
1085A
330
10859
330
10858
330
10857
330
10856
330
10855
330
10854
330
10853
330
1085E
330
1085D
330
1085C
330
1085B
330
1085A
330
10859
330
10858
330
10857
330
10856
330
10855
330
10854
330
10853
330
1085E
330
1085D
330
1085C
330
1085B
330
1085A
330
10859
330
10858
330
10857
330
10856
330
10855
330
10854
330
10853
330
108B4
330
1085F
 75
     1
 76
     1
 52
0.0
 41
1.0
 77
     0
 78
     2
 53
0.0
 43
0.0
 44
0.0
 45
0.0
 46
6.985
 79
     2
 49
5.08
 49
-1.905
 53
90.0
 43
0.0
 44
0.0
 45
-6.985
 46
0.0000000000000004
 79
     2
 49
5.08
 49
-1.905
 98
        1
 10
0.0
 20
0.0
1001
GradientColor1ACI
1070
     5
1001
GradientColor2ACI
1070
     2
1001
ACAD
1010
0.0
1020
0.0
1030
0.0
```

### Sample 3: `A-WALL 1 HATCH`

- Parsed paths: `[{'flags': 1, 'labels': ['external'], 'polyline': False, 'edge_types': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 'vertices': 0, 'edges': 12}]`

```dxf
  0
HATCH
  5
20885
330
70
100
AcDbEntity
  8
A-WALL 1 HATCH
100
AcDbHatch
 10
0.0
 20
0.0
 30
0.0
210
0.0
220
0.0
230
1.0
  2
ANGLE
 70
     0
 71
     1
 91
        1
 92
        1
 93
       12
 72
     1
 10
20658.28261538675
 20
15839.56305185257
 11
20668.17964739596
 21
15829.66109460106
 72
     1
 10
20668.17964739596
 20
15829.66109460106
 11
20675.25247400427
 21
15836.73040317898
 72
     1
 10
20675.25247400427
 20
15836.73040317898
 11
20658.28613341726
 21
15853.70518703872
 72
     1
 10
20658.28613341726
 20
15853.70518703872
 11
20600.99623789067
 21
15796.44378755748
 72
     1
 10
20600.99623789067
 20
15796.44378755745
 11
20674.51704710104
 21
15722.88639083199
 72
     1
 10
20674.51704710104
 20
15722.88639083199
 11
20731.80694262764
 21
15780.14779031323
 72
     1
 10
20731.80694262764
 20
15780.14779031323
 11
20714.84060204063
 21
15797.12257417297
 72
     1
 10
20714.84060204063
 20
15797.12257417297
 11
20707.76777543254
 21
15790.05326559505
 72
     1
 10
20707.76777543254
 20
15790.05326559505
 11
20717.66480744151
 21
15780.15130834351
 72
     1
 10
20717.66480744151
 20
15780.15130834351
 11
20674.52056513132
 21
15737.02852601811
 72
     1
 10
20674.52056513132
 20
15737.02852601811
 11
20615.13837307679
 21
15796.44026952717
 72
     1
 10
20615.13837307679
 20
15796.44026952717
 11
20658.28261538675
 21
15839.56305185257
 97
       12
330
1085E
330
1085D
330
1085C
330
1085B
330
1085A
330
10859
330
10858
330
10857
330
10856
330
10855
330
10854
330
10853
 75
     1
 76
     1
 52
0.0
 41
1.0
 77
     0
 78
     2
 53
0.0
 43
0.0
 44
0.0
 45
0.0
 46
6.985
 79
     2
 49
5.08
 49
-1.905
 53
90.0
 43
0.0
 44
0.0
 45
-6.985
 46
0.0000000000000004
 79
     2
 49
5.08
 49
-1.905
 98
        1
 10
0.0
 20
0.0
1001
GradientColor1ACI
1070
     5
1001
GradientColor2ACI
1070
     2
1001
ACAD
1010
0.0
1020
0.0
1030
0.0
```
