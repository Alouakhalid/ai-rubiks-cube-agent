from typing import List, Dict, Any

KNOWLEDGE_DOCUMENTS: List[Dict[str, Any]] = [
    {
        "id": "kociemba_two_phase_1992",
        "title": "Two-Phase Algorithm and Optimal Cube Solving",
        "author": "Herbert Kociemba",
        "year": 1992,
        "citation": "Kociemba, H. (1992). The Two-Phase Algorithm. Mathematics of the Rubik's Cube.",
        "category": "Algorithm",
        "content": (
            "The Kociemba Two-Phase Algorithm solves the 3x3x3 Rubik's Cube by decomposing the search "
            "into two coset spaces. In Phase 1, an arbitrary cube state is transformed into the subgroup "
            "G1 = <U, D, R2, L2, F2, B2>. During this phase, all 12 edge orientations are corrected so "
            "the flip coordinate is 0, all 8 corner orientations are corrected so the twist coordinate is 0, "
            "and the 4 middle-slice (E-slice) edges are placed into their correct slice. "
            "In Phase 2, the cube is completely solved within G1 using only quarter turns of U and D, "
            "and half turns (180 degree rotations) of R, L, F, and B. This guarantees a solution length "
            "of at most 20 to 22 moves in under 50 milliseconds."
        ),
    },
    {
        "id": "singmaster_notes_1981",
        "title": "Notes on Rubik's 'Magic Cube'",
        "author": "David Singmaster",
        "year": 1981,
        "citation": "Singmaster, D. (1981). Notes on Rubik's 'Magic Cube' (Fifth Edition). Penguin Books.",
        "category": "Group Theory",
        "content": (
            "The Rubik's Cube group has an order of exactly 43,252,003,274,489,856,000 states (approx 4.33e19). "
            "Physical legality of any state is governed by three fundamental parity invariants: "
            "1. Edge Orientation Parity: The sum of all 12 edge orientation values modulo 2 must equal 0. "
            "An isolated flipped edge is physically impossible. "
            "2. Corner Orientation Parity: The sum of all 8 corner orientation values modulo 3 must equal 0. "
            "An isolated twisted corner is physically impossible. "
            "3. Permutation Parity: The sign of the corner permutation must match the sign of the edge permutation. "
            "Swapping exactly two pieces without affecting any other piece is impossible without disassembling the cube."
        ),
    },
    {
        "id": "gods_number_2010",
        "title": "God's Number is 20",
        "author": "Tomas Rokicki, Herbert Kociemba, Morley Davidson, John Dethridge",
        "year": 2010,
        "citation": "Rokicki, T., Kociemba, H., Davidson, M., & Dethridge, J. (2010). God's Number is 20. Mathematics of Computation.",
        "category": "Combinatorics",
        "content": (
            "Every position of Rubik's Cube can be solved in 20 moves or fewer in the Half-Turn Metric (HTM), "
            "where any turn of any face (90 or 180 degrees) counts as a single move. "
            "The Superflip position, where all 12 edges are in their correct positions but flipped, "
            "was mathematically proven to require a minimum of 20 moves: "
            "U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2. "
            "In Quarter-Turn Metric (QTM), God's Number is 26."
        ),
    },
    {
        "id": "fridrich_cfop_1997",
        "title": "The CFOP (Fridrich) Speedcubing System",
        "author": "Jessica Fridrich",
        "year": 1997,
        "citation": "Fridrich, J. (1997). Speedcubing Solution: Cross, F2L, OLL, PLL. Binghamton University.",
        "category": "Speedcubing",
        "content": (
            "The CFOP method decomposes the cube solution into four intuitive, high-efficiency stages: "
            "1. Cross: Solving the 4 bottom edges to align with the bottom center and adjacent side centers. "
            "2. F2L (First Two Layers): Pairing each of the 4 bottom corners with its corresponding middle-layer "
            "edge and inserting them together into their respective slots. "
            "3. OLL (Orientation of the Last Layer): Orienting all top-layer pieces so that the top face "
            "shows a solid color, utilizing 57 standard algorithmic cases. "
            "4. PLL (Permutation of the Last Layer): Permuting the top-layer pieces into their final positions "
            "without disturbing their orientations, using 21 standard permutations (such as T-Perm, Y-Perm, U-Perm)."
        ),
    },
    {
        "id": "wca_regulations_2024",
        "title": "WCA Scrambling and Orientation Regulations",
        "author": "World Cube Association Regulations Committee",
        "year": 2024,
        "citation": "World Cube Association. (2024). WCA Regulations & Guidelines, Article 4 & 5: Scrambles.",
        "category": "Regulations",
        "content": (
            "WCA scrambles must be generated using official computer random-state scramblers. "
            "A standard competition scramble is between 18 and 22 moves. "
            "Scramble sequences never contain consecutive moves of the same face (e.g., R R is reduced to R2), "
            "nor do they contain redundant parallel moves (such as R L R'). "
            "Standard orientation for inspection and color transcription defines: "
            "White on UP, Green on FRONT, Red on RIGHT, Blue on BACK, Orange on LEFT, and Yellow on DOWN."
        ),
    },
    {
        "id": "commutators_and_conjugates",
        "title": "Commutators and Conjugates in Permutation Puzzles",
        "author": "Douglas Hofstadter & David Singmaster",
        "year": 1982,
        "citation": "Hofstadter, D. (1982). Metamagical Themas: The Magic Cube's Lovable Secrets. Scientific American.",
        "category": "Group Theory",
        "content": (
            "A commutator is an operation of the form [A, B] = A B A' B'. "
            "In the Rubik's Cube group, commutators produce highly localized piece transformations, "
            "typically cycling exactly 3 corners or 3 edges while leaving the remaining 23 pieces completely undisturbed. "
            "A conjugate is an operation of the form A B A', where A is a setup move that brings target pieces "
            "into an operating position, B executes the transformation, and A' undoes the setup. "
            "Conjugates and commutators form the mathematical foundation of all advanced blindfolded and intuitive solving algorithms."
        ),
    },
]
