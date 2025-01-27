# Modified WAND Retrieval Algorithm with UCB-based Adaptive thresholding

This is a Python implementation of the Modified WAND algorithm with UCB-based adaptive thresholding.

## Why UCB for the WAND Algorithm?

The UCB-based adaptive threshold adjustment algorithm can be integrated with the WAND algorithm to improve the efficiency of threshold tuning during the query evaluation phase. In WAND, the threshold (θ) plays a critical role in determining which documents make it to the top-k list, directly impacting pruning efficiency. UCB can help dynamically adjust this threshold based on feedback, thereby improving retrieval performance.

## Where UCB Fits in the WAND Algorithm

### 1. Threshold Initialization and Adjustment

Currently, the WAND algorithm initializes θ to −∞ and updates it when the top-k list is full. UCB can dynamically adjust θ throughout the query evaluation process based on the distribution of document scores and observed rewards.

### 2. Candidate Selection Efficiency

The UCB-based algorithm adjusts θ to balance exploring additional candidates and focusing on promising ones.

### 3. Pivot Document Processing

The pivot determination loop evaluates document candidates to decide the evaluation order. UCB can enhance this step by incorporating a dynamic policy for scoring candidates relative to their impact on θ.

## How to Test the Code

To test the code and execute the necessary commands, follow these steps:

1. **Download and Unzip Data**:
- Ensure you have your `download.sh` script ready and open your terminal (Linux/Mac/WSL).

2. **Make the Script Executable**:
    `chmod +x download.sh`

3. **Trigger the downloads**:
    `./download.sh`


Make sure you have Python and prerequisite libraries installed and that your environment is set up correctly to run this test script.

**Note:** This project is intended for hobby and learning purposes only. It is not meant for commercial use or production environments.Z
