# 3Blue1Brown Video Projects - Code Groupings

This document catalogs the natural groupings of code in the 3Blue1Brown videos repository, organized by mathematical concepts and video series. Each entry includes the folder structure, files, scene classes, and dependencies.

---

## Foundational Classics (2015-2017)

### Moser's Circle Problem
- **Folder**: `_2015/`
- **Files**: `moser_main.py`, `moser_intro.py`
- **Main Scenes**: 
  - `CircleScene` (base class)
  - `CircleScene`, `CountSections`, `MoserPattern`
  - `CountLines`, `CountIntersectionPoints`, `NonGeneralPosition`
  - `GeneralPositionRule`, `LineCorrespondsWithPair`, `IllustrateNChooseK`
  - `IntersectionPointCorrespondances`, `LinesIntersectOutside`
  - `ApplyEulerToMoser`, `ShowMoserGraphLines`
  - `PascalsTriangleScene`, `DrawPascalsTriangle`, `PascalRuleExample`
  - `FormulaRelatesToPowersOfTwo`, `MoserSolutionInPascal`
- **Dependencies**: Graph theory utilities, Euler's formula visualization
- **Description**: Explores Moser's circle problem - counting regions formed by chords in a circle and connecting to Pascal's triangle through Euler's formula and combinatorics.
- **Estimated Scenes**: 50+

### Pythagorean Theorem Proof
- **Folder**: `_2015/`
- **Files**: `pythagorean_proof.py`
- **Main Scenes**:
  - `Triangle` (custom Polygon)
  - `DrawPointsReference`, `DrawTriangle`, `DrawAllThreeSquares`
  - `AddParallelLines`, `HighlightEmergentTriangles`
  - `DrawAllThreeSquaresWithMoreTriangles`
  - `ZoomInOnTroublePoint`, `DrawTriangleWithAngles`
  - `CompletelyFillLargeSquare`, `FillComponentsOfLargeSquare`
  - `ShowRearrangementInBigSquare`
- **Dependencies**: Polygon geometry, region coloring, visual proof construction
- **Description**: Visual proof of the Pythagorean theorem using rearrangement and area calculations with interactive geometry demonstrations.
- **Estimated Scenes**: 25+

### Essence of Linear Algebra (Complete Series)
- **Folder**: `_2016/eola/`
- **Files**: 
  - 16 files: `chapter0.py` through `chapter11.py` (plus `chapter8p2.py`)
  - Support files: `footnote.py`, `footnote2.py`, `thumbnails.py`
- **Main Scenes**:
  - Chapter 0: `OpeningQuote`, `UpcomingSeriesOfVidoes`, `AboutLinearAlgebra`
  - Chapters 1-11: Linear transformations, vectors, matrices, determinants, eigenvalues
  - Key scene bases: `LinearTransformationScene`, `GraphScene`, `PiCreatureScene`
- **Dependencies**: 
  - Custom `LinearTransformationScene` class
  - Matrix animation utilities
  - Vector visualization helpers
- **Description**: Comprehensive visual exploration of linear algebra concepts from vectors and matrices to determinants, eigenvalues, and transformations. Each chapter builds understanding of core LA principles.
- **Estimated Scenes**: 200+

### Essence of Calculus (Complete Series)
- **Folder**: `_2017/eoc/`
- **Files**: 
  - 11 files: `chapter1.py` through `chapter10.py`
  - Support files: `footnote.py`, `old_chapter1.py`
- **Main Scenes**:
  - Chapter 1: Derivatives - `IntroduceCircle`, `ApproximateOneRing`, `GraphRectangles`
  - Chapters 2-10: Integration, chain rule, implicit differentiation, limits
  - Key scene bases: `TeacherStudentsScene`, `PiCreatureScene`, `GraphScene`
- **Dependencies**: 
  - `TeacherStudentsScene` for narrative dialogue
  - Graph animation utilities
  - Calculus-specific visualizations
- **Description**: Visual calculus series explaining derivatives, integrals, and calculus fundamentals through animation and geometric intuition. Features Pi creature as instructor.
- **Estimated Scenes**: 180+

### Neural Networks (Deep Learning Introduction)
- **Folder**: `_2017/nn/`
- **Files**: `part1.py`, `part2.py`, `part3.py`, `network.py`, `mnist_loader.py`, `playground.py`
- **Main Scenes**:
  - Neural network visualization scenes
  - Activation function animations
  - Backpropagation explanations
  - Training process visualizations
- **Dependencies**: 
  - Custom `Network` class for NN simulation
  - MNIST dataset loader
  - Graph and node visualization utilities
- **Description**: Introduction to neural networks and deep learning concepts, including network architecture visualization, forward propagation, backpropagation, and gradient descent.
- **Estimated Scenes**: 40+

---

## Intermediate Projects (2018-2020)

### Basel Problem / Infinite Series
- **Folder**: `_2018/basel/`
- **Files**: Various scene files for Basel problem exploration
- **Main Scenes**:
  - Series convergence visualizations
  - Basel problem (π²/6 derivation)
  - Zeta function animations
- **Dependencies**: Complex number utilities, series analysis tools
- **Description**: Explores the Basel problem and infinite series convergence, demonstrating why 1 + 1/4 + 1/9 + ... = π²/6.
- **Estimated Scenes**: 30+

### Essence of Probability (EOP Series)
- **Folder**: `_2018/eop/`
- **Files**: 
  - Multiple chapters in `chapter0/`, `chapter1/`, `chapter2/`
  - Reusable components in `reusables/`
- **Main Scenes**:
  - Probability distribution animations
  - Bayes' theorem visualizations
  - Conditional probability scenarios
- **Dependencies**: Probability-specific visualization utilities, reusable scene components
- **Description**: Visual exploration of probability theory including distributions, Bayes' theorem, and fundamental probability concepts.
- **Estimated Scenes**: 120+

### Bayes Theorem
- **Folder**: `_2019/bayes/`
- **Files**: `part1.py`, `footnote.py`
- **Main Scenes**:
  - Custom mobjects: `BayesDiagram`, `ProbabilityBar`, character classes (`Steve`, `Linda`, `Librarian`, `Farmer`, etc.)
  - Scene classes showing Bayes' theorem derivation and applications
- **Dependencies**: 
  - SVG-based character and icon mobjects
  - Probability visualization utilities
  - Diagram and layout helpers
- **Description**: Focused explanation of Bayes' theorem with concrete examples (e.g., librarian/farmer problem) and visual probability demonstrations.
- **Estimated Scenes**: 15+

### Differential Equations Series (Complete)
- **Folder**: `_2019/diffyq/`
- **Files**: 
  - 5 parts: `part1/` through `part5/`
  - Each part contains: main scenes, Pi creature scenes, wordy scenes, shared constructs
  - Integration files: `all_part1_scenes.py` through `all_part5_scenes.py`
  - Special: `fourier_montage_scenes.py`
- **Main Scenes**:
  - Pendulum animations and analysis
  - Phase space visualizations
  - Fourier series and transforms
  - Heat equation demonstrations
  - Complex function plotting
  - Phase portraits and stability analysis
- **Dependencies**: 
  - Custom `Pendulum` class
  - `TeacherStudentsScene` for dialogue
  - Physics simulation utilities (gravity, forces)
  - Fourier analysis tools
  - 3D graph plotting utilities
- **Description**: Comprehensive differential equations series from modeling with ODEs (pendulum, population dynamics) to PDEs (heat equation) to Fourier analysis. Includes physics applications and mathematical theory.
- **Estimated Scenes**: 250+

### Colliding Blocks (Billiard Ball Problem)
- **Folder**: `_2019/clacks/`
- **Files**: 
  - Main problems: `question.py`, `solution1.py`, `name_bump.py`
  - Advanced solution: `solution2/` (6 files)
  - Each solution variant: block collisions, mirror visualization, physics scenes, phase space
- **Main Scenes**:
  - `Block` and collision mechanics
  - Phase space diagrams
  - Mirror/reflection geometry
  - Pi creature problem explanation
  - Billiard ball physics animations
- **Dependencies**: 
  - Physics collision simulation
  - Phase space visualization
  - Geometry and reflection utilities
  - Custom block and collision mobjects
- **Description**: Explores the surprising result that colliding blocks can reveal digits of π. Solutions include direct collision counting, mirror geometry approach, and phase space analysis.
- **Estimated Scenes**: 60+

---

## Recent Projects (2022-2025)

### Borwein Integrals
- **Folder**: `_2022/borwein/`
- **Files**: `main.py`, `supplements.py`
- **Main Scenes**:
  - `ShowIntegrals`, `SineLimit`, `WriteFullIntegrals`
  - `WriteTwoCosPattern`, `MovingAverages`
  - Pattern recognition and convergence visualizations
- **Dependencies**: 
  - Integration visualization tools
  - Function plotting utilities
  - `InteractiveScene` for exploration
- **Description**: Explores surprising Borwein integrals that appear to converge to π but eventually diverge, demonstrating the importance of rigorous proof in mathematics.
- **Estimated Scenes**: 25+

### Central Limit Theorem (CLT)
- **Folder**: `_2023/clt/`
- **Files**: `main.py`, `wordy_scenes.py`, `galton_board.py`, `dice_sims.py`
- **Main Scenes**:
  - Dice simulation and histogram animations
  - Galton board visual demonstrations
  - Gaussian curve emergence
  - Statistical distribution animations
- **Dependencies**: 
  - Simulation and randomization utilities
  - Histogram and chart plotting
  - Galton board physics/animation
- **Description**: Visual demonstration of the Central Limit Theorem showing how various distributions converge to normal distribution. Includes dice simulations and Galton board animations.
- **Estimated Scenes**: 30+

### Transformers and Attention Mechanisms
- **Folder**: `_2024/transformers/`
- **Files**: 
  - Core files: `attention.py`, `embedding.py`, `ml_basics.py`, `mlp.py`
  - Advanced topics: `auto_regression.py`, `generation.py`, `network_flow.py`
  - Supporting: `helpers.py`, `chm.py`, `almost_orthogonal.py`
  - Supplements and legacy: `supplements.py`, `old_auto_regression.py`
- **Main Scenes**:
  - Attention: `AttentionPatterns`, `QueryMap`, `KeyMap`, `DescribeAttentionEquation`
  - Embeddings: Word and token embedding visualizations
  - Networks: `MLPExplanations`, `TransformerArchitecture`
  - Machine Learning: Loss functions, gradient descent, optimization
  - Network flow and information propagation
- **Dependencies**: 
  - `InteractiveScene` for interactive exploration
  - Matrix and tensor visualization
  - Text processing and tokenization
  - Neural network architecture diagrams
  - Custom helpers for transformers-specific visualizations
- **Description**: Deep dive into transformer architecture and attention mechanisms that power modern LLMs. Covers embeddings, attention heads, multi-head attention, positional encoding, and the complete transformer pipeline.
- **Estimated Scenes**: 150+

### Laplace Transforms
- **Folder**: `_2025/laplace/`
- **Files**: 
  - Core: `main_equations.py`, `main_supplements.py`
  - Foundations: `prequel_equations.py`, `exponentials.py`
  - Applications: `shm.py` (simple harmonic motion), `integration.py`
  - Supplementary: `supplements.py`
- **Main Scenes**:
  - Exponential function animations
  - Laplace transform derivation
  - Solving differential equations using Laplace transforms
  - Simple harmonic motion analysis
  - Inverse Laplace transforms and convolution
- **Dependencies**: 
  - Complex plane visualization
  - Integral visualization
  - Differential equation solvers
  - Custom integration utilities
- **Description**: Introduction to Laplace transforms from exponential functions through solving differential equations. Shows how Laplace transforms convert ODEs to algebraic equations, with applications to SHM and electrical engineering.
- **Estimated Scenes**: 60+

---

## Other Notable Projects

### Convolutions & Signal Processing
- **Folder**: `_2022/convolutions/`, `_2023/convolutions2/`
- **Description**: Visual exploration of convolution operations used in signal processing and deep learning.

### Galois Theory
- **Folder**: `_2022/galois/`
- **Description**: Group theory and field extensions in abstract algebra.

### Zeta Function / Riemann Hypothesis
- **Folder**: `_2022/zeta/`, `_2025/zeta/`
- **Description**: Complex analysis and the Riemann zeta function, building toward the Riemann hypothesis.

### Infinity / Limits
- **Folder**: `_2022/infinity/`
- **Description**: Exploring concepts of infinity, limits, and cardinality.

### Colluding Blocks Reboot
- **Folder**: `_2025/colliding_blocks_v2/`
- **Description**: Updated version of the billiard ball/block collision problem with modern rendering.

### Quantum Computing (Grover's Algorithm)
- **Folder**: `_2025/grover/`
- **Description**: Introduction to quantum algorithms, specifically Grover's search algorithm.

### Guest Videos & Collaborations
- **Folder**: `_2025/guest_videos/`
- **Description**: Animations for collaborative content and guest appearances.

### Cosmic Distance Ladder
- **Folder**: `_2025/cosmic_distance/`
- **Description**: Methods for measuring distances to astronomical objects.

### Other 2024-2025 Projects
- **Folder**: `_2024/antp/`, `_2024/holograms/`, `_2024/inscribed_rect/`, `_2024/linalg/`, `_2024/manim_demo/`, `_2024/puzzles/`
- **Description**: Various mathematical topics including holography, linear algebra review, inscribed rectangles, and puzzle solutions.

---

## Custom Utilities & Dependencies

### Core Imports
All projects import from `manim_imports_ext.py` which provides:
- Manim animation framework (3b1b fork)
- Core scene classes: `Scene`, `InteractiveScene`, `MovingCameraScene`
- Special scene types: `PiCreatureScene`, `TeacherStudentsScene`, `GraphScene`, `LinearTransformationScene`
- Mobject bases: `VMobject`, `VGroup`, `SVGMobject`, `TextMobject`, `Tex`
- Utility functions: color constants, geometric helpers, animation utilities

### Project-Specific Custom Classes
- **Characters**: Pi creature (π), teachers, students in `custom/characters/`
- **Backgrounds**: Scene backdrops in `custom/backdrops.py`
- **Drawing utilities**: Custom shapes and visualizations in `custom/drawings.py`
- **End screens**: Standard video credits and end screens in `custom/end_screen.py`
- **Legacy utilities**: Older reusable code in `once_useful_constructs/`

### Configuration
- `custom_config.yml`: Manim rendering settings (4K resolution, 30fps, custom fonts)
- `stage_scenes.py`: Utility for staging and ordering rendered scenes for videos

---

## Project Statistics Summary

| Category | Count |
|----------|-------|
| Total Year Directories | 11 (_2015 through _2025) |
| Major Video Series | 15+ |
| Total Python Files | 300+ |
| Total Scene Classes | 1000+ |
| Largest Project | Differential Equations Series (~250 scenes) |
| Second Largest | Transformers Series (~150 scenes) |
| Most Foundational | Essence of Linear Algebra (16 chapters) |

---

## Code Organization Patterns

### Scene Hierarchy
Most projects follow a consistent inheritance pattern:
```
Scene (base)
├── GraphScene (for mathematical plots)
├── PiCreatureScene (with Pi character)
│   └── TeacherStudentsScene (dialogue-based)
├── LinearTransformationScene (linear algebra)
├── MovingCameraScene (3D and dynamic views)
└── InteractiveScene (for modern interactive development)
```

### File Organization
- **Monolithic**: Older projects (moser_main.py) have many scenes in one file
- **Modular**: Newer projects split scenes by topic/chapter:
  - `main.py` - Primary content scenes
  - `supplements.py` - Additional/bonus scenes
  - `part1/`, `part2/` - Chapter-based divisions
  - `wordy_scenes.py` - Dialogue and explanatory scenes
  - `shared_constructs.py` - Reusable components

### Development Philosophy
- Interactive development with `manimgl -se` (stepping through code)
- Checkpoint system for rapid iteration (`checkpoint_paste()`)
- Visual preview before rendering (`-p` flag)
- Group-based animations with `lag_ratio` for staggered effects
- Extensive use of `add_updater()` for dynamic positioning

---

## Glossary

- **Scene**: A complete animated sequence that renders to video
- **Mobject**: Manim "mathematical object" - any visual element
- **VGroup**: Vector group, container for related mobjects
- **InteractiveScene**: Modern Manim scene class supporting interactive development
- **LaTeX/Tex**: Mathematical typesetting in animations (using `Tex()` not `MathTex()`)
- **Updater**: Function that dynamically updates mobject properties frame-by-frame
- **Lag Ratio**: Parameter for staggering animations across multiple objects

---

## Dataset Folder: Standalone Scripts

The `dataset/` folder contains self-contained, educational Manim scripts extracted from the video projects. Each script:

- **Completely standalone**: Only imports from `manimlib` and `numpy` (plus standard library)
- **Self-documented**: Includes detailed docstrings explaining educational objectives, story arc, and implementation
- **Production-ready**: Follows a consistent structure with clear sections for imports, configuration, utilities, and scenes
- **Dependency-free**: All necessary utility code is inlined within the script

### Dataset Structure

Each standalone script includes:
1. **Header Documentation**: Educational objectives, story arc, narrative flow, technical notes
2. **Imports Section**: Only manimlib and numpy
3. **Configuration Constants**: Colors, sizes, and visual parameters
4. **Utility Functions**: Helper functions specific to the concept
5. **Scene Implementations**: Complete scene classes with detailed comments
6. **Scene Order**: Documented sequence explaining the narrative progression

### Current Dataset Scripts

**Set Theory & Logic:**

1. **circle_intersection_geometry.py** - Set theory through circle intersections
   - Demonstrates intersection, union, and difference operations visually
   - 4 scenes: CircleIntersection, CircleUnion, CompareIntersectionAndUnion, DynamicCircleOverlap
   - Educational focus: Set theory, boolean operations, geometric visualization

**Analysis & Calculus:**

2. **geometric_series_visual.py** - Visual proof of geometric series convergence
   - Shows why 1/2 + 1/4 + 1/8 + ... = 1 through square subdivision
   - 3 scenes: GeometricSeriesSquare, AlgebraicFormula, GeneralGeometricSeries
   - Educational focus: Infinite series, limits, visual proofs, algebraic derivation

3. **basel_problem.py** - Basel problem: sum of 1/n² = π²/6
   - Shows convergence to π²/6 and Euler's proof via sin(x)/x
   - 4 scenes: IntroduceSeries, PartialSums, SurprisingResult, VisualIntuition
   - Educational focus: Infinite series, convergence, π appearance in unexpected places

4. **limits_epsilon_delta.py** - Formal epsilon-delta limit definition
   - Challenge-response game interpretation with complete proof
   - 4 scenes: InformalLimit, EpsilonDelta, VisualProof, WorkingExample
   - Educational focus: Formal limits, epsilon-delta proofs, mathematical rigor

5. **derivative_introduction.py** - Derivative as slope of tangent line
   - Shows secant lines approaching tangent as limit
   - 4 scenes: IntroduceFunction, SecantLines, LimitToTangent, DerivativeDefinition
   - Educational focus: Derivatives, limits, rate of change, tangent lines

6. **chain_rule.py** - Chain rule for composite functions
   - Visual proof of why rates multiply in composition
   - 4 scenes: CompositionIntro, RateOfChange, ChainRuleFormula, Examples
   - Educational focus: Chain rule, composition, rate multiplication, derivative rules

7. **product_rule.py** - Product rule for derivatives
   - Visual proof using area of expanding rectangle
   - 4 scenes: IntroduceProduct, AreaRectangle, ProductRuleFormula, Examples
   - Educational focus: Product rule, d/dx[fg] = f'g + fg', derivative rules

8. **taylor_series.py** - Taylor series polynomial approximation
   - Shows how polynomials approximate sin(x), e^x through derivatives
   - 4 scenes: IntroduceFunction, LinearApproximation, HigherOrderTerms, ConvergenceRadius
   - Educational focus: Taylor series, polynomial approximation, convergence

9. **exponential_growth.py** - e and exponential functions
   - Shows e as limit (1+1/n)^n and unique derivative property
   - 4 scenes: DefineExponential, NumberE, CompoundInterest, DerivativeProperty
   - Educational focus: Natural exponential, e, compound interest, d/dx[e^x] = e^x

10. **implicit_differentiation.py** - Implicit differentiation
    - Finding dy/dx when y is not isolated (e.g., x² + y² = r²)
    - 4 scenes: IntroduceImplicitCurve, ExplicitVsImplicit, DerivativeFormula, CircleExample
    - Educational focus: Implicit differentiation, related rates, non-function curves

11. **integration_as_area.py** - Integration as area under curve
    - Visualizes Riemann sums converging to definite integral
    - 4 scenes: AreaProblem, RiemannSums, IncreasingRectangles, FundamentalTheorem
    - Educational focus: Integration, Riemann sums, area under curves, limits

**Linear Algebra:**

12. **vector_addition.py** - Vector addition and parallelogram law
    - Demonstrates tip-to-tail method and parallelogram construction
    - 4 scenes: IntroduceVectors, VectorAddition, ParallelogramLaw, VectorSubtraction
    - Educational focus: Vectors, addition, geometric interpretation, parallelogram law

13. **dot_product.py** - Dot product as projection
    - Shows a·b = |a||b|cos(θ) with geometric interpretation
    - 4 scenes: IntroduceVectors, GeometricInterpretation, ProjectionFormula, Applications
    - Educational focus: Dot product, projection, orthogonality, work component

14. **cross_product.py** - Cross product in 3D geometry
    - 3D visualization of perpendicular vector and right-hand rule
    - 4 scenes: IntroduceVectors, RightHandRule, AreaParallelogram, Properties
    - Educational focus: Cross product, 3D vectors, right-hand rule, parallelogram area

15. **matrix_transformations.py** - 2D linear transformations
    - Shows how matrices transform the plane with grid visualization
    - 4 scenes: IntroduceGrid, ShearTransform, RotationTransform, ComposedTransforms
    - Educational focus: Linear transformations, matrices, geometric interpretation

16. **determinants_area.py** - Determinants as area scaling factor
    - Shows det(M) = area scaling factor visually
    - 4 scenes: UnitSquare, LinearTransform, MeasureArea, GeneralPrinciple
    - Educational focus: Determinants, area scaling, linear transformations, geometric meaning

17. **eigenvalues_eigenvectors.py** - Eigenvectors as special transformation directions
    - Visualizes vectors that only get scaled, not rotated (Av = λv)
    - 4 scenes: IntroduceTransform, FindSpecialVectors, EigenvalueScaling, Applications
    - Educational focus: Eigenvalues, eigenvectors, eigenspaces, linear transformations

18. **inverse_matrices.py** - Matrix inverse and solving systems
    - Shows AA^(-1) = I geometrically and solving Ax = b
    - 4 scenes: IntroduceSystem, InverseTransform, SolvingEquations, NonInvertible
    - Educational focus: Matrix inverse, solving linear systems, singularity

19. **null_space.py** - Null space and kernel of transformation
    - Shows vectors that map to zero under transformation
    - 4 scenes: IntroduceTransformation, VectorsToZero, GeometricMeaning, RankNullity
    - Educational focus: Null space, kernel, rank-nullity theorem, linear dependencies

20. **change_of_basis.py** - Change of basis transformations
    - Shows same vector in different coordinate systems
    - 4 scenes: DifferentBases, TransformationMatrix, SameVectorDifferentCoords, Applications
    - Educational focus: Change of basis, coordinate systems, basis transformations

21. **least_squares.py** - Least squares linear regression
    - Fitting line to data by minimizing squared errors
    - 4 scenes: IntroduceProblem, ErrorMinimization, NormalEquation, BestFitLine
    - Educational focus: Least squares, regression, overdetermined systems, projections

22. **quaternions.py** - Quaternions for 3D rotations
    - 4D number system i²=j²=k²=ijk=-1, uses ThreeDScene
    - 4 scenes: IntroduceQuaternions, MultiplicationRule, ThreeDRotations, AvoidGimbalLock
    - Educational focus: Quaternions, 3D rotations, gimbal lock, 4D numbers

**Complex Analysis & Number Theory:**

23. **complex_multiplication.py** - Complex number multiplication as rotation and scaling
    - Demonstrates geometric interpretation of complex multiplication
    - 4 scenes: IntroduceComplexPlane, MultiplyByI, GeneralMultiplication, PolarForm
    - Educational focus: Complex numbers, polar form, Euler's formula, geometric transformations

24. **prime_spirals.py** - Ulam spiral and prime number patterns
    - Reveals diagonal patterns in the Ulam prime spiral
    - 4 scenes: SpiralConstruction, HighlightPrimes, DiagonalPatterns, PrimeDistribution
    - Educational focus: Prime numbers, number theory, visual patterns, Ulam spiral

25. **golden_ratio.py** - Golden ratio and Fibonacci sequence
    - Shows φ = (1+√5)/2 and Fibonacci ratio convergence
    - 4 scenes: FibonacciSequence, GoldenRatio, GoldenRectangle, NatureSpirals
    - Educational focus: Golden ratio, Fibonacci, phi, golden rectangle, spirals in nature

**Geometry & Topology:**

26. **pythagorean_visual_proof.py** - Visual proof of Pythagorean theorem
    - Proves a² + b² = c² through area rearrangement
    - 4 scenes: IntroduceTheorem, ShowSquares, VisualProofByRearrangement, AlternativeProof
    - Educational focus: Pythagorean theorem, visual proofs, geometric reasoning

27. **euler_polyhedra_formula.py** - Euler's polyhedra formula V - E + F = 2
    - Verifies formula for Platonic solids with 3D visualization
    - 4 scenes: IntroducePolyhedra, CountComponents, VerifyFormula, ProofSketch
    - Educational focus: Euler's formula, polyhedra, topology, graph theory

28. **mobius_strip.py** - Möbius strip non-orientable surface
    - 3D construction showing one edge and one surface (uses ThreeDScene)
    - 4 scenes: ConstructStrip, OneEdgeSurface, AntWalking, NonOrientable
    - Educational focus: Non-orientable surfaces, topology, Möbius strip, one-sided surfaces

29. **brachistochrone.py** - Brachistochrone curve (fastest descent)
    - Ball rolling down curves, cycloid is fastest
    - 4 scenes: IntroduceProblem, CompareRamps, CycloidSolution, PhysicsExplanation
    - Educational focus: Calculus of variations, cycloid, optimization, physics

**Combinatorics & Discrete Math:**

30. **moser_circle_problem.py** - Moser's circle problem (surprising pattern break)
    - Shows why 1,2,4,8,16,31... breaks the power-of-2 pattern
    - 4 scenes: IntroduceCircle, DrawChords, CountRegions, SurprisingPattern
    - Educational focus: Combinatorics, induction fallacy, binomial coefficients

31. **graph_coloring.py** - Graph coloring problem
    - Map coloring, Four Color Theorem, chromatic number
    - 4 scenes: IntroduceColoringProblem, FourColorTheorem, ChromaticNumber, GreedyAlgorithm
    - Educational focus: Graph theory, coloring, algorithms, Four Color Theorem

**Physics & Differential Equations:**

32. **simple_harmonic_motion.py** - Pendulum and circular motion projection
    - Shows SHM as projection of uniform circular motion
    - 4 scenes: IntroducePendulum, CircularMotion, ProjectionToSHM, Equation
    - Educational focus: Simple harmonic motion, differential equations, circular motion

33. **colliding_blocks_pi.py** - Computing π from elastic collisions
    - Famous problem: blocks compute digits of π (314 collisions for mass ratio 100²)
    - 4 scenes: SetupBlocks, CountCollisions, SurprisingPattern, PhaseSpace
    - Educational focus: Elastic collisions, conservation laws, π from physics, phase space

**Signal Processing & Fourier Analysis:**

34. **fourier_series_intro.py** - Fourier series building square wave
    - Builds square wave from sine wave harmonics
    - 4 scenes: TargetWave, AddSineWaves, ConvergenceToSquare, GeneralPrinciple
    - Educational focus: Fourier series, harmonics, signal decomposition

35. **fourier_transform.py** - Continuous Fourier Transform
    - Transition from discrete series to continuous transform
    - 4 scenes: FromSeriesToTransform, FrequencyDomain, WavePackets, Applications
    - Educational focus: Fourier transform, frequency analysis, uncertainty principle

36. **convolution_intro.py** - Convolution as sliding overlap integral
    - Flip-and-slide visualization of f*g convolution
    - 4 scenes: IntroduceFunctions, SlidingProduct, ConvolutionGraph, Applications
    - Educational focus: Convolution, signal processing, integral transforms, smoothing

**Probability & Statistics:**

37. **probability_dice.py** - Probability distributions with dice
    - Demonstrates probability distributions and sum of dice
    - 4 scenes: SingleDie, TwoDiceSum, DistributionShape, CentralLimitHint
    - Educational focus: Probability, distributions, law of large numbers, CLT preview

38. **binomial_distribution.py** - Binomial distribution
    - n trials with probability p, coin flips
    - 4 scenes: CoinFlips, BinomialFormula, DistributionShape, NormalApproximation
    - Educational focus: Binomial distribution, Pascal's triangle, normal approximation

39. **bayes_theorem.py** - Bayes' theorem with visual examples
    - Medical test example with tree diagrams and area representations
    - 4 scenes: ProbabilityIntro, ConditionalProbability, BayesFormula, MedicalTest
    - Educational focus: Bayes' theorem, conditional probability, false positives, medical testing

40. **central_limit_theorem.py** - Central Limit Theorem demonstration
    - Shows sum of any distribution converging to normal
    - 4 scenes: MultipleSamples, SumDistribution, EmergentNormal, UniversalPhenomenon
    - Educational focus: CLT, normal distribution emergence, sampling, universality

41. **markov_chains.py** - Markov chains and random walks
    - State transitions, transition matrices, steady-state distributions
    - 4 scenes: IntroduceRandomWalk, TransitionMatrix, SteadyState, PageRankExample
    - Educational focus: Markov chains, random walks, steady state, PageRank

**Machine Learning & Optimization:**

42. **gradient_descent.py** - Gradient descent optimization
    - Ball rolling down surface with learning rate effects
    - 4 scenes: IntroduceLoss, GradientDirection, IterativeSteps, LocalMinima
    - Educational focus: Optimization, gradient descent, learning rate, neural network training

### Dataset Statistics

- **Total Scripts**: 42
- **Total Lines of Code**: 28,288
- **Total Scenes**: 168
- **Topics Covered**: 13 major areas (set theory, calculus, linear algebra, complex analysis, number theory, geometry, topology, combinatorics, graph theory, physics, signal processing, probability, machine learning)
- **Average Scenes per Script**: 4.0
- **Average Lines per Script**: 673
- **Total Size**: 886KB

### Usage

To render a scene from the dataset:
```bash
cd dataset
manimgl circle_intersection_geometry.py CircleIntersection
```

To preview without rendering:
```bash
manimgl circle_intersection_geometry.py CircleIntersection -p
```

### Design Philosophy

The dataset scripts are designed to:
- Teach mathematical concepts through visual animation
- Serve as examples of clean, well-documented Manim code
- Be easily modifiable for educational purposes
- Demonstrate best practices in mathematical animation
