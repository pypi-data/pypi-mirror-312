![tucan](https://images.unsplash.com/photo-1611788542170-38cf842212f4?q=80&w=2940&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D)

TUCAN (Tool to Unformat, Clean, and Analyze) is a code parser for scientific codebases. Its target languages are:

- Very old FORTRAN
- Recent FORTRAN
- Python (Under development)
- C/C++ (Early development)

## Installation

You can instal it from [PyPI](https://pypi.org/project/tucan/) with:

```bash
pip install tucan
```

You can also install from the sources from one of our [gitlab mirrors](https://codehub.hlrs.de/coes/excellerat-p2/uc-2/tucan).


## What is does?


### Remove coding archaisms

First it is a code cleaner. For example, this loop in `tranfit.f', a piece of [CHEMKIN](https://en.wikipedia.org/wiki/CHEMKIN) II package  in good'old FORTRAN77. (Do not worry, recent Chemkin is not written that way, probably)  :

```fortran
(547)      DO 2000 K = 1, KK-1
(548)         DO 2000 J = K+1, KK
(549)            DO 2000 N = 1, NO
(550)               COFD(N,J,K) = COFD(N,K,J)
(551) 2000 CONTINUE
```

Is translated  with the command `tucan clean tranfit.f` as : 
```fortran
(547-547)        do 2000 k  =  1,kk-1
(548-548)           do 2000 j  =  k+1,kk
(549-549)              do 2000 n  =  1,no
(550-550)                 cofd(n,j,k)  =  cofd(n,k,j)
(551-551)              end do ! 2000
(551-551)           end do ! 2000
(551-551)        end do ! 2000
```


The cleaned version is a simpler code for further analysis passes, like computing cyclomatic complexity, extracting structures, etc...


### Extracting code structure


Here we start from a file of [neko](https://github.com/ExtremeFLOW/neko/blob/develop/src/adt/htable.f90), an HPC code in recent Fortran, finalist for the Gordon Bell Prize in 2023.

`tucan struct htable.f90` provides a nested dictionary of the code structure. Here is a part of the output:

```yaml
(...)
type htable.h_tuple_t :
    At path ['htable', 'h_tuple_t'], name h_tuple_t, lines 47 -> 52
    Nb. Statements  6
    Nb. lines of code  6
    Ctls. Pts. (McCabe)    0          | 0          Int. avg.
    Halstead Difficulty    8.25       | 8.25       Int. avg.
    Maintainability Index  94.17      | 94.17      Int. avg.
    Average indents        2.2        | 2.2        Int. avg.
    Halstead time          48 sec     | 48 sec     Ext. avg.
    Structural complexity  6          | 6          Ext. avg.
    Nb. of Loops           0          | 0          Ext. avg.

procedure htable.htable_t.hash :
    At path ['htable', 'htable_t', 'hash'], name htable.htable_t.hash, lines 60 -> 60
    Nb. Statements  1
    Nb. lines of code  1
    Ctls. Pts. (McCabe)    0          | 0          Int. avg.
    Halstead Difficulty    0          | 0          Int. avg.
    Maintainability Index  378.29     | 378.29     Int. avg.
    Average indents        0          | 0          Int. avg.
    Halstead time          0 sec      | 0 sec      Ext. avg.
    Structural complexity  4          | 4          Ext. avg.
    Nb. of Loops           0          | 0          Ext. avg.
    Refers to 1 callables:
       - htable.hash

procedure htable.htable_t.htable_clear :
    At path ['htable', 'htable_t', 'htable_clear'], name htable.htable_t.htable_clear, lines 61 -> 61
    Nb. Statements  1
    Nb. lines of code  1
    Ctls. Pts. (McCabe)    0          | 0          Int. avg.
    Halstead Difficulty    0          | 0          Int. avg.
    Maintainability Index  378.29     | 378.29     Int. avg.
    Average indents        0          | 0          Int. avg.
    Halstead time          0 sec      | 0 sec      Ext. avg.
    Structural complexity  4          | 4          Ext. avg.
    Nb. of Loops           0          | 0          Ext. avg.
    Refers to 1 callables:
       - htable.htable_clear

procedure htable.htable_t.htable_free :
    At path ['htable', 'htable_t', 'htable_free'], name htable.htable_t.htable_free, lines 62 -> 62
    Nb. Statements  1
    Nb. lines of code  1
    Ctls. Pts. (McCabe)    0          | 0          Int. avg.
    Halstead Difficulty    0          | 0          Int. avg.
    Maintainability Index  378.29     | 378.29     Int. avg.
    Average indents        0          | 0          Int. avg.
    Halstead time          0 sec      | 0 sec      Ext. avg.
    Structural complexity  4          | 4          Ext. avg.
    Nb. of Loops           0          | 0          Ext. avg.
    Refers to 1 callables:
       - htable.htable_free
(...)
module htable :
    At path ['htable'], name htable, lines 36 -> 1482
    Nb. Statements  1079
    Nb. lines of code  1447
    Ctls. Pts. (McCabe)    0          | 3.01       Int. avg.
    Halstead Difficulty    4          | 15.25      Int. avg.
    Maintainability Index  -28.7      | 76.61      Int. avg.
    Average indents        1          | 2.36       Int. avg.
    Halstead time          28 sec     | 7.87 hrs   Ext. avg.
    Structural complexity  1          | 474        Ext. avg.
    Nb. of Loops           0          | 18         Ext. avg.
    Refers to 89 contains:
       - htable.h_tuple_t
       - htable.htable_t
       - htable.interface66
       - htable.htable_i4_t
       - htable.htable_i8_t
       - htable.htable_r8_t
(...)

```

*(This output will change as we update and improve tucan in the next versions!)*

This information allows the creation and manipulation of graphs to extract the structure of the code


### Interpreting Conditional Inclusions "IF DEFS". 

An other example of tucan is the analysis of [ifdefs](https://en.cppreference.com/w/c/preprocessor/conditional) in C or FORTRAN:

```
#ifdef FRONT
        WRITE(*,*) " FRONT is enabled " ! partial front subroutine
        SUBROUTINE dummy_front(a,b,c)
        WRITE(*,*) " FRONT 1"     ! partial front subroutine
#else                
        SUBROUTINE dummy_front(a,d,e)
        WRITE(*,*) " FRONT 2"       ! partial front subroutine
#endif
        END SUBROUTINE

        SUBROUTINE dummy_back(a,b,c)
#ifdef BACK
        WRITE(*,*) " FRONT is enabled " ! partial front subroutine
        WRITE(*,*) " BACK 1"    ! partial back subroutine
        END SUBROUTINE  
#else
        WRITE(*,*) " BACK 2"    ! partial back subroutine
        END SUBROUTINE  
#endif
```

Depending on the pre-definition of variables FRONT and BACK, this code snippet can be read in four ways possible.
Here are usages:

`tucan cpp-clean templates_ifdef.f` yields:

```fortran
        SUBROUTINE dummy_front(a,d,e)
        WRITE(*,*) " FRONT 2"       ! partial front subroutine
        END SUBROUTINE

        SUBROUTINE dummy_back(a,b,c)


        WRITE(*,*) " BACK 2"    ! partial back subroutine
        END SUBROUTINE
```


`tucan cpp-clean templates_ifdef.f -v FRONT` yields:

```fortran
        WRITE(*,*) " FRONT is enabled " ! partial front subroutine
        SUBROUTINE dummy_front(a,b,c)
        WRITE(*,*) " FRONT 1"     ! partial front subroutine


        END SUBROUTINE

        SUBROUTINE dummy_back(a,b,c)


        WRITE(*,*) " BACK 2"    ! partial back subroutine
        END SUBROUTINE
```

`tucan cpp-clean templates_ifdef.f -v FRONT,BACK` yields:

```fortran
         WRITE(*,*) " FRONT is enabled " ! partial front subroutine
        SUBROUTINE dummy_front(a,b,c)
        WRITE(*,*) " FRONT 1"     ! partial front subroutine


        END SUBROUTINE

        SUBROUTINE dummy_back(a,b,c)
        WRITE(*,*) " BACK is enabled " ! partial front subroutine
        WRITE(*,*) " BACK 1"    ! partial back subroutine
        END SUBROUTINE
```

#### scanning ifdef variables

A simpler usage of tucan : scan the current ifdefs variables. Still on [neko](https://github.com/ExtremeFLOW/neko) in the `/src` folder (an old version though) : 

```bash
/neko/src >tucan cpp-scan-pkge .
 - Recursive path gathering ...
 - Cleaning the paths ...
 - Analysis completed.
 - Global ifdef variables : HAVE_PARMETIS, __APPLE__
 - Local to device/opencl/check.c : CL_ERR_STR(err)
 - Local to math/bcknd/device/opencl/opr_opgrad.c : CASE(LX), STR(X)
 - Local to math/bcknd/device/opencl/opr_dudxyz.c : CASE(LX), STR(X)
 - Local to common/sighdl.c : SIGHDL_ALRM, SIGHDL_USR1, SIGHDL_USR2, SIGHDL_XCPU
 - Local to math/bcknd/device/opencl/opr_conv1.c : CASE(LX), STR(X)
 - Local to math/bcknd/device/opencl/opr_cfl.c : CASE(LX), STR(X)
 - Local to krylov/bcknd/device/opencl/pc_jacobi.c : CASE(LX), STR(X)
 - Local to math/bcknd/device/opencl/ax_helm.c : CASE(LX), STR(X)
 - Local to bc/bcknd/device/opencl/symmetry.c : MAX(a,
 - Local to gs/bcknd/device/opencl/gs.c : GS_OP_ADD, GS_OP_MAX, GS_OP_MIN, GS_OP_MUL
 - Local to sem/bcknd/device/opencl/coef.c : DXYZDRST_CASE(LX), GEO_CASE(LX), STR(X)
 - Local to math/bcknd/device/opencl/opr_cdtp.c : CASE(LX), STR(X)
```
This feature is useful to see all potential variables that surcharge your codebase via conditional inclusions.

## More about tucan

`Tucan` is used by  `anubis`, our open-source  tool to explore the git repository of a code, and `marauder's map`  our open-source tool to show codes structures by in-depth vizualisation of callgraphs and code circular-packing .

